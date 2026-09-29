# PREREG C7 — ONTWERP (niet uitgevoerd): FTMO-EV met MT5-realisme (2026-09-29)

**Status: alleen ontwerp. Niets hiervan is in MT5 gedraaid. Sandro beslist of dit wordt uitgevoerd.**

## Wat getest zou worden
1. Kandidaat: de C4-combinatie RSI(2) (gepoold, 6 indices/goud) + ORB (7 FTMO-symbolen), gewichten en schaal
   vooraf vastgezet op 2021-09..2023 (RSI 0,62 / ORB 0,38, schaal 3,90), als één MT5-EA of twee EA's op één account.
   Nul-edge-controle: dezelfde EA met willekeurige in-/uitstapmomenten (zelfde aantal trades, houdduur, grootte).
2. Realisme dat de Python-tool mist:
   - equity per tick/M1 (intraday-dips) i.p.v. slot-tot-slot;
   - dagverlies volgens FTMO: equity < balance om 00:00 CE(S)T − 5% van het startkapitaal;
   - echte FTMO-swaps per symbool (incl. drievoudige swap), echte spread/commissie, FTMO-servertijd;
   - ≥ 4 handelsdagen; FTMO-nieuwsvenster (±2 min rond aangewezen nieuws geen orders, ook geen SL/TP);
   - Standard-account: geen posities over weekend/rollover > 2 u → RSI(2)-sleeve vereist **Swing-account**
     (of weekend-sluiting, wat de strategie verandert).
3. Output: dag-equityreeks uit MT5 → `ftmo_economics.py` (P(fase 1), P(funded), live-breuk, €/mnd | funded,
   EV/poging, break-even fee), naast de nul-edge-controle.
4. Beslisregel (voorstel): EV/poging > 0 én > nul-edge-controle + 2 SE, P(live-breuk 12 mnd) < 30%,
   en MT5-Sharpe ≥ 1,0 op 2024–2026 met ongewijzigde parameters.

## Verwachtingswaarde-tabel (Python, slot-tot-slot, OPTIMISTISCH) — `C7_ev_tabel.csv`
| Reeks (schaal 1) | Funded | €/mnd \| funded | EV/poging | Nul-drift-controle EV |
|---|---|---|---|---|
| C4-combinatie (schaal zoals C4, 2021–26, in-sample) | 89,8% | €808 | €8.640 | €524 |
| RSI(2) gepoold (B2b, 1990–2026) | 18,2% | €215 | €24 | −€510 |
| SPY @ 10% vol (referentie) | 59,5% | €467 | €3.092 | €219 |
Fee €540 aangenomen (niet geverifieerd). De C4-rij rust op 5,2 jaar met in-sample gewichten/schaal en een
uitzonderlijk 2022; verwacht in MT5 duidelijk lagere cijfers.

## FTMO-voorwaarde-risico's (bronnen: ftmo.com FAQ/forbidden-trading-practices, 29-09-2026; te verifiëren)
1. **Weekend/rollover (Standard FTMO Account):** posities sluiten vóór het weekend en bij rollover > 2 u →
   RSI(2) (houdt dagen, ook over het weekend) past alleen op een **Swing-account**.
2. **Nieuwsvenster:** op aangewezen instrumenten geen openen/sluiten (incl. SL/TP) van 2 min vóór tot 2 min na
   geselecteerd nieuws → ORB-stops en US-open-trades kunnen hierop botsen (bv. 10:00 ET-releases).
3. **'Gap trading' / handelen vlak vóór marktsluiting** staat op de lijst verboden praktijken.
4. **'Inconsistent position sizing' en 'risk concentration'** (gecorreleerde symbolen) — relevant voor de
   gelijktijdige index-legs van RSI(2) (SPX/NDX/DAX/FTSE/N225 sterk gecorreleerd).
5. **'Unfair advantage tools'** — de samenvatting noemt o.a. AI/ultrasnelle software; exacte tekst verifiëren.
   Een zelf ontworpen regel-EA is waarschijnlijk toegestaan, maar dit moet Sandro nagaan.
6. **Derde-partij-EA / max. kapitaalallocatie:** eigen EA, dus laag risico.
7. **Best Day Rule / 'profit distribution'** bestaat; exacte drempel niet gevonden — nagaan in Trading Objectives.
8. **Server-limieten:** 200 open orders, 2.000 posities/dag — ruim voldoende.
9. **Loterijconstructie:** EV > 0 zonder edge (nul-drift-controle) is optiewaarde, geen vaardigheid; FTMO
   kan 'niet-realistisch' gedrag afwijzen. Niet opschalen op basis van EV alleen.
