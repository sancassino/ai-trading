# PREREG_S2_GER40_OPEN — GER40 Frankfurt Open-Drive Continuation (2026-09-30)

**Status:** Pre-registration. Auteur: Strateeg-2.  
**Branch:** `grok/strateeg-2` · **Niet in catalogus** (A1 ORB = US/multi cash-open incl. GER40 als deel van B4a; dit is **alleen GER40**, Frankfurt 09:00-drive, exit vóór US cash — andere window + single-asset).

## 1. Exacte regel

**Instrument:** `GER40.cash` (FTMO Cash CFD).  
**Pre-range:** hoog/laag van 08:00–09:00 Europe/Amsterdam (pre-open / auction window op M5).  
**Entry-venster:** 09:00–09:30.  
**Long:** eerste M5-slot ≥ 09:00 die boven pre-range high sluit; entry op die bar-close.  
**Short:** eerste M5-slot die onder pre-range low sluit; entry op die bar-close.  
**Geen trade** als beide kanten binnen 09:00–09:30 worden geraakt (two-way = skip).  
**Stop:** terug voorbij pre-range mid ( (high+low)/2 ) óf 1,0× ATR(14,D1) — **strenger van de twee** (vooraf vast).  
**Exit:** hard flat 15:15 Europe/Amsterdam (vóór US cash open 15:30) — **swap = 0**.  
**Sizing:** 0,75% risico per trade.  
**Filter:** DAX-futures proxy of GER40: vorige dag close > SMA(20,D1) → alleen long toegestaan; < SMA(20) → alleen short; geen tegen-trend open-drives.

## 2. Mechanisme

Europese equity-open absorbeert overnight news in de eerste halfuur. Continuation van de open-drive (niet mean-reversion) vangt institutionele herpositionering in lokale sessie. Exit vóór US open beperkt gap-/beta-shock van NY. Positief scheef: asymmetrische payoff (vaste invalidatie vs. sessielengte tot 15:15). Verschil met A1: geen US500/US100/XAU multi-ORB; geen 15:30 US-open range.

## 3. Instrument / dataset

| Item | Waarde |
|------|--------|
| FTMO-symbool | GER40.cash |
| Kosten | roundtrip_intraday ≈ 0,72 bp (COSTS_FTMO.csv GER40cash); swap 0 |
| Ontdekking | M5 GER40/FTMO of cash-index proxy 2012–2024-12-31 |
| Reserve-OOS | 2025-01→ onaangeraakt tot shortlist |
| Feestdagen | Duitse/EU feestdagen zonder cash-sessie uitsluiten |

## 4. Kostenpoort

Bruto mean ≥ 2× 0,72 bp; **kosten < 50% bruto**. +50% spread-stress. Fail → geen trial.

## 5. Beslisregel

1. Dag-geclusterde t ≥ **2,0**.  
2. Kosten < 50% bruto.  
3. Skew > 0 of max dagdip ≤ −1,5% bij 0,75% risk.  
4. FTMO-EV via `engine/ftmo.py` ≥ **€150/poging netto**.  
5. Rapportage apart: alleen-long vs alleen-short helften (beide moeten t>0 richting; gepoolde t≥2,0).  
6. Correlatie met A1 multi-ORB: \|ρ\| > 0,7 → "overlap-sleeve", geen aparte shortlist-plaats tenzij Δ FTMO-EV > €50.

## 6. Verwachte uitkomst / falen

**Verwacht:** werkt vooral in trendregimes (SMA-filter); faalt in choppy EU mornings.  
**Falen:** t < 2; kostenpoort; FTMO-EV < €150; of short-helft systematisch negatief (one-sided artefact).

## 7. Constraints

Geen post-hoc range-lengte tuning. Geen 2025+ peek. Geen real money.
