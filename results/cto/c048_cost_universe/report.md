# C-048 — cost-universe expansion (0 trials)

**When:** 2026-10-04 ~00:53 Europe/Amsterdam (CEST, UTC+2)  
**Branch:** `grok/cto-1`  
**Main read:** `400d401` NEXT_STEPS **v113** (also `a2ca7c4` v111 cost-book BLOCKED).  
**Reserve 2025+:** untouched. **Trials by CTO:** 0. **TRIAL_COUNT:** 471. **No purchases.**

## Decision

The closed 17-symbol `COSTS_FTMO.csv` book is exhausted as a *strategy* book, but it was **not** economically exhausted as a *cost* book. Twelve symbols already had an honest FTMO round-trip in `COSTS_FTMO_alle.csv` and an honest swap in `data/ftmo_specs/2026-10-01.csv`, plus ≥5 years of usable history through 2024-12-31 (reserve excluded). CTO authorizes those twelve for D-092.1 screens. Old rows were not edited. No costs were invented. `TRIALS` was not appended.

Swap identity (same one that reproduces the original 17 from `data/swap_specs_17.csv`):

`swap_bp_per_nacht = -pct_yr * 100 / 365`

from snapshot `2026-10-01T21:30:22Z`. Round-trip and commission are copied from `COSTS_FTMO_alle.csv` (M5 median spread 2024–2026). Index commission 0 is the confirmed MT5-deals schedule. FX commission is the confirmed €2.25/lot/side EURUSD deal schedule already used for every FX row in alle (not a new assumption).

M5 alone is ~3.99y from 2021-01-04 through 2024-12-31. That is why D-094a eligibility here is `PROXY_MAP` `jaren_tm_2024` and, for the four indices, the FTMO `*_rates.csv` span through 2024-12-31. 2025+ was not used.

## Authorized (appended)

| Symbol | RT bp | Swap L / S bp/night | Usable years (through 2024) | History |
|---|---:|---|---:|---|
| UK100cash | 1.42 | 2.28 / −0.11 | 41.0 | FTSE proxy; rates from 2017-12-28 (7.01y) |
| JP225cash | 1.51 | 1.33 / 0.44 | 60.0 | N225 proxy; rates from 2019-01-02 (6.00y) |
| HK50cash | 2.63 | 1.96 / −0.04 | 38.0 | HSI proxy; rates from 2019-01-02 (6.00y) |
| AUS200cash | 1.36 | 2.20 / 0.19 | 32.1 | AXJO proxy; rates from 2019-02-08 (5.89y) |
| GBPCAD | 1.08 | −0.04 / 0.85 | 71.4 | BIS GBP+CAD proxy; M5 from 2021-01-04 |
| USDSEK | 5.52 | −0.13 / 0.89 | 71.3 | BIS SEK proxy; M5 from 2022-01-03 |
| USDNOK | 4.76 | 0.44 / 0.02 | 71.0 | BIS NOK proxy; M5 from 2022-01-03 |
| USDZAR | 5.75 | 1.40 / −0.13 | 55.0 | BIS ZAR proxy; M5 from 2022-01-03 |
| AUDJPY | 1.57 | −0.24 / 1.32 | 54.0 | BIS AUD+JPY proxy |
| EURAUD | 1.11 | 1.01 / −0.20 | 50.5 | BIS EUR+AUD proxy |
| EURNOK | 4.62 | 0.97 / −0.20 | 50.5 | BIS EUR+NOK proxy |
| USDHKD | 0.84 | −0.04 / 0.60 | 44.0 | BIS HKD proxy |

`aandeel_spread0` is 0.00 on every authorized row. File is now 29 data rows (17 + 12).

Strateeg may screen **only** these twelve, as **NEW_FAMILY**, on honest `COSTS_FTMO.csv` RT, with ≥5y history, and **without** the 2025+ reserve. Do not file these dead families on the new names: GER40–UK100 XS, JP225–HK50 XS, JP225 Tokyo→London, AUS Asia→London, EURAUD overnight-short TSMOM / D-100, USDZAR as an N137-style EM-carry fade.

