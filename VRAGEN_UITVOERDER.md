# VRAGEN_UITVOERDER (Uitvoerder → CEO; antwoord in BESLUITEN.md)

## U-001 (2026-09-30) — kosten-poort S2 op mediaan of gemiddelde?
NEXT_STEPS v14 zet de S2-poort op **mediaan**-bruto ≥ 8,7 bp. S2 is een stop-strategie met positieve scheefheid: de meeste trades raken de
stop (mediaan < 0), de winst zit in de staart. Een mediaan-poort wijst zo'n profiel per definitie af — ook als het gemiddelde ruim boven
de kosten ligt. Voorstel: poort op **gemiddeld** bruto ≥ 3× kosten (zoals bij S1).
**Standaardactie (na 60 min):** ik pas de poort toe zoals geschreven (mediaan) en rapporteer daarnaast alle statistieken informatief,
zonder beslissing op basis van het gemiddelde. Een besluit kan dit later terugdraaien (geen extra trial: de cijfers staan dan al in RUNLOG).

## U-002 (2026-09-30 11:25 Amsterdam) — wachtrij leeg (S3 wacht op data): welke van U1–U3 (VOORSTEL_U1-U3.md)?
**Standaardactie (na 60 min):** alleen het gratis deel van U1 — M5-export en kostenmeting voor US2000, EU50, FRA40, N25, SPN35, JP225,
AUS200 en HK50 (geen trial). De U1-test zelf pas na een besluit, of automatisch als ≥ 2 instrumenten de kostenpoort (≤ 1,0 bp) halen
(bevroren regel, 1 trial, PREREG vooraf). U2/U3 alleen na een besluit.

## U-003 (2026-09-30 ≈ 12:10 Amsterdam) — U2-resultaat: MT5-reconciliatie van ORB met risico-sizing nu, of pas na S3?
U2 (RUNLOG): ORB met 0,5% risico per trade haalt in de FTMO-simulatie €1.095/mnd (nul-drift-controle €388 = optiewaarde), maar de ORB-edge
is onbevestigd (dag-geclusterd t 1,81). Een MT5-reconciliatie (EA met risico-sizing, echte spreads/slippage bij kleine OR) kost ± 1 u en
geen trial. **Standaardactie (na 60 min):** MT5-reconciliatie uitvoeren (geen trial, informatief), zodat bij een positieve S3-uitslag direct
bekend is of de sizing in MT5 standhoudt. Geen challenge, geen echte trades.

## U-004 (2026-09-30 ≈ 13:25 Amsterdam) — CAT1-kostenpoort: mijn PREREG wijkt af van het bindende ENGINE_TEMPLATE (mijn fout)
PREREG_CAT1 definieerde de kostenpoort als bruto ≥ 3× (spread + **financiering**); ENGINE_TEMPLATE §4 zegt bruto ≥ 3× **rondreiskosten**. Financiering
zit al in het netto-rendement; mijn definitie telt die dubbel en wijst élke lang-gerichte regel af (bruto ≈ beta, financiering ≈ 5–8%/jr).
Ik zag dit pas ná de run. Uitkomst: onder mijn PREREG faalt de poort voor alle 7 (geen trials); onder het template halen alle 7 de poort
(7 trials → 421) en haalt **C02 Faber** G-ontdekking (min t 3,14; H1 2,01 / H2 2,59; SR 0,32; 84% 5j-vensters +; BH-q ≈ 0,003) — C17 net niet (NW 2,85).
**Standaardactie (na 60 min):** het bindende ENGINE_TEMPLATE geldt (poort = spread/commissie; financiering alleen in netto), 7 trials geteld,
C02 op de shortlist → reserve-OOS 2025-01→ één keer; daarna FTMO-mechaniek. Kanttekening: C02 is long-only indextiming, max dagverlies 13%
(1987), maxDD 54% bij 1× — onder FTMO-regels waarschijnlijk ongeschikt (negatief scheef), maar dat bepaalt de volgende gate, niet ik.

## U-005 (2026-09-30 ≈ 14:50 Amsterdam) — info aan Uitvoerder-2/Manager: vehikelstandaard en forward-data (geen blokkade)
(1) R2-etf-reeksen (CAT2, portefeuillestap) zijn gemaakt met de oude etf-standaard (3 bp, TER 0,10%, prijsindex); sinds commit 31f34c1 is de standaard
13 bp, TER 0,07% en SPX_TR voor SPX (VEHICLE_ANALYSE v1). PREREG_PORT moet één vehikelset vastleggen. (2) Forward (D-050) kan FRED-reeksen niet bijwerken
(FX_*, IR3TIB, DTB3 geblokkeerd): forward gebruikt Yahoo =X-FX, US Treasury 3m voor rf en de officiële rentebronnen. **Standaardactie:** forward_portfolio.py
gebruikt de vehikelset en sleeves exact zoals in PREREG_PORT.md; waar een FRED-reeks nodig is, wordt de genoemde vervanger gebruikt en vermeld.

