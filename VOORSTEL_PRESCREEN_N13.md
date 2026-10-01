# VOORSTEL_PRESCREEN_N13 — GER40 US-Open Sync

**Status:** **geen PREREG** — D-092.1 FAIL (U2 `d4cefff`; mean −3,34 < 2,16 bp; N=92≪150).  
**Auteur:** Strateeg (Claude). Branch `claude/trusting-faraday-34tsmg`.  
**Instrument:** `GER40cash` (RT 0,72 bp → drempel 2,16 bp).  
**Grond:** GER40 beweegt sterk mee met de eerste minuten van de US-cashsessie (15:30 CET). De eerste M5-bar van US500 geeft een directe sync-impuls voor GER40: ETF-arbs, futures-hedgers en correlation-traders drijven GER40 mee. Cross-asset momentum 15:30–17:00 CET is een onderscheidend mechanisme — nog niet getest in deze combinatie.

---

## Idee (mechanisme)

Bij US-open (15:30 CET) activeren Amerikaanse institutionele traders S&P500 futures en cash. GER40 reageert vrijwel direct via index-arbitrage (DAX-futures ↔ S&P-futures correlatie ~0,85 intradag). Als US500 de eerste 5 minuten sterk stijgt/daalt, volgt GER40 dezelfde richting gedurende de nakomende 90 minuten (15:35–17:00 CET). Dit is een correlatie-gedreven continuation, niet een reverse-mean-reversion.

**Onderscheid van dode sleeves:**
- ≠ N11 GER40 XETRA ORB (ochtend 09:30 CET breakout; dit = middag 15:35 CET US-sync)
- ≠ N9 GER40 Ochtend-Fade (fade; dit = continuation US-sync)
- ≠ N6 GER40 pre-close (signal = interne GER40 trend; dit = externe US500 signal)
- ≠ GER_US_LEAD (dead; dat was relatieve performance multi-dag; dit = intradag cross-asset sync)

---

## Regel (bevriesbaar zodra screen PASS)

**US-Open signal:**  
- `P_US500_1530` = M5-close van de 15:30 CET bar van `US500cash`  
- `P_US500_1525` = M5-close van de 15:25 CET bar van `US500cash` (laatste bar vóór open)  
- `us_open_bp = 1e4 × (P_US500_1530 − P_US500_1525) / P_US500_1525`

**Entry GER40 (max 1 trade/dag):**  
- `us_open_bp ≥ +0,15%` (+15 bp) → **LONG** GER40 op 15:30 CET close  
- `us_open_bp ≤ −0,15%` (−15 bp) → **SHORT** GER40 op 15:30 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag, GER40) vanaf instapprijs.  
**Exit:** hard flat 17:00 CET (90 min). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/GER40cash.csv.gz` + `data/m5gz/US500cash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek aan §1 hierboven (US500 15:30/15:25 signal ≥ ±0,15%, GER40 entry, stop ATR14, flat 17:00 CET).
- **Maatstaf:** mean bruto retour GER40 in bp.
- **Gate:** mean bruto ≥ **2,16 bp** (3 × 0,72 bp RT GER40 COSTS).
- **Rapporteer ook N.**
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS + N≥150 → Strateeg schrijft PREREG_FTMO_N13. FAIL of N<150 → STOP.
