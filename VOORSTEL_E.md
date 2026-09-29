# VOORSTEL E — FTMO-validatie van de enige kandidaat (C4: RSI(2) + ORB), 2026-09-29

Backlog C1–C7 + D1–D4 afgerond; enige kandidaat met DSR ≥ 0,5 is de C4-combinatie. Die rust voor de RSI(2)-poot
op Yahoo-prijsindices. Drie hypothesen, alle **zonder nieuwe strategieparameters** (validatie, geen nieuwe trials):

## E1 (best onderbouwd, nu uitvoeren) — RSI(2) repliceert op FTMO-data met FTMO-kosten
- Data: FTMO-M5 (2021–2026) → dagbars per instrument op FTMO-servertijd (servertijd-dag = NY+7u, dus dagslot = 17:00 NY),
  voor US500, US100, US30, GER40, UK100, XAUUSD. SMA200 vereist 200 dagen historie: RSI(2)-signalen vanaf dag 201;
  daarvoor aanvullen met FTMO-D1-slotkoersen (`*_rates.csv`, vanaf 2017/2019) waar beschikbaar.
- Regel ongewijzigd (B2b): instap op slot als RSI(2) < 10 én slot > SMA200, uitstap op slot als RSI(2) > 70.
- Kosten FTMO: spread = mediaan M5-spread van de laatste bar van de dag; swap = huidige FTMO-swap (swap_specs_FTMO.csv:
  US500 −4,95%, US100 −7,12%, US30 −8,33%, GER40 −6,52%, UK100 −8,28%, XAUUSD −7,93%/jr long), per kalendernacht.
- Vergelijking: dezelfde instrumenten/periode in B2b (Yahoo) — correlatie maandrendement en totaal.
- **Beslisregel:** gepoold netto positief in 2021–2023 én 2024–2026, en maandcorrelatie met de Yahoo-versie ≥ 0,7.
  Faalt E1 → de C4-kandidaat vervalt.

## E2 — ORB onder FTMO-Standard-regels (nieuwsvenster)
- ORB-trades uit B4 waarvan instap of stop binnen ±2 min van een 'high-impact' US-release valt (08:30 of 10:00 ET,
  eerste vrijdag = NFP, CPI, FOMC 14:00 ET) zouden op een Standard-account niet mogen → effect op expectancy meten
  (kalender van releases nodig; anders benadering: alle trades met instap 10:00 ET ± 2 min uitsluiten).

## E3 — C4 onder weekend-regel (Standard) vs Swing
- RSI(2)-poot: posities vrijdag vóór sluiting dicht (Standard) vs doorhouden (Swing); effect op Sharpe/EV.

Volgorde: E1 → (alleen als E1 slaagt) E3 → E2.
