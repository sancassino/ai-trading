# VOORSTEL_PRESCREEN_N9 — GER40 Ochtend-Fade naar XETRA-Open

**Status:** Pre-screen aanvraag (D-092.1) — 2026-10-01 02:55 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen PREREG vóór screen-PASS.**  
**Instrument:** `GER40cash` (RT 1,40 bp → drempel 4,20 bp).  
**Grond:** PREREG_S2_LUNCH_OPEN PASS (+4,72 bp, US30/US100): fade van ochtendimpuls terug naar session-open werkt voor US cash. Hetzelfde mechanisme voor XETRA: GER40 ochtend-impuls (09:00–10:30 CET) fadet terug naar XETRA-open. GER40 dagrange 60–100 bp (hoog) → potentieel bruto ruimschoots boven drempel 4,20 bp.

---

## Idee (mechanisme)

Bij XETRA-open (09:00 CET) activeren institutionele orders (ETF-rebalancers, DAX-futures-hedgers). De initiaalbeweging in de eerste 90 minuten reflecteert overnight-positionering en Aziatische sessie-feedback. Na dit initial-balance-venster is er een "inventory liquidation" fase: market makers en delta-hedgers sluiten hun ochtend-inventaris, wat de prijs terug drijft richting de auction-open. Mechanisme is identiek aan US LUNCH_OPEN maar getimed op het XETRA-ritme.

**Onderscheid van dode sleeves:**
- ≠ N6 (N6 = 17:30–17:55 CET close-drive; dit = 10:30–12:00 CET ochtend-fade)
- ≠ GER_US_LEAD (dat was relatieve performance US-vs-GER; dit = absolute GER40-fade)
- ≠ VWAP_PB (geen VWAP; anker = XETRA-open 09:00 CET)
- ≠ B4b (onvoorwaardelijke laatste-30-min; dit = conditionele ochtend-fade)

---

## Regel (bevriesbaar zodra screen PASS)

**Session open:** open van eerste M5-bar na 09:00 CET (`P_open`).  
**Ochtend-beweging:**  
- `P_entry` = M5-close van de 10:30 CET bar  
- `morn_bp = 1e4 × (P_entry − P_open) / P_open`  
- `atr_bp = 1e4 × ATR14(D1_prior) / P_open`

**Signalen (max 1 trade/dag):**
- `morn_bp ≥ +0,40 × atr_bp` → **SHORT** op 10:30 CET close
- `morn_bp ≤ −0,40 × atr_bp` → **LONG** op 10:30 CET close
- Anders → geen trade

**Target:** `P_open` (fade terug naar XETRA-open).  
**Stop:** voorbij ochtend-extreem (09:00–10:30 high/low) + buffer 0,15 × ochtendrange.  
**Time exit:** hard flat 12:00 CET. Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/GER40cash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek aan §1 hierboven (threshold 0,40× ATR14, target = P_open, stop = extreem+buffer, flat 12:00).
- **Maatstaf:** mean bruto retour in bp (1 bp = 0,01%).
- **Gate:** mean bruto ≥ **4,20 bp** (3 × 1,40 bp RT).
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS → Strateeg schrijft PREREG_FTMO_N9. FAIL → STOP.
