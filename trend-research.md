# Trend-following op indices/cross-asset — eerste bevindingen (24 sep 2026)

Status: Python/Yahoo-onderzoek, NOG NIET gevalideerd met echte MT5/FTMO-data.
Blocker: SSH naar de VM (34.70.160.155:22) is geblokkeerd op omgevingsniveau
van deze cloud-sessie (raw TCP timeout, los van tooling) — actie nodig van
Sandro: sessie-titelbalk → cloud-omgeving-menu → Edit → Network access →
host toevoegen. Zodra dat open staat kan alles hieronder op de FTMO Strategy
Tester geverifieerd worden, wat volgens de eigen regel uit het
overdrachtsdocument verplicht is voordat we iets vertrouwen.

## Waarom deze richting

Overdrachtsdocument concludeerde: kortetermijn mean-reversion op edelmetalen
(Variant I) heeft geen aantoonbare edge over 20+ jaar — winst zat vrijwel
volledig in 2024-2026. Aanbevolen vervolgrichting: trend-volgend op
instrumenten met structurele langetermijndrift (indices). Dat is hier
opgepakt.

## Methode

- Data: Yahoo Finance, dagkoersen. SP500 (1960-), Nasdaq (1971-), DAX (1988-),
  Dow (1992-), plus Gold/Bonds10Y/Crude futures continuous contracts (2000-)
  voor cross-asset diversificatie.
- Strategie: long-only trend-volgend. Entry als close > SMA(200), ATR-based
  trailing stop (3x ATR(20)), exit bij trendbreuk of stop. Positiegrootte:
  vast % van kapitaal risico per trade (risk_pct), stop-afstand-gebaseerd.
- Robuustheidscheck: parametergrid (trend_period 100-250, ATR-mult 2-4) —
  geen cliff-edge gevoeligheid, monotoon risk/return-gedrag. Geen teken van
  overfitting (vgl. document sectie 4: "beter naarmate je een parameter
  losser zet zonder meer risico" = verdacht — hier NIET het geval, meer
  risico geeft consistent meer DD).

## Kernresultaat 1: edge bestaat, en is structureel anders dan mean-reversion

| Index | Jaren getest | % positief | Periode |
|---|---|---|---|
| SP500 | 63 | 70% | 1960-2026 |
| Nasdaq | 54 | 78% | 1971-2026 |
| DAX | 38 | 61% | 1988-2026 |
| Dow | 35 | 66% | 1992-2026 |

Dit is fundamenteel anders dan goud (16/18 jaar verlies bij zilver, winst bij
goud vrijwel alleen 2024-2026). Consistent over decennia, robuust over
parameters.

## Kernresultaat 2: DD-limiet is de bottleneck, niet de edge

Zelfde les als GER30 in het overdrachtsdocument: positiegrootte opschalen
naar €1-2k/maand-niveau rendement duwt de (trailing) drawdown ver over
FTMO's limiet heen, op één instrument én op een gecorreleerde multi-index-mix
(SP500+Nasdaq+DAX+Dow correleren te sterk tijdens crashes — geen echte
diversificatie, zelfde valkuil als goud+zilver).

Cross-asset mix (indices + goud + 10Y bonds + ruwe olie, 2000-2026, 27 jaar,
19/27 jaar positief) geeft wél een merkbaar betere trade-off:

| risk per instrument | CAGR | laagste equity ooit t.o.v. $100k start | gem. $/maand |
|---|---|---|---|
| 0,5% | 4,3% | -2,0% | $662 |
| 0,75% | 6,4% | -3,0% | $1.341 |
| 1,0% | 8,4% | -4,0% | $2.422 |
| 1,25% | 10,4% | -5,0% | $4.095 |

Let op: FTMO's max-drawdown-regel is **statisch** (10% onder startkapitaal,
geen trailing peak) — dat is gunstiger dan eerdere berekeningen aannamen.

## Kernresultaat 3: Monte Carlo (block-bootstrap, FTMO-regels)

Zelfde methode als het overdrachtsdocument (bootstrap van échte jaarblokken,
niet losse dagen), nu met binnen-jaar maandelijkse stappen zodat intra-jaar
drawdown-doorbraken zichtbaar worden:

