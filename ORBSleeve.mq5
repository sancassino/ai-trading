//+------------------------------------------------------------------+
//| ORBSleeve.mq5                                                     |
//| Opening-range breakout (first 30 min) per symbol, one trade/day. |
//| Stop orders on OR high/low (OCO), SL = other side, flat at the    |
//| session close. Session times in server time (server = NY + 7h);   |
//| European sessions shift +1h in the US/EU DST-mismatch weeks.      |
//+------------------------------------------------------------------+
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input string SymbolList = "US500.cash,US100.cash,US30.cash,XAUUSD,GER40.cash,UK100.cash,EURUSD";
input double LegFrac    = 0.142857;   // notional per trade as fraction of equity
input int    RangeMin   = 30;
input double RiskPct    = 0.0;        // >0: risico per trade als fractie van equity (verlies bij stop = OR-breedte); 0 = LegFrac-notional
input double MaxLevPos  = 4.0;        // max notional per positie als veelvoud van equity (alleen bij RiskPct > 0)
input ulong  MagicNumber = 20260931;
input string DiagBestandsnaam = "ORBSleeve_output.csv";

string syms[];
int    sessType[];       // 0 = New York, 1 = Frankfurt, 2 = London
int    dayKey[];         // yyyymmdd of the session state
int    stage[];          // 0 wait range, 1 orders placed/armed, 2 traded, 3 done
double orHi[], orLo[];

datetime dayDate[];
double   dayStartBal[], dayStartEq[], dayMinEq[], dayEndEq[];
int      dayCount = 0;

void TrackDaily()
  {
   datetime now = TimeCurrent(), d = now - (now % 86400);
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
   FileWrite(fh, "close_time", "symbol", "profit", "raw_profit", "swap", "commission", "volume", "open_time", "side", "price_in", "price_out", "comm_in");
   int total = HistoryDealsTotal();
   for(int i = 0; i < total; i++)
     {
      ulong t = HistoryDealGetTicket(i);
      if(t == 0 || HistoryDealGetInteger(t, DEAL_ENTRY) != DEAL_ENTRY_OUT) continue;
      long pid = HistoryDealGetInteger(t, DEAL_POSITION_ID);
      datetime ot = 0; double pin = 0, cin = 0; long tin = -1;
      for(int j = i - 1; j >= 0; j--)
        {
         ulong t2 = HistoryDealGetTicket(j);
         if(HistoryDealGetInteger(t2, DEAL_POSITION_ID) == pid && HistoryDealGetInteger(t2, DEAL_ENTRY) == DEAL_ENTRY_IN)
           {
            ot = (datetime)HistoryDealGetInteger(t2, DEAL_TIME); pin = HistoryDealGetDouble(t2, DEAL_PRICE);
            cin = HistoryDealGetDouble(t2, DEAL_COMMISSION); tin = HistoryDealGetInteger(t2, DEAL_TYPE); break;
           }
        }
      double raw = HistoryDealGetDouble(t, DEAL_PROFIT), sw = HistoryDealGetDouble(t, DEAL_SWAP), cm = HistoryDealGetDouble(t, DEAL_COMMISSION);
      FileWrite(fh, TimeToString((datetime)HistoryDealGetInteger(t, DEAL_TIME), TIME_DATE|TIME_MINUTES), HistoryDealGetString(t, DEAL_SYMBOL),
                DoubleToString(raw + sw + cm + cin, 2), DoubleToString(raw, 2), DoubleToString(sw, 2), DoubleToString(cm, 2),
                DoubleToString(HistoryDealGetDouble(t, DEAL_VOLUME), 2), TimeToString(ot, TIME_DATE|TIME_MINUTES),
                (tin == DEAL_TYPE_BUY ? "1" : "-1"), DoubleToString(pin, 6), DoubleToString(HistoryDealGetDouble(t, DEAL_PRICE), 6),
                DoubleToString(cin, 2));
     }
   FileClose(fh);
  }

// n-th Sunday (n>=1) or last Sunday (n=0) of a month, as day number
int SundayOf(int year, int month, int n)
  {
   MqlDateTime t; t.year = year; t.mon = month; t.day = 1; t.hour = 0; t.min = 0; t.sec = 0;
   datetime first = StructToTime(t);
   MqlDateTime f; TimeToStruct(first, f);
   int firstSunday = 1 + (7 - f.day_of_week) % 7;
   if(n > 0) return firstSunday + 7 * (n - 1);
   int dim = 31; if(month == 4 || month == 6 || month == 9 || month == 11) dim = 30;
   int last = firstSunday; while(last + 7 <= dim) last += 7;
   return last;
  }

// 1 in the weeks where the US is on DST but Europe is not (NY-Europe offset 5h instead of 6h / London 4h instead of 5h)
bool DstMismatch(datetime server)
  {
   MqlDateTime s; TimeToStruct(server - 7 * 3600, s);   // New York local date
   int md = s.mon * 100 + s.day;
   int usStart = 300 + SundayOf(s.year, 3, 2), euStart = 300 + SundayOf(s.year, 3, 0);
   int euEnd = 1000 + SundayOf(s.year, 10, 0), usEnd = 1100 + SundayOf(s.year, 11, 1);
   return (md >= usStart && md < euStart) || (md >= euEnd && md < usEnd);
  }

// session open/close for the server day containing 'now', in server time
void Session(int k, datetime now, datetime &op, datetime &cl)
  {
   datetime d0 = now - (now % 86400);
   int shift = (sessType[k] != 0 && DstMismatch(now)) ? 3600 : 0;
   if(sessType[k] == 0) { op = d0 + 16 * 3600 + 30 * 60; cl = d0 + 23 * 3600; }
   else { op = d0 + 10 * 3600 + shift; cl = d0 + 18 * 3600 + 30 * 60 + shift; }
  }

