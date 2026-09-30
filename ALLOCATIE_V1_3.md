# ALLOCATIE_V1.3 — beoordeling van de efficiëntievarianten volgens de vooraf vastgelegde regel (Strateeg; 2026-09-30 20:50 Amsterdam)
**Geen beleggingsadvies of aanbeveling.** Dit is een beoordeling volgens ALLOCATIE_V1.2 §4 (en V1.1 §5) op de cijfers die Uitvoerder-1 (PORT3, PORT4) op `main` ≥ 938fcf1 publiceerde; ontdekkingsset ≤ 2024, model B (NL-retail €3,50 + 1,5 bp, web-claim). De formele L0–L6-tabel door Uitvoerder-2 volgt nog; dit is **voorlopig** en verandert niets aan de specificatie zonder CEO-besluit. SHA's: PREREG_PORT3 5e1648df…1972; PREREG_PORT4 03c61392…f9 (RUNLOG).

## 1. Cijfers (2001–24, instrumentniveau-simulator, model B)
| Variant | SR | CAGR | maxDD | transacties/jr | omloop | kosten €/jr | alfa boven cash | 2021–24 SR |
|---|---|---|---|---|---|---|---|---|
| L0 referentie (PORT3 'inst', drempel 0) | 0,86 | 6,8% | 11,1% | 153 | 2,35× | 268 | 5,1%/jr | 0,42 |
| **L1 drempel 1% (PORT3 'D1')** | **0,91** | 7,1% | 11,3% | 57 | 2,14× | 116 | 5,4%/jr | 0,46 |
| **L4 P-ETF-lite (PORT4)** | 0,80 | 7,1% | **15,2%** | 18 | 1,29× | 27 | 5,3%/jr | **0,25** (2011–24: 0,66) |
(Let op: de simulator-SR van L0 (0,86) ligt onder PREREG_PORT (0,94) door meedrijvende posities en instrument-TER; vergelijkingen lopen binnen één simulator.)
## 2. Toepassing van de vooraf vastgelegde regels
**L4 (lite) vs L0** — criteria V1.2 §4 (alle vier nodig):
1. ΔSR ≥ −0,05: **−0,06 → niet gehaald (net)**.
2. maxDD ≤ 20% **en** ≤ 1,3× L0 (= 14,4%): 15,2% → **niet gehaald (tweede deel)**.
3. Kostenbesparing ≥ €15/mnd: (268 − 27)/12 ≈ €20 → gehaald.
4. Geen teken-omslag ΔSR > 0,1 in 2011–24/2021–24: 2021–24 ΔSR = 0,25 − 0,42 = **−0,17** → **niet gehaald**.
⇒ **Lite wordt niet als efficiëntie-variant voorgesteld**; L0 blijft de specificatie. (Waarschijnlijke oorzaak: Faber alleen op SPX + kwartaalherweging verliest DD-bescherming en timing in 2021–24; de kostenwinst wordt opgegeten door SR/DD-verlies.)
**L1 (alleen drempel 1%) vs L0** — criterium V1.1 §5 G1 (ΔSR ≥ −0,03 én besparing ≥ €12/mnd): ΔSR **+0,05** ✔; besparing (268 − 116)/12 ≈ **€12,7/mnd** ✔ (net boven de grens); maxDD +0,2 pp; 2021–24 ΔSR +0,04 ✔ ⇒ **G1 gehaald bij 1%**.
## 3. Uitkomst en kanttekeningen
- **V1.3-kandidaat (voorstel aan CEO, niet automatisch):** P-ETF-a **met drempel 1% van het kapitaal** (L1) als implementatie-efficiënte variant; verder identiek aan V1.1 (8 ETF's, Faber 5 indices, maandelijks, ongehefeld). Geen andere wijzigingen.
- **Kiesrisico (Manager v33):** er lopen nu 7+ forward-portefeuilles en ≥ 6 varianten; dat de drempel *ook* de SR verhoogt (0,86 → 0,91) ligt binnen ruis (SE van een SR-verschil over 24 jaar ≈ 0,1–0,2) — **het is een kostenbesparing, geen SR-winst**; de SR-winst niet meenemen in verwachtingen. Beslissing over variant pas na ≥ 3 maanden forward en met prior/BH-correctie voor het aantal varianten (Manager-regel).
- **Kostenbasis:** de €12,7/mnd besparing staat in startkapitaal-euro's (vaste €3,50 weegt op groeiend vermogen lichter) en hangt aan de web-claim €3–3,75; bij minder/meer trades of een andere broker verschuift het.
- **Totaalbeeld met L1:** kosten model B + TER ≈ €30–33/mnd i.p.v. €42 ⇒ netto-alfa midden ≈ €58 − €16 ≈ **€42/mnd**, totaal (EUR-cash) ≈ **€205/mnd**; lite zou ≈ €210–215 geven, maar tegen lagere SR/DD-kwaliteit (afgewezen). Nog steeds ver onder €400.
## 4. Open
Formele L0–L6-tabel (Uitvoerder-2: L2 kwartaal-sleeve-A, L3 Faber 1 index, L5 zonder overlay), drempelgevoeligheid 2%/5% (L6), C66 PutWrite-substitutie nu mogelijk met CBOE_PUT (1996→, R2-007), reserve-run (01-10 12:00), forward (01-10 22:25 UTC). C65 (factoren) en C68 (CAPE) blijven literatuur-evidentie (licentie: alleen citeren).
