# PREREG CAT3 — catalogusrun 3 (Uitvoerder-2; D-043 punt 5: prio-3 + v1.1-nieuwkomers) — vastgelegd vóór berekening, 2026-09-30

Engine/gates/vehikelset zoals PREREG_CAT2 en PREREG_PORT (etf 13 bp/TER 0,07%; future R2-fix; ontdekking ≤ 2024-12-31; reserve-OOS niet aangeraakt). Eén variant per regel, 0 vrije parameters →
**8 trials** (C04, C16, C29, C33, C43, C44, C45, C55). Niet gedraaid en waarom: C13 (FX-value: geen CPI per land in de repo), C24 (earnings: te korte data), C14 (Shiller-licentie niet gecontroleerd), C23/C28/C31/C46/C47 (prio 4, run 4).
Primair vehikel staat per regel vast: long/kas-regels etf, long/short future. Vehikelrapporten (geen trial) volgen voor cfd_retail waar relevant.
| ID | regel (exact) | universum (vooraf) | vehikel |
|---|---|---|---|
| C04 | lang als EMA50 > EMA200, kort anders (slot-signaal, positie vanaf dat slot); gewicht 0,10/σ60, cap 3; start 1990 (FX-pegs) | 6 FX-majors (FRED) + goud-future | future |
| C16 | lang op handelsdagen waarvan de volgende handelsdag in nov–apr valt, anders kas | SPX, NDX, DAX, N225, FTSE (prijsindex) | etf |
| C29 | z = (slot − gem20)/σ20 van slot; |z| > 2 → tegen de afwijking in, 5 handelsdagen vast; daarna weer signaal; start 2004 | EURGBP, EURJPY, EURCHF (Yahoo) | future |
| C33 | C05-signaal (TSMOM 1/3/12m, 0,10/σ60, cap 3) alleen als σ60 < de mediaan van alle σ60 tot t (expanding, min. 250 obs); maandelijks | U12 (als C01/C05) | future |
| C43 | maandeinde: positie = −teken(Δ 10j-rente over 63 dagen) (lang bij dalende, kort bij stijgende rente); start 1985 | SPX, NDX, DAX | future |
| C44 | maandeinde: lang SPY als (HYG/IEF)-ratio (adjclose) 63-daags rendement > 0, anders kas; start 2008 (HYG 2007) | SPY | etf |
| C45 | maandeinde: lang SPX als (TNX − IRX) > 0, anders kas (T10Y2Y niet beschikbaar → proxy 10j−3m; vermeld) | SPX (prijsindex; etf-TR-proxy waar de engine die heeft) | etf |
| C55 | DAA: maandeinde; canaries EEM en AGG met 13612W-momentum; beide > 0: 100% risico, één: 50%, geen: 0% (rest SHY); risico = top-6 op 13612W uit {SPY, IWM, EFA, EEM, VNQ, DBC, GLD, TLT, LQD, HYG}; start 2005; benchmark 60/40 SPY/IEF | ETF's | etf |
**Verwachting (kort, vooraf):** C16/C43/C44/C45 t < 3 (gepubliceerde/algemene effecten, verval); C29 kostenpoort ok maar t ≈ 1–2; C04 SR 0,2–0,4; C33 ≥ C05 in SR maar t ≈ 3; C55 SR 0,4–0,6 met korte sample (≈ 20 jr) en t ≈ 2–3. Verwacht 0–1 door G-ontdekking; elke overlevende blijft een ontdekkingsresultaat (winnaarsvloek), geen kandidaat.
