//+------------------------------------------------------------------+
//| TrendFollow_CrossAsset.mq5                                        |
//| Long-only trend-following EA, single-symbol per chart instance.   |
//| Entry: close > SMA(TrendPeriod). Exit: ATR trailing stop or       |
//| trend break (close < SMA(TrendPeriod)).                           |
//| Position size: fixed % risk of equity per trade, based on stop    |
//| distance (ATR * ATRStopMult).                                     |
//|                                                                    |
//| Run one instance per instrument (indices, gold, bonds, crude) to  |
//| build the cross-asset portfolio described in trend-research.md.   |
//| _Symbol-independent: attach to any chart, no per-symbol edits.    |
//+------------------------------------------------------------------+
#property copyright "internal research"
#property version   "1.00"
#property strict

input ENUM_TIMEFRAMES TF = PERIOD_D1; // timeframe for SMA/ATR/signals
input int    TrendPeriod   = 200;   // SMA period for trend filter
input int    ATRPeriod     = 20;    // ATR period
input double ATRStopMult   = 3.0;   // trailing stop distance = ATR * this
input double RiskPct       = 1.0;   // % of equity risked per trade
input bool   UseTrendExit  = false; // also exit on close<SMA*(1-buffer) (false = pure ATR trailing stop)
input double ExitBufferPct = 0.0;   // hysteresis band below SMA before trend-exit fires
input double EntryBufferPct = 0.0;  // hysteresis band above SMA before entry fires
input int    Slippage      = 5;     // points
input ulong  MagicNumber   = 20260924;
input string DiagBestandsnaam = "TrendFollow_output.csv"; // FILE_COMMON deal export

#include <Trade\Trade.mqh>
CTrade trade;

int hSMA, hATR;

void ExportDeals()
  {
   if(!HistorySelect(0, TimeCurrent())) return;
   int fh = FileOpen(DiagBestandsnaam, FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI, ';');
   if(fh == INVALID_HANDLE) { Print("ExportDeals: file open failed ", GetLastError()); return; }
   FileWrite(fh, "close_time", "symbol", "profit", "balance_after");
   int total = HistoryDealsTotal();
   for(int i = 0; i < total; i++)
     {
      ulong ticket = HistoryDealGetTicket(i);
      if(ticket == 0) continue;
      if(HistoryDealGetInteger(ticket, DEAL_ENTRY) != DEAL_ENTRY_OUT) continue; // only closing deals
      datetime ct = (datetime)HistoryDealGetInteger(ticket, DEAL_TIME);
      double profit = HistoryDealGetDouble(ticket, DEAL_PROFIT) + HistoryDealGetDouble(ticket, DEAL_SWAP) + HistoryDealGetDouble(ticket, DEAL_COMMISSION);
      string sym = HistoryDealGetString(ticket, DEAL_SYMBOL);
      FileWrite(fh, TimeToString(ct, TIME_DATE|TIME_MINUTES), sym, DoubleToString(profit, 2), "");
     }
   FileClose(fh);
   Print("ExportDeals: wrote ", total, " deal records to ", DiagBestandsnaam);
  }

int OnInit()
  {
   hSMA = iMA(_Symbol, TF, TrendPeriod, 0, MODE_SMA, PRICE_CLOSE);
   hATR = iATR(_Symbol, TF, ATRPeriod);
   if(hSMA == INVALID_HANDLE || hATR == INVALID_HANDLE)
     {
      Print("Indicator init failed");
      return(INIT_FAILED);
     }
   trade.SetExpertMagicNumber(MagicNumber);
   trade.SetDeviationInPoints(Slippage);
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   ExportDeals();
   IndicatorRelease(hSMA);
   IndicatorRelease(hATR);
  }

bool HasOpenPosition()
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(PositionGetString(POSITION_SYMBOL) == _Symbol &&
         PositionGetInteger(POSITION_MAGIC) == (long)MagicNumber)
         return true;
     }
   return false;
  }

double LotsForRisk(double stopDistance)
  {
   double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   double riskMoney = equity * RiskPct / 100.0;
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   if(tickSize <= 0 || tickValue <= 0 || stopDistance <= 0) return 0.0;

   double valuePerPointPerLot = tickValue / tickSize; // money per 1.0 price unit per 1 lot
   double lots = riskMoney / (stopDistance * valuePerPointPerLot);

   double minLot  = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot  = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double lotStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   lots = MathFloor(lots / lotStep) * lotStep;
   lots = MathMax(minLot, MathMin(maxLot, lots));
   return lots;
  }

