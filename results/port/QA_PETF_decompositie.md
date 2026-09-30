# QA P-ETF-a — decompositie (ontdekking ≤ 2024; reserve niet aangeraakt)

| variant | periode | SR (excess) | vol | CAGR totaal | excess/jr | cash/jr (≈ verschil) | maxDD |
|---|---|---|---|---|---|---|---|
| **basis (PREREG_PORT)** | 2001-04-02→2024-12-31 | 0.94 | 6.1% | 7.4% | 5.7% | 1.7% | 11.2% |
| basis 2001–2010 | 2001-04-02→2010-12-31 | 1.09 | 5.8% | 8.6% | 6.4% | 2.2% | 7.0% |
| basis 2011–2024 | 2011-01-03→2024-12-31 | 0.83 | 6.3% | 6.5% | 5.1% | 1.4% | 11.2% |
| basis decennium 2001s | 2001-04-02→2010-12-31 | 1.09 | 5.8% | 8.6% | 6.4% | 2.2% | 7.0% |
| basis decennium 2011s | 2011-01-03→2020-12-31 | 0.97 | 6.1% | 6.5% | 5.9% | 0.6% | 11.2% |
| basis 2021–2024 | 2021-01-04→2024-12-31 | 0.53 | 6.7% | 6.5% | 3.3% | 3.2% | 10.2% |
| zonder obligatiepoot (C52 = SPY + goud) | 2001-04-02→2024-12-31 | 0.79 | 8.0% | 7.9% | 6.2% | 1.7% | 16.9% |
| C02 op prijsindex (geen SPX_TR) | 2001-04-02→2024-12-31 | 0.92 | 6.1% | 7.3% | 5.5% | 1.7% | 11.2% |
| alleen C52 lang (beide 'sleeves' = C52L) | 2001-04-02→2024-12-31 | 0.81 | 6.4% | 6.8% | 5.1% | 1.7% | 15.3% |
| alleen C02 | 1928-10-01→2024-12-31 | 0.47 | 11.8% | 8.6% | 5.0% | 3.6% | 51.0% |

**Bijdrage per activum binnen C52 lang (etf, ≤ 2024, jaarlijks gemiddeld, vóór kasrente):**

- SPY: gem. gewicht 0.25, bijdrage +2.31%/jr, SR van de bijdrage +0.56
- BOND10_SYN: gem. gewicht 0.52, bijdrage +2.05%/jr, SR van de bijdrage +0.53
- GOLD_F: gem. gewicht 0.20, bijdrage +2.25%/jr, SR van de bijdrage +0.61

**Haircut en nulbenchmark (M-012 optie C; P-ETF-a basis, ontdekking):**

- Ontdekking: CAGR totaal 7.4% = excess ≈ 5.7% + cash ≈ 1.7% (USD-cash 2001–24).
- **A — haircut op totaal (D-054, conservatief):** 30–50% → 3.7–5.2%/jr ≈ €246–344/mnd.
- **B — haircut op excess + cash apart:** excess 30–50% korting → 2.8–4.0%/jr = €188–264/mnd **alfa boven cash**; plus cash in eigen valuta: bij USD-3m nu 4.25% ≈ €283/mnd (EUR-geldmarkt is lager; ESTR niet in de repo — nog op te halen).
- **Nulbenchmark cash-only:** ≈ €283/mnd (USD-3m nu) — elk resultaat eerst hiermee vergelijken.
- Lezing: het beoordelingsgetal is de **alfa boven cash**; de totale €/mnd hangt sterk van het renteniveau af.

**Aanvulling (ECB, officieel):** €STR nu 2.44% → cash-only in EUR ≈ €163/mnd; P-ETF-a in EUR-perspectief (optie B) = alfa boven cash €188–264/mnd + EUR-cash ≈ €163/mnd. Reeksen: data/daily/YLD_ESTR (2019→), YLD_EURIBOR3M (1994→, maandgemiddelde).
  return hold_monthly(s * np.minimum(3.0, 0.10 / sg) * calm, month_end(df["date"]))

**EUR-consistent (v25 QA-2; ontdekking ≤ 2024):** EUR-cash = €STR (2019-10→) / Euribor 3m (ervoor); excess t.o.v. EUR-cash, geannualiseerd (meetkundig).

| portefeuille | periode | alfa USD (t.o.v. USD-cash) | alfa EUR gehedged (t.o.v. EUR-cash) | alfa EUR ongehedged (t.o.v. EUR-cash) | SR ongehedged | €/mnd ongehedged alfa na 30–50% haircut |
|---|---|---|---|---|---|---|
| P-ETF-a | 2003-12-02→2024-12-31 | 5.8%/jr | 5.5%/jr | 6.9%/jr | 0.61 | €231–324 |
| P-ETF+ | 2005-04-01→2024-12-31 | 5.7%/jr | 5.4%/jr | 7.3%/jr | 0.64 | €244–341 |

Lezing: gehedged ≈ USD-alfa (hedge ruilt USD-rente voor EUR-rente); ongehedged voegt het EURUSD-resultaat toe (vol ↑, SR ↓) — twee getallen, geen gemengde 'alfa'.
