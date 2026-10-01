# VOORSTEL_PRESCREEN_N31 — XAUUSD Asia→London Handoff Continuation

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:25; N=21≪150, mean **−0,01** < 2,49 bp). Artifacts `results/R2/n28_n31_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrument:** `XAUUSD` (RT **0,83 bp** → drempel **2,49 bp**).  
**Track 2:** commodity/metaal — **Asia-sessie impuls vervolgt in London AM**, tegengesteld aan AM_FADE / N25 NY-PM fade.  
**Grond:** Asia (00:00–08:00 CET) zet vaak de goudrichting; London open (08:00) amplificeert via COMEX/ETF overlap tot AM-fix (~12:00–13:00). Continuation 08:00→12:00 van Asia-move. Swap 0.

**D-094a:** train 2021–2023 = 3y. Reden **(b)**: Asia→London gold handoff is structureel (proxy GC); FTMO-M5 = kosten. Herhaal in PREREG.

---

## Idee (mechanisme)

Asia-impuls 00:00→08:00 CET. Als |asia_bp| ≥ 40 bp → continue op 08:00; flat **12:00 CET**.

**Onderscheid:**
- ≠ **S2-XAU_AM_FADE** / **N10** (fade van London-extensie)
- ≠ **N25** NY-afternoon fade / **N4** Pre-NY BO / **N7** Pre-London BO / **N8** Post-AM-Fix cont. / **N12** NY-Open cont. / **N19** OVN gap fill
- ≠ **S2-XAU** London–NY overlap breakout
- ≠ ORB-familie

---

## Regel (bevriesbaar zodra screen PASS)

- `P_0000` = M5-close 00:00 CET (of eerste bar ≥00:00 die kalenderdag)  
- `P_0800` = M5-close 08:00 CET  
- `asia_bp = 1e4 × (P_0800 − P_0000) / P_0000`  
- `|asia_bp| ≥ 40` → side = sign(asia_bp); entry 08:00; stop 1×ATR14; flat **12:00 CET**.

---

## Pre-screen aanvraag

- **Data:** `data/m5gz/XAUUSD.csv.gz`, train **2021-01-01 … 2023-12-31**.
- **Gate:** mean bruto ≥ **2,49 bp**. N≥150.
- **Geen test/reserve.** PASS → PREREG_FTMO_N31 (D-094a (b)).
