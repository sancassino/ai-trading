# PREREG_S2_USOIL_EIA — USOIL EIA Inventory Window Breakout (2026-09-30)

**Status:** Pre-registration. Auteur: Strateeg-2.  
**Branch:** `grok/strateeg-2` · **Niet in catalogus** (geen EIA/olie-event sleeve in A/B-tier; A1 is index/XAU ORB, niet weekly inventory).

## 1. Exacte regel

**Instrument:** `USOIL.cash` (FTMO WTI Cash CFD).  
**Event:** EIA Weekly Petroleum Status Report — woensdag (of officiële uitsteldatum), publicatie ~10:30 America/New_York (= 16:30 Europe/Amsterdam winter / 15:30 zomer; gebruik **exacte EIA-timestamp** uit kalenderbestand).  
**Pre-range:** hoog/laag van de 20 minuten vóór release (M1 of M5).  
**Entry:** binnen 2 minuten na release, long als mid > range_high, short als mid < range_low; anders flat (geen trade).  
**Stop:** 1,25× pre-range breedte vanaf entry (vast).  
**Take-profit:** 2,0× pre-range breedte (R:R 1:1,6 t.o.v. stopafstand) óf time-stop.  
**Time-stop / flat:** uiterlijk 90 minuten na release of 18:30 Europe/Amsterdam — **zelfde dag, swap = 0**.  
**Sizing:** 0,5% risico (olie gap/spread hoger).  
**Filter:** alleen als pre-range breedte ∈ [0,15%, 0,80%] van prijs (te krap = noise; te wijd = al geprijsd). Geen richtingsbias uit inventory-surveys (voorkomt lookahead op “expected”).

## 2. Mechanisme

EIA-print is een herhaalde, geplande liquiditeitsschok in WTI: inventory surprise herprijst spot binnen minuten. Breakout van de pre-release range is een event-microstructuurregel, niet een sessie-ORB. Dagelijks-vlak vermijdt USOIL overnight swap (long swap meevaller, short swap zwaar in COSTS_FTMO — intraday elimineert beide). Positief scheef door TP > stop in R-units en harde time-stop (beperkt loser-staart).

## 3. Instrument / dataset

| Item | Waarde |
|------|--------|
| FTMO-symbool | USOIL.cash |
| Kosten | roundtrip_intraday ≈ 3,34 bp (hoog); poort dus strenger |
| Kalender | EIA-release datums 2015–2024 vooraf vastgelegd (`eia_dates` of handmatige lijst in PREREG-bijlage bij implementatie) |
| Prijsdata | M1/M5 WTI 2015–2024-12-31 (FTMO of Dukascopy) |
| Reserve-OOS | 2025-01→ onaangeraakt |
| N events ontdekking | ≈ 500 wekelijkse prints → power oké voor cluster-t op weekniveau |

## 4. Kostenpoort

Door hogere spread: bruto mean ≥ 3× 3,34 bp **én** kosten < 50% bruto. Fail → geen trial (waarschijnlijk struikelpunt — dan hypothese dood zonder FDR-belasting).

## 5. Beslisregel

1. Week-geclusterde t (één obs per EIA-event) ≥ **2,0**.  
2. Kosten < 50% bruto.  
3. Skew van event-P&L > 0; worst single-event loss ≤ −1,5% equity bij 0,5% risk.  
4. FTMO-EV ≥ **€150/poging** via `engine/ftmo.py` (lage trade-frequentie ≈ 1/week → EV moet per funded-maand nog kloppen; rapporteer ook E[€/mnd] bij 1 trade/week).  
5. **Extra:** split pre-2020 vs 2020–2024; beide t > 0 vereist (COVID-olie regime-check).

## 6. Verwachte uitkomst / falen

**Verwacht:** kostenpoort is de hoofdadversary; als bruto edge < ~10 bp/event sterft de regel eerlijk.  
**Succes:** t≥2, kosten<50%, FTMO-EV≥€150, stabiel over beide deelsamples.  
**Falen:** kostenpoort; of alleen COVID-subsample drijft t; of dagdip > 2% bij gaps.

## 7. Constraints

Geen gebruik van inventory “consensus” of API-surprise na zien van P&L. Geen 2025+. Geen real money. Kalenderfout = implementatiefout, geen hertuning van range.
