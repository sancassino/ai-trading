# ALLOCATIE_V1.2 — implementatie-efficiënte varianten (Strateeg; 2026-09-30 20:25 Amsterdam; D-080) — aanvulling op V1.1 (V1 en V1.1 blijven ongewijzigd)
**Geen beleggingsadvies of aanbeveling.** Kosten/tarieven/ISIN = web-claims, onbevestigd. Deze versie legt **vooraf** vast welke efficiëntievarianten worden doorgerekend en hoe ze worden beoordeeld (niet na resultaat kiezen). Reproduceerbaarheid: rust op V1.1-SHA's (PREREG_PORT 9f17d335…, PREREG_PORT2 b1a2f3f2…) en `main` ≥ 4119333.

## 1. Waarom (D-080)
Referentie (P-ETF-a, 8 ETF's, maandelijkse herweging zonder drempel): omloop 2,36×/jr ≈ 118 trades/jr; NL-retail-kosten (€3,50/trade + 1,5 bp spread + TER) ≈ €42/mnd vs €15/mnd in de engine ⇒ **≈ €26/mnd extra ≈ ½ van de premie-gebaseerde alfa (€58)**. Kosten zijn de enige schroef die zeker te draaien is. De 8-ETF-maandversie blijft **referentie**.

## 2. P-ETF-lite — exacte definitie (voor `PREREG_PORT3.md`; Uitvoerder-1/2 leggen vast vóór 01-10 12:00 en wijzigen niets daarna)
| Onderdeel | Regel |
|---|---|
| Instrumenten | 4: S&P 500-tracker (belegging én Faber-signaal), 10j-obligatie, goud, cash/geldmarkt |
| Sleeve A (C52 'lang') | zelfde regel: gewicht ∝ 1/σ60 over S&P 500 / obligatie / goud; schaal s = min(1; 8%/σ_P); **herweging per kwartaal (eerste handelsdag van jan/apr/jul/okt)** |
| Sleeve B (C02-lite) | Faber **alleen op S&P 500** (SPX-signaal, 10-maands-SMA, maandeinde; long of cash); een flip wordt **op de eerste handelsdag van de volgende maand uitgevoerd** |
| Combinatie | sleeves ∝ 1/σ60 (zoals PREREG_PORT) |
| **Drempelregel** | buiten de kwartaaldatum en flips wordt alleen gehandeld als |Δgewicht| ≥ **2% van het kapitaal** voor dat instrument (één waarde, niet geoptimaliseerd) |
| Hefboom | geen |
## 3. Varianten die worden doorgerekend (gevoeligheid, geen trials; elk apart t.o.v. referentie én t.o.v. lite)
| ID | Wijziging | Dekt D-080 |
|---|---|---|
| L0 | referentie: 8 ETF's, maandelijks, geen drempel | — |
| L1 | alleen drempel 2% (verder referentie) | (b) |
| L2 | alleen kwartaalherweging sleeve A (Faber 5 indices maandelijks) | (b) |
| L3 | Faber op 1 indexsignaal (SPX) i.p.v. 5 regio-indices, rest referentie | (a) (proxy; zie §5) |
| L4 | **P-ETF-lite** = L1 + L2 + L3 (definitie §2) | (a)+(b) |
| L5 | *zonder* C02-overlay (alleen sleeve A, S&P 500 buy-and-hold binnen A) | (c) — DD-effect van C02 geïsoleerd |
| L6 | L4 met drempel 1% / 5% (gevoeligheid van de ene drempel) | (b) |
Rapporteer per variant: omloop/jr, trades/jr, kosten (model A en **model B NL-retail**) in €/mnd, TER, SR (excess), alfa boven cash, totaal €/mnd (EUR gehedged én ongehedged), maxDD, p95-DD, 2022, tracking-verschil vs L0 (rendement en DD), periode 2001–24 én 2011–24 én 2021–24.
## 4. Beslisregel (vooraf)
- **Lite wordt als efficiëntie-variant voorgesteld (V1.3-kandidaat)** alleen als: ΔSR(L4 vs L0) ≥ −0,05 **én** maxDD(L4) ≤ 20% en ≤ 1,3× maxDD(L0) **én** netto kostenbesparing (model B) ≥ €15/mnd **én** in 2011–24 en 2021–24 geen teken-omslag van ΔSR > 0,1.
- Faalt één van de vier → L0 blijft specificatie; L1/L2 afzonderlijk mogen worden voorgesteld als ze hun eigen criterium uit V1.1 §5 halen.
- L5 beslist over de vraag 'is de C02-overlay de kosten waard': overlay is de kosten waard als ΔmaxDD ≥ 5 pp verbetering **en** ΔSR ≥ −0,03 t.o.v. L5, anders voorgesteld te schrappen (→ CEO-besluit; niets automatisch).
## 5. Kanttekeningen
(1) SPX-only-Faber (L3) vervangt 5 indices door 1; een **wereldwijd aandelen-UCITS** (MSCI World/ACWI) is hiervoor de praktische belegging, maar er is geen lange D2-reeks (ACWI/URTH-proxy ≥ 2008) → L3 gebruikt SPX als proxy en **rapporteert de tracking-fout** naar een wereldindex waar de korte proxy dat toelaat. (2) Kwartaalherweging vergroot de afwijking van 1/σ-gewichten tussendoor (vooral na vol-schokken) — meet DD-effect in 2008/2020/2022. (3) Drempel op kapitaalgewicht: voorkomt micro-trades, maar laat drift toe. (4) Kosten model B blijven web-claims. (5) Alles is ontdekkingsset; reserve-OOS wordt niet hergebruikt voor keuze tussen varianten.
## 6. Verwachte uitkomst (mijn schatting, niet bindend)
Omloop L4 ≈ 0,6–1,0×/jr (≈ 25–40 trades) ⇒ kosten model B + TER ≈ €15–20/mnd (≈ −€22/mnd t.o.v. L0); ΔSR ≈ −0,02…−0,06; ΔmaxDD ≈ +1…+4 pp. Dus de alfa boven cash (midden €58) houdt ≈ €45–50/mnd over i.p.v. €32; totaal ≈ €210/mnd. **Geen doorbraak naar €400**, wel een verbetering van de netto-verhouding.
## 7. Status H1–H8: ongewijzigd t.o.v. V1.1 §5 (H4 niet gehaald; H7 nog niet gestart; reserve-run 01-10 12:00; forward 01-10 22:25 UTC).
