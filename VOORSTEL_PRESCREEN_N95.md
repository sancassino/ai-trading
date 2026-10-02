# VOORSTEL_PRESCREEN_N95 — XAUUSD London-AM → NY cash continuation, session-flat (NEW_FAMILY T)

**Status:** **geen PREREG — D-092.1 FAIL** Strateeg `n94_n95_prescreen` (2026-10-02 ~21:05 CEST).  
N=**226**, mean bruto **+1,40 bp < gate 2,49** (med −0,97; years 2021 +0,34 / 2022 +2,06 / 2023 +1,86). Artifact: `results/R2/n94_n95_prescreen/`.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY T** (gold London-AM directional impulse → NY cash-session continuation).  
**Instrument:** `XAUUSD` (RT **0,83 bp**; intradag-flat = geen swap).  
**Gate:** 3 × 0,83 = **2,49 bp**.

**D-094a:** train 2021–2023. Reden **(b)**: goud liquiditeit migreert London AM → NY (Batten et al. gold microstructure / London–NY handoff; FTMO-M5 = kosten).

**Onderscheid (historisch):** ≠ S2-XAU_AM_FADE fade / N36 NY-drive FAIL_T / N12/N10/N25 fades / N82 XAG / N86 VoV MR.

## Regel (bevroren; geen retune)
- am_bp 08:00→11:00; trade iff |am_bp|≥25; continuation @15:30; flat 21:00 same day.

## Pre-screen result
- FAIL (mean). **STOP** — geen fade-rewrite, geen XAG twin, geen overnight. Dead screen T.
