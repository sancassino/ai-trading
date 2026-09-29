# Verslag NEXT_STEPS (supervisor-opdracht 2026-09-29)

**Kort: alle drie de toetsen vallen negatief uit. De FTMO-uitvoerbare momentum-edge is niet
aangetoond. Stap 4 (ensemble-run) is conform de opdracht niet uitgevoerd, omdat stap 1 faalde.**

## Stap 1 — Lange validatie 2000–2026 zonder hindsight/survivorship → NEGATIEF
Nieuwe simulator `momentum_sim.py` volgt exact de EA-regels (rebalans 1e handelsdag, lookback
N×30d, SMA10 op 10 samples à 30d, aangehouden legs niet herschaald, CFD-boekhouding).
Kosten zoals opgedragen: 8%/jr financiering (constant %), 0,05% spread per kant. 30% exposure,
9 configs (TopN 2–4 × lb 1–3), niets getuned. Regime: SPY.

- **Universum A** (26 ETF's: SPY, QQQ, DIA, IWM, EFA, EEM, EWJ, EWG, EWU, GLD, SLV, USO, TLT, IEF,
  HYG, 11 SPDR-sectoren; GLD/SLV/USO vóór hun start gespliced met GC=F/SI=F/CL=F).
- **Universum B** (point-in-time top-10 S&P 500 op marktkap. per jaareinde vóór het handelsjaar;
  `universe_pit_top10.csv`, bron [finhacker.cz](https://www.finhacker.cz/en/top-20-sp-500-companies-by-market-cap/),
  opgehaald 29-09-2026). **Survivorship-check:** alle 31 namen (incl. GE, Citigroup, AIG, Intel,
  Cisco, Merck, Pfizer) hebben volledige adjusted data op Yahoo; geen enkele ontbreekt.
  Gedelistte bedrijven (Enron, Lucent, WorldCom) stonden op geen enkel jaareinde in de top-10.
  Kanttekening: de lijst per jaar is automatisch van de bronpagina uitgelezen.

| Ensemble (9 configs) | CAGR | €/mnd op €80k | Jaren positief | Max DD (maand) |
|---|---|---|---|---|
| A, 8% financiering | +0,04%/jr | €3 | 13/27 (48%) | 27,8% |
| B, 8% financiering | +0,25%/jr | €17 | 9/27 (33%) | 25,1% |
| A, 4% / 0% (gevoeligheid) | +0,97% / +1,90% | €64 / €126 | 52% / 70% | 20,5% / 12,5% |
| B, 4% / 0% (gevoeligheid) | +1,19% / +2,13% | €79 / €142 | 37% / 56% | 19,3% / 15,1% |
| Referentie SPY buy & hold 30% (8%) | +2,18% | €145 | 17/27 (63%) | 34% |

Per config (8%): A −0,5 … +0,75%/jr, B −0,6 … +1,2%/jr, trailing DD 22–39%.
Episodes (ensemble A / B): 2000–02 −7,0% / −5,9%; 2008 +0,5% / −0,5%; 2020-Q1 −3,3% / −0,3%;
2022 −1,1% / −9,9%. B was alleen in 2019–2024 duidelijk positief; 2000–2018 overwegend negatief.

**Beslisregel** (≥65% jaren positief, DD < 20% bij 30% exposure): **faalt voor A én B.**
De CFD-financiering is ongeveer even groot als de bruto edge, en de strategie verslaat een
passieve SPY-positie niet.

## Stap 2 — Reconciliatie Python ↔ MT5 (T10, 2021–2026)
- TopN=2/lb=3/SMA10/30%: correlatie maandrendement 0,895 (0,915 vanaf 2021-02), totaal
  Python +20,0% vs MT5 +9,0% → **criterium (≥0,95, <15%) niet gehaald**.
- Oorzaken: MT5-datagat januari 2021 (posities pas ~25 jan gevuld); 10 van 56 maanden een
  andere #2-keuze bij krappe ranking. Vultiming maakt nauwelijks uit.
- Per config correlatie 0,87–0,94, afwijkingen in beide richtingen (geen systematische bias).
- **Ensemble van 9 vanaf 2021-02: correlatie 0,951, totaal +19,7% vs +18,2% → wél binnen criterium.**
- Gevolg: de Python-resultaten van stap 1 zijn overdraagbaar op ensemble-niveau (zoals hierboven
  gerapporteerd), niet per losse config.

## Stap 3 — Rang-gevoeligheid T10 (ensemble-EA in MT5, €80k EUR, 30%, swap-gecorrigeerd)
Basis steeds de 9 indices/goud/olie/EURUSD van T10 + 10 aandelen. Trekkingen vooraf vastgelegd
(`universe_step3.csv`, `random.Random(42)`), geen enkele weggelaten.

| Universum | €/mnd | Jaren+ | Stat. DD | Train → test €/mnd |
|---|---|---|---|---|
| T10 (origineel) | 186 | 5/6 | 4,7% | 107 → 318 |
| META → NVDA | 242 | 4/6 | 4,7% | 217 → 284 |
| BABA → NVDA | 406 | 5/6 | 4,2% | 406 → 406 |
| rand1 | 96 | 4/6 | 1,3% | 168 → −24 |
| rand2 | 64 | 1/6 | 14,5% | −127 → 382 |
| rand3 (incl. NVDA, PLTR) | 333 | 5/6 | 1,4% | 188 → 575 |
| rand4 | 1 | 2/6 | 8,2% | −103 → 173 |
| rand5 | −77 | 2/6 | 10,3% | −117 → −12 |

Willekeurige trekkingen gemiddeld **€83/mnd**, spreiding −€77 … €333 — **veel groter dan het
niveau** (verwachting bij echte edge: alle positief, spreiding ≪ niveau). Het resultaat hangt
vooral af van de vraag of NVDA in het universum zit.

## Stap 4 — Niet uitgevoerd
Voorwaarde ("alleen als 1 én 2 slagen") niet vervuld: stap 1 faalde. Ter info: een ensemble-EA-run
op T10 bestond al vóór deze opdracht (zie Bevindingen: €186/mnd @30%; @60% breekt de dagregel,
met dagguard stort hij in).

## Conclusie en beslispunt
Drie onafhankelijke toetsen (27 jaar historie zonder survivorship; willekeurige universums;
universum-gevoeligheid) wijzen dezelfde kant op: **er is geen robuuste momentum-edge die na
CFD-kosten binnen de FTMO-regels bruikbaar is.** Het positieve resultaat in 2021–2026 komt vooral
van de uitzonderlijke mega-cap-rally (NVDA e.d.) in precies die periode.

Beslispunt voor Sandro: deze strategiefamilie stoppen, of een fundamenteel andere richting kiezen.
Verder variëren binnen momentum-rotatie is op basis van deze resultaten data-mining.
