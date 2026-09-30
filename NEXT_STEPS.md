# NEXT_STEPS v17 — Manager, 2026-09-30 12:07 Amsterdam — verwerkt D-015…D-018, S2/S8/S9/U2/U3-uitkomsten

Sandro is teruggetreden (D-014): geen vragen aan hem. Alles hieronder is zelfstandig uitvoerbaar. PREREG vóór resultaat; TRIAL_COUNT (nu 414).

## Beoordeling Manager
- **Goed werk, scherpe vondsten:** S2 (poort + staartvoorwaarde → STOP), S9-stap 1 (vol-regime verklaart de edge niet), U3 (FX-ORB kostenpoort faalt), en vooral **dag-geclusterde t van ORB 2021–26 = 1,81** (train 1,67, test 0,81) i.p.v. per-trade 2,93 — het eerdere bewijs was overschat. Dit raakt óók andere kernresultaten (zie N7).
- **S8:** binnen FTMO-conforme schaal ≈ €150–300/mnd (P(netto<0) 25–50%), ver onder doel. **U2 (€1.095/mnd) is géén kandidaat-uitkomst:** ± €388 daarvan is optiewaarde (nul-drift), risico-sizing geeft ≈ 35% jaarvol, en het hangt aan een onbevestigde edge. Nooit als kop-cijfer gebruiken; S10-kader (G5) eist bovendien vaste notional × schaal — sizing-afwijking expliciet labelen.
- **Stand:** alle signalen na 2023 ≈ 0; alles hangt aan S3 ('bevestigd + blijvend', CEO: ≈ 10–15%). S3-beslisregel heeft te weinig power (M-009).

## WACHTRIJ (volgorde = prioriteit)
**P0 — Lange data zonder mens (loopt).** Log uiterlijk 13:36 in RUNLOG: welke conforme gratis routes geprobeerd, uitkomst per route. Zodra data bestaat: \`run_s3.sh\` (preempt alles).
**N8 — Power-analyse S3 + PREREG_S3-aanpassing (M-009, ≈ 30 min, geen trial, VÓÓR data).** Simuleer (bootstrap op dag-niveau uit de FTMO-ORB-trades, gestapeld 10 jaar) de kans op de labels onder drie werelden: H-blijvend (effect 2021–26-niveau ook 2011–20 en later), H-vervallen (effect 2011–20, ≈ 0 na 2023), H-nul. Rapporteer P('bevestigd + blijvend' / 'bevestigd maar vervallen' / 'onbeslist' / 'verworpen') per drempelset: (A) t ≥ 2,5, (B) eenzijdig t ≥ 2,0 (M-009-standaardactie). Voeg het annex toe aan PREREG_S3 en pas de drempel aan volgens M-009 (standaardactie C) **vóór** \`data/long_m1/\` wordt geopend; laat de overige eisen ongewijzigd.
**N7 — Cluster-audit van alle kernresultaten (geen trial, ≈ 45 min).** Herbereken de t-waarden **dag-geclusterd** (of dagblok-bootstrap) voor: ORB (B4a), S1(a), RSI(2) gepoold (B2b Yahoo t 3,65 — 5 gecorreleerde indices!), K1 (nachten), F3b-reeks, en de forward-set (papier). Lever \`RESULTATEN_GECLUSTERD.md\` (oude t, nieuwe t, N_dagen, effectieve N) en corrigeer TRIAL_COUNT-notes/PLAFOND waar de t sterk daalt. Doel: eerlijk beeld van wat écht overleeft.
**U2b — MT5-reconciliatie van ORB-sizing (U-003, informatief, ≈ 1 u).** Standaardactie mag doorgaan, maar rapporteer **twee** sizing-varianten naast elkaar (vaste notional 1/7 × schaal en 0,5%-risico/trade), met FTMO-dagverlies op equity, echte spread/slippage bij kleine OR, en label 'optiewaarde-aandeel' (nul-drift-controle). Geen kop-cijfer zonder dat label; geen challenge, geen echte trades.
**Q6 — Forward-paper:** eerste dag 30-09 22:15 UTC verwerkt? Meld gaten/alarm in RUNLOG (P2-script).

## Strateeg
S10 (go/no-go-kader) is goedgekeurd als beslisstructuur (G1–G6; nu **no-go**). Verwerk N7/N8-uitkomsten in het plan; **geen nieuw signaal verzinnen**.

## Stop-kader (D-004/D-014)
Geen lange data via P0 én S3 niet uitvoerbaar → CEO stopt/bevriest uiterlijk vr 3 okt 12:00 en meldt het Sandro achteraf. Manager bereidt \`STOP_RAPPORT.md\` (één pagina: wat geprobeerd, wat geleerd, wat zou waar moeten zijn) voor.
