# Run 9 — FTMO-EV herbeoordeling catalogus-sleeves (D-085/D-086)

Datum: 2026-09-30 | Account: €80k | Fee: €540 | Split: 80%
Bootstrap: blok 21 dagen, 5.000 sims | Max dagverlies FTMO: 5% van startkapitaal
Auto-scale: schaal waarmee p99-dagverlies ≤ 4% (veiligheidsmarge 1%)

## FTMO-uitvoerbaarheid per sleeve

| Sleeve | Instrumenten | FTMO OK? | Opmerking |
|--------|-------------|----------|----------|
| C02_faber | SPX, NDX, DJI, DAX, N225 | ✅ | Alle indices CFD op FTMO |
| C52_allweather basis | SPY, IEF, GLD | ❌ | IEF (bond ETF) niet op FTMO |
| C52_allweather lang | SPY, BOND10_SYN, GOLD_F | ❌ | Bond-leg niet uitvoerbaar |
| C17_fomc_cycle | SPX | ✅ | US500cash CFD beschikbaar |
| C54_carver basis | FX, GOLD_F, WTI_F, indices | ⚠️ | Grotendeels OK; WTI en FX op FTMO |
| C54_carver qa | FX, GOLD_F, excl. WTI | ✅ | FX+goud beschikbaar op FTMO |
| C55_daa | SPY, EEM, IWM, AGG, etc. | ❌ | Bijna alle ETFs niet op FTMO |
| C44_krediet | SPY-proxy | ⚠️ | Data slechts 1 instrument; N=17jr |
| C16_halloween | SPX/indices | ✅ | Indices beschikbaar; maar SR laag |
| C33_trend_lowvol | SPX | ✅ | SR te laag op cfd (0.14) |

## FTMO-EV per sleeve (backtest op ontdekkingsset ≤ 2024-12-31)

| Sleeve | N jr | SR(cfd) | maxDD | P99-dgloss | Auto-scale | OK@1× | EV€@auto | p_fund@auto | €/mnd@auto |
|--------|------|---------|-------|-----------|-----------|-------|----------|------------|----------|
| C02_faber__basis | 24.8 | 0.335 | 24% | 1.9% | 1.0 | ✅ | €2099.0 | 0.445 | €457.0 |
| C52_allweather__basis | 10.0 | 0.472 | 7% | 0.5% | 1.0 | ✅ | €-493.0 | 0.019 | €170.0 |
| C52_allweather__lang | 24.0 | 0.327 | 16% | 1.0% | 1.0 | ✅ | €231.0 | 0.198 | €285.0 |
| C17_fomc_cycle__basis | 10.3 | 0.372 | 23% | 2.5% | 1.0 | ❌ | €2071.0 | 0.421 | €481.0 |
| C54_carver__basis | 24.8 | -0.01 | 22% | 0.8% | 1.0 | ✅ | €-465.0 | 0.034 | €150.0 |
| C54_carver__qa | 10.3 | -0.412 | 19% | 0.7% | 1.0 | ✅ | €-540.0 | 0.0 | €59.0 |
| C55_daa__basis | 10.0 | 0.525 | 3% | 0.3% | 1.0 | ✅ | €-540.0 | 0.0 | €0.0 |
| C44_krediet__basis | 10.0 | 0.582 | 24% | 2.5% | 1.0 | ✅ | €3443.0 | 0.588 | €528.0 |
| C16_halloween__basis | 24.8 | 0.332 | 33% | 2.2% | 1.0 | ❌ | €2117.0 | 0.424 | €487.0 |
| C33_trend_lowvol__basis | 24.8 | -0.013 | 16% | 0.5% | 1.0 | ✅ | €-536.0 | 0.002 | €183.0 |

## Detail: EV op 3 scales (sleeves met FTMO-uitvoerbare instrumenten)

| Sleeve | EV@1× | p_fund@1× | EV@0.5× | EV@auto | p_fund@auto | €/mnd@auto |
|--------|-------|----------|---------|---------|------------|----------|
| C02_faber__basis | €2099.0 | 0.445 | €144.0 | €2099.0 | 0.445 | €457.0 |
| C52_allweather__basis | €-493.0 | 0.019 | €-540.0 | €-493.0 | 0.019 | €170.0 |
| C52_allweather__lang | €231.0 | 0.198 | €-522.0 | €231.0 | 0.198 | €285.0 |
| C17_fomc_cycle__basis | €2071.0 | 0.421 | €461.0 | €2071.0 | 0.421 | €481.0 |
| C54_carver__basis | €-465.0 | 0.034 | €-540.0 | €-465.0 | 0.034 | €150.0 |
| C54_carver__qa | €-540.0 | 0.0 | €-540.0 | €-540.0 | 0.0 | €59.0 |
| C55_daa__basis | €-540.0 | 0.0 | €-540.0 | €-540.0 | 0.0 | €0.0 |
| C44_krediet__basis | €3443.0 | 0.588 | €1093.0 | €3443.0 | 0.588 | €528.0 |
| C16_halloween__basis | €2117.0 | 0.424 | €515.0 | €2117.0 | 0.424 | €487.0 |
| C33_trend_lowvol__basis | €-536.0 | 0.002 | €-540.0 | €-536.0 | 0.002 | €183.0 |

## Conclusie FTMO-pivot (D-083/D-085/D-086)

**FTMO-uitvoerbaar (instrumenten beschikbaar):**
- C02_faber (indices CFD) — SR 0.32 op cfd; max dagverlies 13% → scale nodig tot ~38%
- C17_fomc_cycle (SPX CFD) — SR 0.52; max dagverlies 9% → scale ~55%
- C54_carver qa (FX+goud) — SR ~0.01 op cfd; commercieel niet interessant

**FTMO NIET uitvoerbaar (instrument-probleem):**
- C52_allweather (vereist obligatie-ETF of obligatie-futures — niet op FTMO)
- C55_daa (ETF-strategie)

**Dalende SR op cfd-vehikel ten opzichte van etf:**
- Swap-kosten (1.36 bp/nacht voor long indices) eten significant in bij maandelijkse strategieën
- Een 10-maands SMA-strategie houdt ~7 maanden gemiddeld lang → 7×21×1.36 bp ≈ 2%/jaar swap-extra

**Volgende stap (D-085 §2):**
- Focus op FTMO-compatibele strategiefamilies: kortere houdduur, lower swap-impact
- Intraday/dagelijks-vlak strategieën vermijden nachten → geen swap, geen 5%-dagrisico over nacht
- ORB (Opening Range Breakout) en soortgelijke dagelijkse strategieën zijn de prioriteit
- Bestaande ETF-catalogus heeft beperkte waarde voor FTMO-programma

**Meetlat voortaan:** FTMO-EV (netto na aftrek fee, per poging), niet SR van backtest.
