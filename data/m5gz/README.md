# data/m5gz — eenmalige FTMO-M5-momentopname (U-006 optie A, NEXT_STEPS v39)

- **Bron:** FTMO-MT5 (server `FTMO-Server`, servertijd = New York + 7 u), M5-bars geëxporteerd met `mt5_export_m5.py` op de VM; lokaal op Debian in `data/m5/`.
- **Periode:** 2021-01 → 2026-09-29 (momentopname; **niet dagelijks bijgewerkt**). Reserve-OOS 2025-01→ zit erin — alleen gebruiken zoals PREREG/CEO toestaan.
- **Symbolen (24):** FX EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, NZDUSD, EURGBP, EURJPY, GBPJPY, AUDJPY, EURCHF, EURAUD, GBPAUD; metalen XAUUSD, XAGUSD;
  indices US500cash, US100cash, US30cash, GER40cash, UK100cash, JP225cash, AUS200cash, EU50cash.
- **Toegevoegd (NEXT_STEPS v41, 2026-09-30 ≈ 21:20Z):** 41 US-aandelen (universe_us41.txt: AAPL, AMZN, BABA, BAC, GOOG, MSFT, NFLX, NVDA, PFE, RACE, T, TSLA, V,
  WMT, ZM, META, GE, BA, RTX, LMT, PLTR, AMD, INTC, QCOM, AVGO, CSCO, JNJ, SBUX, KO, MSTR, GME, NKE, CVX, FDX, JPM, DIS, IBM, ASML, AZN, BRK.B, XOM) voor A2,
  en BTCUSD, ETHUSD, USOILcash, UKOILcash voor S2. Totaal 69 symbolen, ≈ 159 MB. Let op aandelen: FTMO-aandelen openen vanaf 2024 om 09:35 ET en sommige
  symbolen hebben een uur-offset (zie Q2-RUNLOG: sessie = alle bars van de NY-datum); veel aandelen-bars hebben spread 0 (= ontbrekend, zie COSTS_FTMO_alle.csv).
- **Formaat:** gzip van de originele CSV (identieke inhoud; `CHECKSUMS_bron_csv.sha256` = SHA-256 van de ongecomprimeerde bron, `CHECKSUMS.sha256` = van de .gz).
  Kopregel `# ... point=<p>;` gevolgd door `time;open;high;low;close;spread` (spread in punten; × point = prijs). Tijd = servertijd.
- **Laden:** `b4_sim.load` leest `data/m5/<SYM>.csv`. Voor de gz-versie:
  ```python
  import gzip, io
  from datetime import datetime
  def load_gz(sym):
      point, bars = None, []
      for line in gzip.open(f"data/m5gz/{sym}.csv.gz", "rt"):
          if line.startswith("#"):
              point = float(line.split("point=")[1].split(";")[0]); continue
          if not line[0].isdigit():
              continue
          t, o, h, l, c, sp = line.rstrip().split(";")
          bars.append((datetime.strptime(t, "%Y.%m.%d %H:%M"), float(o), float(h), float(l), float(c), int(sp) * point))
      return bars
  ```
  Of: `mkdir -p data/m5 && for f in data/m5gz/*.csv.gz; do gunzip -c "$f" > data/m5/$(basename "$f" .gz); done` en dan `b4_sim.load` gewoon gebruiken.
- **Kosten:** spreads per uur in `COSTS_FTMO_alle_per_uur.csv`; swaps (tijdvariabel) in `data/ftmo_specs/`. Aandelen-M5 (A2) zijn toegevoegd (v41).
- **Licentie/gebruik:** FTMO-platformdata, alleen voor intern onderzoek in deze privé-repo; niet herverspreiden.
