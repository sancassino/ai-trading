# VOORSTEL_PRESCREEN_N30 — Cross-Sectional 5d Momentum Basket (5-asset)

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:25; N=553, mean **+0,44** < 4,83 bp). Artifacts `results/R2/n28_n31_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrumenten:** `US100cash`, `US30cash`, `US500cash`, `GER40cash`, `XAUUSD` (zelfde pool als N26).  
**Track 4:** cross-sectioneel **momentum** (niet reversal) — long top-1 / short bottom-1 op prior **5d** return; hold één US-ochtendsessie.  
**Grond:** Jegadeesh–Titman korte-horizon XS-momentum: relatieve winnaars blijven kort winnen. Tegengesteld mechanisme aan N26 (1d reversal). Pool ≥5 → D-094a **(c)**.

**D-094a:** train 2021–2023 = 3y. Reden **(c)**: ≥5-asset pool; XS-momentum literatuur decennia. Herhaal in PREREG.

**Kosten / gate:** zelfde conservatieve worst-pair als N26: 3 × (0,83+0,78) = **4,83 bp**.

---

## Idee (mechanisme)

Elke dag: 5d close-to-close return (22:00 CET closes, t−1 vs t−6). Rank. Dag t: **long** argmax, **short** argmin, entry 15:30 CET, flat **21:00 CET** (langere hold dan N26 17:25 — vangt volle US-sessie). Swap 0.

**Onderscheid:**
- ≠ **N26** XS **1d reversal** (tegenovergesteld teken + andere lookback/exit)
- ≠ **N23** US100 **single-name** 2d TSMOM
- ≠ **B1** FX month TSMOM
- ≠ **N2** twin-index intradag z-score

---

## Regel (bevriesbaar zodra screen PASS)

1. Per symbool: `ret5 = 1e4 × (C_{t-1} − C_{t-6}) / C_{t-6}` met C = M5-close ~22:00 CET.  
2. `long_sym` = argmax(ret5); `short_sym` = argmin(ret5); ties → skip.  
3. Entry beide 15:30 CET; exit beide **21:00 CET**.  
4. Combined equal-weight bruto bp = 0,5 × (long_leg + short_leg).

**Stop:** geen in bruto pre-screen. **Swap = 0**.

---

## Pre-screen aanvraag

- **Data:** m5gz pool 5, train **2021-01-01 … 2023-12-31**.
- **Gate:** mean combined bruto ≥ **4,83 bp**. N≥150.
- **Geen test/reserve.** PASS → PREREG_FTMO_N30 (D-094a **(c)**).
