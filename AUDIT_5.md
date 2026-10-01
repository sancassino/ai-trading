# AUDIT_5 — ORB meta-filter (PREREG_ORB_META_V1, trial 7)

**Datum:** 2026-10-02  
**Bron:** `origin/claude/ftmo-trading-strategy-98mplz:results/ceo/orb_meta_stability.py` + `PREREG_ORB_META_V1.md`  
**Trades:** `results/b4/B4_a_ORB_trades.csv` (9249 trades, 7 symbolen, 2021–2024)

---

## 1. Numerieke reproductie — GEBLOKKEERD

M5-data (`data/m5gz` / `data/m5/`) is niet aanwezig in de repository (zie `data/CHECKSUMS_m5_lokaal.sha256`: "lokaal, niet in repo"). Numerieke reproduktie van features en walk-forward is niet mogelijk. De per-jaar uitkomsten worden hieronder uitsluitend vergeleken met CEO-gerapporteerde waarden uit `shock_results.md`.

**CEO-gerapporteerd (trial 7, orb_meta_stability.py):**

| Jaar | top-50% | rest | alle | corr |
|------|---------|------|------|------|
| 2022 | +7,5 bp | +4,6 bp | +6,1 bp | +0,011 |
| 2023 | +4,2 bp | −1,0 bp | +1,6 bp | +0,037 |
| 2024 | +3,2 bp | −2,8 bp | +0,3 bp | +0,071 |

Gepoold 2022–24: gefilterd **+4,97 bp** (N=2.615, dag-t **+2,93**) vs ongefilterd +2,61 bp (dag-t +2,27).  
Toegevoegde waarde (sel − niet-sel per dag): **+3,2 bp, t = 1,76** (< 2,0 formele drempel).

**Oordeel numeriek:** NIET ONAFHANKELIJK GEVERIFIEERD — M5-data ontbreekt. PREREG-eis "Auditor reproduceert onafhankelijk" kan op dit punt niet worden ingevuld. **Aanbeveling:** CEO publiceert M5-data (of commithet orb_meta_stability.py output-CSV) zodat Auditor de nummers kan kontroleren alvorens PASS te verlenen.

---

## 2. Lookahead in features

Analyse van `orb_meta_stability.py` (statisch):

| Feature | Code | Lookahead? |
|---------|------|------------|
| `prev_ret` | `D.ret.shift(1)` | Nee |
| `prev_rng` | `D.rng.shift(1)` | Nee |
| `atr20` | `D.rng.rolling(20).mean().shift(1)` | Nee |
| `rng_ratio` | `prev_rng / atr20` | Nee (beide shift(1)) |
| `r5` | `D.ret.rolling(5).sum().shift(1)` | Nee |
| `r20` | `D.ret.rolling(20).sum().shift(1)` | Nee |
| `gap` | `(D.open / D.close.shift(1) - 1)*1e4` | **Zie §3** |
| `gap_atr` | `gap / atr20` | Afhankelijk van gap |
| `dist_hi20` | `(D.close.shift(1) / D.high.rolling(20).max().shift(1) - 1)*1e4` | Nee (beide shift(1)) |
| `vol5_20` | `D.ret.rolling(5).std().shift(1) / D.ret.rolling(20).std().shift(1)` | Nee |
| `dow`, `month`, `sym` | kalender / categorisch | Nee |

**Resultaat:** geen harde lookahead in features, met uitzondering van één punt bij de drempel (zie §4).

---

## 3. Gap-feature: tijdzone en economische interpretatie

**Code:** `f['gap'] = (D.open / D.close.shift(1) - 1) * 1e4`

`D` is het resultaat van `d.resample('D')` op M5-data. M5-data is broker-time (UTC+2/UTC+3, IC Markets-stijl). De broker-dag begint om 00:00 broker-time.

**Consequentie per instrument:**

