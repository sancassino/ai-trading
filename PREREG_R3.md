# PREREG R3 — vorm van het rendement vs vereiste Sharpe onder FTMO (vastgelegd vóór berekening, 2026-09-30)
Synthetische dagreeksen (100.000 dagen, seed 21) met jaarvol 10% en SR ∈ {1; 1,5; 2; 3; 4}, vijf vormen (dagrendement = μ + σ·z,
z met gemiddelde 0 en variantie 1):
- normaal (z ~ N(0,1));
- positief scheef (skew ≈ +1,5: z = (G − k)/√k, G ~ Gamma(k = 1,78));
- negatief scheef (z = −(G − k)/√k; mean-reversion-achtig profiel);
- dikke staarten (Student-t, 3 vrijheidsgraden, genormeerd);
- volatiliteitsclustering (GARCH(1,1) α = 0,10, β = 0,85, normale innovaties).
Dagdip (dagverlies t.o.v. dagstart) d = 1,2 × max(0, −r) (geen meegedragen zwevend verlies; zelfde voor alle vormen).
Simulatie = Q1b (q1b_products.simulate): 20.000 paden × 24 mnd, blok 21 d, schalen 0,3–3, producten 2-Step en 2-Step+Scaling.
Rapport: beste netto €/mnd per (vorm, SR, product) en vereiste SR voor €500/€900 per vorm. Vraag: brengt positieve scheefheid de
vereiste SR onder ~2? Geen trials.
