# VOORSTEL_PRESCREEN_N11 — GER40 XETRA Opening Range Breakout (ORB)

**Status:** **GESLOTEN** — C-012 PASS → PREREG_FTMO_N11 → U2 FAIL_T (`e6b2395`); TRIAL_COUNT 446. Dead set.  
**Auteur:** Strateeg (Claude). Branch `claude/trusting-faraday-34tsmg`.  
**Instrument:** `GER40cash` (RT 1,40 bp → drempel 4,20 bp).  
**Grond:** F2-ORB referentie (≤2024 ≈€513/m) bewijst dat ORB-mechanisme voor index-futures werkt. GER40 heeft identieke institutionele ORB-dynamiek via XETRA-veiling bij 09:00 CET. Onderscheidend van N9 (fade ≠ breakout), N6 (ochtend ≠ close), S2-GER40-open (momentum ≠ ORB).

---

## Idee (mechanisme)

Bij XETRA-open (09:00 CET) stelt het veilingproces een opening-prijs op basis van geaccumuleerde overnight orders. De eerste 30 minuten (09:00–09:30 CET) vormen de "opening range": tight consolidatie terwijl institutionele orders verwerkt worden. Na 09:30 CET activeert de directionale orderflow (ETF-hedgers, DAX-futures arbs, optiondelta-hedgers). Een breakout van de ORB weerspiegelt geaccumuleerde institutionele richting en heeft continuatiekracht: mechanisme identiek aan F2-ORB (bewezen index-ORB edge).

**Onderscheid van dode sleeves:**
- ≠ N9 GER40 Ochtend-Fade (fade van 90-min impuls terug naar open; dit = breakout van 30-min ORB)
- ≠ N6 GER40 pre-close momentum (17:30 CET; dit = 09:30 CET entry, exit 13:00 CET)
- ≠ S2-GER40-open (momentum-continuation via S2-structuur; dit = ORB clean entry)
- ≠ IB_FADE/VWAP_PB (VWAP-gebaseerd; dit = ORB prijs-niveaus zonder VWAP)

---

## Regel (bevriesbaar zodra screen PASS)

**Opening Range (ORB):**  
- `ORB_high` = max high van M5-bars 09:00–09:30 CET (6 bars na XETRA-open)  
- `ORB_low` = min low van M5-bars 09:00–09:30 CET  
- `ORB_range = ORB_high − ORB_low`  
- **Filter:** `ORB_range / ORB_mid ≥ 0,10%` (anders geen trade; filtert gapless open-doji)

**Entry (max 1 trade/dag):**  
- Eerste M5-slotkoers ná 09:30 CET > `ORB_high` → **LONG**  
- Eerste M5-slotkoers ná 09:30 CET < `ORB_low` → **SHORT**  
- OCO: zodra één kant geactiveerd, andere geannuleerd  

**Stop:** `ORB_low` voor long, `ORB_high` voor short (volledige ORB-breedte als stop).  
**Exit:** hard flat 13:00 CET (3,5 uur na entry; vóór US pre-market beïnvloedt GER40). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/GER40cash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek aan §1 hierboven (ORB 09:00–09:30, breakout entry, stop=ORB-opposite, flat 13:00).
- **Maatstaf:** mean bruto retour in bp (1 bp = 0,01%).
- **Gate:** mean bruto ≥ **4,20 bp** (3 × 1,40 bp RT).
- **Rapporteer ook N (aantal trades):** N ≥ 150 vereist voor PREREG.
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS + N≥150 → Strateeg schrijft PREREG_FTMO_N11. FAIL of N<150 → STOP.
