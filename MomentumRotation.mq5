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
input double DailyGuardPct   = 0;      // 0 = off. >0: flatten + wait for next month if equity < day-start balance - pct% of initial capital (FTMO daily-loss protection)
input double TotalGuardPct   = 0;      // 0 = off. >0: flatten + wait for next month if equity < initial capital - pct% (FTMO max-loss protection)
input double InitialCapital  = 0;      // 0 = balance at EA start

input bool   AbsMomentumFilter = false; // true: only hold instruments whose own lookback return > 0; empty slots stay in cash (dual momentum)
input bool   RankByRiskAdj   = false;  // true: rank on return / ATR%(20) instead of raw return (vol-adjusted momentum)
input string UniverseList    = "";     // comma-separated symbols, or "file:<name>" = read from Common\Files (tester truncates long strings); empty = DEFAULT_UNIVERSE

string DEFAULT_UNIVERSE[] = {"US500.cash","US100.cash","US30.cash","EU50.cash","UK100.cash","GER40.cash","XAUUSD","USOIL.cash","EURUSD","AAPL","MSFT","AMZN","GOOG","META","NVDA","TSLA"};
string UNIVERSE[];

datetime lastRebalanceMonth = 0;

// Daily equity log (for FTMO daily-loss / floating-drawdown analysis):
// per server day the balance+equity at the first tick, the lowest equity
// seen during the day, and the equity at the last tick.
datetime dayDate[];
double   dayStartBal[], dayStartEq[], dayMinEq[], dayEndEq[];
int      dayCount = 0;

string   rankLog[];      // one line per instrument per rebalance: month;symbol;return
int      rankCount = 0;
datetime lastAttempt = 0; // retry throttle for ProcessPendingRebalance

double   initialCap = 0;
bool     guardHalted = false; // flat until the next monthly rebalance
int      guardTriggers = 0;
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

void TrackDaily()
  {
   datetime now = TimeCurrent();
   datetime d = now - (now % 86400);
   double eq  = AccountInfoDouble(ACCOUNT_EQUITY);
   if(dayCount == 0 || dayDate[dayCount - 1] != d)
     {
      dayCount++;
      ArrayResize(dayDate, dayCount, 4096);
      ArrayResize(dayStartBal, dayCount, 4096);
      ArrayResize(dayStartEq, dayCount, 4096);
      ArrayResize(dayMinEq, dayCount, 4096);
      ArrayResize(dayEndEq, dayCount, 4096);
      int i = dayCount - 1;
      dayDate[i] = d;
      dayStartBal[i] = AccountInfoDouble(ACCOUNT_BALANCE);
      dayStartEq[i] = eq;
      dayMinEq[i] = eq;
      dayEndEq[i] = eq;
      return;
     }
   int i = dayCount - 1;
   if(eq < dayMinEq[i]) dayMinEq[i] = eq;
   dayEndEq[i] = eq;
  }

void AddRankLine(string line)
  {
   ArrayResize(rankLog, rankCount + 1, 8192);
   rankLog[rankCount++] = line;
  }

void ExportRanks()
  {
   string fn = DiagBestandsnaam;
   StringReplace(fn, ".csv", "_ranks.csv");
   int fh = FileOpen(fn, FILE_WRITE|FILE_TXT|FILE_COMMON|FILE_ANSI);
   if(fh == INVALID_HANDLE) return;
   FileWriteString(fh, "time;symbol;ret;rank;lots\n");
   for(int i = 0; i < rankCount; i++) FileWriteString(fh, rankLog[i] + "\n");
   FileClose(fh);
  }

void ExportDaily()
  {
   string fn = DiagBestandsnaam;
   StringReplace(fn, ".csv", "_daily.csv");
   int fh = FileOpen(fn, FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI, ';');
   if(fh == INVALID_HANDLE) return;
   FileWrite(fh, "date", "start_balance", "start_equity", "min_equity", "end_equity");
   for(int i = 0; i < dayCount; i++)
      FileWrite(fh, TimeToString(dayDate[i], TIME_DATE), DoubleToString(dayStartBal[i], 2), DoubleToString(dayStartEq[i], 2), DoubleToString(dayMinEq[i], 2), DoubleToString(dayEndEq[i], 2));
   FileClose(fh);
  }

