# VOORSTEL_PRESCREEN_N87 — US30cash Intraday Opening-Gap Fade (D-100 family D; NEW_FAMILY L)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** track 2+4 + **D-100 family D** intradag-flat; filed 2026-10-01 ~13:50 CEST; pipeline vervanging na C-030 N82–N86 DIAG_FAIL).  
**Auteur:** Strateeg (Claude). **NEW_FAMILY L** (opening gap fade — nooit eerder geprobeerd in pipeline).  
**Instrument:** `US30cash` (RT **0,45 bp** — COSTS_FTMO; intradag-flat = geen swap).  
**Track 2+4 + D-100 family D:** intradag mean-reversion van opening gap. Flat vóór US close → nul overnight swap.

**Gate (intradag-flat):**  
0,45 + 0 = **0,45 bp/trade** → gate 3 × 0,45 = **1,35 bp**.

**D-094a:** train 2021–2023. Reden **(b)**: equity-index opening gap fade literatuur (Trietsch 2005; S&P/Dow futures institutional rebalancing bij open; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N40** GER40 mid-morning FAIL (ander index + ander mechanisme: dat was momentum, dit = mean-reversion gap)
- ≠ **N80** UKOIL OVN-gap continuation FAIL_COST_GATE (continuation ≠ fade; energie ≠ equity)
- ≠ **ORB** BARRED (range breakout ≠ gap fade; ORB = prijsuitbraak na opening range, dit = terugkeer naar prior close)
- ≠ enig TSMOM / FX carry / metals
- ≠ **N85** US500→US100 lead-lag DIAG_FAIL (cross-asset lead-lag ≠ gap-fade single instrument)

## Regel
- `gap_bp = 1e4 × (open_t − close_{t-1}) / close_{t-1}` (open = eerste M5-bar ≤ 07:05 CET US30; close_{t-1} = laatste M5-bar ≤ 22:00 CET)
- `gap_bp < −30` → **LONG** op open; flat 21:55 CET (voor nacht)
- `gap_bp > +30` → **SHORT** op open; flat 21:55 CET
- `|gap_bp| ≤ 30` → skip
- Max 1 positie per dag. Geen overnight hold. **Non-overlapping** (één intradag positie tegelijk).
- Bilateraal (long + short).

## Pre-screen
- Data: `data/m5gz/US30cash.csv.gz` → M5 bars, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **1,35 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N87. FAIL → STOP (geen drempel-grid, geen US500/US100-switch).
