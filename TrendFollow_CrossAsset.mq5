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

input int    TrendPeriod   = 200;   // SMA period for trend filter
input int    ATRPeriod     = 20;    // ATR period
input double ATRStopMult   = 3.0;   // trailing stop distance = ATR * this
input double RiskPct       = 1.0;   // % of equity risked per trade
input int    Slippage      = 5;     // points
input ulong  MagicNumber   = 20260924;

int hSMA, hATR;
double slLevel = 0.0; // current trailing stop level for the open position

int OnInit()
  {
   hSMA = iMA(_Symbol, PERIOD_D1, TrendPeriod, 0, MODE_SMA, PRICE_CLOSE);
   hATR = iATR(_Symbol, PERIOD_D1, ATRPeriod);
   if(hSMA == INVALID_HANDLE || hATR == INVALID_HANDLE)
     {
      Print("Indicator init failed");
      return(INIT_FAILED);
     }
   slLevel = 0.0;
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
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
      double newStop = bid - atr * ATRStopMult;
      if(newStop > slLevel) slLevel = newStop; // trail up only, long-only

      double maVal[];
      ArraySetAsSeries(maVal, true);
      if(CopyBuffer(hSMA, 0, 0, 1, maVal) <= 0) return;
      bool trendBroken = (bid < maVal[0]);

      if(bid <= slLevel || trendBroken)
        {
         MqlTradeRequest req = {};
         MqlTradeResult  res = {};
         req.action    = TRADE_ACTION_DEAL;
         req.symbol    = _Symbol;
         req.volume    = PositionGetDouble(POSITION_VOLUME);
         req.type      = ORDER_TYPE_SELL;
         req.position  = ticket;
         req.price     = bid;
         req.deviation = Slippage;
         req.magic     = MagicNumber;
         OrderSend(req, res);
         slLevel = 0.0;
        }
     }
  }

void TryOpenPosition(double atr)
  {
   double maVal[], maPrev[];
   ArraySetAsSeries(maVal, true);
   ArraySetAsSeries(maPrev, true);
   if(CopyBuffer(hSMA, 0, 0, 1, maVal) <= 0) return;
   if(CopyBuffer(hSMA, 0, 1, 1, maPrev) <= 0) return;

   double closePrev = iClose(_Symbol, PERIOD_D1, 1);
   double closeNow  = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   bool wasBelow = closePrev < maPrev[0];
   bool isAbove  = closeNow > maVal[0];

   // enter on trend-cross-up only (avoids re-entering every bar while trend holds)
   if(!(wasBelow && isAbove)) return;

   double stopDistance = atr * ATRStopMult;
   double lots = LotsForRisk(stopDistance);
   if(lots <= 0) return;

   MqlTradeRequest req = {};
   MqlTradeResult  res = {};
   req.action    = TRADE_ACTION_DEAL;
   req.symbol    = _Symbol;
   req.volume    = lots;
   req.type      = ORDER_TYPE_BUY;
   req.price     = closeNow;
   req.deviation = Slippage;
   req.magic     = MagicNumber;
   req.sl        = 0.0; // managed manually via ManageOpenPosition (trailing)
   if(OrderSend(req, res))
      slLevel = closeNow - stopDistance;
  }

datetime lastBarTime = 0;

void OnTick()
  {
   datetime barTime = iTime(_Symbol, PERIOD_D1, 0);
   if(barTime == lastBarTime) return; // act once per new daily bar
   lastBarTime = barTime;

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
