"""engine/ftmo.py — FTMO-EV module (D-085/D-086).

Rekent voor een dagelijkse overschot-rendements-reeks:
  p_phase1, p_funded, ev_per_attempt (€), breach_live, payout_per_month_given_funded

FTMO 2-Step (regels per 30-09-2026, aanname fee €540, split 80%, account €80.000):
  Fase 1: doel +10% op startkapitaal, max dagverlies 5% van startkapitaal (op balance 00:00),
          max totaalverlies 10% statisch, ≥ 4 handelsdagen, geen tijdslimiet.
  Fase 2: doel +5%, overige regels identiek.
  Funded: 12 maanden papier; maandelijks: als equity > startkapitaal → uitbetaling (equity − start) × split;
          balance teruggeslagen naar start.
  Fee-restitutie: bij de eerste uitbetaling wordt de fee terugbetaald.

Bootstrap: blok-bootstrap op dagrendementen (standaard bloklengte 21, ~1 handelsmaand).
  Serie kan korter zijn (2015→ voor C54qa); power-caveat bij < 15 jaar.

Publieke API:
  ftmo_ev(daily_total_rets, *, account, fee, split, phase1, phase2, block, n_sims, seed) -> dict
  ev_from_series(path, *, start_date, ...) -> dict   (leest date;excess;total CSV)
  ev_shortlist(series_dir, rules, ...) -> list[dict] (batch over sleeves)

Benadering: dagverlies gemeten op slot-tot-slot (geen intraday low); floating equity = dagrendement
toegepast op equity bij dagstart.
"""
from __future__ import annotations
import os
import random
import math
import numpy as np
from datetime import date

# ── FTMO-standaardparameters (aannames; FTMO-website 30-09-2026, niet gegarandeerd) ──
FTMO_ACCOUNT   = 80_000.0   # EUR
FTMO_FEE       = 540.0      # EUR (aanname, niet bevestigd)
FTMO_SPLIT     = 0.80       # winstsplit funded
FTMO_PHASE1    = 0.10       # winstdoel fase 1
FTMO_PHASE2    = 0.05       # winstdoel fase 2
FTMO_DAY_LOSS  = 0.05       # max dagverlies (balance 00:00 - 5% van startkapitaal)
FTMO_MAX_LOSS  = 0.10       # statisch max totaalverlies
FTMO_MIN_DAYS  = 4          # min handelsdagen per fase
FTMO_BLOCK     = 21         # bootstrap-bloklengte (dagelijks; ~1 maand)


def _run_phase(rets_iter: "generator", target: float | None, account: float,
               day_loss_frac: float, max_loss_frac: float, min_days: int,
               max_days: int) -> tuple[str, float]:
    """Simuleer één FTMO-fase.  Retourneert ('pass'|'fail', eindequity_frac_van_startkapitaal)."""
    eq = 1.0               # fractie van startkapitaal
    balance_start = 1.0   # dagstart-balance (teruggeslagen naar 1 na elke dag, zie FTMO-regels)
    days = 0
    while days < max_days:
        r = next(rets_iter)
        days += 1
        day_loss = max(0.0, balance_start - eq * (1 + r))  # verlies t.o.v. balance_start
        eq *= 1 + r
        if day_loss >= day_loss_frac or eq <= 1 - max_loss_frac:
            return "fail", eq
        balance_start = eq  # volgende dag begint met huidige equity als balance
        if target is not None and eq >= 1 + target and days >= min_days:
            return "pass", eq
    return "timeout" if target is not None else "done", eq


def _run_funded(rets_iter: "generator", account: float, fee: float, split: float,
                day_loss_frac: float, max_loss_frac: float,
                live_months: int, days_per_month: int) -> tuple[float, float, bool]:
    """Simuleer funded-fase.  Retourneert (gross_payout, fee_restitutie, breached)."""
    eq = 1.0
    total_payout = 0.0
    fee_restored = False
    for _ in range(live_months):
        balance_start_month = eq
        breached_month = False
        for _ in range(days_per_month):
            r = next(rets_iter)
            day_loss = max(0.0, eq - eq * (1 + r))  # slot-tot-slot benadering
            eq *= 1 + r
            if eq - balance_start_month < -day_loss_frac or eq < 1 - max_loss_frac:
                breached_month = True
                break
        if breached_month:
            return total_payout * account, (fee if fee_restored else 0.0), True
        if eq > 1.0:
            payout = (eq - 1.0) * split * account
            total_payout += eq - 1.0
            if not fee_restored and payout > 0:
                fee_restored = True
            eq = 1.0
    return total_payout * account, (fee if fee_restored else 0.0), False