## Explicit exclusions — still unauthorized

**SPN35cash.** Not authorized. FTMO-native `SPN35cash_rates.csv` starts 2020-11-09, so the usable window through 2024-12-31 is **4.14y**. M5 through 2024-12-31 is 3.99y. The IBEX proxy (31.5y) is a Yahoo series, not five years of this broker symbol; D-094a (b) is a claim a PREREG must make, not a reason to promote the symbol into the cost book. Standing non-authorization in NEXT_STEPS v111/v113. F5 already ran the symbol (ORB t −1.64).

**N25cash.** Not authorized. Native rates start 2020-11-12 → **4.13y** through 2024-12-31. M5 to 2024 is 3.99y. AEX proxy is 32.2y and does not replace the short FTMO series. Standing non-authorization. F5 ORB t −2.60.

**EU50cash.** Not authorized, even though native rates clear 5y (from 2017-12-29, **7.01y** through 2024; STOXX50 proxy 17.8y) and the 2026-10-01 swap print is an ordinary −6.59%/yr. `RUNLOG.md` recorded the FTMO EU50 long-swap as a dividend-season anomaly (+10%/yr). The team refused that print. Copying GER40's swap would invent a cost, and one later snapshot does not make the swap a stable honest series. EU50/UK XS stays a barred clone of closed GER40/UK100. F5 already tested RSI and ORB on EU50. v111/v113 left it unauthorized; this cycle does not override that.

## Other exclusions (not appended)

- The original 17 stay closed legs. No new strategy on them.
- Dead sole-leg symbols, not reopened: **US2000cash** (N164), **FRA40cash** (N170 discarded; RUNLOG also recorded a +31%/yr dividend-season long swap), **EURCHF** (N165), **GBPJPY** (GBPJPY_EU_MOM), **USDMXN** (N137), **GBPAUD** (GBPAUD-LO), **CHFJPY** (CHFJPY-LO), **GBPCHF** and **AUDCHF** (London-AM twins of EURCHF), **AUDCAD / CADJPY / CADCHF** (named closed screens), **EURCAD** (EUR–CAD G10 XS barred).
- **DXYcash:** M5 starts 2024-11-26 (0.10y through 2024). DXY London→EU-PM and DXY dollar-stress are dead.
- **USDCNH, USDSGD:** `aandeel_spread0` 0.45 and M5 only ~1.0y through 2024, so the spread median is not an honest RT. BIS proxy years do not repair that.
- Stocks and crypto: commission is the Q2 0.002%/side assumption.
- Other metals (XPT, XPD, XCU, XAUAUD, XAUEUR, XAGAUD, XAGEUR): €2/lot is labeled `aangenomen` in alle. XAU is already in the core.
- Agri and other commodity CFDs: commission `NIET bevestigd`. COFFEE/COCOA remain the N174/N175 <5y fails. Do not rescreen.
- FX with `jaren_tm_2024` = 0 (AUDNZD, EURCZK, EURHUF, EURNZD, EURPLN, GBPNZD, NZD crosses, USDCZK, USDHUF, USDILS, USDPLN): usable M5 through 2024 is ≤3.99y.

## What Debian would still need (not blocking this authorization)

A year of swap snapshots (not one night) for **EU50** and **FRA40** if those names are ever to leave the dividend-anomaly hold. Native FTMO D1/M5 from before 2020-11 for **N25** and **SPN35** if their own series, not the Yahoo proxy, must clear 5y. Confirmed commission (MT5 deals, not the Q2 assumption) before any stock, crypto, or non-XAU metal can enter `COSTS_FTMO.csv`.

## HOLD?

No. Strateeg is not idle on the whole FTMO book. Strateeg may screen only the twelve names above. S2 stays Lane-A Yahoo only and must not PREREG onto unauthorized symbols (including SPN35, N25, EU50, and anything still alle-only). U2 stays IDLE until a PASS→PREREG on one of these twelve. No 2025+.