| risk/instrument | Fase 1 slaagt | Funded | Live ≥$1k/mnd, 12mnd |
|---|---|---|---|
| 0,5% | 88,6% | 84,9% | 12,8% |
| 0,75% | 84,8% | 77,5% | **51,7%** |
| 1,0% | 84,7% | 73,6% | **64,2%** |
| 1,25% | 84,0% | 72,3% | 67,4% |

Ter vergelijking, oude mean-reversion-resultaat (100% goud, echte FTMO-data):
funded ~30%, live ≥$1k/mnd 12mnd ~1%. Dit is dus een orde van grootte beter.

## Beperkingen van dit resultaat (waarom dit NOG GEEN besluit is)

1. **Yahoo-data, geen FTMO-broker-data.** Document sectie 4: Python/Yahoo-sim
   was voor goud 6,8x te laag en voor zilver zelfs kwalitatief fout t.o.v.
   echte MT5-uitkomst. Dezelfde onzekerheid geldt hier — richting is
   waarschijnlijk correct (trendvolgen op indices is een bekend, breed
   gepubliceerd fenomeen), exacte cijfers zijn dat niet per se.
2. **Futures-continuous-contracts (Gold/Bonds/Crude) op Yahoo hebben
   bekende roll-datamankementen** (sprongen bij contractwissel) — kan ruis
   toevoegen die met echte CFD-data op FTMO niet optreedt.
3. **Monte Carlo is maand-granulariteit, geen tick-niveau.** Onderschat
   waarschijnlijk intra-maand drawdown-risico enigszins.
4. **Nog niet gecheckt tegen FTMO's exacte symbolenlijst** — welke van deze
   instrumenten (indices, goud, bonds, olie) daadwerkelijk verhandelbaar
   zijn op dit FTMO-account, met welke spread/swap. `SymbolListerEA.mq5`
   stond hiervoor al klaar op de VM (zie overdrachtsdocument sectie 5),
   resultaat nooit opgehaald.
5. **Risico per trade (0,75-1% van kapitaal) zit ruim onder FTMO's
   3%-max-risico-per-trade-regel** — geen probleem, ruimte over.

## Status 24 sep 2026 (vervolgsessie)

Nieuwe sessie kon de VM niet bereiken: SSH (poort 22) en de TLS-relay
(poort 443 via `34.70.160.155.nip.io`) timen allebei uit op
environment-netwerkniveau, ook al claimt het overdrachtsdocument dat de
nip.io-host al was toegevoegd. Yahoo Finance is in déze sessie eveneens
geblokkeerd (proxy 403) — dus zelfs het Python/Yahoo-onderzoek kon niet
verder uitgebreid worden. Actie vereist van Sandro: sessie-titelbalk →
cloud-omgeving-menu → Edit → Network access → `34.70.160.155.nip.io`
(opnieuw) toevoegen, en de sessie verifieert dit dan als eerste stap.

Wel gedaan zonder netwerktoegang: `TrendFollow_CrossAsset.mq5` geschreven
(long-only, SMA200 trendfilter + ATR-trailing-stop, risk-% positiesizing,
`_Symbol`-onafhankelijk zodat één EA op elk instrument in de cross-asset
mix gedraaid kan worden). Nog NIET gecompileerd of getest — dat vereist
`metaeditor64.exe` op de VM, dus wacht op netwerktoegang.

**Volgende stappen zodra VM bereikbaar is** (in volgorde):
1. Verbinding verifiëren (`whoami`).
2. `SymbolListerEA`-resultaat ophalen (`SymbolList_FTMO.csv`, zie
   overdrachtsdocument sectie 5) om te bevestigen welke indices/bonds/olie
   daadwerkelijk verhandelbaar zijn op dit FTMO-account, met welke
   spread/swap — dit bepaalt of de cross-asset mix hierboven zo haalbaar is.
3. `TrendFollow_CrossAsset.mq5` compileren, los per instrument in de
   Strategy Tester draaien op FTMO's echte data (net als Variant I eerder),
   jaar-voor-jaar cijfers vastleggen zoals in het overdrachtsdocument.
4. Cross-asset combinatie (indices + goud + bonds + olie) valideren met
   echte data, Monte Carlo herhalen met échte trades i.p.v. Yahoo-simulatie.
5. Pas dan een besluit nemen — dezelfde regel als bij Variant I: geen
   Python-cijfer vertrouwen totdat MT5 het bevestigt.
