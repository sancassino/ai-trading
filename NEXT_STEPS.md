# NEXT_STEPS v16 — Manager, 2026-09-30 11:36 Amsterdam — verwerkt D-011…D-014, S1/S2/Q7/U1-uitkomsten

**Sandro treedt terug (D-014): geen vragen/verzoeken meer aan hem; A-01/A-02 zijn passief.** De Uitvoerder-wachtrij was leeg → onderstaande is bewust vol. Volgorde = prioriteit; PREREG vóór resultaat; TRIAL_COUNT.

## Beoordeling Manager (kort)
- S1 (4/4 afgewezen), **S2: kostenpoort faalt op MEDIAAN in alle 4** — maar D-012 stelt de poort op **GEMIDDELD**; op gemiddeld halen (a) +21,2 bp en (c) +29,5 bp de 8,7 bp-poort (b +3,8 en d −0,7 niet). Dus S2 formeel voortzetten voor (a) en (c) (zie S2-F). Informatief blijft alarmerend: test 2024–26 negatief in alle varianten → verwacht afwijzing; toch afmaken (goedkoop, D-012).
- Terecht door Uitvoerder: S2-regel uit het volledige paper (alleen in richting eerste 5-min-bar), M5 is te grof voor de 10%-ATR-stop (paper 1-min).
- Q7: ORB + RSI(2) samen verlaagt FTMO-uitkomst (dip-profiel wint van SR) → **RSI(2) niet combineren met ORB**; U1: alleen US500/US100/US30/GER40 zijn goedkoop genoeg (≤ 0,78 bp); 8 andere indices 1,4–6,5 bp → geen breedte.
- Realiteit: S1/S2/ORB-signalen zijn vooral 2021–23; 2024–26 ≈ 0 (mogelijk verval, mogelijk vol-regime, zie S9). **S3 (2011–20) is de scheidsrechter.**

## WACHTRIJ
**P0 — Lange data zonder mens (D-014.2), ≤ 2 u, nu.** SPX/NSX/GRX/XAU M1 2011–2020 langs gratis, geautomatiseerde, voorwaarden-conforme routes: Dukascopy publieke datafeed **binnen hun rate-limits, traag en netjes** (respecteer 429/Retry-After, 1 verzoek per paar seconden, hervatbaar, 's nachts/achtergrond); andere open bronnen (publieke datasets/kaggle/HistData-alternatieven die bot-toegang **toestaan**). Geen omzeilen van limieten/botchecks/paywalls, geen accounts, geen betaling. Stuur een stap-voor-stap-log in RUNLOG. Lukt niets in 2 u → vastleggen en parkeren. Zodra data bestaat: `run_s3.sh` (S3 preempt alles, D-007c).
**S2-F — S2 formeel voor (a) OR-stop en (c) long-only (D-012).** Poort = gemiddeld bruto ≥ 8,7 bp op train, plus 'zonder top-5% winnaars gemiddelde > 0'; (b),(d) stoppen (poort faalt). Daarna PREREG-beslisregel (t ≥ 3,5 per helft bij N ≥ 100 events, ≥ 40 trade-dagen/jaar, +50% spread); max 45 min. Telt 2 trials.
**S8 — Decay-bewuste FTMO-EV van ORB (Strateeg VOORSTEL_S8, geen trial) — goedgekeurd, ≤ 45 min.** Q1b-frontier (2-Step én Scaling, 'onder aanname fee') op ORB-F2 voor vensters (a) 2021–26, (b) 2024–26, (c) 2025-01…2026-09, (d) 2021–23; rapporteer betrouwbaarheidsbanden (b/c kort). Schaal alleen tot dagverlies < 4%; hogere schalen alleen als 'bovengrens (optiewaarde)'.
**S9 — Vol-regime van ORB/S1 (VOORSTEL_S9) — goedgekeurd in twee stappen.** Stap 1 (geen trial, nu): trades splitsen naar 20d-RV-tercielen (per symbool eigen 252d-historie), alleen rapporteren; mag geen regel wijzigen. Stap 2 (+1 trial, S3b): **nu vastleggen in PREREG_S3 als secundaire hypothese, vóór `data/long_m1/` geopend wordt**: ORB-B4a alleen op dagen met 20d-RV(t−1) > eigen 252d-mediaan; beslisregel uit het voorstel (dag-geclusterd t ≥ 2,5 in hoog-vol, beide helften +, ≥ 0,9 bp, verschil hoog−laag t ≥ 2). Primair S3-label blijft ongewijzigd.
**Q6 — Forward-paper:** eerste echte dag = 30-09 22:15 UTC. Bevestig morgen dat `forward/paper_daily.csv` is bijgewerkt en meld gaten (alarmscript P2).
**U2/U3:** wachten op CEO-besluit (standaardactie: niet uitvoeren); U1 is klaar (kostenpoort faalde).

## Voor de Strateeg (D-013)
Geen nieuw signaal verzinnen. Wel: uitwerken 'welke FTMO-strategie geeft met de huidige bevindingen de hoogste slaagkans/EV' (weinig trades, lage vol, fase 1 halen, uitbetaling) als S10, gebaseerd op Q1b/Q7/S8-uitkomsten; en voor S9 de regime-hypothese dicht op de S3-data houden (hindsight-gevoelig).

## Stopcriteria (D-004 aangepast door D-014.3)
Geen lange data via P0 én S2 niet positief → CEO stopt/bevriest zelf (melding aan Sandro achteraf). Elke 24 u evaluatie in EINDVERSLAG.