double Lots(string s, double width)
  {
   double price = SymbolInfoDouble(s, SYMBOL_ASK);
   double tv = SymbolInfoDouble(s, SYMBOL_TRADE_TICK_VALUE), ts = SymbolInfoDouble(s, SYMBOL_TRADE_TICK_SIZE);
   if(price <= 0 || tv <= 0 || ts <= 0) return 0;
   double step = SymbolInfoDouble(s, SYMBOL_VOLUME_STEP), mn = SymbolInfoDouble(s, SYMBOL_VOLUME_MIN), mx = SymbolInfoDouble(s, SYMBOL_VOLUME_MAX);
   double eq = AccountInfoDouble(ACCOUNT_EQUITY);
   double lotsN = eq * LegFrac / (price * tv / ts);
   if(RiskPct > 0 && width > 0)
      lotsN = MathMin(eq * RiskPct / (width * tv / ts), eq * MaxLevPos / (price * tv / ts));
   double lots = MathFloor(lotsN / step) * step;
   return lots < mn ? 0 : MathMin(mx, lots);
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

int CountOrders(string s)
  {
   int n = 0;
   for(int i = OrdersTotal() - 1; i >= 0; i--)
     {
      ulong t = OrderGetTicket(i);
      if(t != 0 && OrderGetInteger(ORDER_MAGIC) == (long)MagicNumber && OrderGetString(ORDER_SYMBOL) == s) n++;
     }
   return n;
  }

void DeleteOrders(string s)
  {
   for(int i = OrdersTotal() - 1; i >= 0; i--)
     {
      ulong t = OrderGetTicket(i);
      if(t != 0 && OrderGetInteger(ORDER_MAGIC) == (long)MagicNumber && OrderGetString(ORDER_SYMBOL) == s) trade.OrderDelete(t);
     }
  }

void CloseAll(string s)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong t = PositionGetTicket(i);
      if(t != 0 && PositionGetInteger(POSITION_MAGIC) == (long)MagicNumber && PositionGetString(POSITION_SYMBOL) == s) trade.PositionClose(t);
     }
  }

void Handle(int k)
  {
   string s = syms[k];
   datetime now = TimeCurrent();
   datetime op, cl;
   Session(k, now, op, cl);
   MqlDateTime dt; TimeToStruct(now, dt);
   int key = dt.year * 10000 + dt.mon * 100 + dt.day;
   if(key != dayKey[k]) { dayKey[k] = key; stage[k] = 0; }
   if(dt.day_of_week == 0 || dt.day_of_week == 6) return;
   // sessie-einde: alles plat
   if(now >= cl - 60)
     {
      if(HasPos(s)) CloseAll(s);
      if(CountOrders(s) > 0) DeleteOrders(s);
      if(!HasPos(s) && CountOrders(s) == 0) stage[k] = 3;
      return;
     }
   if(now < op + RangeMin * 60) return;
   if(stage[k] == 0)
     {
      MqlRates r[];
      int n = CopyRates(s, PERIOD_M5, op, op + RangeMin * 60 - 1, r);
      if(n < RangeMin / 5 || r[0].time != op) { stage[k] = 3; return; } // geen volledige opening range
      double hi = r[0].high, lo = r[0].low;
      for(int i = 1; i < n; i++) { hi = MathMax(hi, r[i].high); lo = MathMin(lo, r[i].low); }
      orHi[k] = hi; orLo[k] = lo;
      double lots = Lots(s, hi - lo);
      if(lots <= 0 || hi <= lo) { stage[k] = 3; return; }
      double ask = SymbolInfoDouble(s, SYMBOL_ASK), bid = SymbolInfoDouble(s, SYMBOL_BID);
      bool ok = true;
      if(ask >= hi) ok = trade.Buy(lots, s, 0, lo, 0);
      else if(bid <= lo) ok = trade.Sell(lots, s, 0, hi, 0);
      else
        {
         ok = trade.BuyStop(lots, hi, s, lo, 0, ORDER_TIME_GTC, 0) && trade.SellStop(lots, lo, s, hi, 0, ORDER_TIME_GTC, 0);
        }
      if(ok) stage[k] = 1;
      return;
     }
   if(stage[k] == 1 && HasPos(s))
     {
      if(CountOrders(s) > 0) DeleteOrders(s);   // OCO
      stage[k] = 2;
     }
  }

int OnInit()
  {
   trade.SetExpertMagicNumber(MagicNumber);
   string parts[];
   int n = StringSplit(SymbolList, ',', parts);
   ArrayResize(syms, n); ArrayResize(sessType, n); ArrayResize(dayKey, n); ArrayResize(stage, n);
   ArrayResize(orHi, n); ArrayResize(orLo, n);
   for(int i = 0; i < n; i++)
     {
      syms[i] = parts[i];
      SymbolSelect(syms[i], true);
      sessType[i] = (syms[i] == "GER40.cash") ? 1 : ((syms[i] == "UK100.cash" || syms[i] == "EURUSD") ? 2 : 0);
      dayKey[i] = 0; stage[i] = 0;
     }
   EventSetTimer(10);
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason) { EventKillTimer(); ExportAll(); }
void Step() { TrackDaily(); for(int k = 0; k < ArraySize(syms); k++) Handle(k); }
void OnTick()  { Step(); }
void OnTimer() { Step(); }
//+------------------------------------------------------------------+
