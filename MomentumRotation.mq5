//+------------------------------------------------------------------+
//| MomentumRotation.mq5                                              |
//| Cross-sectional momentum rotation across a fixed instrument list. |
//| Monthly rebalance: rank all instruments by trailing N-month       |
//| return, hold the top K equal-weighted, size each leg as a fixed   |
//| fraction of equity (ExposureFrac / K notional exposure).          |
//| Attach to ANY one chart of the listed symbols -- it manages all   |
//| symbols from OnTimer, independent of the chart's own _Symbol.     |
//+------------------------------------------------------------------+
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input int    LookbackMonths = 1;
input int    TopN           = 3;
input double ExposureFrac   = 0.50;  // total notional exposure as fraction of equity
input bool   UseInverseVolWeight = false; // false = equal weight per leg
input double MaxLegWeight   = 1.0;   // cap on any single leg's weight (inverse-vol mode only)
input bool   SelectBottom   = false; // true = buy the K WORST-momentum instruments (symmetry test)
input ulong  MagicNumber    = 20260925;
input string DiagBestandsnaam = "MomentumRotation_output.csv";
input int    RegimeSMAMonths = 0;      // 0 = disabled. >0: only trade when RegimeSymbol > its N-month SMA
input string RegimeSymbol    = "US500.cash";

string UNIVERSE[] = {"US500.cash","US100.cash","US30.cash","EU50.cash","UK100.cash","GER40.cash","XAUUSD","USOIL.cash","EURUSD","AAPL","MSFT","AMZN","GOOG","META","NVDA","TSLA"};

datetime lastRebalanceMonth = 0;
bool   rebalancePending = false;
string targetSyms[];   // this month's target legs
double targetLots[];   // pre-computed lot size per leg

void ExportDeals()
  {
   if(!HistorySelect(0, TimeCurrent())) return;
   int fh = FileOpen(DiagBestandsnaam, FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI, ';');
   if(fh == INVALID_HANDLE) return;
   FileWrite(fh, "close_time", "symbol", "profit", "raw_profit", "swap", "commission");
   int total = HistoryDealsTotal();
   for(int i = 0; i < total; i++)
     {
      ulong ticket = HistoryDealGetTicket(i);
      if(ticket == 0) continue;
      if(HistoryDealGetInteger(ticket, DEAL_ENTRY) != DEAL_ENTRY_OUT) continue;
      datetime ct = (datetime)HistoryDealGetInteger(ticket, DEAL_TIME);
      double rawProfit = HistoryDealGetDouble(ticket, DEAL_PROFIT);
      double swap = HistoryDealGetDouble(ticket, DEAL_SWAP);
      double comm = HistoryDealGetDouble(ticket, DEAL_COMMISSION);
      double profit = rawProfit + swap + comm;
      string sym = HistoryDealGetString(ticket, DEAL_SYMBOL);
      FileWrite(fh, TimeToString(ct, TIME_DATE|TIME_MINUTES), sym, DoubleToString(profit, 2), DoubleToString(rawProfit, 2), DoubleToString(swap, 2), DoubleToString(comm, 2));
     }
   FileClose(fh);
   Print("ExportDeals: wrote deal records to ", DiagBestandsnaam);
  }

int OnInit()
  {
   trade.SetExpertMagicNumber(MagicNumber);
   for(int i = 0; i < ArraySize(UNIVERSE); i++)
      SymbolSelect(UNIVERSE[i], true);
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   ExportDeals();
  }

double MonthsAgoClose(string sym, int monthsAgo)
  {
   datetime target = TimeCurrent() - monthsAgo * 30 * 86400;
   int shift = iBarShift(sym, PERIOD_D1, target, false);
   if(shift < 0) return -1;
   double c = iClose(sym, PERIOD_D1, shift);
   return c;
  }

double CurrentClose(string sym)
  {
   return iClose(sym, PERIOD_D1, 1); // last fully closed daily bar
  }

bool HasPositionOn(string sym)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(PositionGetInteger(POSITION_MAGIC) != (long)MagicNumber) continue;
      if(PositionGetString(POSITION_SYMBOL) == sym) return true;
     }
   return false;
  }

bool IsTarget(string sym)
  {
   for(int i = 0; i < ArraySize(targetSyms); i++)
      if(targetSyms[i] == sym) return true;
   return false;
  }

// Retry-friendly: called on every tick while a rebalance is pending. Closes
// any open leg that is no longer a target, then opens any target leg that
// isn't filled yet. Safe to call repeatedly -- a broker "Market closed"
// rejection on one leg just gets retried next tick without disturbing legs
// that already succeeded.
void ProcessPendingRebalance()
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(PositionGetInteger(POSITION_MAGIC) != (long)MagicNumber) continue;
      string sym = PositionGetString(POSITION_SYMBOL);
      if(!IsTarget(sym))
         trade.PositionClose(ticket);
     }

   bool allFilled = true;
   for(int i = 0; i < ArraySize(targetSyms); i++)
     {
      if(HasPositionOn(targetSyms[i])) continue;
      allFilled = false;
      if(targetLots[i] > 0)
         trade.Buy(targetLots[i], targetSyms[i], 0.0, 0.0, 0.0);
     }

   // also confirm no stray non-target positions remain
   bool anyStray = false;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(PositionGetInteger(POSITION_MAGIC) != (long)MagicNumber) continue;
      if(!IsTarget(PositionGetString(POSITION_SYMBOL))) { anyStray = true; break; }
     }

   if(allFilled && !anyStray)
      rebalancePending = false;
  }