int OnInit()
  {
   trade.SetExpertMagicNumber(MagicNumber);
   initialCap = (InitialCapital > 0) ? InitialCapital : AccountInfoDouble(ACCOUNT_BALANCE);
   if(StringLen(UniverseList) > 0)
     {
      string list = UniverseList;
      if(StringFind(list, "file:") == 0)
        {
         int fh = FileOpen(StringSubstr(list, 5), FILE_READ|FILE_TXT|FILE_COMMON|FILE_ANSI);
         if(fh == INVALID_HANDLE) { Print("Universe file not found: ", list); return(INIT_FAILED); }
         list = "";
         while(!FileIsEnding(fh)) list += FileReadString(fh);
         FileClose(fh);
        }
      string parts[];
      int n = StringSplit(list, ',', parts);
      ArrayResize(UNIVERSE, 0);
      for(int i = 0; i < n; i++)
        {
         StringTrimLeft(parts[i]); StringTrimRight(parts[i]);
         if(StringLen(parts[i]) == 0) continue;
         int k = ArraySize(UNIVERSE);
         ArrayResize(UNIVERSE, k + 1);
         UNIVERSE[k] = parts[i];
        }
     }
   else
      ArrayCopy(UNIVERSE, DEFAULT_UNIVERSE);
   for(int i = 0; i < ArraySize(UNIVERSE); i++)
      if(!SymbolSelect(UNIVERSE[i], true))
         Print("Universe: cannot select ", UNIVERSE[i]);
   Print("Universe size: ", ArraySize(UNIVERSE));
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   Print("Equity guard triggers: ", guardTriggers);
   ExportRanks();
   ExportDaily(); // before ExportDeals: runners wait for the deals file
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

double AtrPct(string sym)
  {
   int h = iATR(sym, PERIOD_D1, 20);
   double buf[]; ArraySetAsSeries(buf, true);
   double pct = 0;
   if(h != INVALID_HANDLE && CopyBuffer(h, 0, 1, 1, buf) > 0)
     {
      double px = iClose(sym, PERIOD_D1, 1);
      if(px > 0) pct = buf[0] / px;
     }
   if(h != INVALID_HANDLE) IndicatorRelease(h);
   return pct;
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
      if(now <= 0 || then <= 0)
        {
         AddRankLine(TimeToString(TimeCurrent(), TIME_DATE) + ";" + s + ";NA;;");
         continue;
        }
      rets[count] = (now - then) / then;
      if(AbsMomentumFilter && rets[count] <= 0)
        {
         AddRankLine(TimeToString(TimeCurrent(), TIME_DATE) + ";" + s + ";" + DoubleToString(rets[count], 4) + ";neg;");
         continue;
        }
      if(RankByRiskAdj)
        {
         double v = AtrPct(s);
         if(v <= 0)
           {
            AddRankLine(TimeToString(TimeCurrent(), TIME_DATE) + ";" + s + ";NA;;");
            continue;
           }
         rets[count] /= v;
        }
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
   if(k <= 0)
     {
      // nothing qualifies (e.g. all momentum negative with AbsMomentumFilter): go flat
      ArrayResize(targetSyms, 0);
      ArrayResize(targetLots, 0);
      rebalancePending = true;
      return;
     }
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
      for(int i = 0; i < k; i++) legWeight_[i] = AbsMomentumFilter ? 1.0 / TopN : 1.0 / k;
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
   for(int i = 0; i < count; i++)
     {
      string lotStr = "";
      for(int j = 0; j < k; j++) if(targetSyms[j] == syms[i]) lotStr = DoubleToString(targetLots[j], 2);
      AddRankLine(TimeToString(TimeCurrent(), TIME_DATE) + ";" + syms[i] + ";" + DoubleToString(rets[i], 4) + ";" + IntegerToString(i + 1) + ";" + lotStr);
     }
   rebalancePending = true;
  }

// Closes every position of this EA. Returns true when none remain.
bool CloseAll()
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(PositionGetInteger(POSITION_MAGIC) != (long)MagicNumber) continue;
      trade.PositionClose(ticket);
     }
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket != 0 && PositionGetInteger(POSITION_MAGIC) == (long)MagicNumber) return false;
     }
   return true;
  }

bool GuardBreached()
  {
   if(dayCount == 0) return false;
   double eq = AccountInfoDouble(ACCOUNT_EQUITY);
   if(DailyGuardPct > 0 && eq < dayStartBal[dayCount - 1] - initialCap * DailyGuardPct / 100.0) return true;
   if(TotalGuardPct > 0 && eq < initialCap * (1.0 - TotalGuardPct / 100.0)) return true;
   return false;
  }

void OnTick()
  {
   TrackDaily();
   if(!guardHalted && GuardBreached())
     {
      guardHalted = true;
      guardTriggers++;
      rebalancePending = false;
      PrintFormat("Equity guard hit at %s: equity %.2f, day-start balance %.2f", TimeToString(TimeCurrent()), AccountInfoDouble(ACCOUNT_EQUITY), dayStartBal[dayCount - 1]);
     }
   if(guardHalted)
     {
      // keep retrying the flatten (market-closed rejections) until the new month
      CloseAll();
      MqlDateTime g;
      TimeToStruct(TimeCurrent(), g);
      if((datetime)(g.year * 100 + g.mon) == lastRebalanceMonth) return;
      guardHalted = false;
     }
   MqlDateTime dt;
   TimeToStruct(TimeCurrent(), dt);
   datetime monthKey = (datetime)(dt.year * 100 + dt.mon); // crude month id
   if(monthKey != lastRebalanceMonth)
     {
      lastRebalanceMonth = monthKey;
      PrepareRebalance();
     }
   if(rebalancePending && TimeCurrent() - lastAttempt >= 60)
     {
      lastAttempt = TimeCurrent();
      ProcessPendingRebalance();
     }
  }
//+------------------------------------------------------------------+
