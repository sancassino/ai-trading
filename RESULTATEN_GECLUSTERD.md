# RESULTATEN_GECLUSTERD (N7, 2026-09-30) — oude t vs geclusterde/autocorrelatie-robuuste t

Trade-resultaten: per-trade-t vs **dag-geclusterd** (gemiddelde per dag, t over dagen). Dagreeksen: gewone t vs **Newey-West (lag 5)** en blok-bootstrap (21 d).

| resultaat | methode | oude t | nieuwe t | N (trades/dagen) | N-dagen / bootstrap-t |
|---|---|---|---|---|---|
| ORB-B4a FTMO 2021–26 (7 symbolen) | per trade → dag | +2.93 | **+1.81** | 9249 | 1490 |
| ORB-B4a S3-set (US500, US100, GER40, XAU) | per trade → dag | +3.73 | **+2.90** | 5091 | 1457 |
| S1(a) noise-area FTMO 2021–26 | per trade → dag | +2.19 | **+2.05** | 5357 | 1261 |
| K1 max 1 nacht Yahoo | per trade → dag | +3.05 | **+3.01** | 2022 | 1428 |
| K1 max 2 nachten Yahoo | per trade → dag | +3.59 | **+3.30** | 1441 | 1121 |
| K1 max 1 nacht FTMO | per trade → dag | +1.79 | **+0.43** | 472 | 275 |
| K1 max 2 nachten FTMO | per trade → dag | +1.53 | **+0.94** | 331 | 224 |
| B2b RSI(2) Yahoo gepoold 1990–2026 | dagreeks: t → NW / bootstrap | +3.65 | **+3.80** | 9554 | bootstrap-t 3.99 |
| F3b RSI(2)+ORB MT5 2021–26 | dagreeks: t → NW / bootstrap | +2.14 | **+2.29** | 1305 | bootstrap-t 2.35 |
| F2 ORB MT5 2021–26 | dagreeks: t → NW / bootstrap | +2.21 | **+2.22** | 1487 | bootstrap-t 2.14 |

## Lezing
- **ORB (7 symbolen, B4a):** 2,93 → **1,81** — symbolen handelen op dezelfde dagen en bewegen samen; per-trade-t overschatte het bewijs.
  Op de **S3-set** (US500, US100, GER40, XAU; zonder US30, EURUSD, UK100) is het beeld sterker: 3,73 → **2,90** (1.457 dagen).
  De MT5-dagreeks F2 (portefeuille, 1/7 per trade) geeft t 2,21, NW 2,22, bootstrap 2,14 — consistent met ± 2.
- **S1(a):** 2,19 → 2,05 (weinig overlap tussen symbolen per dag); blijft ver onder de lat.
- **K1 (RSI(2)-nachten):** Yahoo robuust (3,05 → 3,01; 3,59 → 3,30), FTMO zakt sterk (1,79 → **0,43**; 1,53 → 0,94) — de FTMO-trades clusteren op
  dezelfde dagen (marktbrede dips). Was al afgewezen.
- **B2b RSI(2) Yahoo (t 3,65):** was al een gepoolde **dagreeks** (portefeuille), dus al 'geclusterd' over indices; autocorrelatie-robuust
  NW 3,80 / bootstrap 3,99 → **overleeft**. F3b-dagreeks 2,14 → NW 2,29 / bootstrap 2,35 (ongewijzigd beeld).
- **Forward-set (papier):** nog geen data (eerste dag 30-09 22:15 UTC) → n.v.t.

**Correctie eerdere logs:** in S9-stap-1 en U2 staat 'ORB-B4a … 5 symbolen'; het B4a-trade-bestand bevat 7 symbolen (US500, US100, US30, GER40,
XAU, EURUSD, UK100). De cijfers zelf kloppen (berekend op dat bestand); alleen het label was fout. N8 (power) gebruikte expliciet de 4 S3-symbolen.
