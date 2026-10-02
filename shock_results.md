
## ORB-meta reserve-run (D-104, EENMALIG, 2025-01→2026-09, N=3049, vaste thr 0.690)
corr −0.037; ongefilterd +1.20bp (dag-t 0.86); gefilterd +0.06bp (N=1473); rest +2.27bp; toegevoegde waarde −2.63bp t=−1.15. ftmo_ev gefilterd SR 0.02, EV ≤ €15/mnd vs ongefilterd SR 0.64. **FAIL** op alle PREREG-criteria. Filter = in-sample/regime-ruis; niet herhalen met andere parameters op dezelfde reserve.

## Databron verrassingscijfers (2026-10-02)
faireconomy ff_calendar: alleen lopende week (forecast+actual), geen historie → eigen archief opbouwen vanaf nu (forward). FRED (csv, 200 OK): historische actuals, géén consensus; ALFRED vintages geven releasetijden. Historische consensus 5+ jr niet vrij beschikbaar → test op "surprise = actual − AR-naïeve voorspelling" is zwakke proxy. Actie: forward-archief starten (wekelijks snapshot ff_calendar), proxy-test op NFP/CPI via FRED in volgende cyclus.

## NFP-surprise-proxy (nfp_proxy.py, FRED PAYEMS, N≈40–47, <2025)
corr(surprise,reactie) −0,2; vervolgbeweging na eerste uur: |t| ≤ 1,4 voor US500/US100/XAU/EURUSD, geen consistent teken. Proxy-surprise zwak en N te klein; NUL. Geen vervolg zonder echte consensus-historie. Forward-archief ff_calendar gestart (data/calendar/).
