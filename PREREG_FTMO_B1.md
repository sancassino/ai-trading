# PREREG FTMO-B1 — TSMOM-mix op FX (stub) — 2026-09-30

**Status:** STUB — onvoldoende bevroren specs voor een trial. Geen run tot OPEN-punten dicht zijn.  
**Tier:** B1 (STRATEGIE_CATALOGUS §9).  
**Basisregel (referentie, niet automatisch overgenomen):** `PREREG_CAT1.md` C05 — positie = gemiddelde teken(21d, 63d, 252d) × 0,10/σ60 (cap 3), maandeinde.

## 1. Hypothese (richting)
Multi-horizon TSMOM op FTMO-FX-majors: FX-swap ≈ renteverschil/carry; trendfilter kan drag beperken. Positief-scheef verwacht; omloop laag (maand).

## 2. OPEN (blokkeert freeze)
1. **Universum:** welke paren? Kandidaat-lijst uit CAT1-U12 FX: EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF (NZDUSD viel af op kosten 1,85 bp in CAT1). Bevestig tegen actuele `COSTS_FTMO.csv` + tijdvariabele swaps (`data/ftmo_specs/`).
2. **Swap vs carry:** per paar long/short swap (bp/nacht) vs 3m-renteverschil — tabel **vóór** run; schrap paren waar \|swap\| systematisch carry opeet zonder trend-edge.
3. **Signaaldata:** FRED noon FX (lange historie) vs FTMO D1 (korte, echte spreads). Primair pad? (Voorstel tot besluit: ontdekking op FRED-proxy + FTMO-kostenmodel; bevestiging op FTMO D1 2021–24 — twee stappen, één trial-label alleen op FTMO-stap.)
4. **Sizing:** 10%/σ60 zoals C05 of FTMO-dagverlies-bounded (≤ 2% p95)? Voor FTMO-EV is dagverlies-bound bindend.
5. **Beslisdrempels FTMO-EV:** kopieer A4-drempels of lager (B-tier)? Manager/CEO.
6. **Relatie C12:** B2 is carry+trend; voorkom dubbele family zonder vooraf gezegd verschil (B1 = pure TSMOM-mix; B2 = carry-primary).

## 3. Voorlopige (niet-bevroren) schets — NIET uitvoeren
- Maandeinde herweging; long/short per pair volgens C05-mix; equal-risk over pairs die meedoen.
- Kosten: `COSTS_FTMO.csv` rondreis bij herweging + swap elke kalendernacht (long/short apart; vrijdag 3×).
- Ontdekking ≤ 2024-12-31; reserve 2025→ dicht.
- Poort: bruto ≥ 3× (spread + swap over hold); anders STOP.

## 4. Wat wél al vastligt uit repo (geen inventie)
- C05-definitie in `PREREG_CAT1.md` (regels + U12).
- Gemeten FX-rondreis: EURUSD 0,63 / GBPUSD 0,70 / USDJPY 0,78 bp (`COSTS_FTMO.csv`).
- Swaps zijn tijdvariabel (RUNLOG: US500 long −4,95%→−7,47%/jr binnen één dag) → constante-swap-model = benadering; +50% gevoeligheid verplicht.

## 5. Volgende stap
Strateeg of Uitvoerder-1: swap-vs-carry-tabel voor U12-FX uit laatste `data/ftmo_specs/` snapshot + FRED 3m-rentes → dan dit stub upgraden tot volledige PREREG (zelfde secties als A4/A5).

---
**Aangemaakt:** 2026-09-30 21:41 CEST — D-090 re-kickoff.  
**Auteur:** Strateeg (`claude/trusting-faraday-34tsmg`)
