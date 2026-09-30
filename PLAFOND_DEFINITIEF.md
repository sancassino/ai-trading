# Definitieve stand — wat is haalbaar met FTMO €80.000? (2026-09-30)

**Kernconclusie:** na ± 394 geteste varianten is er geen strategie die €880/mnd binnen de FTMO-regels haalt.
Het beste realistische niveau is **± €50–150 per maand**, met ongeveer **1 op 4 kans op een verliesjaar**. Een FTMO-challenge
is daarmee economisch niet de moeite (verwachte opbrengst per poging ≈ €0 of negatief).

| Variant (alle in MetaTrader 5 nagebouwd, FTMO-kosten) | "Kwaliteit" (Sharpe, 95%-marge) | ≈ €/mnd op €80k | Met realistische extra kosten | Kans op verliesjaar | Slechtste dag |
|---|---|---|---|---|---|
| **Kern:** koop-na-daling (RSI(2)), max 1 nacht | 0,48 (−0,24 … 1,17) | €99 | ≈ €50 (Sharpe 0,23) | 28% | 3,6% |
| Koop-na-daling, oorspronkelijke regel | 0,49 (−0,12 … 1,14) | €84 | lager | 24% | 3,8% |
| Koop-na-daling + uitbraak-strategie (ORB) — **ORB niet bevestigd buiten 2021–26** | 0,95 (0,23 … 1,65) | €225 | ≈ €146 (Sharpe 0,66) | 13–24% | 3,8% |
| Nodig voor €880/mnd | ≈ 1,4 | €880 | — | — | < 5% |

- Een Sharpe van 0,5 of lager met een marge die tot onder 0 loopt betekent: **het is niet zeker dat er überhaupt een voordeel is.**
- FTMO-challenge (fee ≈ €540, secundaire bron): slaagkans ≈ 1 op 6, ≈ 2,5 jaar tot funded, verwachte opbrengst ≈ −€10 per poging.
- Zonder FTMO: €80.000 eigen geld in een S&P 500-fonds gaf 2000–2026 gemiddeld ≈ €557/mnd, maar met dalingen tot −55%.
  Voor gemiddeld €880/mnd is ≈ €126.000 eigen vermogen nodig.
- Wat nog kan veranderen: (1) lange minuutdata (zie DATA_REQUEST_SANDRO.md) om de ORB-uitbraak buiten 2021–26 te toetsen —
  alleen de variant mét ORB komt boven €100/mnd; (2) de papieren test vooruit in de tijd (loopt sinds 30 sep 2026,
  wekelijks rapport in forward/weekrapport.md) — die vangt fouten, maar bewijst pas na jaren iets.

**Beslissing voor Sandro:** doel bijstellen (± €50–150/mnd, dan is een challenge nog steeds niet zinvol), stoppen, data voor de
ORB-toets aanleveren (optie B in DATA_REQUEST_SANDRO.md), of een eigen, nieuw idee met regels aandragen.
