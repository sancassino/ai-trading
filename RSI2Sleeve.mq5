//+------------------------------------------------------------------+
//| RSI2Sleeve.mq5                                                    |
//| Long-only RSI(2) mean-reversion on a fixed list of symbols (D1).  |
//| Per symbol on each new D1 bar (server time), using the last       |
//| closed bar: flat & RSI(2) < EntryRSI & close > SMA(TrendSMA) ->   |
//| buy; long & RSI(2) > ExitRSI -> close. Notional per position =    |
//| equity * LegFrac. Retries unfilled orders at most once a minute.  |
//| Attach to any chart; works from OnTimer, independent of _Symbol.  |
//+------------------------------------------------------------------+
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input string SymbolList  = "US500.cash,US100.cash,US30.cash,GER40.cash,UK100.cash,XAUUSD";
input double LegFrac     = 0.1666667; // notional per open position as fraction of equity
input double EntryRSI    = 10;
input double ExitRSI     = 70;
input int    TrendSMA    = 200;
input int    MaxIndexPositions = 0;   // 0 = onbeperkt; XAUUSD telt niet als index
input double DayGuardPct = 0;         // 0 = uit; >0: flat + geen instap rest van de dag als equity < dagstart-balance - pct% startkapitaal
input ulong  MagicNumber = 20260930;
input string DiagBestandsnaam = "RSI2Sleeve_output.csv";

string   syms[];
int      hRsi[], hSma[];
datetime lastBar[];
int      want[];          // 1 = should be long, 0 = should be flat, -1 = no pending action
datetime lastAttempt = 0;
double   initialCap = 0;
datetime guardDay = 0;

// daily equity log (same format as MomentumRotation)
datetime dayDate[];
double   dayStartBal[], dayStartEq[], dayMinEq[], dayEndEq[];
int      dayCount = 0;

void TrackDaily()
  {
   datetime now = TimeCurrent();
   datetime d = now - (now % 86400);
   double eq = AccountInfoDouble(ACCOUNT_EQUITY);
   if(dayCount == 0 || dayDate[dayCount - 1] != d)
     {
      dayCount++;
      ArrayResize(dayDate, dayCount, 4096); ArrayResize(dayStartBal, dayCount, 4096);
      ArrayResize(dayStartEq, dayCount, 4096); ArrayResize(dayMinEq, dayCount, 4096); ArrayResize(dayEndEq, dayCount, 4096);
      int i = dayCount - 1;
      dayDate[i] = d; dayStartBal[i] = AccountInfoDouble(ACCOUNT_BALANCE); dayStartEq[i] = eq; dayMinEq[i] = eq; dayEndEq[i] = eq;
      return;
     }
   int i = dayCount - 1;
   if(eq < dayMinEq[i]) dayMinEq[i] = eq;
   dayEndEq[i] = eq;
  }

void ExportAll()
  {
   string fn = DiagBestandsnaam;
   StringReplace(fn, ".csv", "_daily.csv");
   int fh = FileOpen(fn, FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI, ';');
   if(fh != INVALID_HANDLE)
     {
      FileWrite(fh, "date", "start_balance", "start_equity", "min_equity", "end_equity");
      for(int i = 0; i < dayCount; i++)
         FileWrite(fh, TimeToString(dayDate[i], TIME_DATE), DoubleToString(dayStartBal[i], 2), DoubleToString(dayStartEq[i], 2),
                   DoubleToString(dayMinEq[i], 2), DoubleToString(dayEndEq[i], 2));
      FileClose(fh);
     }
   if(!HistorySelect(0, TimeCurrent())) return;
   fh = FileOpen(DiagBestandsnaam, FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI, ';');
   if(fh == INVALID_HANDLE) return;
   FileWrite(fh, "close_time", "symbol", "profit", "raw_profit", "swap", "commission", "volume", "open_time");
   int total = HistoryDealsTotal();
   for(int i = 0; i < total; i++)
     {
      ulong t = HistoryDealGetTicket(i);
      if(t == 0 || HistoryDealGetInteger(t, DEAL_ENTRY) != DEAL_ENTRY_OUT) continue;
      double raw = HistoryDealGetDouble(t, DEAL_PROFIT), sw = HistoryDealGetDouble(t, DEAL_SWAP), cm = HistoryDealGetDouble(t, DEAL_COMMISSION);
      // opentijd: via position id
      long pid = HistoryDealGetInteger(t, DEAL_POSITION_ID);
      datetime ot = 0;
      for(int j = 0; j < total; j++)
        {
         ulong t2 = HistoryDealGetTicket(j);
         if(HistoryDealGetInteger(t2, DEAL_POSITION_ID) == pid && HistoryDealGetInteger(t2, DEAL_ENTRY) == DEAL_ENTRY_IN)
           { ot = (datetime)HistoryDealGetInteger(t2, DEAL_TIME); break; }
        }
      FileWrite(fh, TimeToString((datetime)HistoryDealGetInteger(t, DEAL_TIME), TIME_DATE|TIME_MINUTES), HistoryDealGetString(t, DEAL_SYMBOL),
                DoubleToString(raw + sw + cm, 2), DoubleToString(raw, 2), DoubleToString(sw, 2), DoubleToString(cm, 2),
                DoubleToString(HistoryDealGetDouble(t, DEAL_VOLUME), 2), TimeToString(ot, TIME_DATE|TIME_MINUTES));
     }
   FileClose(fh);
  }

