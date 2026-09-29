# PREREG F5 — breedte met identieke regels (vastgelegd vóór berekening, 2026-09-30)

Regels ongewijzigd: RSI(2) = E1 (FTMO-D1, drempel 10, SMA200, uitstap > 70, eind-van-dag-spread, FTMO-longswap);
ORB = B4a (30 min, stop andere kant, sessie-einde, spread per bar + commissie). Data FTMO, 2021–2026.
- **Nieuwe RSI(2)-sleeves (8):** JP225, AUS200, HK50, EU50, FRA40, SPN35, N25 (.cash), XAGUSD — FTMO-D1-slotkoersen,
  swap = huidige FTMO-longswap per symbool (opgevraagd via MT5).
- **Nieuwe ORB-sleeves (8):** dezelfde symbolen op FTMO-M5; sessies (lokaal): JP225 Asia/Tokyo 09:00–15:00;
  AUS200 Australia/Sydney 10:00–16:00; HK50 Asia/Hong_Kong 09:30–16:00; EU50/FRA40/SPN35/N25 Europe/Berlin 09:00–17:30;
  XAGUSD America/New_York 09:30–16:00. Commissie: indices 0; XAGUSD als XAUUSD (0,0006%/kant).
- **IBS-sleeve (2):** IBS < 0,2 (B2a-regel) op US500 en US100, FTMO-D1-OHLC, zelfde kosten als RSI(2) op FTMO.
- **Beslisregel per sleeve (opnemen):** t ≥ 2 op FTMO-data 2021–2026 **én** correlatie (dagrendement) < 0,5 met de
  bestaande poot van dezelfde soort (RSI(2) gepoold-6 resp. ORB gepoold-7; IBS tegen RSI(2) gepoold-6) **én** positief in
  beide helften (2021–2023, 2024–2026). Opgenomen sleeves → combinatie herberekenen (E3-procedure, schaal door
  dagverliesregel < 4% zoals F3b) en DSR.
- Trials +18 (8 + 8 + 2) → 382.
