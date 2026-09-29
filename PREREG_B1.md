# PREREG B1 — statistiek-tools en retroactieve toets (vastgelegd vóór berekening, 2026-09-29)

- Sharpe op dagrendementen (√252), standaardfout volgens Lo (2002)/Mertens (incl. scheefheid en
  kurtosis), 95%-interval via stationaire block-bootstrap (blok 21 dagen, 2000 trekkingen, seed 1).
- t-stat = gemiddeld dagrendement / sd × √T.
- Gedeflateerde Sharpe (Bailey & López de Prado 2014): SR0 uit N trials met Var[SR] = variantie van
  de SR-schatter; gerapporteerd voor **N = 300** (eerlijke telling, zie TRIAL_COUNT.md) en N = 30
  (grove schatting "effectief onafhankelijk"). DSR = kans dat de ware SR > 0 na correctie.
- Minimale trackrecordlengte (95%, SR* = 0).
- required_sharpe: benodigde jaarlijkse Sharpe voor doel-€/mnd op €80k zodat de kans om ooit 10%
  onder de start te zakken ≤ 5% (Brownse beweging: P = exp(−2μD/σ²)).
- Retroactief op: 16-universum-ensemble (EUR, swap-gecorr.), beste in-sample config
  (t2/lb1/SMA10/guard3/60%), T10-ensemble-EA, lange ensembles A en B (8% fin.), ronde-2 familie 1 en 2.
