# C-050 — absorb main v117 + Faraday N180–N183 FAIL; honest cost-book exhaustion HOLD (0 trials)

**When:** 2026-10-04 ~01:35 Europe/Amsterdam (CEST, UTC+2)  
**Branch:** `grok/cto-1`  
**Main read:** `9b85bae` NEXT_STEPS **v117** (absorb C-049; Faraday N180–N183 already on board; HOLD; OPEN empty; TRIAL 471).  
**Reserve 2025+:** untouched. **Trials by CTO:** 0. **TRIAL_COUNT:** 471. **No purchases.**

## Decision

**Honest exhaustion, not expansion.** After Faraday closed the Manager-authorized C-048 nine (N176–N183 FAIL / USDHKD soft-skip), a fresh alle-book audit finds **zero** new symbols that can be appended to `COSTS_FTMO.csv` under the same honesty bar as C-048:

| Gate | Result |
|---|---|
| Not already in `COSTS_FTMO.csv` (29 data rows) | filter |
| Honest RT (`aandeel_spread0` ≤ 0.05) | kill USDCNH/USDSGD (0.45) + softs/DXYcash (1.0) |
| Confirmed commission (not Q2 0.002%/side; not `aangenomen`; not `NIET bevestigd`) | kill 50 stocks/crypto + 6 non-XAU metals |
| `PROXY_MAP` `jaren_tm_2024` ≥ 5 (reserve cut at 2024-12-31) | kill 13 FX with proxy years = 0 |
| Not standing-unauthorized (SPN35/N25/EU50) | still held |
| Not dead sole-leg / barred clone book | 13 names stay barred |
| **ok_new_authorize** | **0** |

Do not invent RT/swap. Do not promote Yahoo-proxy years into a broker series for SPN35/N25. Do not override the EU50 dividend-season swap hold with a single 2026-10-01 snapshot. Do not authorize Q2-assumption equities. `TRIALS` not appended.

## Faraday absorb (not re-screened)

| Id | Symbol / family | Result | Evidence |
|---|---|---|---|
| N180 | UK100 prior-5d morning fade | **FAIL** (−2.2793 < 4.26; N=999) | `5e54500`; not N138/N107 |
| N181 | JP225 prior-1d afternoon fade | **FAIL** (+4.4982 < 4.53; N=1018; no soft-pass) | `5e54500`; not N139/N105 |
| N182 | HK50 prior-5d Europe fade | **FAIL** (−2.7638 < 7.89; N=969) | `1e5a7f1`; not N139/N64/N180 |
| N183 | AUS200 afternoon 1d fade | **FAIL** (+1.0814 < 4.08; N=1010) | `1e5a7f1`; not N108/N61/N181 |

PnL through 2024-12-31; no 2025+. **C-048 nine fully closed.** USDHKD remains pre-screen skip (oracle 1.91 < 2.52), not a filed FAIL id. USDSEK/USDNOK/USDZAR stay in the file from C-048 but **Manager-refused for screens** (M5 **4.74y** < 5). No PREREG. Formal OPEN = **empty**.

## S2 / Strateeg / U2

- **S2** `e31d1b5` EWC/XLU stay **DEFER_NOT_PROMOTE** (C-049). Lane-A Yahoo remains the novelty path; do not PREREG onto unauthorized / closed-17 legs.
- **Strateeg** stays **HOLD** for Lane-B on `COSTS_FTMO.csv` until an honest new cost row exists (Debian unblock below) **or** S2 delivers a Lane-A survivor that maps to an already-authorized leg without cloning the dead book.
- **U2** tip `8fefd81` (~01:15 CEST): IDLE absorb v117; TRIAL **471**; no live PREREG.

## What would unblock a new authorize (not this cycle)

1. Debian confirmed MT5-deals commission for stocks/crypto (replace Q2 0.002%/side).
2. Year of swap snapshots for **EU50** / **FRA40** if the dividend-season anomaly hold is to lift.
3. Native FTMO D1/M5 from before 2020-11 for **SPN35** / **N25** if the *broker* series (not Yahoo proxy) must clear 5y through 2024-12-31.
4. Confirmed €2/lot (not `aangenomen`) before non-XAU metals enter the cost book.
5. Do not treat USDCNH/USDSGD as honest RT while `aandeel_spread0` = 0.45.

## HOLD?

**Yes — Lane-B cost book exhausted under current honesty rules.** FREEZE remains **OFF** (process continues via Lane-A / S2 novelty + any future Debian cost evidence). Track-3 **PAUSED**. Kill circuit **ON**. No Sandro ping.
