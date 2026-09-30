# VERWACHTING — premie-gebaseerde forward-looking verwachting voor P-ETF-a/b (Strateeg, 2026-09-30 18:20 Amsterdam; D-072)
**Status:** eerste versie. Alle cijfers zijn *web-claims of eigen aannames* (gemarkeerd), geen bewijs. Doel: de verwachting niet op de 2001–24-backtest baseren (obligatie- én goudbull), maar op langetermijnpremies met waarderingscaveat.

## 0. Samenvatting
Premie-gebaseerd komt **P-ETF-a (ongehefeld) uit op ≈ €140 / €240 / €340 per maand totaal (laag / midden / hoog)**, d.w.z. **alfa boven cash ≈ −€20…+€175/mnd (midden ≈ €79)** plus EUR-cash ≈ €163. **Dat ligt onder het €400–500-doel** in alle drie de scenario's; de CEO meldt dit volgens D-072 aan Sandro als tussenresultaat. **Hefboom helpt niet** in het midden-scenario: het marginale excess per eenheid hefboom (≈ 1,2%) is lager dan de financieringsopslag (rf + 1,5%). De backtest (€380/mnd alfa) weerspiegelt vooral gerealiseerde bull-premies (obligaties, goud), niet een structurele alfa.

## 1. Bouwstenen (per activaklasse, excess t.o.v. cash) — scenario's
| Klasse | Historisch/lange termijn (web-claim) | Waardering nu (web-claim/data) | Forward excess laag / midden / hoog |
|---|---|---|---|
| **Aandelen** | wereldwijd 125 jr: reëel 5,2% vs bills 0,5% ⇒ ≈ 4,7%; laatste 25 jr ERP 4,3% ([UBS/DMS Yearbook 2025](https://www.ubs.com/global/en/investment-bank/insights-and-data/2025/global-investment-returns-yearbook-2025)) | **Shiller-CAPE ≈ 41** (top 1% historie; [Nasdaq/Fool-samenvatting](https://www.fool.com/investing/2026/09/18/market-signal-seen-only-once-point-next/)); Vanguard 10-jr-verwachting VS-aandelen ≈ 3,9–5,9% nominaal, ex-VS 4,7–6,7% ([Vanguard VCMM, dec. 2025-run](https://corporate.vanguard.com/content/corporatesite/us/en/corp/vemo/vemo-return-forecasts)) bij USD-3m ≈ 4,1% ⇒ excess ≈ 0…+2% | **0% / 2,0% / 4,3%** (laag = waarderingsmodel; hoog = historische ERP zonder waarderingscorrectie) |
| **Obligaties (10j Treasury, D ≈ 8)** | 125 jr: bonds reëel 1,7% vs bills 0,5% ⇒ ≈ +1,2% (UBS/DMS) | 10j-yield **5,26%** vs 3m **4,07%** (repo `data/daily/TNX_10Y`, `IRX_3M`, 29-09) ⇒ carry +1,2%/jr; risico: rentestijging | **−0,5% / +1,0% / +1,8%** |
| **Goud** | 2025–2040-model WGC ≈ 5%/jr nominaal ([WGC via Kitco](https://www.kitco.com/news/article/2024-10-17/new-wgc-model-predicts-gold-will-provide-annual-return-5-2025-2040); **belanghebbende bron**); geen rente/dividend, cash levert 4% | GOLD_F ≈ **4.180** (repo, 29-09; uitgesplitst: sterk gestegen sinds 2024) | **−1,5% / −0,25% / +1,0%** (laag: reëel 0 + inflatie 2,5% − cash 4%) |
Aannames: USD-3m 4,07% (data); EUR-cash €STR 2,44% (data). Verschil USD/EUR-cash is een valuta- en rente-keuze van Sandro (hedged ⇒ renteverschil).

## 2. Blootstelling van P-ETF-a (aanname; **Uitvoerder-1 moet de werkelijke gemiddelde exposures leveren**)
P-ETF-a = 1/σ-weging van C52 lang (SPY 0,25 · 10j-obligatie 0,52 · goud 0,20 van de sleeve) en C02 (5 aandelenindices, long/cash). Mijn benadering (sleeve-weging ≈ 60/40, C02 gemiddeld ≈ 75% belegd): **aandelen ≈ 0,45 · obligaties ≈ 0,31 · goud ≈ 0,12 · cash-rest ≈ 0,12** van het kapitaal.
## 3. Uitkomst (80k, ongehefeld)
| Scenario | excess/jr | alfa boven cash €/mnd | + EUR-cash €163 = totaal | na box 3 (≈ −€37, onbevestigd) |
|---|---|---|---|---|
| Laag | 0,45×0 + 0,31×(−0,5) + 0,12×(−1,5) = **−0,34%** | ≈ −€22 | ≈ €141 | ≈ €104 |
| Midden | 0,45×2,0 + 0,31×1,0 + 0,12×(−0,25) = **+1,18%** | ≈ €79 | ≈ €242 | ≈ €205 |
| Hoog | 0,45×4,3 + 0,31×1,8 + 0,12×1,0 = **+2,61%** | ≈ €174 | ≈ €337 | ≈ €300 |
**Gehefeld (P-ETF-b, 1,6×, rf + 1,5% op 0,6 geleend ⇒ −0,9%/jr):** midden 1,18×1,6 − 0,9 = +0,99% ≈ **€66** (*lager* dan ongehefeld); hoog 2,61×1,6 − 0,9 = 3,28% ≈ €219; laag negatief. **Regel:** hefboom loont pas als excess per eenheid > 1,5% (de opslag).
## 4. Vergelijking met de backtest
Backtest 2001–24: alfa 5,7%/jr ≈ €380/mnd. Uit de QA-decompositie (C52 lang, contributies/gewicht, *benaderend*): gerealiseerde excess per eenheid ≈ **aandelen +9%, obligaties +3,9%, goud +11%**, tegen forward-midden **+2,0 / +1,0 / −0,25%**. Het verschil (≈ 4,5 procentpunt alfa ≈ €300/mnd) is **gerealiseerde bull-premie**, niet structuur. **Wat wél structuur is:** (a) DD-reductie (maxDD 11% vs 31% 60/40 in ontdekking; repliceert cross-market, run 5: DD-effect is filtermechanica), (b) 1/σ-weging/vol-target die bij gelijk excess per risico het risico verlaagt, (c) geen alfa (run 5: nul-kalibratie p 0,46). Het structurele rendement-verbeterend deel is dus klein; het structurele *risico*-deel is reëel.
## 5. Wat hieruit volgt (voor CEO/Sandro, niet aan mij om te beslissen)
1. Premie-gebaseerd ligt totaal **≈ €140–340, midden ≈ €240** (na box 3 ≈ €205): **onder €400–500**; alfa boven cash is midden ≈ **€79/mnd**. Dat moet als tussenresultaat naar Sandro (geen fout van het team, wel een andere boodschap dan de backtest).
2. **Cash alleen** levert EUR ≈ €163/mnd (USD-fonds ≈ €270, met valuta-risico). Het project moet dus de extra €/mnd-verwachting boven cash (€79 midden) afwegen tegen risico en kosten (13 bp/TER/box 3/tijd).
3. Wat het getal zou veranderen: (i) waarderingsherstel of hogere premies (hoog-scenario), (ii) echte diversifiers met positief excess (ontbreken), (iii) hefboom alleen bij excess/eenheid > 1,5%, (iv) rente-daling (cash-deel daalt, obligatie-deel stijgt) — en **niet** tuning op de 2001–24-backtest.
## 6. Onzekerheden
Composite exposures zijn geschat; CAPE/ERP zijn gemiddelden met brede spreiding (10-jr-verwachtingen hebben SE ≈ 2–3%/jr); goud-bron belanghebbend; 2026-rente en 10y-yield uit Yahoo-data; EUR/USD en hedgekosten niet doorgerekend; box 3 onbevestigd.
## 7. Aanvragen (geen trial)
Uitvoerder-1/2: (1) gemiddelde exposures P-ETF-a (per activaklasse, 2001–24 en 2021–24); (2) gerealiseerde excess per activaklasse per decennium naast mijn forward-scenario's; (3) herbereken §3 met echte exposures en een Monte-Carlo met scenario's (steekproef uit premie-verdelingen, SE 2–3%/jr) → p(totaal ≥ €400).
