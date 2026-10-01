# Eindstand FTMO-onderzoek (tussenstand — D-094 FREEZE OFF; bijgewerkt 2026-10-01 ~09:28)

**Conclusie:** nog geen sleeve met een **gevalideerde** na-kosten edge (formele t + reserve). Evaluatie (€540) **NIET kopen** op basis van wat er nu ligt. Zoeken gaat door (D-094); alleen Sandro beslist over stoppen/aankoop.

## Cijfers
- **TRIAL_COUNT = 448** (P1 ORB+BTC reserve one-shot FAIL, CTO C-020 / D-096).
- P1: day-clust t≈0,24; ann SR≈0,20; BTC-leg mean <0 op reserve 2025→ — P1 dood; reserve voor P1 verbruikt.
- Pre-screen PASS → PREREG pending formal U2: **N35, N36, N40, N41** + S2 **GBPJPY_EU_MOM**.
- C17/FX_INTRADAG/B1/A2 en N1–N34/N37–N39/N42 STOP of pre-screen FAIL; N43 underpowered (geen PREREG).
- Engine `engine/ftmo.py` onafhankelijk gevalideerd (Auditor). Integriteit: PREREG vóór resultaat, TRIALS append-only, geen 2025+ buiten CEO-vrijgave.

## Wat kan heropenen / doorloopt
1. U2 formal gates op N35/N36/N40/N41 + GBPJPY (geen evaluatie-advies tot PASS + Auditor).
2. Lange M1-data via HistData (SANDRO_ACTIES / M-001) voor A1-ORB.
3. Nieuwe pre-screens (N44–N45 OPEN); D-094 tracks 2+4.
4. Definitief stoppen — alleen Sandro.

Agents openen of kopen nooit iets. `EINDSTAND_FTMO.md` = tussenstand, geen einde (D-094).
