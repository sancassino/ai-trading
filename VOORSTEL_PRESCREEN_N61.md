# VOORSTEL_PRESCREEN_N61 — AUS200 short-only TSMOM 20→10 (D-100 family A)

**Status:** **geen PREREG — D-092.1 FAIL_MEAN** mean **−26,05** < 50 (N=45).
**Auteur:** Strateeg (Faraday).  
**Instrument:** `AUS200cash` **short-only** when ret20 < 0. C-024 best_side=short (+0,64 %/jr).  
**Gate:** 3× RT ≈ 6 bp → bindend **50 bp** (D-097). Swap_gate short ≈ 0. Hold 10d non-overlap.

**D-094a (b):** equity TSMOM (Moskowitz–Ooi–Pedersen); proxy ASX/AORD if needed; FTMO-M5 kosten.

**Onderscheid:** ≠ **IDX_SHORT** (US100+US30 CEO/CTO PREREG); ≠ N35/N41 intradag EU→US FAIL_T; ≠ N52/N55 index long FAIL; ≠ ENERGY/TSMOM_DIV.

## Regel
- `ret20 < 0` → **SHORT**; else flat. Exit t+10. Non-overlap. Geen long-been.

## Pre-screen
- Train 2021–2023. PASS iff mean bruto ≥ **50**, N≥150. FAIL → STOP (geen US-add; geen L/H-grid).
