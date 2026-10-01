# PREREG_FTMO_N11 — GER40 XETRA Opening Range Breakout (ORB)

**Status:** PREREG bevroren — wacht U2 cost-gate.  
**Auteur:** Strateeg (Claude), branch `claude/trusting-faraday-34tsmg`.  
**Datum bevriezing:** 2026-10-01 04:00 Europe/Amsterdam.  
**Instrument:** `GER40cash`.  
**Kosten RT (COSTS_FTMO.csv):** 0,72 bp → D-092.1 drempel 3 × 0,72 = **2,16 bp**.  
**D-092.1 pre-screen:** PASS (mean +3,33 bp > gate 2,16 bp; N=496; CTO C-012 `cdabfe8`).  
**Caveat:** median −14,0 bp (skew-fragile; formele dag-geclusterd-t kan FAIL_T geven).

---

## 1. Mechanisme

Bij XETRA-open (09:00 CET) stelt het veilingproces een openingsprijs op basis van geaccumuleerde overnight orders. De eerste 30 minuten (09:00–09:30 CET) vormen de "opening range" (ORB): een tight consolidatie terwijl institutionele orders worden verwerkt. Na 09:30 CET activeert de directionale flow (ETF-hedgers, DAX-futures-arbs, option-delta-hedgers). Een breakout van de ORB weerspiegelt geaccumuleerde institutionele richting en heeft continuatiekracht. Mechanisme identiek aan F2-ORB (bewezen index-ORB edge, referentie ≈€513/mnd).

**Onderscheid van dode sleeves:**
- ≠ N9 GER40 Ochtend-Fade (fade 90-min impuls → open; dit = breakout 30-min ORB)
- ≠ N6 GER40 pre-close (17:30 CET; dit = 09:30 CET entry, exit 13:00 CET)
- ≠ S2-GER40-open (momentum-continuation; dit = ORB price-level entry)
- ≠ IB_FADE / VWAP_PB (VWAP-gebaseerd; dit = ORB prijsniveaus)

---

## 2. Regel (bevroren)

**Opening Range (ORB) — M5-data:**  
- `ORB_high` = max(high) van bars 09:00–09:30 CET (6 bars, 09:00/09:05/09:10/09:15/09:20/09:25 CET)  
- `ORB_low` = min(low) van bars 09:00–09:30 CET  
- `ORB_mid` = (ORB_high + ORB_low) / 2  
- **Minimale breedte:** `(ORB_high − ORB_low) / ORB_mid ≥ 0,10%` → anders geen trade die dag

**Entry-signaal (max 1 trade/dag, OCO):**  
- Eerste M5-slotkoers ná 09:30 CET > `ORB_high` → **LONG** op die slotkoers  
- Eerste M5-slotkoers ná 09:30 CET < `ORB_low` → **SHORT** op die slotkoers  
- Als geen breakout vóór 10:30 CET: geen trade

**Stop:** `ORB_low` voor long; `ORB_high` voor short (volledige ORB-breedte als stop).  
**Target:** geen vaste target (exit via time stop).  
**Time exit:** hard flat 13:00 CET (vóór US pre-market GER40 beïnvloedt). Swap = 0 (intradag).

---

## 3. Kosten en drempel

| Parameter | Waarde |
|-----------|--------|
| Instrument | GER40cash |
| RT-kosten | 0,72 bp (COSTS_FTMO.csv) |
| D-092.1 drempel | 3 × 0,72 = **2,16 bp** |
| +50% stress | 3 × 1,08 = 3,24 bp |
| Pre-screen uitkomst | +3,33 bp mean bruto (C-012, N=496) |

---

## 4. Dataverdeling (D-084/D-091.5, bindend)

| Periode | Rol | Status |
|---------|-----|--------|
| 2021-01-01 … 2023-12-31 | Train (U2 cost-gate + formele t) | OPEN — U2 screen |
| 2024-01-01 … 2024-12-31 | Test (alleen na CEO-vrijgave) | ONAANGERAAKT |
| 2025-01-01 → | Reserve | ONAANGERAAKT |

---

## 5. Uitvoerder-2 instructie

**Volgorde (D-092.1):**
1. **Cost-gate train:** bereken mean bruto (bp) op train 2021–2023 m.b.v. bovenstaande bevroren regel. Gate = 2,16 bp. PASS → stap 2. FAIL → STOP.
2. **Stress-gate (+50%):** gate_stress = 3,24 bp. PASS → stap 3. FAIL → vermelding; optioneel formele t.
3. **Formele t-test (dag-geclusterd, Newey-West L=5):** drempel t ≥ 2,0. PASS → shortlist. FAIL_T → STOP.
4. **Test (2024):** alleen na CEO-vrijgave; nu ONAANGERAAKT.

**Let op:** regel is identiek aan §2 hierboven — geen parameterwijziging na dit PREREG.  
**TRIAL_COUNT:** append TRIALS.csv bij stap 3. Huidige stand: 445.  
**Reserve 2025+ onaangeraakt.**

---

## 6. Economische logica (FTMO-EV)

- GER40cash dagrange: 60–100 bp. ORB stop = volledige ORB-breedte (typisch 10–25 bp). Mean bruto +3,33 bp na kosten 0,72 = netto ~2,6 bp/trade. N ≈ 150–200/jr (3 jaar train = 496 trades).
- F2-ORB mechanisme (bewezen): identieke ORB-logica voor US-indices. GER40 is de grootste Europese index-future; XETRA-veiling geeft schone ORB.
- FTMO-EV: afhankelijk van t-test uitkomst. Indien t ≥ 2,0: kandidaat portfolio-blend naast F2-ORB (correlatie GER40↔ORB-US laag; diversificatie-EV).
- Skew-risico: median = −14 bp (winners zijn groot, verliezers zijn frequent). FTMO daily-loss-limit (5%) is risico bij gestapelde verliesdagen.
