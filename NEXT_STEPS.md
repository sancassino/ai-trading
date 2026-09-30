# NEXT_STEPS v18 — Manager, 2026-09-30 12:37 Amsterdam — FASE 2 (CEO D-025…D-028, PROGRAMMA_FASE2.md)

**Bindend kader:** `CEO_MANDAAT.md` (CEO-branch `claude/upbeat-dirac-g2810q`): alleen Sandro beslist over stoppen/bevriezen/pauzeren; **geen stopcriteria**; horizon weken–maanden; lege wachtrij bestaat niet. Uitvoerder blijft op */10. Manager verscherpt/versoepelt geen CEO-drempels (zie M-009 ingetrokken).

## Beoordeling Manager (kort; blokkeringen alleen methodisch, schriftelijk in VRAGEN_MANAGER)
- N7/N8/U2b/P0 goed uitgevoerd. **Terugdraaien vereist:** de S3-drempel is door mijn M-009-standaardactie op eenzijdig t ≥ 2,0 gezet; D-023/D-026 zeggen 'vast'. **Zet PREREG_S3.md + s3_run.py terug naar de vastgelegde dag-geclusterde t ≥ 2,5 (D-006)**, behoud het power-annex als informatie (M-009 ingetrokken; bevestiging CEO volgt binnen 30 min, standaardactie = terugdraaien).
- N7-uitkomsten (dag-geclusterd): ORB 2,93→1,81 (S3-set 2,90), S1(a) 2,05, K1-FTMO 0,43/0,94 (vervalt), **RSI(2) Yahoo-dagreeks overleeft (NW 3,80 / bootstrap 3,99)**, F3b 2,29–2,35. Dit is een van de weinige robuuste lange-historie-bewijzen → in fase 2 hoort RSI(2)-overnight (negatief-scheef) bij de catalogus, met FTMO-dipprofiel-toets.

## WERKSTROMEN (WIP-limiet 1 per stroom; tijd ≈ D 30% / R 50% / F 20%; S3 preempt R zodra SPX-data compleet)
### D — Data (achtergrondproces + dagelijkse check)
- **D1 Dukascopy-lake** (P0-methode: eerlijke UA, 1 verzoek/8 s, back-off, hervatbaar; niets omzeilen; werkdagen; jaren < 10 w data overslaan). Volgorde: **SPX (2012–2020) → GRX → NSX → XAU**, daarna prioriteitenlijst uit PROGRAMMA_FASE2 (US500, GER40, US100, XAUUSD, EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, US30, USOIL, XAGUSD …). Voortgang in `data/DATA_CATALOGUS.md` (symbool, jaren, gaten, checksum, QA). S3 voorlopig op US500 zodra SPX 2012–2020 compleet is (D-021), definitief met ≥ 2 van 3 indices.
- **D2 Lange dagdata (nu starten, hoogste ROI):** FRED + Yahoo/Stooq-daghistorie binnen de gebruiksvoorwaarden en met rate-limiet: indices (S&P/Nasdaq/Dow/DAX/FTSE/Nikkei/…), sectoren/ETF's, goud/zilver/olie/koper-proxy's, FX-dagreeksen, rentes/spreads, VIX — **≥ 15 reeksen, 20–50 jaar**; **commit de dagreeksen in de repo** (`data/daily/`, klein) zodat ook een cloud-agent erop kan rekenen (M-010 stap 1). Elk bestand D3-QA (gaten, splits, DST, vergelijking met FTMO-overlap).
### R — Catalogus-onderzoek (Strateeg-eigenaar catalogus; Uitvoerder bouwt/draait)
- **R0 Engine + kostenmodel (nu):** één gemeenschappelijke engine (`engine/`) die per catalogusregel dezelfde pijplijn draait; kostenmodel = S0 (per instrument/uur) + swap; per regel outputs: netto SR, **dag-geclusterde t**, skew, dagdip-profiel (Q1b-mechaniek), per-jaar/per-regime, correlatie met bestaande sleeves. **Sjabloon staat in `ENGINE_TEMPLATE.md` (Manager)**; bouw daarop.
- **R1 Eerste catalogus-run op D2 (lange dagdata) zodra `STRATEGIE_CATALOGUS.md` v1 (Strateeg) bestaat:** ontdekkingsset = pre-2025; **reserve-OOS 2025-01→heden onaangeraakt**; multiple testing over de hele catalogus (Benjamini-Hochberg FDR + DSR met echte trial-teller, vooraf vastgelegd); shortlist ≤ 5.
- **R2 S3:** zodra SPX-data compleet → `run_s3.sh` (preempt R).
### F — Forward/MT5-onderhoud (≈ 20%)
- Forward-paper (F3b) dagelijks + alarmen; weekrapport maandag (forward_week.py); MT5-EA's onderhouden. **Forward-status nu:** `forward/paper_daily.csv` bestond bij mijn controle (12:36) nog niet → controleer 22:15 UTC-run van vanavond en meld.

## Manager-deliverables (lopend)
(a) deze v18 ✔; (b) `ENGINE_TEMPLATE.md` ✔; (c) weekrapport maandag in `EINDVERSLAG.md` (opzet staat); (d) tweede-Uitvoerder-voorstel = M-010.
