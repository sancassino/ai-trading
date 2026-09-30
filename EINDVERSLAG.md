# EINDVERSLAG (Manager, 2026-09-30 10:54) — voor Sandro

## Stand in 7 regels
1. **Doel (ambitie):** ≈ €800–900/mnd uit FTMO €80k, aantoonbaar en binnen de regels. Realistische kans (CEO/Strateeg): **≤ 10%**.
2. **Getest:** ~404 vooraf-vastgelegde varianten; vrijwel alles afgewezen na kosten. Nieuw sinds ochtend: FX-ML, aandelen-ML, H4-breakout FX/goud (R1/R2/R4) — afgewezen.
3. **Enige overlevende richting:** ORB (dagelijks-vlak, positief scheef): historisch ≈ €484–513/mnd (2021–26), ≈ €155–164 met realistische kosten — **onbevestigd** buiten 2021–26. RSI(2) is negatief-scheef en kost onder FTMO-regels te veel.
4. **FTMO-mechaniek:** vereiste Sharpe ≈ 1 voor elke-dag-vlak + positief-scheef; ≈ 3–4 voor overnight/negatief-scheef. Fee €540/€80k is **onbevestigd** → alle geld-uitkomsten 'onder aanname'.
5. **Kosten gemeten (S0):** rondreis intraday: indices 0,45–0,78 bp, FX-majors 0,63–1,22, goud 0,83; olie/zilver duur.
6. **Team:** Manager + Strateeg + **CEO** (beslist; Sandro hoeft niet meer te beslissen) + Uitvoerder. Ritme: Manager :05/:35, CEO :10/:40, Strateeg :20/:50, Uitvoerder */10.
7. **Wachtrij:** S1 noise-area-momentum → S2 earnings-ORB → S3 ORB-bevestiging (wacht op data).

## Succes in trappen (CEO D-003)
Trap 1 **ORB bevestigd** op 2011–20 · Trap 2 ≥ 1 dagelijks-vlakke, positief-scheve sleeve met netto SR ≥ 0,8 · Trap 3 ≥ €300/mnd onder FTMO-mechaniek → pas dan besluit over echte evaluatie. €800–900 alleen bij twee onafhankelijke sleeves in Trap 2.

## Stopcriteria (CEO D-004)
Stop/pauze als S3 verworpen/onbeslist én S1+S2 falen; óf **vr 3 okt 12:00** zonder lange data en zonder positieve S1/S2 → bevriezen op forward-paper. Elke 24 u evaluatie hier.

## Wat alleen jij kunt (van de CEO, `SANDRO_ACTIES.md`)
- **A-01 (hoog, 30–45 min):** HistData **alleen 2011–2020** downloaden: SPX/USD → NSX/USD → GRX/EUR → XAU/USD (≈ 40 zips, niet uitpakken, in `data/long_m1/` op de Debian/VM of Drive-link). Stappen: `DATA_REQUEST_SANDRO.md`. SPX eerst geeft al een voorlopige uitslag.
- **A-02 (laag, 2 min):** FTMO-bestelpagina: prijs + accountgroottes (bestaat €80k?).
Verder niets.
