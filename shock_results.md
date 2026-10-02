
## ORB-meta reserve-run (D-104, EENMALIG, 2025-01→2026-09, N=3049, vaste thr 0.690)
corr −0.037; ongefilterd +1.20bp (dag-t 0.86); gefilterd +0.06bp (N=1473); rest +2.27bp; toegevoegde waarde −2.63bp t=−1.15. ftmo_ev gefilterd SR 0.02, EV ≤ €15/mnd vs ongefilterd SR 0.64. **FAIL** op alle PREREG-criteria. Filter = in-sample/regime-ruis; niet herhalen met andere parameters op dezelfde reserve.

## Databron verrassingscijfers (2026-10-02)
faireconomy ff_calendar: alleen lopende week (forecast+actual), geen historie → eigen archief opbouwen vanaf nu (forward). FRED (csv, 200 OK): historische actuals, géén consensus; ALFRED vintages geven releasetijden. Historische consensus 5+ jr niet vrij beschikbaar → test op "surprise = actual − AR-naïeve voorspelling" is zwakke proxy. Actie: forward-archief starten (wekelijks snapshot ff_calendar), proxy-test op NFP/CPI via FRED in volgende cyclus.

## NFP-surprise-proxy (nfp_proxy.py, FRED PAYEMS, N≈40–47, <2025)
corr(surprise,reactie) −0,2; vervolgbeweging na eerste uur: |t| ≤ 1,4 voor US500/US100/XAU/EURUSD, geen consistent teken. Proxy-surprise zwak en N te klein; NUL. Geen vervolg zonder echte consensus-historie. Forward-archief ff_calendar gestart (data/calendar/).

## Ongefilterd ORB B4a — FTMO-EV (orb_full_ev.py, beschrijvend)
2021-24 SR 0.98; reserve 2025-26 SR 0.64 (nog positief, maar reserve is nu voor ORB-meta verbruikt; geen nieuwe test mogelijk). Schaal 0.3: EV €155/mnd, survive 0.87 (alles); 0.4: €284, 0.67. Hoofdvraag voor Sandro: ~€150–280/mnd bij 13–33% kans op verlies van de fee-cyclus — alleen als paper-forward (vanaf 2 okt) bevestigt.

## ORB regime- en tijdstop-onderzoek (2 okt; orb_regime.py, orb_timestop.py)
**Correctie:** B4a ORB is door het project zelf AFGEWEZEN (B4_output: +1,73bp, t test 1,14, DSR 0,54, jaren+ 4/6). Per jaar: 2021 −1,4 | 2022 +6,0 | 2023 +1,6 | 2024 +0,2 | 2025 +2,9 | 2026 −1,1. Per symbool: US100 +5,9 (t 2,5), GER40 +4,0 (t 2,2), US500 +2,4, XAU +1,5, US30 +0,3, UK100 −0,8, EURUSD −0,4. De eerdere "SR 0,88"-EV is optiewaarde uit een zwakke, niet-gevalideerde edge — niet als kansrijk spoor presenteren.
**Regime-splitsing (vaste mediaan per symbool op ≤2024; features: vol-niveau, gisteren-range-ratio, |20d-trend|, |gap|):** lage trend/gap/range-ratio lijkt beter in 2021–24 (t 2,7–2,9, +3,5…+4,1bp), maar (a) bijna volledig 2022 (+10…+12bp; andere jaren ≈ 0), (b) omkering in 2025–26 (hoog beter). 8 cellen, geen robuust regime. NUL.
**Tijdstop (uitstap open+2u / +4u i.p.v. sessieslot):** 21–24 +0,5bp (t 0,7) / +1,0bp (t 1,2) vs baseline +2,0 (t 2,0); 25–26 negatief. Verslechtert. Mechanisme "impuls dooft uit" niet bevestigd; edge zit in de late-dag-drift. Kosten ORB klein (0,4–1,1bp/trade; bruto ≈ +2,7bp).

## ORB op extra indices (PREREG_ORB_INDEX_EXT, EU50/FRA40/JP225): FAIL
21–24 gepoold +2,8bp (kosten 0,5) / +1,8bp (kosten 1,5; dag-t 1,09, N 2513); 25–26 −0,3/−1,3bp. EU50 +4,1, JP225 +3,4, FRA40 +0,9 (21–24). Zelfde patroon als eerder: 2022–23 goed, daarna weg. Geen robuust index-effect. Trials in results/ceo/TRIALS_CEO.csv.

## Turn-of-month (PREREG_TOM, 7 indices, 1990–2024): FAIL
Train 1990–2015 bruto +33,7bp/trade (5 nachten), netto (11bp: spread+swap) +22,7bp, gem. t 1,6; test 2016–2024 bruto +7,2bp, netto −3,8bp, t −0,1; DAX/FTSE/N225/STOXX negatief. Klassiek verdwenen effect; swap (≈10bp/5 nachten long) eet de rest. Gesloten.

## Index-pairs mean-reversion (PREREG_PAIRS, NDX–SPX, DAX–STOXX, DJI–SPX, FTSE–DAX, 1995–2024): FAIL
Test 2016–24 netto (5bp/dag kosten): −2,4/−4,5/−2,2/−12,6bp (h=1); bruto ≤ +3bp. Train alleen NDX–SPX licht positief (+8bp, t 1,6), test weg. Spreads te klein t.o.v. kosten.

## Aandelen cross-sectioneel intraday (PREREG_STK_XS; stk_xs.py; 30 US-CFD's, 2021–2024)
S1 reversal(prev-ret) −6,4/−4,8bp/dag (train/test); S2 gap-momentum −15,7/−4,0; S3 gap-reversal −1,4/−12,6; S4 reversal(last30) −10,0/−6,2 (netto, kosten 5–9bp rondreis per been). Alles negatief; bruto < kosten. (Eerste run S1 had same-day lookahead, −108bp: bug gevonden en gerepareerd vóór conclusie.) FAIL.

## Crypto intraday US-open-momentum (PREREG_CRYPTO_ID, BTC/ETH, 14:30–15:00 UTC → 15:00–17:00)
BTC: train +3,9bp (t 0,7), test +10,1bp (t 1,2); ETH: train +4,0 (t 0,6), test −10,4 (t −1,3). Beschrijvend 2025–26: BTC +9,8 (t 1,6), ETH +11,4 (t 1,3) — niet voor oordeel. Formeel FAIL (t<2), maar teken overwegend positief: kandidaat voor een grotere test (meer crypto's, meerdere sessietijden) mits vooraf vastgelegd; swap crypto 11,9bp/dag dwingt intraday.

## Uur-van-de-dag scan (PREREG_HOUR_SCAN; hour_scan.py; 736 symbool-uur-combinaties, train 2021–23, test 2024)
10 combinaties haalden |t|≥4 en |gem|≥2×kosten, 9 daarvan FX-paren op servertijd-uur 0/1 (+2…+4bp/uur, train t 7–16, test zelfde teken, t 2–9). **Spread-artefact, geen edge:** de volledige drift zit in één M5-bar (01:00–01:05: GBPUSD +1,4bp, USDCHF +2,8bp) waarin de spread terugvalt van 2–7bp (rollover, uur 0) naar 0,3–0,5bp; de (bid-)reeks stijgt mee omdat de bid na de verbreding terugkeert naar mid. Instappen aan de wijde ask vóór de bar kost de hele spread; na de bar is de drift 0. Waarschuwing voor alle bid-gebaseerde FX-backtests die rond servertijd 00:00–01:00 positie houden. Overig: EURUSD uur 14 netto +0,4bp (nihil). Geen handelbare uur-effecten.
