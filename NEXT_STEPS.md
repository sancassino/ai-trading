# NEXT_STEPS — supervisor, 2026-09-29 ~17:00

## Beoordeling van ronde 1
Uitstekend uitgevoerd: stappen 1–3 netjes, negatief resultaat eerlijk gerapporteerd, stap 4 terecht overgeslagen. Momentum-rotatie op aandelen/indices-CFD's is afgewezen (27 jaar: ≈ +0–0,3%/jr netto, ≈ SPY buy&hold). **Geen verdere MT5-runs, geen nieuwe parametervarianten voor deze familie.**

Kanttekening op jullie stap 1 (geen reden om de conclusie te wijzigen, wel te vermelden): 8%/jr financiering is voor 2009–2021 te hoog; jullie 0%-gevoeligheid gaf bruto +2%/jr, dus de conclusie houdt.

## Wat het doel eigenlijk vraagt
€880–2.000/mnd op €80k = 13–30%/jr bij max 10% DD en max 5% dagverlies. Dat vereist netto Sharpe ≳1,5 bij lage DD. Bekende publieke edges (momentum, trend, carry) halen na kosten typisch Sharpe 0,3–0,7. Verwacht dus eerlijk: niet haalbaar. Nog één laatste, strikt begrensde poging om dat te falsifiëren:

## Opdracht (alleen Python, lange data 2000–2026, geen MT5 tenzij beide drempels gehaald)
Pre-registratie: leg **vóór** het draaien in `PREREG_ronde2.md` vast: families, parameters (geen grid, één vaste set uit literatuur), kosten, beslisregel. Niets aanpassen na het zien van resultaten.

**Familie 1 — Tijdreeks-trend, multi-asset, vol-getarget** (managed-futures-stijl): ETF/FX/grondstof-universum (SPY, EFA, EEM, TLT, IEF, GLD, USO/CL=F, DBC-proxy, EURUSD, USDJPY, GBPUSD, AUDUSD), signaal = 12-maands rendement > 0 → long, < 0 → short (of flat), gewicht = 10% jaarvol-target / eigen 60-daagse vol, maandelijks herbalanceren. Één vaste set (12m, geen varianten). Kosten: spread 0,05%/kant, financiering realistisch per periode (gebruik historische korte rente, bv. FRED/Yahoo ^IRX, niet flat 8%).
**Familie 2 — FX-carry + trend-combo op G10** (high-minus-low rente, 3 long/3 short, maandelijks; rente uit FRED indien beschikbaar, anders melden en overslaan).

Rapporteer per familie: netto CAGR, vol, Sharpe, max maand-DD, %jaren+, per-jaar-tabel, 2000–02/2008/2020/2022. Vergelijk met SPY b&h op gelijke vol.

**Beslisregel (hard):** doorgaan naar MT5-implementatie alleen als Sharpe netto ≥ 0,7 over ≥ 20 jaar, ≥ 65% jaren positief, max DD < 15% bij 10% vol-target, én de FTMO-dagregel (max dagverlies 5%) in de dagreeks niet wordt overschreden. Anders: schrijf "afgewezen", update RUNLOG, en **stop** — wacht op beslissing van Sandro (zie EINDVERSLAG.md).

## Verwacht beeld (prior)
Familie 1: Sharpe netto 0,3–0,6, DD 15–25% bij 10% vol; mogelijk sterke jaren 2008/2022 maar veel zwakke jaren 2011–2019. Familie 2: carry-Sharpe ~0,3, crash-risico. Meest waarschijnlijke uitkomst: beide falen de beslisregel, en zelfs bij slagen is 13%/jr bij DD<10% ver weg. Een uitkomst die veel beter is dan dit → extra wantrouwen (lookahead-bug, survivorship) en eerst controleren.
