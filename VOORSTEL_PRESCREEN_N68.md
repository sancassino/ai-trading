# VOORSTEL_PRESCREEN_N68 — GER40 short-only TSMOM 20→10 (D-100 family A)

**Status:** **BARRED** — family-A overnight index-short closed (C-025 after IDX_SHORT FAIL_COST_GATE U2 `72f40d3`). Geen screen/PREREG.  
**Instrument:** `GER40cash` short-only when ret20 < 0 (C-024 best_side=short ≈ 0 %/jr). Gate **50 bp**.  
**Onderscheid:** ≠ IDX_SHORT (US100/US30); ≠ N64 HK50 underpowered; ≠ N35/N41 intradag; ≠ S2-GER40 open STOP.
## Regel
- ret20 < 0 → SHORT; exit t+10; non-overlap.
## Pre-screen
- Train 2021–2023. PASS iff mean ≥ 50, N≥150. FAIL → STOP.
