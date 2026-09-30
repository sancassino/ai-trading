# PREREG Q1b — FTMO-producten en vereiste Sharpe (vastgelegd vóór berekening, 2026-09-30)

## Producten (regels ftmo.com/en/trading-objectives, 30-09-2026; split/refund uit how-it-works en FAQ)
- **2-Step Standard/Swing** (voor de simulatie gelijk; Swing vereist voor onze meerdaagse posities): +10% → +5%, dagverlies 5%
  van startkapitaal t.o.v. dagstart-balance, max. verlies statisch 10%, min. 4 dagen, 80% split, fee terug bij eerste reward.
- **2-Step + Scaling Plan** (benadering): als 2-Step, maar split 90% vanaf de 5e maand funded mits cumulatief winstgevend
  (kapitaalgroei +25% niet gemodelleerd — conservatief).
- **1-Step:** +10% in één fase, dagverlies **3%** van startkapitaal t.o.v. dagstart-balance, max. verlies **trailing**: hoogste
  eerdere eind-van-dag-balance − 10% van startkapitaal (ook funded, zonder plafond — conservatief), **Best Day Rule** (beste dag
  ≤ 50% van de som van de winst op positieve dagen; anders doorhandelen), 90% split, fee **niet** terug.
- Fee voor alle producten €540 (niet geverifieerd; zelfde aanname — gevoeligheid gemeld).
## Reeksen
- Reeks A (F3b-MT5, historisch) en **synthetisch**: z = gestandaardiseerde dagrendementen van A, r' = μ + σ·z met σ = 10%/√252,
  μ = SR · 10% / 252 voor SR ∈ {1, 1,5, 2, 3, 4}; dagdip d' = d · σ / sd(A) (zelfde staart- en dipstructuur).
## Simulatie
Als Q1: 20.000 paden, 24 mnd, blok 21 d, schalen t ∈ {0,3; 0,5; 0,75; 1; 1,5; 2; 2,5; 3}; per (product, reeks) de schaal met het
hoogste verwachte netto €/mnd. Rapport: tabel beste netto €/mnd per product × SR, P(netto < 0), en de door interpolatie vereiste SR
voor €500 en €900 per product. Geen nieuwe trials.
