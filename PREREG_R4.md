# PREREG R4 — positief-scheve breakout met trailing stop op kosten-lage FX/goud (vastgelegd vóór berekening, 2026-09-30)
- Symbolen (7 laagste kosten uit R1, < 0,45 bp per kant): EURUSD, GBPUSD, USDJPY, USDCAD, USDCHF, XAUUSD, GBPJPY. FTMO-M5 2021–2026
  → H4-bars in servertijd (blokken 00/04/08/12/16/20).
- Regel (Donchian 20/10 met ATR-trailing, één vaste set): long als H4-slot > hoogste high van de 20 vorige H4-bars; short als
  slot < laagste low van de 20 vorige. Uitstap: slot onder (long) / boven (short) het 10-bar-kanaal, óf trailing stop 3 × ATR(20, H4)
  vanaf het hoogste slot (long) / laagste slot (short) sinds instap (getest op het H4-slot; vulling op dat slot). Eén positie per symbool;
  omkeren alleen na uitstap. Instap op het H4-slot.
- Grootte: gelijk risico, notional per positie = 1/7 van de equity × (0,5% / ATR%(20, H4)) genormaliseerd zodat de gemiddelde
  bruto hefboom ≈ 1; (vaste regel, geen tuning).
- Kosten: spread instapbar (long) / uitstapbar (short) + commissie (R1-tabel) + swap per kalendernacht volgens huidige FTMO-specs
  (data/swap_specs_fx.csv; long/short apart, constant).
- Dagreeks (equity op het slot van elke serverdag, incl. zwevend) → SR, skew, max dagdip, en Q1b-frontier (2-Step).
- **Beslisregel:** gepoolde per-trade netto t ≥ 3 in train (2021–2023) én test (2024–2026), dag-skew > 0, dag-SR ≥ 1,0.
  Trials +1 → 410.
