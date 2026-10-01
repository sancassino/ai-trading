# VOORSTEL_PRESCREEN_N26 — Cross-Sectional 1d Reversal Basket (5-asset, 1 sessie flat)

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:22; N=581, mean **+0,77** < 4,83 bp). Artifacts `results/R2/n24_n27_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrumenten (pool ≥5, alle in COSTS + m5gz):** `US100cash`, `US30cash`, `US500cash`, `GER40cash`, `XAUUSD`.  
**Track 4:** andere horizon/mechanisme — **cross-sectioneel** 1-dag reversal, hold ≈1 sessie (sync flat), geen single-name TSMOM.  
**Grond:** Klassieke short-horizon cross-sectional reversal (Jegadeesh): gisteren’s relatieve winnaar mean-revert vs verliezer over de volgende liquid sessie. Pool van 5 FTMO-liquide namen geeft D-094a**(c)** (multi-asset evidence) i.p.v. single-symbol 3y-excuse alleen.

**D-094a:** train 2021–2023 = 3y per been. Schriftelijke reden **(c)**: cross-sectionele pool ≥5 symbolen met gedeeld mechanisme; literatuur XS-reversal decennia; FTMO-M5 toetst kosten op de twee actieve benen. Herhaal in PREREG.

**Kosten / gate:** long 1 + short 1 → RT_pair = RT_i + RT_j. Binding pre-screen gate = 3 × worst-case pair in pool: XAU 0,83 + US500 0,78 = **1,61 bp** → **4,83 bp**. U2 mag ook per-trade gate 3×(RT_long+RT_short) rapporteren; pooled mean bruto moet ≥ **4,83 bp** (conservatief).

---

## Idee (mechanisme)

Elke dag t−1: close-to-close return per pool-lid (laatste M5 vóór 22:00 CET). Rank. Op dag t: **long** de laagste return (bottom-1), **short** de hoogste (top-1), equal notional (1 unit bp-risk; geen ATR-sizing in pre-screen — equal €-notional OK). Entry synchroon 15:30 CET (US open; GER40 nog open). Flat synchroon **17:25 CET** (vóór XETRA-close; alle benen gelijk). Swap = 0.

**Onderscheid van dode sleeves:**
- ≠ **N23** US100 2d **TSMOM** (time-series momentum single name; dit = **cross-sectioneel reversal**, 1 sessie)
- ≠ **B1** FX overnight-month TSMOM
- ≠ **N2** US100↔US500 relative morning z-score (twin-index intradag; dit = 5-asset prior-day rank, EOD-ish sync)
- ≠ ORB / gap / single-symbol fades N20–N22

---

## Regel (bevriesbaar zodra screen PASS)

**Signal (eens per kalenderdag):**  
1. Voor elk symbool in pool: `ret_prev = 1e4 × (C_{t-1} − C_{t-2}) / C_{t-2}` met `C` = M5-close dichtst bij **22:00 CET** (of laatste bar die dag).  
2. `long_sym` = argmin(ret_prev); `short_sym` = argmax(ret_prev); bij gelijke rank → skip dag.  
3. Entry: M5-close **15:30 CET** op beide benen (signed: +1 long_sym, −1 short_sym).  
4. Exit: M5-close **17:25 CET** beide benen.  
5. Trade-PnL bruto bp = 0,5 × (long_leg_bp + short_leg_bp) **of** rapporteer sum van benen / 2 (equal-weight); wees consistent. Gate vergelijkt met **4,83 bp** op diezelfde definitie (aanbevolen: mean van combined equal-weight bp).

**Stop:** geen aparte stop in bruto pre-screen (zuivere hold); optioneel later 1,5×ATR in PREREG.  
**Swap:** 0 (intradag sync).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/{US100cash,US30cash,US500cash,GER40cash,XAUUSD}.csv.gz`, train **2021-01-01 … 2023-12-31**.
- **Regel:** prior-day rank reversal; entry 15:30 / exit 17:25 CET; equal-weight combined bp.
- **Maatstaf:** signed mean bruto combined bp + median + N (N = handelsdagen met geldige rank; verwacht N≫150).
- **Gate:** mean bruto ≥ **4,83 bp**. N≥150.
- **Geen test/reserve aanraken.**
- **Uitkomst:** PASS + N≥150 → PREREG_FTMO_N26 (D-094a **(c)** + kosten per been). FAIL → STOP.
