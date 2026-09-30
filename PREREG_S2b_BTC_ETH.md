# PREREG_S2b_BTC_ETH — BTC+ETH gepoolde US Cash-Open Impulse (2026-09-30)

**Status:** Pre-registration (D-091.1). Auteur: Strateeg-2.  
**Branch:** `grok/strateeg-2` · **Commit vóór enig gate-/trialresultaat.**  
**Parent:** `PREREG_S2_BTC_USOPEN.md` — regel daar **bevroren ongewijzigd** (geen post-hoc drempelwijziging op die PREREG; D-091).

## 0. Waarom S2b (geen kloon van een dode sleeve)

S2-BTC TRAIN (CTO `4a34698`): N=132, mean bruto **+22,91 bp**, kosten/stress PASS, **FAIL alleen power** (N&lt;150 per §6 parent).  
S2b = **zelfde bevroren regel** op twee FTMO-crypto-instrumenten (BTCUSD + ETHUSD), power-drempel op **gepoolde** N ≥ 150. Geen wijziging van gap/range/stop/flat van de parent. Distinct van Q3 (H1 TSMOM/σ-omkeer) en van dode ORB/XAU/GER40/USDJPY/USOIL-sleeves.

## 1. Exacte regel (identiek aan parent, per instrument)

**Instrumenten:** `BTCUSD` en `ETHUSD` (FTMO Crypto I CFD), elk apart gesignaleerd.  
**Kalender:** alleen US equity cash-handelsdagen (NYSE); crypto-weekend zonder US cash → geen trade.  
**Pre-range:** hoog/laag van 14:30–15:30 Europe/Amsterdam (60 min vóór US cash open) op M5 **van dat instrument**.  
**Entry-venster:** 15:30–16:00 Europe/Amsterdam.  
**Long:** eerste M5-slot ≥ 15:30 die boven pre-range high sluit; entry op die bar-close.  
**Short:** eerste M5-slot die onder pre-range low sluit; entry op die bar-close.  
**Geen trade** als beide kanten binnen 15:30–16:00 worden geraakt (two-way = skip) of als pre-range breedte ∉ [0,20%, 1,50%] van mid.  
**Stop:** terug voorbij pre-range mid ((high+low)/2) — vast; geen trailing.  
**Exit:** hard flat 21:00 Europe/Amsterdam **zelfde dag** óf stop — **geen overnight** (crypto-swap zwaar → swap≈0).  
**Max 1 trade / instrument / dag;** geen herentry op hetzelfde instrument.  
**Zelfde dag beide instrumenten:** beide mogen (onafhankelijke closes); sizing 0,40% risico per trade (gecombineerd ≤ 0,80% — FTMO 5%-dagregel). Richting mag verschillen; geen force-align tussen BTC en ETH.  
**Filter (0 vrije parameters, gelijk parent):** alleen handelen als |US100cash gap| ≥ 0,15% (gap = cash-open / vorige cash-close − 1); richting van de crypto-trade = **gelijkteken** met US100-gap; anders skip. Gap bekend bij 15:30 — geen lookahead.

**Verboden:** gap-drempel, range-uren, width-band, stop-formule of flat-tijd wijzigen t.o.v. parent; BTC-only N-drempel in parent verlagen; 2025+ peek.

## 2. Mechanisme

Zelfde cross-asset impulse als parent: US cash-open risk-on/off schok → crypto liquidity break in gap-richting. ETH als tweede liquiditeitsbeen vergroot event-N zonder nieuwe vrije parameters. Positief scheef: vaste mid-stop vs. runner tot 21:00; harde flat vermijdt overnight-swapstaart. ETH heeft **hogere RT-kosten** → strengere poort op ETH-been (zie §4).

## 3. Instrument / dataset

| Item | Waarde |
|------|--------|
| FTMO-symbolen | BTCUSD, ETHUSD |
| Kosten BTC | rondreis ≈ **1,25 bp** (COSTS_FTMO_alle: 0,85 + 2×0,20) |
| Kosten ETH | rondreis ≈ **7,98 bp** (COSTS_FTMO_alle: 7,58 + 2×0,20) — poort streng |
| Data | `data/m5gz/BTCUSD.csv.gz`, `data/m5gz/ETHUSD.csv.gz` + US100cash M5/D1 voor gap (v41) |
| Ontdekking / TRAIN-poort | 2021–2024-12-31 (CTO mag TRAIN 2021–2023 aanhouden zoals parent-gate; **geen 2025-01→**) |
| Reserve-OOS | 2025-01-01→ — **één blik na shortlist, nooit eerder** (D-084) |
| Kalender | NYSE cash-dagen |

## 4. Kostenpoort (vóór trial-telling)

Alles op ontdekkings-/TRAIN-set, reserve onaangeraakt:

1. **Per been:** mean bruto ≥ 2× fixed RT van dat been (BTC: 2×1,25; ETH: 2×7,98) **én** kosten &lt; 50% bruto op dat been.  
2. **+50% spread-stress** per been: zelfde poort.  
3. **Gepoold:** kosten &lt; 50% bruto over alle trades; mean bruto gepoold ≥ 2× trade-gewogen fixed RT.  
4. Als **ETH-been** poort FAIL → **S2b STOP** (geen post-hoc drop-ETH / BTC-only herlabelen — dat zou parent-power omzeilen).  
5. Fail → stop, **geen TRIALS-append**.

## 5. Beslisregel (na kostenpoort PASS)

1. **Power:** N_trades **gepoold** (BTC+ETH) ≥ **150** op TRAIN/ontdekking.  
2. Dag-geclusterde t (Newey–West, lags=5) op **som dag-P&L over beide instrumenten** ≥ **2,0**.  
3. Kosten &lt; 50% bruto (gepoold, herbevestigd).  
4. Skew van dag-P&L &gt; 0 **of** max gecombineerde dagdip ≤ −1,5% bij sizing §1.  
5. FTMO-EV via `engine/ftmo.py` ≥ **€150/poging netto** (design-drempel; geen gefabriceerde uitkomst). Ambitie-kalibratie CTO (D-091.4) informeert apart of SR×skew €800/mnd haalbaar is — verandert deze drempel niet.  
6. Beide helften 2021–22 / 2023–24: mean netto gepoold &gt; 0.  
7. Correlatie dag-P&L vs A1/GS01 informatief; \|ρ\| &gt; 0,7 → label "equity-beta sleeve".  
8. Correlatie vs Q3a/Q3b: \|ρ\| &gt; 0,5 → overlap-waarschuwing (andere regel, overlapping crypto).

## 6. Verwachte uitkomst / falen

**Verwacht (kwalitatief):** BTC-been draagt de edge; ETH voegt N toe op dezelfde US-gap-dagen maar moet door ~8 bp RT — faalkans hoog op ETH-kostenpoort.  
**Falen:** ETH- of BTC-kostenpoort; gepoolde N &lt; 150; t &lt; 2; FTMO-EV &lt; €150; helft-split fail.  
**Niet falen door:** parent-PREREG herschrijven of N-drempel op BTC-only verlagen.

## 7. Constraints / eigenaarschap

- Geen engine-run door Strateeg-2; **CTO** draait cost-gate zodra deze PREREG op `grok/strateeg-2` staat (NEXT_STEPS v42 prio 1).  
- Geen real money. Geen 2025+ reserve.  
- Geen heropening S2-XAU / GER40 / USDJPY / USOIL / A5 / A2.  
- Extra niet-kloon PREREGs op top-10 `results/screen_cost_vol.csv` volgen **nadat** Uitvoerder-2 die screen landt (D-091.2–3) — niet deze commit.
