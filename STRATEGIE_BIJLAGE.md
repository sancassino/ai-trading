# STRATEGIE_BIJLAGE (Strateeg, 2026-09-30) — kostentabel, gap-details, bronnen

## A. Kosten-eerst, per instrument (swap uit `swap_specs_FTMO.csv`, bp = 0,01%; nacht = pct/jr ÷ 365)
Intraday-rondreis = spread + 2×commissie. Kolom "status": G = gemeten in repo, A = a-priori (niet in repo; S0 moet meten).
| Rang | Instrument | Intraday-rondreis (bp) | Status | Swap long (bp/nacht) | Swap short (bp/nacht) |
|---|---|---|---|---|---|
| 1 | EURUSD (en FX-majors) | commissie 0,46 (€2,25/lot/kant ≈ 0,23 bp/kant) + spread ≈ 0,1–0,5 | comm G, spread A | −1,13 | +0,14 |
| 2 | US500.cash | 0,77 | G (E1, eind-van-dag) | −1,36 | −0,81 |
| 3 | US30.cash | 0,54 | G | −2,28 | +0,12 |
| 4 | US100.cash | 0,74 | G | −1,95 | −0,21 |
| 5 | XAUUSD | 0,77 + comm 0,11 ≈ 0,9 | G | −2,17 | −0,10 |
| 6 | GER40.cash | 1,41 | G | −1,79 | −0,02 |
| 7 | XAGUSD | onbekend (commissie-spec ontbreekt) | A | −3,16 | +0,19 |
| 8 | US-aandelen | ≈ 2,9 (Q2, incl. commissie) | G | −2,3…−2,4 | −1,8…−1,9 |
| 9 | FX-crosses | a-priori 1–3 | A | niet in specs | niet in specs |
| 10 | UK100 | 7,4 (eind-van-dag; middag mogelijk lager) | G | −2,27 | +0,10 |
| 11 | Crypto (BTC/ETH) | 8–9 (Q3) | G | −8,2 | −8,2 |
| 12 | Exotics (USDZAR e.d.) | a-priori > 10 | A | — | — |
Niet-bruikbaar als bron: EU50 long +2,8 / FRA40 +31%/jr / USOIL long +5,3 bp-nacht (dividend-/roll-verwerking in de swap, momentopname; short USOIL −24 bp/nacht). Let op: E1-spreads zijn de **eind-van-dag**-bar (bovengrens); B4 gebruikte de instap-bar-spread.
Bruto-poort: ORB heeft ≈ 1,7 bp netto bij ≈ 0,8–1,4 bp kosten → bruto ≈ 2,5–3 bp ≈ 3× kosten: precies op de grens, daarom kostengevoelig (G1: −70% bij +50% spread + 1 punt slippage).

## B. Wat de recente literatuur waard is hier
- Noise-area (Zarattini/Aziz/Barbon, SFI 24-97): SPY 2007–begin 2024, totaal +1.985% netto, 19,6%/jr, Sharpe 1,33, trailing stops (bron: sfi.ch, ideas.repec.org/p/chf/rpseri/rp2497). Gepubliceerd 2024 → verwacht verval; onze 2021–26 ligt grotendeels in hun steekproef.
- Stocks-in-Play ORB (Zarattini/Barbon/Aziz, SFI 24-98): >7.000 US-aandelen 2016–2023, 5-min ORB, top-20 relatief volume, netto > 1.600%, Sharpe 2,81 (bron: ideas.repec.org/p/chf/rpseri/rp2498, cxoadvisory.com). Screening in paper: open > $5, gem. volume ≥ 1 mln, ATR14 > $0,50, relatief volume ≥ 100%. Hun kosten zijn aandelen-commissies, niet CFD-spread 2,9 bp.
- Beide: **ik heb de papers niet zelf gelezen, alleen samenvattingen**; PREREG moet de exacte regel uit het paper overnemen (Uitvoerder/Manager: SSRN-tekst).

## C. Venue-bronnen (alle secundair; FTMO zelf niet opnieuw geopend)
- FTMO 2-Step: 10%/5% doelen, 5% dag, 10% totaal statisch, fee 100% terug bij eerste reward; accountgroottes 10k–200k; 100k 2-Step ≈ €540 — propfirmmap.com/blog/ftmo-review-2026…, buttondown.com/Cypinto/archive/ftmo-pricing…
- FTMO 80% split (tot 90% Scaling), FundedNext tot 95%, The5ers tot 100%, Topstep 90% + wekelijks, trailing HWM-drawdown, Apex 100% eerste $25k, EOD-trailing, CME-only — track360.io/blog/best-prop-trading-firms-2026…, propfirmmap.com/blog/topstep-vs-apex…
- Regels per firma "verifieer zelf" (propfirmmap.com zegt dat expliciet); geen bron gaf 1-Step/trailing-details → die komen uit `PREREG_Q1b.md` (ftmo.com/trading-objectives, door Uitvoerder gecontroleerd).

## D. Data-notities
FRED-FX dagreeksen (data/fred: DEXUSEU, DEXJPUS, DEXUSUK, DEXUSAL, DEXUSNZ, DEXCAUS, DEXSZUS, …) gaan terug tot 1971 (noon NY) → geschikt voor D1-trend (S4) zonder aankoop. `mt5_export_m5.py` schrijft `spread` maar niet `tick_volume` (S2b/S0 vereist aanpassing).
