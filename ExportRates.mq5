//+------------------------------------------------------------------+
//| ExportRates.mq5 - dumps real MT5 daily closes to FILE_COMMON CSV |
//| and exits immediately. Launched via Strategy Tester like the     |
//| trading EAs (same ini pattern), but does not trade.               |
//+------------------------------------------------------------------+
#property strict
input string OutFile = "rates_output.csv";

int OnInit()
  {
   return(INIT_SUCCEEDED); // let the tester run through to ToDate so full history gets cached
  }

void OnTick() {}

void OnDeinit(const int reason)
  {
   MqlRates rates[];
   int n = CopyRates(_Symbol, PERIOD_D1, 0, 100000, rates);
   int fh = FileOpen(OutFile, FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI, ';');
   if(fh != INVALID_HANDLE)
     {
      FileWrite(fh, "date", "close");
      for(int i = 0; i < n; i++)
         FileWrite(fh, TimeToString(rates[i].time, TIME_DATE), DoubleToString(rates[i].close, 5));
      FileClose(fh);
      Print("ExportRates: wrote ", n, " bars to ", OutFile);
     }
  }
