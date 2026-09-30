# PREREG_S2_USDJPY_HANDOFF — USDJPY Tokyo-Range London-Handoff Breakout (2026-09-30)

**Status:** Pre-registration. Auteur: Strateeg-2.  
**Branch:** `grok/strateeg-2` · **Niet in catalogus A/B-tier** (A5/U3 = London-open ORB op EUR/GBP; GS02 = Asian-range *fade* EUR/GBP; B1 dood overnight TSMOM — dit is **USDJPY-only**, Tokyo-range **continuation** bij London-handoff, intraday-flat).

## 1. Exacte regel

**Instrument:** `USDJPY` (FTMO Forex).  
**Tokyo-range (TR):** hoog/laag van alle M5-bars met open-timestamp in **[00:00, 08:00) Europe/Amsterdam** (Asia/Tokyo cash-achtige liquiditeitspoort in server-/EU-tijd; vaste Amsterdam-klok, geen aparte Tokyo-DST-mapping).  
**Entry-venster:** 09:00–10:30 Europe/Amsterdam (London open + eerste 90 min handoff).  
**Long:** eerste M5-slot ≥ 09:00 die **boven TR_high sluit**; entry op die bar-close.  
**Short:** eerste M5-slot die **onder TR_low sluit**; entry op die bar-close.  
**Geen trade** als (a) beide kanten binnen 09:00–10:30 worden geraakt (two-way = skip), of (b) TR-breedte ∉ [0,08%, 0,60%] van mid (te krap = noise; te wijd = al uitgeprijsd), of (c) geen close-break vóór 10:30.  
**Stop:** terug voorbij TR mid `((high+low)/2)` — vast; geen trailing.  
**Exit:** hard flat **16:00 Europe/Amsterdam** óf stop — **zelfde dag, swap ≈ 0** (geen overnight; post-B1 NEXT_STEPS v39: geen nieuwe overnight maand-sleeves).  
**Max 1 trade/dag;** geen herentry.  
**Sizing:** 0,75% risico per trade (stop-afstand → notional).  
**Filter (0 vrije parameters):** alleen handelen als |USDJPY D1-rendement vorige sessie| ≥ mediaan |D1| van vorige 20 sessies (prior-day impulse → handoff-continuation vaker dan pure mean-reversion). Geen andere filters.

## 2. Mechanisme

USDJPY is de primaire Asia–Europe liquiditeitshandoff: Tokyo bouwt een range op yen-flows; London open herprijst met EU/UK orderflow. Een **breakout-continuation** van de Tokyo-range in de eerste London-uren is microstructuur-momentum, niet Asian-range *fade* (GS02) en niet EUR/GBP London ORB (A5/U3). Positief scheef: vaste mid-stop vs. runner tot 16:00; intraday-flat vermijdt FX overnight-swap asymmetrie.

## 3. Instrument / dataset

| Item | Waarde |
|------|--------|
| FTMO-symbool | USDJPY |
| Kosten (COSTS_FTMO.csv) | roundtrip_intraday ≈ 0,78 bp (spread_med 0,27 + 2×0,26 commissie); swap irrelevant (intraday) |
| Ontdekking | M5 USDJPY FTMO of Dukascopy-proxy 2015–2024-12-31; geen peek in 2025-01→ |
| Reserve-OOS | 2025-01-01→ — **één blik na shortlist, nooit eerder** (D-084) |
| Kalender | alle FX-handelsdagen met volledige Tokyo+London overlap; JP/UK banker feestdagen zonder liquiditeit uitsluiten (lijst vooraf bij implementatie) |

## 4. Kostenpoort (vóór trial)

Gemiddelde bruto per trade ≥ 2× 0,78 bp **én** **kosten < 50% bruto** op ontdekkingsset.  
+50%-spread-gevoeligheid: zelfde poort. Faalt poort → stop, **geen trial-telling**.

## 5. Beslisregel (statistiek + FTMO-EV)

1. Dag-geclusterde t (Newey–West, lags=5) op dag-P&L ≥ **2,0**.  
2. Kosten-aandeel < 50% bruto.  
3. Scheefheid dag-P&L > 0 óf max dagdip ≤ −1,5% bij 0,75% risk.  
4. Beide helften 2015–19 / 2020–24: mean netto > 0.  
5. Via `engine/ftmo.py`: FTMO-EV ≥ **€150/poging netto** (fee-aanname expliciet; default €540 tot Sandro bevestigt).  
6. Correlatie dagreeks met A5/U3 (EUR/GBP London ORB) en met GS02: als \|ρ\| > 0,6 → label "FX-sessie-overlap", geen aparte shortlist tenzij Δ FTMO-EV > €50.  
7. N_trades ontdekking < 200 → STOP zonder trial (power).

## 6. Verwachte uitkomst / falen

**Verwacht:** matige hitrate op duidelijke yen-handoff dagen; na kosten SR_dag ≈ 0,25–0,55.  
**Falen:** kostenpoort; t < 2,0; FTMO-EV < €150; of alleen één deelsample drijft t (regime-artefact).

## 7. Wat niet mag

Geen parameterzoektocht (TR-uren, breedte-band, filter-drempel) na resultaten. Geen 2025+ reserve tot shortlist. Geen echte orders. Geen heropenen van B1/A5/GS02-parameters. Geen overnight-variant.
