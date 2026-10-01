# VOORSTEL_PRESCREEN_N22 — UKOILcash London→NY Session Mean-Reversion

**Status:** **FAIL** — U2 D-092.1 train-only pre-screen 2026-10-01 CEST. N=345, mean bruto=-1.6697 bp, gate=8.13 bp → `NO_PREREG_screen_fail`. See `results/R2/n20_n23_prescreen/`. **No PREREG.**

**U2 pre-screen result:** see RUNLOG_R2 / prescreen.md — mean bruto below gate; N≥150; STOP.
**Auteur:** Strateeg (Grok).  
**Instrument:** `UKOILcash` (Brent CFD; RT **2,71 bp** COSTS_FTMO / `results/screen_cost_vol.csv` → drempel **8,13 bp** = 3× RT; cost_in_costs_ftmo=True; rt_over_day≈0,010).  
**Track 2:** commodity (olie) — niet-US-index.  
**Grond:** London ochtend (ICE/Europe energy desks) zet vaak een directionele impuls in Brent; bij NY-open (15:30 CET) herprijzen US energy desks en paper-oil flow. Extreme London-AM moves (≥ ±40 bp vs 09:00) neigen naar partial mean-reversion in het London→NY handoff-venster wanneer er geen EIA/OPEC-eventfilter nodig is (geen peeking). Intradag flat → swap 0.

**D-094a:** train 2021–2023 = 3y. Schriftelijke reden **(b)**: sessie-handoff / inventory MR op energie is mechanistisch tijdloos; proxy `data/daily/BRENT_F.csv` (langere futures-historie) kan later discovery ondersteunen; FTMO-M5 = kosten/uitvoering. Herhaal in PREREG.

---

## Idee (mechanisme)

UKOILcash volgt ICE Brent. Europees ochtendflow (09:00–12:00 CET) creëert soms een overshoot t.o.v. de London-open. Tussen 15:30–18:00 CET komen US desks bij: als de London-AM impuls groot was zonder verdere catalyst in dit screen (puur prijsregel), fade terug richting London-open over 2–3 uur.

**Onderscheid van dode sleeves:**
- ≠ **S2-USOIL EIA breakout** (dead; USOIL + EIA-window breakout; dit = UKOIL + London-AM fade, geen event-breakout)
- ≠ A5 / N11 / N15–N17 ORB-familie (geen opening-range break)
- ≠ N4/N7/N8/N12 XAU breakouts
- ≠ overnight oil sleeves (we zijn **intradag flat**; UKOIL short-swap is toxisch −27 bp/nacht)

---

## Regel (bevriesbaar zodra screen PASS)

**London-AM impuls:**  
- `P_Lopen` = M5-close 09:00 CET  
- `P_1200` = M5-close 12:00 CET  
- `lon_bp = 1e4 × (P_1200 − P_Lopen) / P_Lopen`

**Signalen (max 1 trade/dag):**  
- `lon_bp ≥ +40 bp` → **SHORT** op 15:30 CET close (fade London-AM long impulse)  
- `lon_bp ≤ −40 bp` → **LONG** op 15:30 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag) vanaf entry.  
**Exit:** hard flat **18:30 CET** (3u na entry). **Swap = 0** (intradag; expliciet geen overnight — short swap UKOIL ≈ +27 bp/nacht kost).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/UKOILcash.csv.gz`, train **2021-01-01 … 2023-12-31** only.
- **Regel:** lon_bp 09:00–12:00 CET ≥ ±40 bp → fade entry 15:30 CET, stop ATR14, flat 18:30 CET.
- **Maatstaf:** signed mean bruto bp + median + N.
- **Gate:** mean bruto ≥ **8,13 bp** (3 × 2,71 bp RT). N≥150.
- **Geen test/reserve (2024/2025+) aanraken.**
- **Uitkomst:** PASS + N≥150 → PREREG_FTMO_N22 (D-094a (b)). FAIL of N<150 → STOP.