def ftmo_ev(
    daily_total_rets: np.ndarray,
    *,
    account: float = FTMO_ACCOUNT,
    fee: float = FTMO_FEE,
    split: float = FTMO_SPLIT,
    phase1: float = FTMO_PHASE1,
    phase2: float = FTMO_PHASE2,
    day_loss: float = FTMO_DAY_LOSS,
    max_loss: float = FTMO_MAX_LOSS,
    min_days: int = FTMO_MIN_DAYS,
    block: int = FTMO_BLOCK,
    n_sims: int = 10_000,
    seed: int = 42,
    max_months: int = 24,
    live_months: int = 12,
    days_per_month: int = 21,
) -> dict:
    """Bereken FTMO-EV voor een numpy array van dagelijkse total-return rendementen.

    Parameters
    ----------
    daily_total_rets : dagelijkse totaalrendementen (inclusief rf/swap/kosten).
    account          : accountgrootte in EUR.
    fee              : FTMO-challenge-fee in EUR (aanname).
    split            : winstsplit (funded).
    phase1 / phase2  : winstdoelen fase 1 / 2.
    day_loss         : max dagverlies als fractie van startkapitaal.
    max_loss         : statisch max totaalverlies (fractie).
    min_days         : min handelsdagen per fase.
    block            : bootstrap-bloklengte (dagen).
    n_sims           : aantal simulaties.
    seed             : random seed.
    max_months       : max duur per fase (maanden; praktische bovengrens).
    live_months      : duur funded-fase (maanden).
    days_per_month   : handelsdagen per maand in de simulatie.

    Returns
    -------
    dict met: p_phase1, p_funded, ev_per_attempt (€; na aftrek fee),
              payout_per_month_given_funded (€/mnd bruto), breach_live,
              months_to_funded (mediaan), n_days (invoer), years (invoer).
    """
    x = np.asarray(daily_total_rets, dtype=float)
    n = len(x)
    if n < block:
        return {k: float("nan") for k in
                ("p_phase1", "p_funded", "ev_per_attempt", "payout_per_month_given_funded",
                 "breach_live", "months_to_funded", "n_days", "years")}

    rng = random.Random(seed)
    max_days = max_months * days_per_month

    def _stream():
        while True:
            s = rng.randrange(n)
            for i in range(block):
                yield float(x[(s + i) % n])

    p1_count = 0
    funded_count = 0
    breach_count = 0
    payouts = []
    months_to_funded_list = []
    ev_list = []

    for _ in range(n_sims):
        st = _stream()
        status1, _ = _run_phase(st, phase1, account, day_loss, max_loss, min_days, max_days)
        if status1 != "pass":
            ev_list.append(-fee)
            continue
        p1_count += 1
        status2, _ = _run_phase(st, phase2, account, day_loss, max_loss, min_days, max_days)
        if status2 != "pass":
            ev_list.append(-fee)
            continue
        funded_count += 1

        gross, fee_back, breached = _run_funded(
            st, account, fee, split, day_loss, max_loss, live_months, days_per_month)
        months_to_funded_list.append(
            (max_months + max_months) * 0.5)  # benadering; fijnere tracking via losse teller
        payouts.append(gross)
        if breached:
            breach_count += 1
            ev_list.append(gross + fee_back - fee)
        else:
            ev_list.append(gross + fee_back - fee)

    n_funded = funded_count or 1
    ev = float(np.mean(ev_list)) if ev_list else float("nan")
    ppm = float(np.mean(payouts) / live_months) if payouts else 0.0
    breach_live = breach_count / n_funded if funded_count else float("nan")

    return {
        "p_phase1": p1_count / n_sims,
        "p_funded": funded_count / n_sims,
        "ev_per_attempt": ev,
        "payout_per_month_given_funded": ppm,
        "breach_live": breach_live,
        "months_to_funded": float(np.median(months_to_funded_list)) if months_to_funded_list else float("nan"),
        "n_days": n,
        "years": n / 252.0,
    }


def ev_from_series(
    path: str,
    *,
    col: str = "total",
    start_date: date | None = None,
    end_date: date | None = None,
    **kw,
) -> dict:
    """Laad een date;excess;total CSV en bereken FTMO-EV op de total-return kolom."""
    dates, excess, total = [], [], []
    with open(path) as f:
        header = f.readline().strip().split(";")
        ci = header.index(col)
        for line in f:
            parts = line.strip().split(";")
            if not parts[0][:4].isdigit():
                continue
            d = date.fromisoformat(parts[0])
            if start_date and d < start_date:
                continue
            if end_date and d > end_date:
                continue
            dates.append(d)
            total.append(float(parts[ci]))

    rets = np.array(total, dtype=float)
    result = ftmo_ev(rets, **kw)
    result["start"] = str(dates[0]) if dates else None
    result["end"]   = str(dates[-1]) if dates else None
    return result


def ev_shortlist(
    series_dir: str,
    rules: list[str],
    vehicle: str = "cfd",
    variant: str | None = None,
    *,
    start_date: date | None = None,
    **kw,
) -> list[dict]:
    """Bereken FTMO-EV voor een lijst van regels vanuit de series-map.

    rules: bijv. ["C02_faber", "C52_allweather", "C17_fomc_cycle"]
    variant: als None, zoekt __basis__ en alle varianten automatisch.
    """
    results = []
    for rule in rules:
        found = [f for f in os.listdir(series_dir)
                 if f.startswith(rule + "__")
                 and f.endswith(f"__{vehicle}.csv")
                 and (variant is None or f"__{variant}__" in f)]
        for fname in sorted(found):
            path = os.path.join(series_dir, fname)
            r = ev_from_series(path, start_date=start_date, **kw)
            parts = fname.replace(".csv", "").split("__")
            r["rule"] = parts[0] if len(parts) > 0 else fname
            r["variant"] = parts[1] if len(parts) > 1 else "basis"
            r["vehicle"] = parts[2] if len(parts) > 2 else vehicle
            results.append(r)
    return results


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("Gebruik: python -m engine.ftmo <series.csv> [--start YYYY-MM-DD]")
        sys.exit(1)
    path = sys.argv[1]
    start = None
    if "--start" in sys.argv:
        idx = sys.argv.index("--start")
        start = date.fromisoformat(sys.argv[idx + 1])
    res = ev_from_series(path, start_date=start)
    print(json.dumps(res, indent=2))