bool RegimeIsRiskOn()
  {
   if(RegimeSMAMonths <= 0) return true; // filter disabled
   // evaluated once per rebalance (monthly), same cadence as the signal
   // itself -- avoids the intrabar/intra-month whipsaw that plagued the
   // earlier trend-following EA, which checked a fast-moving regime signal
   // on every tick.
   double sum = 0; int cnt = 0;
   for(int i = 1; i <= RegimeSMAMonths; i++)
     {
      double c = MonthsAgoClose(RegimeSymbol, i - 1);
      if(c > 0) { sum += c; cnt++; }
     }
   if(cnt == 0) return true;
   double sma = sum / cnt;
   double now = CurrentClose(RegimeSymbol);
   return (now > sma);
  }

void PrepareRebalance()
  {
   if(!RegimeIsRiskOn())
     {
      // risk-off: go/stay flat, no new legs this month
      ArrayResize(targetSyms, 0);
      ArrayResize(targetLots, 0);
      rebalancePending = true;
      return;
     }
   int n = ArraySize(UNIVERSE);
   double rets[]; string syms[];
   ArrayResize(rets, n); ArrayResize(syms, n);
   int count = 0;
   for(int i = 0; i < n; i++)
     {
      string s = UNIVERSE[i];
      double now = CurrentClose(s);
      double then = MonthsAgoClose(s, LookbackMonths);
      if(now <= 0 || then <= 0) continue;
      rets[count] = (now - then) / then;
      syms[count] = s;
      count++;
     }
   // simple selection sort descending by return, top K
   for(int i = 0; i < count - 1; i++)
     {
      int best = i;
      for(int j = i + 1; j < count; j++)
         if(rets[j] > rets[best]) best = j;
      if(best != i)
        {
         double tr = rets[i]; rets[i] = rets[best]; rets[best] = tr;
         string ts = syms[i]; syms[i] = syms[best]; syms[best] = ts;
        }
     }

   int k = MathMin(TopN, count);
   if(k <= 0) return;
   double equity = AccountInfoDouble(ACCOUNT_EQUITY);

   // select either the K best (normal) or K worst (SelectBottom, for the
   // long/short symmetry test) -- syms[] is sorted descending by return.
   string sel[]; ArrayResize(sel, k);
   if(SelectBottom)
      for(int i = 0; i < k; i++) sel[i] = syms[count - 1 - i];
   else
      for(int i = 0; i < k; i++) sel[i] = syms[i];

   // inverse-volatility weighting: legs with higher ATR% get a smaller
   // notional slice, so one volatile single-name mover (e.g. TSLA/NVDA)
   // can't dominate the portfolio's risk the way equal-weight does.
   // MaxLegWeight caps any single leg (a momentarily near-zero ATR% on a
   // thin symbol could otherwise blow up its inverse-vol weight).
   double legWeight_[]; ArrayResize(legWeight_, k);
   if(UseInverseVolWeight)
     {
      double invVol[]; ArrayResize(invVol, k);
      double invVolSum = 0;
      for(int i = 0; i < k; i++)
        {
         string s = sel[i];
         int atrH = iATR(s, PERIOD_D1, 20);
         double atrBuf[]; ArraySetAsSeries(atrBuf, true);
         double atrPct = 0.02;
         if(atrH != INVALID_HANDLE && CopyBuffer(atrH, 0, 1, 1, atrBuf) > 0)
           {
            double px = iClose(s, PERIOD_D1, 1);
            if(px > 0) atrPct = atrBuf[0] / px;
            IndicatorRelease(atrH);
           }
         if(atrPct <= 0) atrPct = 0.02;
         invVol[i] = 1.0 / atrPct;
         invVolSum += invVol[i];
        }
      for(int i = 0; i < k; i++) legWeight_[i] = MathMin(MaxLegWeight, invVol[i] / invVolSum);
      double capSum = 0; for(int i = 0; i < k; i++) capSum += legWeight_[i];
      for(int i = 0; i < k; i++) legWeight_[i] /= capSum; // renormalize to sum 1 after capping
     }
   else
     {
      for(int i = 0; i < k; i++) legWeight_[i] = 1.0 / k;
     }

   ArrayResize(targetSyms, k);
   ArrayResize(targetLots, k);
   for(int i = 0; i < k; i++)
     {
      string s = sel[i];
      double legWeight = legWeight_[i];
      double perLegNotional = equity * ExposureFrac * legWeight;
      double price = SymbolInfoDouble(s, SYMBOL_ASK);
      double tickValue = SymbolInfoDouble(s, SYMBOL_TRADE_TICK_VALUE);
      double tickSize  = SymbolInfoDouble(s, SYMBOL_TRADE_TICK_SIZE);
      double lots = 0;
      if(price > 0 && tickValue > 0 && tickSize > 0)
        {
         double contractValue = price * (tickValue / tickSize);
         if(contractValue > 0)
           {
            lots = perLegNotional / contractValue;
            double minLot  = SymbolInfoDouble(s, SYMBOL_VOLUME_MIN);
            double maxLot  = SymbolInfoDouble(s, SYMBOL_VOLUME_MAX);
            double lotStep = SymbolInfoDouble(s, SYMBOL_VOLUME_STEP);
            lots = MathFloor(lots / lotStep) * lotStep;
            lots = MathMax(minLot, MathMin(maxLot, lots));
            if(lots < minLot) lots = 0;
           }
        }
      targetSyms[i] = s;
      targetLots[i] = lots;
     }
   rebalancePending = true;
  }

void OnTick()
  {
   MqlDateTime dt;
   TimeToStruct(TimeCurrent(), dt);
   datetime monthKey = (datetime)(dt.year * 100 + dt.mon); // crude month id
   if(monthKey != lastRebalanceMonth)
     {
      lastRebalanceMonth = monthKey;
      PrepareRebalance();
     }
   if(rebalancePending)
      ProcessPendingRebalance();
  }
//+------------------------------------------------------------------+
