# VOORSTEL S11 — Ontwerp-input voor run 5 (D-066): cross-market-replicatie van C02/C52 + D2b-dataprioriteiten (Strateeg, 2026-09-30 17:10 Amsterdam)
Geen nieuw signaal; dit is methodiek- en data-advies voor de PREREG die Uitvoerder-2/1 schrijft. Één trial-familie (D-066), geen parameter-aanpassing.

## 1. Waarom dit de sterkste toets is — en wat hij NIET bewijst
Replicatie van bevroren regels op andere markten is de enige onafhankelijke data die we bij decennia-historie nog hebben. **Maar** (a) aandelenindices zijn sterk gecorreleerd (crises 0,8–0,9), dus 6 markten ≈ 2–3 onafhankelijke waarnemingen; (b) een trendfilter beat buy-and-hold **automatisch in markten met een lange bear** (N225 1990–2012, HSI 1997–2003): dat zegt weinig over alpha — het is het DD-filter-effect. De toets moet dus *gekalibreerd op een nul* worden.
## 2. Ontwerp (vooraf vast te leggen)
1. **Universum:** alle D2-aandelenindices met ≥ 20 jr historie, **exclusief de VS-familie** (SPX/NDX/DJI/RUT/SPY tellen als 1 cluster en zijn de ontdekkingsmarkt): DAX (1987), FTSE (1984), CAC (1990), N225 (1965), HSI (1986); STOXX50 (2007) **alleen informatief** (17 jr). Lijst vast vóór berekening (geen verwijderen achteraf).
2. **Regels (bevroren, geen parameters aangepast):** C02 Faber precies als in CAT1/CAT2 (10-mnd-SMA, long/cash); regionale C52 = lokale aandelen + VS-obligatie-proxy + goud, risicopariteit zoals CAT2 (let op: VS-obligatie/goud zijn USD-activa).
3. **Valuta/rente (kritiek):** rapporteer **lokale valuta** voor de aandelenpoot met rf = lokale cash waar beschikbaar (Euribor 1994→ voor DAX/CAC; UK/JP/HK-rente ontbreekt → USD-rf als *benaderde* cash en **label dat**); aparte rij in USD (via FX uit D2). Geen mix stilzwijgend.
4. **Kostenmodel:** ETF-vehikel (13 bp rondreis, TER 0,07%; lokale ETF-kosten onbekend → gevoeligheid 0,20% TER).
5. **Metrics per markt:** netto SR (excess), ΔSR en ΔmaxDD t.o.v. B&H (SR én DD), dag-/maand-geclusterde t, per decennium; gepoold: **markt-geclusterde blokbootstrap** (blokken over markten heen, dezelfde kalenderblokken voor alle markten, zodat gelijktijdige crises meetellen).
6. **Nul-kalibratie (nieuw, belangrijk):** pas *dezelfde regel* toe op **blokgeschudde versies** (stationaire bootstrap, blok ≈ 12 mnd; behoud vol/drift/kruiscorrelatie, vernietig trendstructuur) van elk marktpad, 1.000 replica's → nul-verdeling van ΔSR en ΔmaxDD t.o.v. B&H. Rapporteer de empirische p-waarde van de gepoolde ΔSR. Dit scheidt 'trend-alpha' van 'bear-market-DD-mechanica'.
7. **Beslisregel (vooraf):** *Replicatie* = gepoold ΔSR > 0 met nul-gekalibreerde p ≤ 0,10 **én** ≥ 4 van 5 markten netto SR(excess) > 0 **én** ΔmaxDD < 0 in ≥ 4 van 5. Anders: 'niet gerepliceerd op SR; alleen DD-beschermend' (een eerlijke uitkomst; C02 blijft dan een DD-filter, geen alpha-bron). **Gelezen zonder drempelaanpassing; uitkomst verandert geen regels (D-065.c).**
## 3. Verwachting (eerlijk)
Faber beat B&H op DD in vrijwel elke markt met een grote bear (hoge kans op ≥ 4/5 DD-verbetering); op SR ≈ 50/50 per markt; nul-gekalibreerde p voor ΔSR ≈ 0,1–0,4 (verwacht **geen sterke alpha-replicatie**, wel robuuste DD-reductie). Dat zou C02 herbenoemen van 'edge' naar 'risicobeheerder' — relevant voor S10b-H1/H2 en voor de boodschap aan Sandro.
## 4. D2b-dataprioriteit (Uitvoerder-1; ≤ 4 u) — rang op diversificatiewaarde × licentiehelderheid
| Rang | Bron | Wat | Licentie/voorwaarde (web-claim, onbevestigd) |
|---|---|---|---|
| 1 | **World Bank Pink Sheet** (maandelijks 1960→): goud, zilver, olie (Brent/WTI/Dubai), koper, nikkel/aluminium/…, landbouw, meststoffen | lange maandreeksen voor C58/C59-herhaling (≥ 60 jr, meerdere regimes; vervangt ontbrekende goud-/grondstofhistorie) | **CC BY 4.0** ([bron-samenvatting](https://pypi.org/project/worldbank-commodities/)); download-URL met maandelijkse hash → via officiële pagina, eerlijke UA |
| 2 | **Ken French Data Library** (dagelijks/maandelijks 1926/1963→) | factoren (Mkt/SMB/HML/RMW/CMA/Mom) **als evidentie**, niet als verhandelbare sleeve (long-short, geen UCITS-implementatie) | onderzoek/citeren; licentietekst door mij niet gelezen — vóór gebruik controleren |
| 3 | **Officiële rentes/obligatierendementen** Bund/Gilt/JGB (ECB/BoE/BoJ) + ECB €STR/Euribor (al binnen) | lokale obligatiepoot + lokale cash voor regionale C52 | officiële open data, eerlijke UA |
| 4 | REIT/vastgoed, EM-aandelen, IG/HY-krediet | echte diversifiers — **maar** ETF-proxies hebben < 20 jr; **FRED ICE-BofA-kredietreeksen zijn sinds april 2026 beperkt tot 3 jaar en herdistributie is verboden** ([FRED-voorwaarde](https://fred.stlouisfed.org/data/BAMLH0A2HYB)) → **niet gebruiken/committen** | alternatieve bron zoeken (vrij, lange reeks) of accepteren dat krediet ≤ 17 jr is |
| 5 | Yahoo-ETF's (VNQ 2004→, EEM 2003→, LQD/HYG 2002/07→) | korte reeksen met 'korte-N'-label | Yahoo: persoonlijk gebruik, niet herpubliceren (privé-repo) |
**Niet doen:** ICE-credit via FRED bewaren; scrapen van betaalde indexaanbieders (MSCI factor-/country-indices); alles achter botchecks.
## 5. Aandachtspunten voor de reserve-run (morgen)
Hindsight-labeling blijft: C52-lang/C02/P-ETF+ zijn na ontdekking gekozen; run 4 gaf 0/5 diversifiers → de reserve-uitkomst (1,75 jr, SR-SE ≈ 0,75) kan alleen *grove* tekenfouten vangen. Vooraf opschrijven wat 'falen' is: gepoold excess < 0 over het venster **én** onderkant van het 90%-BI < −1,0 SR → 'verdacht'; anders 'niet informatief'. (Lezing vastgelegd vóór de run.)

---
# ERRATUM + ADDENDUM (2026-09-30 17:40 Amsterdam) — na Manager-QA (NEXT_STEPS v27 §0i) en D2b (15 extra markten)
**Erratum (mijn fout):** ik noemde DAX en N225 'onafhankelijk'. C02 is ontdekt op SPX, NDX, DJI, **DAX, N225** (PREREG_CAT1); die twee zijn dus in-sample en tellen **niet** mee; de Manager heeft gelijk. Correct: onafhankelijk zijn alleen markten buiten die vijf. Ook juist: de tijdsoverlap (ontdekking ≤ 2024) blijft — dit toetst 'andere markt', niet 'andere tijd'.
## Voorstel voor de markt-lijst (vooraf vastleggen in de PREREG; niet op resultaat selecteren)
Met D2b zijn er genoeg markten voor een zinvolle toets. **Regio-clusters** (voor de geclusterde bootstrap; binnen een regio corr 0,7–0,9):
- **Primair (ontwikkeld, betrouwbare lokale rente of valuta-stabiel), ≥ 20 jr:** Europa: FTSE (1984), CAC (1990), AEX (1992), SMI (1990), IBEX (1993), BEL20 (1991) · Noord-Amerika: TSX (1979) · Azië-Pacific: HSI (1986), STI (1987), AXJO (1992), KOSPI (1996), TWII (1997).
- **Secundair (opkomend; alleen in USD met USD-rf, gelabeld):** BVSP, MXX, JKSE, SENSEX. **Reden:** hoge nominale inflatie/rente in de jaren 90 (BRL tot 1994, MXN tot 1996) — lokale-valuta-SMA zonder lokale rf is daar een artefact; **BVSP vóór 1995 en MXX vóór 1997 uitsluiten** (of alleen USD).
- **Informatief (< 20 jr):** STOXX50 (2007), NIFTY (2007), OMXS30 (2008).
- **In-sample (tonen, telt niet mee):** DAX, N225, SPX/NDX/DJI/RUT/SPY.
## Beslisregel bij n = 12 primaire markten (vervangt S11 §2.7; vooraf)
- **Gepoold** ΔSR t.o.v. B&H met **regio-geclusterde** blokbootstrap (clusters: Europa, N-Amerika, Azië-Pacific, [LatAm/EM apart]); nul-gekalibreerde p ≤ 0,10.
- **Tekentelling:** netto SR(excess) > 0 in ≥ 8 van 12 én ΔmaxDD < 0 in ≥ 9 van 12 (een eenzijdige binomiaaltoets onder H0 'pure DD-mechanica' geeft p ≈ 0,19/0,07 bij kans 0,5 — **daarom wordt de nul-kalibratie, niet de tekentelling, leidend**).
- **Labels:** 'gerepliceerd' (beide criteria); **'niet gerepliceerd op SR, alleen DD-beschermend'**; **'onvoldoende power'** als het 90%-BI van gepoold ΔSR nul én +0,3 omvat. Geen label 'edge bevestigd' uit één run; en **pre-1990** (FTSE, TSX, HSI, STI) apart rapporteren als 'andere tijd'-indicatie.
- Rapporteer altijd **aandelenpoot** apart van obligatie-/goudpoot (regionale C52 is geen onafhankelijke test van de timing).
## Verwachting (herzien)
Met 12 markten stijgt de power, maar de markten zijn niet onafhankelijk (wereldwijde crises); ik verwacht DD-reductie in ≥ 10/12 en een gepoolde ΔSR ≈ 0 ± 0,15 (nul-gekalibreerde p ≈ 0,15–0,4) → label 'alleen DD-beschermend' of 'onvoldoende power'. Dat is een bruikbaar, eerlijk antwoord voor S10b-H1/H2.