- **US500 / US100 / US30:** broker-dag start 00:00 UTC+2 ≈ 22:00–23:00 UTC. Dat is de openingstijd van Sunday-evening US-futures. `D.open[maandag]` = Sunday-evening futures open; `D.close[vrijdag]` = latere CET-vrijdagavond CFD-slotkoers. De `gap` meet dus de **weekend-overnacht-move in de futures**, niet de cash-market open gap.
- **GER40 / UK100:** markt sluit ~18:00 CET; broker-dag-grens om 00:00 CET valt tijdens de nacht. `D.open[dag]` = prijs om middernacht, `D.close[gisteren]` = gisteravond-middernacht. Dit is een CET-nacht beweging, niet de beurs-open gap.
- **XAUUSD / EURUSD:** nagenoeg 24u markt; broker-dag-grens om 00:00 is willekeurig.

**Lookahead?** Nee — de ORB-trade wordt ingezet ruim na de opening (eerste 30–60 min past), zodat `D.open` altijd bekend is op beslismoment. PREREG-rechtvaardiging ("open is bekend bij handeldag") is correct.

**Leakage?** Nee. Maar de `gap`-feature heeft een **afwijkende economische betekenis** ten opzichte van een traditionele cash-market gap: het is een broker-daggrens-artifact, niet de koerssprong tussen beurs-slotkoers en beurs-open. Dit verzwakt de theoretische onderbouwing van de feature maar introduceert geen dataleakage.

**Oordeel gap/tijdzone:** GEEN LEAKAGE. Aantekening: de feature meet niet wat de naam suggereert voor 24h-instrumenten.

---

## 4. Walk-forward drempel — lichte within-year lookahead

**Code:**
```python
te['p'] = np.mean(ps, axis=0)   # voorspellingen voor het hele testjaar
thr = te.p.median()              # mediaan van het VOLLEDIGE testjaar
a = te[te.p >= thr]              # selectie gebaseerd op volledig-jaar mediaan
```

`thr` wordt berekend op de volledige `te` (het testjaar), niet op de informatie beschikbaar op het moment van elke individuele trade-beslissing. Hierdoor worden trades vroeg in het jaar vergeleken met een drempel die mede bepaald is door trades laat in het jaar. Dit is een milde vorm van **within-year lookahead**.

**Ernst:** laag. In praktijk convergeert de mediaan van een verdeling snel en is de jaarlijkse mediaan een goede benadering voor een live rolling mediaan. Maar het is strikt genomen niet PREREG-zuiver als "vooraf vastgelegde drempel".

**PREREG-tekst:** "handel de top 50% voorspellingen" — dit beschrijft de selectieregel maar specificeert niet of de mediaan per-jaar of rollend is berekend. Ambigu.

**Aanbeveling:** bij de reserve-run `thr` instellen op de mediaan van het voorafgaande walk-forward jaar (bijv. 2024-run: gebruik mediaan van 2023-testpredikties) om forward-bias te elimineren.

---

## 5. Walk-forward structuur — overige bevindingen

- **Train / test split:** `tr = X[X.date < f'{yr}-01-01']` (expanding); `te = X[date in year yr]`. Schoon.
- **Clip-bounds:** `lo, hi = tr.y.quantile([.02,.98])` — berekend op train only. ✓
- **2025+ data:** `T = T[T.date < '2025-01-01']` vroeg in het script toegepast. Reserve niet aangeraakt. ✓
- **Seeds 0–4, gemiddeld:** correct voor stabiliteitscontrole.
- **FTMO-EV:** CEO evalueert dagelijkse dagreeks (som net_frac per dag). Methode correct.

---

## 6. Samenvatting

| Vraag | Bevinding |
|-------|-----------|
| Per-jaar uitkomsten match? | NIET VERIFIEERBAAR — M5-data ontbreekt in repo |
| Lookahead in features? | Nee, behoudens milde within-year drempel (§4) |
| Leakage via gap of tijdzone? | Nee — gap meet broker-dag-grens, niet cash-market gap (§3) |

**Blocker voor PASS:** M5-data niet beschikbaar → numerieke reproduktie onmogelijk. De PREREG-eis "Auditor reproduceert onafhankelijk" is niet ingevuld.  
**Code-structuur:** PASS (geen harde lookahead, reserve intact, walk-forward schoon).  
**Aanbeveling:** CEO publiceert M5-data of output-CSV (predictions + y per trade per jaar) zodat Auditor de getallen onafhankelijk kan bevestigen.
