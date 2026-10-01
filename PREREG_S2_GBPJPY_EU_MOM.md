# PREREG_S2_GBPJPY_EU_MOM — GBPJPY Europe-morning session momentum (intraday-vlak)

**Status:** Pre-registratie 2026-10-01 ~08:45 Europe/Amsterdam, branch `grok/strateeg-2`.  
**Auteur:** Strateeg-2. **Geen formele trial-resultaten vóór deze commit.**  
**D-092.1:** kost-pre-screen PASS op train 2021–2023 (`results/strateeg2_prescreen/cycle_0840/`) vóór deze PREREG.  
**D-094 / D-094a / D-095:** FREEZE OFF; tracks 2+4; quality>quantity — alleen PREREG bij echte D-092.1 PASS + N≥150.  
**≠** N28 EURJPY Lon→NY mom (entry 15:30, other pair); **≠** N33 USDCAD Lon→NY; **≠** N37 EURUSD H4 trend (Faraday queue — not cloned); **≠** A5/GS02 London ORB; **≠** B1 overnight TSMOM; **≠** S2-USDJPY handoff.

**Universum:** `GBPJPY` (RT 1,11 bp uit `COSTS_FTMO.csv` / `COSTS_FTMO_alle.csv`). In SymbolList_FTMO + `data/m5gz/`. Daily-flat (swap = 0).

---

## 0. D-092.1 pre-screen (train only — geen selectie op test/reserve)

| Idee | Symbool | N | mean bruto | gate 3×RT | Uitkomst |
|------|---------|--:|----------:|----------:|----------|
| GBPJPY_EU_MOM | GBPJPY | **170** | **+3,41 bp** | **3,33 bp** | **PASS** |

Skew ≈ +0,14 (licht positief). Stop-share ≈ 14%. Artefacts: `scripts/s2_d092_prescreen_cycle0840.py`, `results/strateeg2_prescreen/cycle_0840/GBPJPY_EU_MOM_trades.csv`.  
**Verboden:** drempels/vensters/stops wijzigen na zien van test/reserve.

### D-094a historie-notitie (<5j)

Train 2021–2023 + test 2024 = 4 jaar op FTMO-M5 (m5gz start ≈ 2021-01). **Uitzondering (b):** Europe-session momentum / continuation na een duidelijke London-ochtendimpuls is een tijdloos microstructure-mechanisme (liquidity handoff, positioning into midday); langere FX-proxy-literatuur ondersteunt session-momentum; de beschikbare FTMO-M5-reeks toetst kosten/uitvoering. Zonder (b) geen PREREG op dit venster. Auditor mag afwijzen.

---

## 1. Bevroren regel (exact — identiek aan pre-screen)

**Mechanisme:** als GBPJPY in de London-ochtend (08:00→11:30 Europe/Amsterdam) ≥ ±30 bp beweegt t.o.v. 08:00-open, continueren we die richting tot vroeg-middag — vóór de Lon→NY handoff-familie (N28/N33).

**Kalender:** Europe/Amsterdam (DST gelijk aan bestaande M5-sims).

**Signalen (max 1 trade / dag):**
- `P_open` = M5-open van de 08:00-bar  
- `P_entry` = M5-open van de 11:30-bar  
- `ret_bp = 1e4 × (P_entry − P_open) / P_open`  
- `ATR` = D1 ATR(14) van voorgaande dagen (shift-1; geen lookahead)  
- Als `ret_bp ≥ +30` → **LONG** @ 11:30-open  
- Als `ret_bp ≤ −30` → **SHORT** @ 11:30-open  
- Anders → geen trade

**Exit (swap = 0, daily-flat):**
1. **Stop:** `0,40 × ATR` voorbij entry  
2. **Target:** `0,60 × ATR` in trade-richting  
3. **Time:** hard flat **14:30 Europe/Amsterdam**  
4. Same-bar target+stop → **stop wint**

**Sizing:** 0,75% risico per trade (stop-afstand → notional).  
**Verboden na zien:** ±30 bp filter, 0,40/0,60 ATR stop/target, 11:30 entry, 14:30 flat, symbool wijzigen.

---

## 2. Kosten & poort

- RT GBPJPY = **1,11 bp** (`COSTS_FTMO.csv` roundtrip_intraday_bp / alle `rondreis_bp`).  
- Poort train (2021–2023): getekend gemiddeld bruto bp/trade ≥ **3× RT = 3,33 bp** — **al PASS in §0** (N=170 ≥ 150).  
- Formele U2/CTO cost-gate herhaalt +50% RT-stress. FAIL → STOP, geen TRIALS-append.

---

## 3. Data / venster

- M5gz: `GBPJPY` (`data/m5gz/`).  
- **Train:** 2021-01-01 … 2023-12-31  
- **Test:** 2024-01-01 … 2024-12-31  
- **Reserve 2025→ ONAANGERAAKT** (D-084 / D-094.1) — geen touch zonder CEO BESLUITEN per kandidaat.

---

## 4. Beslisregel

1. Kostenpoort (+50% stress) eerst. PASS → TRIAL_COUNT +1.  
2. Dag-geclusterde netto t ≥ 2,0 train én test; mean netto > 0 beide; **N_trades ≥ 150** train (pre-screen N=170).  
3. Kosten < 50% bruto. Skew dag-PnL > 0 **of** max dagdip ≤ −1,5% bij 0,75% risk.  
4. Corr vs N28/N33/A5/EURJPY-session dagreeksen (informatief); |ρ| > 0,5 vs N28 ⇒ label "residual clone", geen shortlist.  
5. `ftmo_ev()`; p95 dagverlies ≤ 2%; **FTMO-EV ≥ €150/poging**.

---

## 5. Faalrisico's

2022 train-jaar zwak (~+0,2 bp mean) terwijl 2021/2023 sterker — regime-/vol-gevoelig; knappe poort-marge (+3,41 vs 3,33); time-exit dominant (~79%) → edge kan dun zijn na +50% stress; FX-cross vs JPY-risk-on/off spikes; niet poolen met N28/N33 zonder aparte PREREG.

---

## 6. Neven-screens deze cyclus (geen PREREG)

| Idee | N | mean bruto | gate | Uitkomst |
|------|--:|----------:|-----:|----------|
| EURGBP_LON_SPIKE_FADE | 37 | +2,23 | 3,12 | FAIL |
| AUS200_ASIA_RANGE_BO | 352 | −2,59 | 4,08 | FAIL |
| UK100_AM_MOM_CONT | 189 | −1,42 | 4,26 | FAIL |
| EURAUD_LON_EXT_FADE | 105 | −0,59 | 3,33 | FAIL |

Details: `results/strateeg2_prescreen/cycle_0840/prescreen.md`. Faraday N35–N37 queue niet gedupliceerd.

---

**Bevroren:** 2026-10-01 08:45 CEST — D-092.1 PASS non-clone (D-094 cadence).  
**Auteur:** Strateeg-2 (`grok/strateeg-2`)
