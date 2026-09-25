#property strict
input string OutFile = "symbol_info_dump.csv";
string SYMS[] = {"AAPL","MSFT","AMZN","GOOG","META","NVDA","TSLA","US500.cash"};

int OnInit()
  {
   int fh = FileOpen(OutFile, FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI, ';');
   if(fh != INVALID_HANDLE)
     {
      FileWrite(fh, "symbol", "swap_long", "swap_short", "swap_mode", "swap_rollover3days");
      for(int i = 0; i < ArraySize(SYMS); i++)
        {
         string s = SYMS[i];
         SymbolSelect(s, true);
         double swapLong = SymbolInfoDouble(s, SYMBOL_SWAP_LONG);
         double swapShort = SymbolInfoDouble(s, SYMBOL_SWAP_SHORT);
         long swapMode = SymbolInfoInteger(s, SYMBOL_SWAP_MODE);
         long rollover3 = SymbolInfoInteger(s, SYMBOL_SWAP_ROLLOVER3DAYS);
         FileWrite(fh, s, DoubleToString(swapLong,4), DoubleToString(swapShort,4), IntegerToString(swapMode), IntegerToString(rollover3));
        }
      FileClose(fh);
      Print("SymbolInfoDump: wrote ", ArraySize(SYMS), " rows");
     }
   return(INIT_FAILED);
  }
void OnTick() {}
