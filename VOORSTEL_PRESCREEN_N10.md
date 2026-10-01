# VOORSTEL_PRESCREEN_N10 — XAU Mid-London Fade naar AM-Fix

**Status:** Pre-screen aanvraag (D-092.1) — 2026-10-01 02:55 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen PREREG vóór screen-PASS.**  
**Instrument:** `XAUUSDcash` (RT 0,83 bp → drempel 2,49 bp).  
**Grond:** XAU_AM_FADE PASS (+18,70 bp): XAU heeft bewezen intradag fade-edge. Dit is een ander venster: fade van mid-London-move terug naar LBMA AM-fixing-niveau, vóór de PM-fixing. Onderscheidend van alle XAU-sleeves die al gefaald zijn.

---

## Idee (mechanisme)

De LBMA AM-fixing (±10:30 CET) stelt een dagelijks ankerpunt. In de mid-London-periode (10:30–12:00 CET) reageren speculatieve traders en algo's op macro-news. Als de prijs significant afwijkt van de AM-fix, is er een reversion-kracht: leveranciers, ETF-arbitrageurs en centrale banken handelen t.o.v. het gefixte niveau. Vóór de PM-fixing (±15:00 CET) is er een correctie-window (12:00–14:30 CET).

**Onderscheid van dode sleeves:**
- ≠ XAU_AM_FADE (fade van EERSTE ochtendbeweging 09:00–09:55 CET; dit = mid-London 10:30–12:00 CET fade naar AM-fix anker)
- ≠ N4 XAU_PRENY (pre-NY range breakout 13:00–15:00 CET; dit is een fade, ander venster, andere richting)
- ≠ N7/N8 (N7 = pre-London range BO; N8 = post-AM-fix continuation; dit = fade terug naar AM-fix, reversion)

---

## Regel (bevriesbaar zodra screen PASS)

**AM-fix-niveau:** `P_amfix` = M5-close van de 10:30 CET bar (proxy voor LBMA AM-fixing).  
**Mid-London-beweging:**  
- `P_entry` = M5-close van de 12:00 CET bar  
- `mid_bp = 1e4 × (P_entry − P_amfix) / P_amfix`

**Signalen (max 1 trade/dag):**
- `mid_bp ≥ +0,20%` (+20 bp) → **SHORT** op 12:00 CET close (fade terug naar AM-fix)
- `mid_bp ≤ −0,20%` (−20 bp) → **LONG** op 12:00 CET close
- Anders → geen trade

**Target:** `P_amfix` (fade terug naar AM-fix niveau).  
**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Time exit:** hard flat 14:30 CET (vóór PM-fixing / pre-NY). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/XAUUSDcash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek aan §1 hierboven (threshold ±20 bp move, fade target = P_amfix, stop = ATR14, flat 14:30).
- **Maatstaf:** mean bruto retour in bp (1 bp = 0,01%).
- **Gate:** mean bruto ≥ **2,49 bp** (3 × 0,83 bp RT).
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS → Strateeg schrijft PREREG_FTMO_N10. FAIL → STOP.
