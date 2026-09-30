# VOORSTEL S10 — Go/no-go-kader voor een echte FTMO-evaluatie (beslisstructuur, GEEN trial, geen nieuw signaal)
(Antwoord op D-013/NEXT_STEPS v16. Bewust geen 'slimme challenge-truc': lage schaal/weinig trades om alleen fase 1 te halen en uitbetaling te minimaliseren, of hoge schaal voor optiewaarde, is gokgedrag/misbruik van de fee-structuur — niet voorgesteld, zie R3: nul-edge geeft al +€216/mnd door vol alleen.)

1. **Logica.** Een evaluatie is alleen verdedigbaar als de edge *zonder* optiewaarde positief is. Het kader legt vooraf vast wanneer het team (CEO → Sandro, die de aankoop altijd zelf doet) mag adviseren te kopen, zodat niemand dit achteraf met hoop invult.
2. **Kosten.** Fee €540 'onder aanname' (M-002 onbevestigd; terug bij eerste reward, dus het echte verlies bij falen is de fee + tijd). ORB-kosten 0,45–0,78 bp (S0) zijn in de frontier al meegenomen (G1: −70% drift).
3. **Kader (alle voorwaarden, vooraf):**
   - **G1 (bewijs):** S3 = 'bevestigd + blijvend' (D-011). Zonder G1: no-go, onafhankelijk van al het andere.
   - **G2 (recent regime):** S8-vensters (b) 2024–26 én (c) 2025–26 geven netto ≥ 3× nul-drift-waarde (beslisregel S8), of S9-stap 2 toont dat 2024–26 een laag-vol-periode was en de edge in het hoog-vol-regime terugkomt (dan wél go, met expliciet regime-risico).
   - **G3 (pessimistisch scenario):** Q1b-frontier ORB-alleen onder '−50% drift + G1-kosten' (€155–164/mnd in de huidige 2021–26-reeks) met P(netto<0) ≤ 35% *binnen de S8-vensters*; nu 50% → nu niet gehaald.
   - **G4 (uitvoering):** papieren forward (F3b) én een aparte ORB-papierreeks ≥ 3 mnd zonder alarm (dag ≥ 4% / DD ≥ 8%) en ORB-bp/trade ≥ 50% van backtest; geen echte order zonder dat.
   - **G5 (regels):** positiegrootte consistent (vaste 1/7 × schaal, dagverlies < 4%), geen martingale/grid/HFT, 2-Step (ORB is intradag-vlak → Standard-account volstaat; Swing is niet nodig), nieuwsregel alleen relevant voor funded Standard (geverifieerd door Manager).
   - **G6 (Auditor, D-005):** onafhankelijke audit vóór enige echte-geld-stap.
4. **Data.** Alleen bestaande uitkomsten (S3, S8, S9, forward). Niets nieuws.
5. **Verwachting.** Huidige stand: G1 open, G2 open, G3 niet gehaald, G4 loopt (eerste forward-dag 30-09), G5/G6 n.v.t. → **no-go nu**. Kans dat alle zes ooit gehaald worden: ≈ 5–8% (G1 ≈ 10–15% alleen al).
6. **PREREG/beslisregel.** Dit document ís de pre-commit: go = G1–G6 alle waar; anders geen advies om te kopen. Drempels worden niet aangepast na het zien van S3/S8.
7. **Falen.** Te streng → we adviseren nooit en missen een echte edge (aanvaardbaar: asymmetrisch, een fee + tijd is goedkoper dan een vals-positief, maar een vals-negatief kost de hele zoektocht). Te los → G3 hangt aan één 2,7-jarig venster met brede band.
