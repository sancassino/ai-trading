# PREREG_S2_BTC_USOPEN — BTCUSD US Cash-Open Impulse Breakout (2026-09-30)

**Status:** Pre-registration. Auteur: Strateeg-2.  
**Branch:** `grok/strateeg-2` · **Niet in catalogus A/B-tier** (Q3 = H1 TSMOM/σ-omkeer op BTC/ETH, niet US-cash-open event; A1 = index/XAU ORB; geen crypto-sleeve in §9).

## 1. Exacte regel

**Instrument:** `BTCUSD` (FTMO Crypto I CFD).  
**Kalender:** alleen US equity cash-handelsdagen (NYSE-kalender); crypto-weekend zonder US cash → geen trade.  
**Pre-range:** hoog/laag van 14:30–15:30 Europe/Amsterdam (60 min vóór US cash open) op M5.  
**Entry-venster:** 15:30–16:00 Europe/Amsterdam (eerste 30 min US cash).  
**Long:** eerste M5-slot ≥ 15:30 die boven pre-range high sluit; entry op die bar-close.  
**Short:** eerste M5-slot die onder pre-range low sluit; entry op die bar-close.  
**Geen trade** als beide kanten binnen 15:30–16:00 worden geraakt (two-way = skip) of als pre-range breedte ∉ [0,20%, 1,50%] van mid (te krap = noise; te wijd = al uitgeprijsd).  
**Stop:** terug voorbij pre-range mid ((high+low)/2) — vast; geen trailing.  
**Exit:** hard flat 21:00 Europe/Amsterdam **zelfde dag** óf stop — **geen overnight / geen server-midnight** (crypto-swap ~−30%/jr per Q3-notitie vermijden → swap≈0).  
**Max 1 trade/dag;** geen herentry.  
**Sizing:** 0,50% risico per trade (crypto-vol hoger dan indices).  
**Filter (0 vrije parameters):** alleen handelen als |US100cash gap| ≥ 0,15% waar gap = US100 cash-open / vorige cash-close − 1 (richting van de BTC-trade moet **gelijkteken** zijn met US100-gap; anders skip). Gap gebruikt alleen open die al bekend is bij 15:30 — geen lookahead.

## 2. Mechanisme

BTC erft op US cash-open een risicopremie-/liquiditeitsschok van US equity (risk-on/off). De pre-open range op BTC is een rustigere consolidatie; een break in de richting van de US100-gap is een **cross-asset impulse**, geen H1-momentum (Q3a) en geen σ-mean-reversion (Q3b). Positief scheef: vaste mid-stop vs. runner tot 21:00; harde flat vermijdt crypto overnight-swapstaart.

## 3. Instrument / dataset

| Item | Waarde |
|------|--------|
| FTMO-symbool | BTCUSD |
| Kosten | rondreis ≈ 1,25 bp (COSTS_FTMO_alle.csv: spread_med 0,85 + 2×0,20 commissie); swap irrelevant (intraday, flat vóór midnight) |
| Ontdekking | M5 BTCUSD FTMO 2021–2024-12-31 + US100cash M5/D1 voor gap; geen peek in 2025-01→ |
| Reserve-OOS | 2025-01-01→ — **één blik na shortlist, nooit eerder** (D-084) |
| Kalender | NYSE cash-dagen; US feestdagen zonder cash-sessie uitsluiten |

## 4. Kostenpoort

Bruto mean ≥ 2× 1,25 bp **én** kosten < 50% bruto op ontdekkingsset.  
+50% spread-stress: zelfde poort. Fail → stop, **geen trial-telling**.

## 5. Beslisregel

1. Dag-geclusterde t (Newey–West, lags=5) op dag-P&L ≥ **2,0**.  
2. Kosten < 50% bruto.  
3. Skew > 0 of max dagdip ≤ −1,5% bij 0,50% risk.  
4. FTMO-EV via `engine/ftmo.py` ≥ **€150/poging netto** (design-drempel; geen gefabriceerde uitkomst).  
5. Beide helften 2021–22 / 2023–24: mean netto > 0.  
6. Correlatie met A1 multi-ORB dagreeks: informatief; \|ρ\| > 0,7 → label "equity-beta sleeve", geen aparte shortlist tenzij Δ FTMO-EV > €50.  
7. Correlatie met Q3a/Q3b: \|ρ\| > 0,5 → overlap-waarschuwing (andere regel, zelfde asset).

## 6. Verwachte uitkomst / falen

**Verwacht (kwalitatief, geen cijfers):** werkt op dagen met duidelijke US equity gap + BTC liquidity; faalt bij risk-parity-dagen (gap en BTC divergéren) of wanneer pre-range al de move heeft.  
**Falen:** kostenpoort; t < 2; FTMO-EV < €150; of filter elimineert N tot onder power (N_trades ontdekking < 150 → STOP zonder trial).

## 7. Constraints

Geen post-hoc tuning van gap-drempel, range-uren of stop-formule. Geen 2025+ peek. Geen real money / geen live trading. Niet heropenen van Q3-parameters.
