# PREREG_S2_XAU_AM_FADE — XAUUSD London morning extreme fade (intraday-vlak)

**Status:** Pre-registratie 2026-10-01 ~00:00 Europe/Amsterdam, branch `grok/strateeg-2`.  
**Auteur:** Strateeg-2. **Geen resultaten vóór deze commit.**  
**Nacht D-091:** non-clone; **≠** dode `PREREG_S2_XAU_OVERLAP` (overlap *breakout*); **≠** N1 (US indices); **≠** GS02 (FX Asian fade).  
**Instrument:** `XAUUSD` (RT ≈ 0,83 bp; in COSTS_FTMO; screen-vriendelijk).

---

## 1. Bevroren regel (exact)

**Mechanisme:** eerste London-uren overdrijven vaak Asia-inventory; extreme moves mean-reverteren intradag voordat NY overlap trend zet. We **faden de ochtendextreem**, we breken geen overlap-range.

**Kalender:** Europe/Amsterdam.

**Asia anchor:** high/low 00:00–08:00.  
**London AM window:** 08:00–11:30.  
**Extreem-check om 11:30:**
- `up_ext = 1e4 × (H_0830_1130 − Asia_high) / Asia_high` (alleen als H > Asia_high)
- `dn_ext = 1e4 × (Asia_low − L_0830_1130) / Asia_low` (alleen als L < Asia_low)
- `atr_bp = 1e4 × ATR(14,D1) / P_0800`

**Trigger (max 1/dag):**
- Als `up_ext ≥ 0,60 × atr_bp` én `up_ext > dn_ext` → **SHORT** op 11:30 M5-close (fade upside extension)
- Als `dn_ext ≥ 0,60 × atr_bp` én `dn_ext > up_ext` → **LONG** op 11:30 M5-close
- Geen Asia-extension → flat

**Exit (swap = 0):**
1. **Target:** terug naar Asia mid `((Asia_high+Asia_low)/2)`  
2. **Stop:** `1,0 × max(up_ext,dn_ext)` voorbij entry in extensie-richting (same-bar → stop)  
3. **Time:** hard flat 14:00 Europe/Amsterdam (**vóór** NY-overlap — voorkomt overlap-breakout-regime van dode S2-XAU)

**Verboden na zien:** 0,60×, 11:30 anker, 14:00 flat wijzigen. Report-only: 0,45× / 0,75× ATR.

**≠ XAU_OVERLAP:** die brak 14:00–14:30 range *with* trend in overlap; deze *fadet* London-AM extensie en is flat vóór overlap.

---

## 2. Kosten & poort

- RT XAUUSD 0,83 bp.  
- Poort train: **getekend gemiddeld bruto ≥ 3× 0,83 bp**.  
- +50% RT-stress. FAIL → STOP.

---

## 3. Data / venster

- M5 XAUUSD 2018–2024-12 (of langste FTMO/Dukascopy in repo).  
- Train 2021–2023 / Test 2024 / **Reserve 2025→ ONAANGERAAKT**.

---

## 4. Beslisregel

1. Kostenpoort → PASS ⇒ trial +1.  
2. Dag-cluster t ≥ 2,0 train én test; mean netto > 0 beide; N ≥ 120 train.  
3. Kosten < 50% bruto; skew > 0 of max dagdip ≤ −1,5% bij 0,75% risk.  
4. Corr vs dode S2-XAU_OVERLAP-dagreeks (als beschikbaar) — \|ρ\| > 0,5 ⇒ label "residual clone", geen shortlist.  
5. `ftmo_ev()`; FTMO-EV ≥ €150/poging; p95 dagverlies ≤ 2%.

---

## 5. Faalrisico's

Trend-dagen London→NY zonder revert; Asia-range te wijd (weinig extensies); 0,83 bp eet kleine fades.

---
**Bevroren:** 2026-10-01 00:00 CEST — nacht non-clone.  
**Auteur:** Strateeg-2 (`grok/strateeg-2`)
