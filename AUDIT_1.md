# AUDIT_1.md — Onafhankelijke audit engine/ftmo.py (D-087 actie 5)

**Auditor:** Claude (onafhankelijk van Grok-CTO)  
**Datum:** 2026-09-30 22:10 Amsterdam  
**Bronbestand:** `engine/ftmo.py` @ commit `fd21313` (branch `grok/cto-1`)  
**Doel:** verificeer of FTMO 2-Step regels correct zijn geïmplementeerd

---

## Bevindingen

### ✅ CORRECT — FTMO-regels

| Regel | Implementatie | Beoordeling |
|-------|--------------|-------------|
| Phase 1 target +10% | `phase1_target=0.10`, check `eq >= 1.0 + phase1_target` | ✅ Correct |
| Phase 2 target +5% | `phase2_target=0.05`, check `eq >= 1.0 + phase2_target` | ✅ Correct |
| Equity reset per fase | `eq[p1] = 1.0` en `eq[p2] = 1.0` bij overgang | ✅ Correct (FTMO meet per fase) |
| Max daily loss 5% van *initieel* account | `dd >= max_daily_loss` waar `dd` = fractie van initieel | ✅ Correct (statische vloer) |
| Max totaal verlies 10% van initieel | `floor = 1.0 - max_dd`, breach als `eq <= floor` | ✅ Correct |
| Intraday trough (als data beschikbaar) | `D = daily_drawdowns * scale`, check `eq - dd <= floor` | ✅ Correct |
| Minimum handelsdagen (4) | `days_in >= min_days` vóór fase-overgang | ✅ Correct |
| Maandelijkse uitbetaling | `since_pay >= block (=21 dagen)` | ✅ Redelijk (proxy) |
| Fee-refund bij eerste uitbetaling | `cash += fee` bij eerste pay | ✅ (expliciet als aanname gemarkeerd) |
| Restart op breach (herkansing) | `fees += fee * breach`, `phase[breach] = 1`, equity reset | ✅ Correct |

### ⚠️ KANTTEKENINGEN (geen blokker, wel documenteren)

**1. Intraday-proxy bij ontbrekende `daily_drawdowns`:**
```python
dd = np.maximum(0.0, -rr) * eq   # close-only proxy
```
Wanneer `daily_drawdowns=None`, schat de code de intradag-trough door `max(0, -r) × eq`. Dit is een *onderschatting* van het werkelijke intradag-dip-risico (de prijs kan diep intradag gaan en toch boven de startwaarde sluiten). Voor strategieën met hoge intradag-volatiliteit (ORB, FX-intradag) is dit relevant: de werkelijke `p_pass_1` zal lager zijn dan gesimuleerd zonder echte minuut-data.  
→ **Aanbeveling:** gebruik altijd `daily_drawdowns` wanneer beschikbaar; label resultaten zonder als "onderschatting breach-risico".

**2. Block-bootstrap wrap-around aan einde reeks:**
```python
idx = (starts + np.arange(block)) % n
```
Bij kleine steekproeven (bijv. C17 FOMC-dagen ≈ 80–120 observaties) wikkelt de bootstrap sterk terug. Dit kan auto-correlatie-structuur verstoren aan de wrap-punten. Bij dagdata (n ≥ 500) is dit verwaarloosbaar; bij event-data is het relevant.  
→ **Aanbeveling:** voor event-studies (C17, ≈80 obs) is block-bootstrap over event-reeksen minder geschikt; gewone bootstrap met block=1 verdedigbaarder of n_blocks beperken.

**3. Naamgeving `exp_payout_monthly` bevat fee-refund, NIET fee-aftrek:**
```python
"exp_payout_monthly": float(cash.mean() / horizon_months),  # bruto incl. refund
"net_ev": float(net.mean()),  # = cash - fees
```
`exp_payout_monthly` is *bruto* (incl. fee-refund, excl. fee-kosten). Dit kan tot verwarring leiden als het als "netto €/maand" wordt gepresenteerd. `net_ev_monthly` is de juiste maatstaf voor Sandro's €/maand-vraag.  
→ **Aanbeveling:** rapporteer altijd `net_ev_monthly`; label `exp_payout_monthly` expliciet als "bruto trader-uitbetaling incl. refund".

**4. `p_pass_1` logica overvangend maar correct:**
```python
passed1 |= p1 | (phase >= 2)
```
`phase >= 2` vangt alle paden die ooit fase 2+ hebben bereikt. Correct; er zijn geen dubbeltellingen door het OR-patroon.

**5. Late-funded right-censoring:**
Incomplete definitie: paden waarbij `funded_day + live_days > horizon` én géén breach in de korte waarneming worden *uitgesloten* (niet als overleefd geteld). Dit is conservatief en correct — vroeg gestopte overlevende gevallen worden niet als succes geteld.

### ❌ GEEN KRITISCHE FOUTEN GEVONDEN

De FTMO 2-Step regels zijn correct geïmplementeerd. Het bestand is intern consistent en sluit aan op `q1_frontier.py` / `ftmo_economics.py` (bewuste keuzes gedocumenteerd in docstring).

---

## Aanbeveling Manager/CEO

`engine/ftmo.py` is **geschikt voor productiegebruik** onder de volgende condities:

1. Altijd `daily_drawdowns` meegeven bij intradag-strategieën (ORB, FX); label resultaten zonder als "onderschatting".
2. Rapporteer `net_ev_monthly` als hoofdgetal, niet `exp_payout_monthly`.
3. Voor event-studies met < 200 observaties (C17): overweeg block=1 of apart te benoemen dat block-bootstrap minder passend is.
4. Fee en split zijn aannames — markeer in elke uitvoer.

**Onafhankelijkheidsnoot:** deze audit is geschreven zonder inzage in Grok-CTO-overleg of Uitvoerder-2-bevindingen; enkel de broncode is gelezen.
