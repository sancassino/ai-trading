# PREREG_S2_XAU_OVERLAP — XAUUSD London–NY Overlap Breakout (2026-09-30)

**Status:** Pre-registration. Auteur: Strateeg-2 (onafhankelijk van Strateeg-1).  
**Branch:** `grok/strateeg-2` · **Niet in catalogus A/B-tier** (A1=index/XAU ORB cash-open; A5=FX London-open — dit is goud in overlap-venster).

## 1. Exacte regel

**Instrument:** `XAUUSD` (FTMO Metals CFD).  
**Sessie:** London–NY overlap 14:00–17:00 Europe/Amsterdam.  
**Range:** hoog/laag van 14:00–14:30 (eerste 30 min overlap), vastgezet op 14:30.  
**Entry (long):** eerste M5-slot > range_high ná 14:30; market.  
**Entry (short):** eerste M5-slot < range_low ná 14:30; market.  
**Max 1 trade/dag;** geen herentry na stop of exit.  
**Stop:** 0,35× ATR(14, M5) van entry (vast; geen trailing).  
**Exit:** hard flat om 17:00 Europe/Amsterdam (zelfde dag) óf stop — **swap = 0**.  
**Sizing:** risico 0,75% account-equity per trade (stop-afstand → notional).  
**Filter (vooraf, 0 vrije parameters):** alleen handelen als Asia-range (00:00–08:00) < mediaan Asia-range van vorige 20 handelsdagen (compressie → expansie). Geen andere filters.

## 2. Mechanisme

Goudliquiditeit piekt in London–NY overlap; orderflow van beide sessies drijft korte impulsbewegingen. Een break van de eerste halfuur-range in de overlap is een microstructuur-breakout, niet de US cash-ORB (A1) en niet FX London-open (A5). Positief-scheef verwachtingsprofiel: vaste stop, winners mogen tot 17:00 lopen; geen overnight-staart.

## 3. Instrument / dataset

| Item | Waarde |
|------|--------|
| FTMO-symbool | XAUUSD |
| Kosten (COSTS_FTMO.csv) | roundtrip_intraday ≈ 0,83 bp; commissie 0,05 bp/kant; swap irrelevant (intraday) |
| Ontdekking | M5/FTMO of Dukascopy-proxy goud 2015–2024-12-31; geen peek in 2025-01→ |
| Reserve-OOS | 2025-01-01→ — **één blik na shortlist, nooit eerder** |
| Kalender | alleen handelsdagen met volledige overlap (geen US feestdag zonder NY-sessie) |

## 4. Kostenpoort (vóór trial)

Gemiddelde bruto per trade ≥ 2× roundtrip (0,83 bp) én **kosten < 50% bruto** op ontdekkingsset.  
+50%-spread-gevoeligheid: zelfde poort. Faalt poort → stop, **geen trial-telling**.

## 5. Beslisregel (statistiek + FTMO-EV)

1. Dag-geclusterde t (Newey–West, lags=5) op dag-P&L ≥ **2,0**.  
2. Kosten-aandeel < 50% bruto.  
3. Scheefheid dag-P&L > 0 óf max dagdip ≤ −1,5% bij gekozen sizing.  
4. Via `engine/ftmo.py`: FTMO-EV (P fase1/2, P 12m survive, E[uitbetaling] na 80% split − fee).  
5. **Drempel acceptatie:** FTMO-EV ≥ **€150/poging netto** (fee-aanname expliciet in rapport; default €540 tot Sandro bevestigt) én t≥2,0.  
6. Correlatie dagreeks met bestaande A1-ORB-dagreeks: als \|ρ\| > 0,7 → label "geen nieuwe sleeve" (informatief, geen fail van t).

## 6. Verwachte uitkomst / falen

**Verwacht:** matige hitrate, dikke rechterstaart op trend-overlapdagen; na kosten SR_dag ≈ 0,3–0,6.  
**Falen:** t < 2,0; of kosten ≥ 50% bruto; of FTMO-EV < €150; of max dagdip structureel > 2% bij 0,75%-risk (FTMO 5%-regel-risico).

## 7. Wat niet mag

Geen parameterzoektocht na resultaten. Geen 2025+ reserve tot shortlist. Geen echte orders.
