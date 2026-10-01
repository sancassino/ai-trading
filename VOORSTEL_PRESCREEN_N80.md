# VOORSTEL_PRESCREEN_N80 — UKOIL overnight-gap continuation, same-day flat (NEW_FAMILY E; D-097/D-100)

**Status:** **PASS → PREREG** — D-092.1 Strateeg screen N=415, mean +12,26 ≥ 8,13 → `PREREG_FTMO_N80.md` OPEN for U2 (2026-10-01 ~13:20 CEST).
**Auteur:** Strateeg (Grok).  
**Instrument:** `UKOILcash` (RT **2,71** bp; swap irrelevant — **EOD flat**).  
**NEW_FAMILY E:** commodity **overnight gap → same-session continuation, flat before night** — ≠ N18 US500 OVN gap, ≠ N19 XAU gap fill, ≠ N22 Lon→NY MR, ≠ N76 Mon→Thu hold, ≠ ENERGY TSMOM.

**Track 2 + D-100:** **intradag-vlak** (swap = 0). Entry after gap observed; exit same CET day.

**Gate:** 3 × RT = 3 × 2,71 = **8,13** bp (swap-free). No D-097 50-floor on pure intradag (consistent with N22 UKOIL intradag gate); edge must clear 8,13 with N≥150.

**D-094a:** train 2021–2023. Reden **(b)**: overnight inventory / news gap continuation in energy futures is a session microstructure effect; distinct from weekly calendar (N76) and from index OVN gaps (N18 FAIL_T). FTMO-M5 = uitvoering. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N18** US500 Overnight Gap Continuation FAIL_T (index; other venue)
- ≠ **N19** XAU Overnight Gap Fill FAIL (metal + fade)
- ≠ **N22** UKOIL Lon→NY session **MR** FAIL (fade vs **continuation**; other window)
- ≠ **N43** UKOIL NY-open drive underpowered; ≠ **N76** Mon→Thu multi-night
- ≠ **ENERGY / N49 / N59** swing TSMOM; ≠ **N78** VIX/US100 overnight
- ≠ ORB / L60 FX / N75–N77 mechanisms

## Regel
1. Prior reference: close ≤ **22:00 CET** prior session (`C_ref`).
2. At **08:00 CET** (London cash open proxy): `gap_bp = (mid_0800 / C_ref − 1) × 1e4`.
3. Trade only if `|gap_bp| ≥ 40`.
4. **Continuation:** if gap_bp ≥ +40 → **LONG**; if gap_bp ≤ −40 → **SHORT**. Entry next M5 after 08:00 signal bar.
5. Exit: flat at **17:00 CET** same day (or last M5 ≤17:00). **No overnight.**
6. Stop: 1,5 × ATR14(H1) from entry (optional in formal; pre-screen may omit stop for mean bruto — report stop_share if used). Non-overlapping (≤1 trade/day).

## Pre-screen
- Data: `data/m5gz/UKOILcash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **8,13** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N80. FAIL → STOP (geen gap-threshold grid, geen USOIL twin, geen overnight hold add-on).