double LotsForNotional(string s, double notional)
  {
   double price = SymbolInfoDouble(s, SYMBOL_ASK);
   double tv = SymbolInfoDouble(s, SYMBOL_TRADE_TICK_VALUE), ts = SymbolInfoDouble(s, SYMBOL_TRADE_TICK_SIZE);
   if(price <= 0 || tv <= 0 || ts <= 0) return 0;
   double step = SymbolInfoDouble(s, SYMBOL_VOLUME_STEP), mn = SymbolInfoDouble(s, SYMBOL_VOLUME_MIN), mx = SymbolInfoDouble(s, SYMBOL_VOLUME_MAX);
   double lots = MathFloor(notional / (price * tv / ts) / step) * step;
   if(lots < mn) return 0;
   return MathMin(mx, lots);
  }

bool HasPos(string s)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong t = PositionGetTicket(i);
      if(t != 0 && PositionGetInteger(POSITION_MAGIC) == (long)MagicNumber && PositionGetString(POSITION_SYMBOL) == s) return true;
     }
   return false;
  }

void ClosePos(string s)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong t = PositionGetTicket(i);
      if(t != 0 && PositionGetInteger(POSITION_MAGIC) == (long)MagicNumber && PositionGetString(POSITION_SYMBOL) == s)
         trade.PositionClose(t);
     }
  }

bool IsIndex(string s) { return s != "XAUUSD"; }

int IndexExposure()
  {
   int n = 0;
   for(int k = 0; k < ArraySize(syms); k++)
      if(IsIndex(syms[k]) && (HasPos(syms[k]) || want[k] == 1)) n++;
   return n;
  }

bool GuardActive() { datetime now = TimeCurrent(); return guardDay == now - (now % 86400); }

void Evaluate()
  {
   int cand[]; double candRsi[];
   for(int k = 0; k < ArraySize(syms); k++)
     {
      string s = syms[k];
      datetime bt = iTime(s, PERIOD_D1, 0);
      if(bt == 0 || bt == lastBar[k]) continue;
      lastBar[k] = bt;
      double r[1], m[1];
      if(CopyBuffer(hRsi[k], 0, 1, 1, r) != 1 || CopyBuffer(hSma[k], 0, 1, 1, m) != 1) continue;
      double c1 = iClose(s, PERIOD_D1, 1);
      bool held = HasPos(s);
      if(!held && r[0] < EntryRSI && c1 > m[0])
        {
         int n = ArraySize(cand); ArrayResize(cand, n + 1); ArrayResize(candRsi, n + 1);
         cand[n] = k; candRsi[n] = r[0];
        }
      else if(held && r[0] > ExitRSI) want[k] = 0;
     }
   // instapkandidaten: laagste RSI(2) eerst, met index-cap
   int n = ArraySize(cand);
   for(int i = 0; i < n; i++)
     {
      int best = i;
      for(int j = i + 1; j < n; j++) if(candRsi[j] < candRsi[best]) best = j;
      int tk = cand[i]; cand[i] = cand[best]; cand[best] = tk;
      double tr = candRsi[i]; candRsi[i] = candRsi[best]; candRsi[best] = tr;
      int k = cand[i];
      if(GuardActive()) continue;
      if(MaxIndexPositions > 0 && IsIndex(syms[k]) && IndexExposure() >= MaxIndexPositions) continue;
      want[k] = 1;
     }
  }

void CheckGuard()
  {
   if(DayGuardPct <= 0 || dayCount == 0 || GuardActive()) return;
   if(AccountInfoDouble(ACCOUNT_EQUITY) < dayStartBal[dayCount - 1] - initialCap * DayGuardPct / 100.0)
     {
      datetime now = TimeCurrent();
      guardDay = now - (now % 86400);
      for(int k = 0; k < ArraySize(syms); k++) want[k] = HasPos(syms[k]) ? 0 : -1;
      PrintFormat("Dagguard %s: equity %.2f < dagstart-balance %.2f - %.1f%%", TimeToString(now), AccountInfoDouble(ACCOUNT_EQUITY), dayStartBal[dayCount - 1], DayGuardPct);
     }
  }

void Execute()
  {
   if(TimeCurrent() - lastAttempt < 60) return;
   lastAttempt = TimeCurrent();
   for(int k = 0; k < ArraySize(syms); k++)
     {
      if(want[k] < 0) continue;
      string s = syms[k];
      bool held = HasPos(s);
      if(want[k] == 1 && !held)
        {
         if(GuardActive()) { want[k] = -1; continue; }
         double lots = LotsForNotional(s, AccountInfoDouble(ACCOUNT_EQUITY) * LegFrac);
         if(lots > 0 && trade.Buy(lots, s) && HasPos(s)) want[k] = -1;
        }
      else if(want[k] == 0 && held)
        {
         ClosePos(s);
         if(!HasPos(s)) want[k] = -1;
        }
      else want[k] = -1;
     }
  }

int OnInit()
  {
   trade.SetExpertMagicNumber(MagicNumber);
   initialCap = AccountInfoDouble(ACCOUNT_BALANCE);
   string parts[];
   int n = StringSplit(SymbolList, ',', parts);
   ArrayResize(syms, n); ArrayResize(hRsi, n); ArrayResize(hSma, n); ArrayResize(lastBar, n); ArrayResize(want, n);
   for(int i = 0; i < n; i++)
     {
      syms[i] = parts[i];
      SymbolSelect(syms[i], true);
      hRsi[i] = iRSI(syms[i], PERIOD_D1, 2, PRICE_CLOSE);
      hSma[i] = iMA(syms[i], PERIOD_D1, TrendSMA, 0, MODE_SMA, PRICE_CLOSE);
      lastBar[i] = 0; want[i] = -1;
     }
   EventSetTimer(60);
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason) { EventKillTimer(); ExportAll(); }

void Step()
  {
   TrackDaily();
   CheckGuard();
   Evaluate();
   Execute();
  }

void OnTick()  { Step(); }
void OnTimer() { Step(); }
//+------------------------------------------------------------------+
