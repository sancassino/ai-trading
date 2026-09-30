# Run 10 — FTMO-EV herbeoordeling (CTO engine, restart=True, horizon=24mnd)

Datum: 2026-09-30 | CTO engine/ftmo.py | Bootstrap 10.000 paden, blok 21 d
Maatstaf: net_ev_monthly (netto €/mnd over 24-mnd horizon incl. restarts)
Verboden: scale > 4% p99-dagverlies als aanbeveling (D-016/D-085)

## Samenvatting: net_ev_monthly per sleeve

| Sleeve | N jr | SR(cfd) | maxDD | p99-dl | scale_auto | p_pass_2@auto | net_EV€/mnd@auto | exp_ppm@auto | p_survive@auto |
|--------|------|---------|-------|--------|-----------|--------------|-----------------|-------------|---------------|
| C02_faber__basis | 24.8 | 0.335 | 24% | 1.9% | 1.0 | 0.502 | 58.0 | 96.0 | 0.753 |
| C52_allweather__basis | 10.0 | 0.472 | 7% | 0.5% | 1.0 | 0.0 | -23.0 | 0.0 | nan |
| C52_allweather__lang | 24.0 | 0.327 | 16% | 1.0% | 1.0 | 0.101 | -17.0 | 7.0 | 0.983 |
| C17_fomc_cycle__basis | 10.3 | 0.372 | 23% | 2.5% | 1.0 | 0.596 | 84.0 | 131.0 | 0.642 |
| C54_carver__basis | 24.8 | -0.01 | 22% | 0.8% | 1.0 | 0.01 | -23.0 | 1.0 | 1.0 |
| C54_carver__qa | 10.3 | -0.412 | 19% | 0.7% | 1.0 | 0.0 | -24.0 | 0.0 | nan |
| C55_daa__basis | 10.0 | 0.525 | 3% | 0.3% | 1.0 | 0.0 | -22.0 | 0.0 | nan |
| C44_krediet__basis | 10.0 | 0.582 | 24% | 2.5% | 1.0 | 0.676 | 131.0 | 168.0 | 0.731 |
| C16_halloween__basis | 24.8 | 0.332 | 33% | 2.2% | 1.0 | 0.623 | 86.0 | 139.0 | 0.624 |
| C33_trend_lowvol__basis | 24.8 | -0.013 | 16% | 0.5% | 1.0 | 0.0 | -23.0 | 0.0 | 1.0 |

## Detail: 3 scales (1×, 0.5×, auto)

| Sleeve | p_pass_2@1× | net_ev/mnd@1× | p_pass_2@0.5× | net_ev/mnd@0.5× | p_pass_2@auto | net_ev/mnd@auto |
|--------|------------|--------------|--------------|----------------|--------------|----------------|
| C02_faber__basis | 0.502 | €58.0 | 0.077 | €-19.0 | 0.502 | €58.0 |
| C52_allweather__basis | 0.0 | €-23.0 | 0.0 | €-22.0 | 0.0 | €-23.0 |
| C52_allweather__lang | 0.101 | €-17.0 | 0.0 | €-23.0 | 0.101 | €-17.0 |
| C17_fomc_cycle__basis | 0.596 | €84.0 | 0.129 | €-14.0 | 0.596 | €84.0 |
| C54_carver__basis | 0.01 | €-23.0 | 0.0 | €-23.0 | 0.01 | €-23.0 |
| C54_carver__qa | 0.0 | €-24.0 | 0.0 | €-22.0 | 0.0 | €-24.0 |
| C55_daa__basis | 0.0 | €-22.0 | 0.0 | €-22.0 | 0.0 | €-22.0 |
| C44_krediet__basis | 0.676 | €131.0 | 0.181 | €-8.0 | 0.676 | €131.0 |
| C16_halloween__basis | 0.623 | €86.0 | 0.142 | €-14.0 | 0.623 | €86.0 |
| C33_trend_lowvol__basis | 0.0 | €-23.0 | 0.0 | €-22.0 | 0.0 | €-23.0 |

## Ranking (FTMO-uitvoerbaar; net_ev_monthly@auto, hoogste eerst)

1. **C44_krediet__basis**: €131.0/mnd (p_pass_2=0.676, SR=0.582) — krediet; N=17jr
2. **C16_halloween__basis**: €86.0/mnd (p_pass_2=0.623, SR=0.332) — seizoen; SPX/indices
3. **C17_fomc_cycle__basis**: €84.0/mnd (p_pass_2=0.596, SR=0.372) — A4; FOMC-cyclus; SPX CFD
4. **C02_faber__basis**: €58.0/mnd (p_pass_2=0.502, SR=0.335) — maandelijks; indices CFD
5. **C52_allweather__lang**: €-17.0/mnd (p_pass_2=0.101, SR=0.327) — wekelijks; SPY+BOND10_SYN(❌)+GOLD_F
6. **C55_daa__basis**: €-22.0/mnd (p_pass_2=0.0, SR=0.525) — DAA; ETFs (❌ FTMO)
7. **C52_allweather__basis**: €-23.0/mnd (p_pass_2=0.0, SR=0.472) — wekelijks; SPY+IEF(❌)+GLD
8. **C54_carver__basis**: €-23.0/mnd (p_pass_2=0.01, SR=-0.01) — multi-instrument; FX/goud/olie
9. **C33_trend_lowvol__basis**: €-23.0/mnd (p_pass_2=0.0, SR=-0.013) — trend+vol; SPX
10. **C54_carver__qa**: €-24.0/mnd (p_pass_2=0.0, SR=-0.412) — multi-instrument 2015→

## Methodische noot

- `restart=True`: bij breach betaalt de simulant opnieuw fee en start fase 1 opnieuw.
- `net_ev_monthly` = mean(cash − fees) / 24 mnd → vergelijkbaar over sleeves.
- `exp_payout_monthly` = mean(cash) / 24 mnd (bruto, excl. fee-aftrek).
- `auto_scale` = min(1.0, 4% / p99-dagverlies) — D-016/D-085 limiet.
- Negatieve `net_ev_monthly`: fee-kosten > verwachte uitbetalingen over horizon.
