# R4-rapportage (D-063; ontdekking ≤ 2024; geen trial)

## 1. C61 — compounding-/pad-afhankelijkheidstest dagelijks-gereste inverse (SPX, prijsindex)

| episode | index-rendement R | naïef −R | −Σ dagrendementen | dagelijks gereset Π(1−r_d)−1 | verschil gereset vs −R |
|---|---|---|---|---|---|
| 2000-03-24 → 2002-10-09 | -49.1% | +49.1% | +60.9% | +72.1% | +22.9 pp |
| 2007-10-09 → 2009-03-09 | -56.8% | +56.8% | +73.6% | +88.5% | +31.7 pp |
| 2020-02-19 → 2020-03-23 (crash, 1 mnd) | -33.9% | +33.9% | +38.2% | +42.2% | +8.3 pp |
| 2022-01-03 → 2022-10-12 | -25.4% | +25.4% | +27.1% | +28.2% | +2.7 pp |

Lezing: het engine-model (dagelijks −1× herwogen) = de dagelijks-gereste inverse. In aanhoudende dalingen pakt de dagelijkse reset gunstig uit t.o.v. −R (+3 tot +32 pp; in zijwaartse, volatiele markten werkt het verval juist tegen). C61 is dus met de juiste dagelijks-herwogen conventie gemodelleerd én dit pad-effect is gunstig voor C61 — ondanks dat faalt C61. Uitkomst C61: SR 0,21 (t 2,1), niet beter dan buy-and-hold en zwakker dan C02 → de inverse-poot voegt niets toe (maxDD 81%, dag −20,5% in 1987 door short na rally).

## 2. C60 obligatie-duurtiming per decennium (etf, excess SR; B&H = synthetische 10j-TR − rf)

| periode | C60 SR | C60 CAGR tot. | C60 maxDD | B&H SR | B&H CAGR | B&H maxDD |
|---|---|---|---|---|---|---|
| 1963–69 | -0.90 | +2.7% | 5.1% | -1.17 | +0.4% | 11.9% |
| 1970s | -0.69 | +3.1% | 15.5% | -0.10 | +5.8% | 14.1% |
| 1980s | +0.65 | +16.3% | 16.1% | +0.35 | +13.8% | 28.6% |
| 1990s | +0.80 | +10.0% | 7.0% | +0.46 | +8.3% | 14.3% |
| 2000s | +0.30 | +4.8% | 14.0% | +0.52 | +6.9% | 12.6% |
| 2010s | +0.41 | +2.6% | 8.4% | +0.59 | +4.1% | 9.8% |
| 2020–24 | -0.30 | +0.8% | 9.6% | -0.45 | -1.5% | 24.2% |
| 2022 | -1.17 | -0.1% | 1.8% | -1.76 | -14.7% | 16.9% |
| alles | +0.26 | +6.2% | 16.1% | +0.21 | +6.1% | 28.6% |

## 3. Diversifier-screen (corr op gemeenschappelijke dagen; ΔSR/ΔmaxDD = P-ETF-a met en zonder de extra sleeve op dezelfde periode)

| sleeve | periode | corr C02 | corr C52L | corr SPX-excess | P-ETF-a (C52L+C02) SR / maxDD | + sleeve: SR / maxDD | ΔSR | ΔmaxDD | screen (corr ≤ 0,3 & ΔSR>0) |
|---|---|---|---|---|---|---|---|---|---|
| C55 | 2005-01-03→2024-12-31 | +0.60 | +0.53 | +0.60 | 0.93 / 11.2% | 0.89 / 10.8% | -0.04 | -0.4 pp | nee |
| C57 | 2003-01-02→2024-12-31 | +0.66 | +0.60 | +0.45 | 0.99 / 11.2% | 0.89 / 8.9% | -0.11 | -2.3 pp | nee |
| C58 | 2005-01-03→2024-12-31 | +0.06 | +0.53 | +0.04 | 0.93 / 11.2% | 0.77 / 14.5% | -0.16 | +3.3 pp | nee |
| C59 | 2007-01-03→2024-12-31 | +0.22 | +0.21 | +0.17 | 0.92 / 11.2% | 0.67 / 15.0% | -0.26 | +3.8 pp | nee |
| C60 | 2001-01-02→2024-12-31 | -0.20 | +0.39 | -0.33 | 0.94 / 11.2% | 0.75 / 7.6% | -0.18 | -3.6 pp | nee |
| C61 | 2001-01-02→2024-12-31 | +0.46 | +0.01 | -0.26 | 0.94 / 11.2% | 0.83 / 13.3% | -0.10 | +2.1 pp | nee |