void ManageOpenPosition(double atr)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(PositionGetString(POSITION_SYMBOL) != _Symbol) continue;
      if(PositionGetInteger(POSITION_MAGIC) != (long)MagicNumber) continue;

      double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
      double curSL = PositionGetDouble(POSITION_SL);
      double newStop = NormalizeDouble(bid - atr * ATRStopMult, (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS));

      bool trendBroken = false;
      if(UseTrendExit)
        {
         // use the last CLOSED bar, not live bid, so the signal only changes
         // once per bar instead of flickering intrabar around the SMA level.
         // ExitBufferPct adds hysteresis: only exit once price is clearly
         // below the SMA, not on every minor touch of the line.
         double maVal[];
         ArraySetAsSeries(maVal, true);
         if(CopyBuffer(hSMA, 0, 1, 1, maVal) > 0)
            trendBroken = (iClose(_Symbol, TF, 1) < maVal[0] * (1.0 - ExitBufferPct / 100.0));
        }

      if(trendBroken)
        {
         trade.PositionClose(ticket);
         continue;
        }

      // trail up only, long-only; broker-side SL so the server enforces it
      // even if this EA doesn't get a tick at the exact crossing moment.
      if(newStop > curSL)
         trade.PositionModify(ticket, newStop, PositionGetDouble(POSITION_TP));
     }
  }

input bool RequireCross      = false; // true = only enter on fresh cross-up (old, restrictive behavior)
input int  BreakoutLookback  = 0;     // >0: also require close = highest close of last N bars (Donchian breakout)

void TryOpenPosition(double atr)
  {
   // signal is evaluated on the last CLOSED bar only (same clock as the
   // trend-exit check) so entry/exit decisions can't fight each other on
   // intrabar noise; only the actual fill price uses the live ask.
   double maVal[], maPrev[];
   ArraySetAsSeries(maVal, true);
   ArraySetAsSeries(maPrev, true);
   if(CopyBuffer(hSMA, 0, 1, 1, maVal) <= 0) return;
   if(CopyBuffer(hSMA, 0, 2, 1, maPrev) <= 0) return;

   double closePrev2 = iClose(_Symbol, TF, 2);
   double closeLast  = iClose(_Symbol, TF, 1);
   double closeNow   = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   bool wasBelow = closePrev2 < maPrev[0];
   bool isAbove  = closeLast > maVal[0] * (1.0 + EntryBufferPct / 100.0);

   // flat + trend up = eligible to (re-)enter; RequireCross reproduces the old, more restrictive gate
   if(RequireCross) { if(!(wasBelow && isAbove)) return; }
   else { if(!isAbove) return; }

   if(BreakoutLookback > 0)
     {
      double highs[];
      ArraySetAsSeries(highs, true);
      if(CopyClose(_Symbol, TF, 1, BreakoutLookback, highs) < BreakoutLookback) return;
      double highest = highs[ArrayMaximum(highs)];
      if(closeLast < highest) return; // not a fresh N-bar high yet
     }

   double stopDistance = atr * ATRStopMult;
   double lots = LotsForRisk(stopDistance);
   if(lots <= 0) return;

   int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   double sl = NormalizeDouble(closeNow - stopDistance, digits);
   trade.Buy(lots, _Symbol, 0.0, sl, 0.0);
  }

void OnTick()
  {
   // NOTE: deliberately no "once per new bar" gate here. Signals are based on
   // closed D1 data so they only change once per day regardless, but entry
   // ORDERS must be retried on every tick that day -- some symbols reject a
   // market order at the very first (00:00) tick of the day with "Market
   // closed" (session boundary quirk in the tester), and without a retry on
   // a later tick the same day, a flat account can stall for years.
   double atrVal[];
   ArraySetAsSeries(atrVal, true);
   if(CopyBuffer(hATR, 0, 0, 1, atrVal) <= 0) return;
   double atr = atrVal[0];

   if(HasOpenPosition())
      ManageOpenPosition(atr);
   else
      TryOpenPosition(atr);
  }
//+------------------------------------------------------------------+
