# PREREG_FTMO_N2 — US100↔US500 relative morning flat (intraday-vlak)

**Status:** Pre-registratie 2026-09-30 23:55 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Uitkomst (Uitvoerder-2, `8c7a8e1`, ~00:05 CEST):** **FORMEEL GESTOPT** — kostenpoort TRAIN FAIL (signed mean bruto −0,84 bp < 3× pair RT 4,32 bp; n=112). Geen trial. Geen herstart zonder CEO.  
**Auteur:** Strateeg (Grok).  
**D-091 prio 3:** niet-kloon; **geen ORB/breakout**; twin-index dispersie.  
**Universum:** `US100cash` + `US500cash` (screen rank 1 + 4; beide in COSTS_FTMO).

---

## 1. Bevroren regel (exact)

**Mechanisme:** intradag relatieve beweging tussen NDX en SPX mean-revert omdat gemeenschappelijke factoren + liquidity waves tijdelijk uiteenlopen; pair flattened vóór overnight elimineert beta/swap.

**Session:** US cash open (zelfde open-tijd beide; DST zoals bestaande sims).

**Signaal (één pair-trade per dag):**
- `r100 = 1e4 × (P_US100_T60 − P_US100_open) / P_US100_open` (T0+60 min).  
- `r500 = 1e4 × (P_US500_T60 − P_US500_open) / P_US500_open`.  
- `diff = r100 − r500`.  
- `σ =` rolling 20-sessie stdev van `diff` (alleen voorgaande sessies; geen look-ahead).  
- Als `diff ≥ +1,25 × σ` → **short US100 / long US500** (equal-risk: elk been risico = 0,5 × dagbudget).  
- Als `diff ≤ −1,25 × σ` → **long US100 / short US500**.  
- Anders → flat.

**Entry:** close van T+60 M5-bar beide benen.  
**Exit:** beide benen flatten op US session close (intraday-vlak). Geen target/stop intradag — time-stop only (voorkomt ORB-achtige level-trading).  
**Verboden na zien:** σ-drempel, 60-min anker, equal-risk wijzigen. Sensitivity (report-only): 1,0× en 1,5× σ.

**≠ catalogus:** geen C07 maand-momentum, geen ORB, geen single-name; twin CFD same-session.

---

## 2. Kosten & poort

- RT per been: US100 0,66 + US500 0,78 = **1,44 bp** pair round-trip (open+close beide).  
- Poort train: **getekend gemiddeld bruto bp/pair-dag ≥ 3× 1,44** (= ≥ 4,32 bp).  
- +50% RT-gevoeligheid. FAIL → STOP.

---

## 3. Data / venster

- M5gz US100 + US500, 2021–2024-12.  
- Train 2021–2023 / Test 2024 / Reserve 2025→ ONAANGERAAKT.

---

## 4. Stats & FTMO-EV

1. Poort → bij PASS trial +1.  
2. Dag-geclusterde t ≥ 2,0 train én test; mean netto > 0 beide; N ≥ 100 tradedagen train.  
3. Netto-β vs US500 dagreturn ≈ 0 (sanity; anders is het gecamoufleerde richting).  
4. `ftmo_ev()` na PASS; p95 dagverlies ≤ 2%.

---

## 5. Faalrisico's

Dispersie te klein t.o.v. 1,44 bp RT; regime waarin NDX persistent leidt (niet mean-revert); sync-fout open-tijden.

---
**Bevroren:** 2026-09-30 23:55 CEST — D-091 nacht.  
**Auteur:** Strateeg (`claude/trusting-faraday-34tsmg`)