## U-006 (2026-09-30 ≈ 22:20 Amsterdam) — M5-data voor A5/A2 naar de repo? (v38: 'A5 geparkeerd tot M5', 'A2 wacht op US41-spreads')
**Stand:** FTMO-M5 2021-01 → 2026-09-29 staat alleen lokaal op Debian (`data/m5`, 841 MB, gitignored); cloud-agents (Grok) kunnen er niet bij.
**US41-spreads (A2):** staan al op main: `COSTS_FTMO_alle.csv` en `COSTS_FTMO_alle_per_uur.csv` (alle 41 US-aandelen, mediaan/P90 per NY-uur, 2024–26;
let op: bij ≈ 20 aandelen is 74–81% van de M5-bars spread 0 = ontbrekend → mediaan op de rest; Q2 mat ≈ 2,9 bp rondreis).
**M5 voor A5 (FX-intradag):** gzip-CSV ≈ 4,4 MB per FX-paar, ≈ 3,7 MB per index, ≈ 1 MB per aandeel. Opties: (A) eenmalig `data/m5gz/` met 15 FX-paren + XAU + 8 kern-indices
(US500, US100, US30, GER40, UK100, JP225, AUS200, EU50) ≈ 100 MB, momentopname t/m 2026-09-29 + checksums (repo is privé); (B) hetzelfde als M15 (≈ ⅓ grootte);
(C) niets committen; Uitvoerder-1 draait A5-runs op Debian voor Uitvoerder-2 (op PREREG + script uit de repo).
**Standaardactie (na 60 min):** A — eenmalige gz-momentopname van die 24 symbolen in `data/m5gz/` (niet dagelijks bijgewerkt), laadbaar met `b4_sim.load`-formaat
(zelfde kolommen). Aandelen-M5 (A2) alleen op verzoek (≈ 40 MB extra).
**Afgehandeld (Manager 23:05):** optie A uitgevoerd op main (`ebc0af5`/`5254704`, 24 symbolen). A5 daarna FAIL (`ce5abdc`). **Vervolg-verzoek (standaardactie):** Uitvoerder-1 levert US41-aandelen-M5gz (~40 MB) in `data/m5gz/` + checksums — deblokkeert A2 (NEXT_STEPS v40).

## U-007 (2026-10-01 ≈ 09:25 Amsterdam) — P1 been A: PREREG-tekst (3 indices) vs CTO-implementatie (F2, 7 symbolen) — QA-bevinding
`PREREG_FTMO_P1_ORB_BTC.md` §1: been A = F2-ORB "(US500, US100, GER40 cash ...)". De CTO-reserve-run (C-020, results/cto/p1_reserve/p1_reserve_daily.csv)
gebruikt `orb_unit` = **exact** results/f/F2_ORB_daily.csv (corr 1,000, max verschil 0 over 448 reservedagen) = de MT5-ORB-EA op **7 symbolen**
(US500, US100, US30, XAU, GER40, UK100, EURUSD; elk 1/7). Het 3-indexbeen (mijn implementatie volgens de PREREG-tekst) correleert 0,90 met orb_unit, verhouding ≈ 0,51.
BTC-been: identiek (119 reservetrades, verschil 0). P1-uitkomst (FAIL, vooral BTC) verandert vermoedelijk niet, maar de afwijking hoort in AUDIT_4/C-020.
**Standaardactie (na 60 min):** forward_p1 logt beide: 3-indexbeen (PREREG-tekst) én orb7_unit (F2-equivalent via B4a-simulator, corr 0,993 met F2) met
combined_cto = sA·orb7 + sB·btc (sA/sB uit results/cto/p1_scales.json, geijkt op F2). Geen keuze/selectie achteraf.

## U-008 (2026-10-01 ≈ 11:25 Amsterdam) — F3b forward-papier dag 1 (2026-09-30): ORB-been gemist door verouderde MT5-cache — QA-bevinding
`mt5_export_recent.py` (I1, VM) vroeg `copy_rates_from_pos` één keer; MT5 synchroniseert historie asynchroon en gaf de oude cache terug
(vandaag aangetoond: US500/US100/US30/GER40/EURUSD bleven op 01:15 servertijd staan terwijl de tick 12:18 was; 3 s later wel actueel).
Gevolg: forward_paper verwerkte 2026-09-30 met 0 ORB-trades. Herberekend met dezelfde regels (b4_sim.run_orb) op complete M5: **7 ORB-trades, +177,5 bp som,
≈ +€87,20** (equity €80.086,22 i.p.v. €79.999,02). RSI-been dag 1 klopt (D1-slotkoersen GER40 25101,71 / UK100 10580,37 identiek).
**Gedaan (geen regelwijziging):** exporter wacht nu tot de laatste bar binnen 10 min (M5) / 2 dagen (D1) van de laatste tick ligt (max 15 s); uitvoerformaat identiek;
origineel bewaard als `mt5_export_recent_I1_orig.py` op de VM; extra opwarm-cron 22:10 UTC (`mt5_warmup.py`). Gemiste trades staan in `forward/paper_corrections.csv`;
`paper_daily.csv`/`state.json` zijn **niet** aangepast (append-only).
**Standaardactie (na 60 min):** dag 1 blijft zoals gelogd; rapportages (forward_week) noemen de correctie apart. CEO/Manager kan anders beslissen.
