# VOORSTEL GS02 — Asian-range fade (FX majors), not London-open ORB

**Grok Strateeg · 2026-09-30 21:42 Europe/Amsterdam · `grok/strateeg-1`**  
**PREREG:** `PREREG_GS02.md`. Distinct from U3 / Claude `PREREG_FTMO_FX_INTRADAG` (both London-**breakout** family).

## 1. Economic logic

London open often **sweeps** the overnight (Asian) range as stops cluster beyond highs/lows; when the sweep **fails** (close back inside Asian range), the move is inventory/stop-driven rather than informed continuation — fade toward range mid / opposite bound. This is the opposite trade of U3 (which buys/sells London OR breakout continuation). FXE RP-003 shows LN–NY overlap is where vol/liquidity concentrate — use overlap as **holding/exit venue**, not as the signal.

Caveats: retail-popular (ICT/SMC variants) → decay risk; QuantifiedStrategies London-breakout page **403** (not used). D1 already tested fixed-clock seasonality (short EUR morning / long US hours) — different rule.

## 2. Cost gate

EURUSD RT 0.63 bp → bruto ≥ 1.89 bp; GBPUSD 0.70 → ≥ 2.10. Intraday-flat → swap 0. Prefer trading only if spread_med in entry hour ≤ symbol daily med (`COSTS_FTMO_per_uur.csv`).

## 3. Rule sketch (frozen in PREREG)

Asian range = high/low of 00:00–07:00 **UTC** (fixed, no DST shift for definition). London observation window 07:00–10:00 UTC. **Fade short** if price makes high > Asian high then an M5 close back ≤ Asian high; **fade long** symmetric. Stop beyond sweep extreme; target mid of Asian range then opposite bound (scale) or EOD 16:00 UTC flat, whichever first. One trade/day/symbol. EURUSD + GBPUSD only.

## 4. Decision rule

Cost gate train 2021–23 first. Pass: day-clustered net t ≥ 2.0 train and test; both years-halves >0; max daily dip compatible with 5% rule at ≤4% risk scale. Else reject. +1 trial if gate passed.

## 5. Expectation

Low (~10%). Fail if sweeps continue (trend days), or edge < costs, or N small. **Do not** “fix” by switching to breakout after seeing fade fail (that would be U3 redux).

## 6. Ask

Uitvoerder: implement only after GS01 gate decision or in parallel if M5 bandwidth allows; need clean UTC session cuts. Manager: keep separate from A5 London-breakout PREREG to avoid double-counting FDR.
