
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
