"""Monte Carlo FTMO-EV simulator (D-085 / FASE 3).

Vectorized block-bootstrap over daily return paths. Aligns with
`q1_frontier.py` (numpy paths, restart-on-breach, fee refund) and
`ftmo_economics.py` / `mc_daily_ftmo.py` (2-Step rules).

Rules (FTMO 2-Step, static; unverified amounts marked as assumptions):
  - Phase 1 profit target +10%, phase 2 +5%, each min ``min_days`` trading days
  - Max daily loss: ``max_daily_loss`` of *initial* account (static), measured
    on equity including floating P&L (intraday trough via ``daily_drawdowns``,
    else close-to-close loss as proxy — see ``ftmo_economics`` caveat)
  - Max loss: ``max_dd`` of *initial* account (static floor at 1 - max_dd)
  - Funded: monthly payout of profit above start × ``split`` (default 80%);
    challenge ``fee`` refunded on first payout (assumption)
  - On breach: new fee + restart phase 1 (models ongoing attempts over horizon)

Returns dict with at least:
  p_pass_1, p_pass_2, p_survive, exp_payout_monthly, net_ev

Smoke test:
  python -m engine.ftmo
  python -m engine.ftmo --csv results/f/F1_RSI2_swapcorr_daily.csv --scale 1.0
"""
from __future__ import annotations

import argparse
import csv
import sys

import numpy as np

# Defaults match D-083 / D-085 assumptions (€80k, fee €540 unverified, 80% split)
DEFAULT_FEE = 540.0
DEFAULT_ACCOUNT = 80_000.0
DEFAULT_SPLIT = 0.8
DEFAULT_PHASE1 = 0.10
DEFAULT_PHASE2 = 0.05
DEFAULT_DAILY_LOSS = 0.05
DEFAULT_MAX_DD = 0.10
DEFAULT_MIN_DAYS = 4
DEFAULT_HORIZON = 504   # ~24 trading months
DEFAULT_BLOCK = 21      # ~1 calendar month
DEFAULT_PATHS = 20_000
DEFAULT_LIVE_MONTHS = 12


def load_daily_equity_csv(path: str, account: float = DEFAULT_ACCOUNT):
    """Load (returns, drawdowns) from an MT5-style daily equity CSV
    (columns: start_balance, min_equity, end_equity — same as q1_frontier).

    ``drawdowns[i]`` = max(0, (start_balance - min_equity) / account) so that
    floating P&L troughs count toward the 5% daily-loss rule.
    """
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter=";") if r.get("date") or r.get("end_equity")]
    r, d, prev = [], [], account
    for x in rows:
        sb = float(x.get("start_balance", prev))
        mn = float(x.get("min_equity", x["end_equity"]))
        en = float(x["end_equity"])
        r.append(en / prev - 1.0)
        d.append(max(0.0, (sb - mn) / account))
        prev = en
    return np.asarray(r, float), np.asarray(d, float)


def ftmo_ev(
    daily_returns,
    fee: float = DEFAULT_FEE,
    account: float = DEFAULT_ACCOUNT,
    split: float = DEFAULT_SPLIT,
    phase1_target: float = DEFAULT_PHASE1,
    phase2_target: float = DEFAULT_PHASE2,
    max_daily_loss: float = DEFAULT_DAILY_LOSS,
    max_dd: float = DEFAULT_MAX_DD,
    min_days: int = DEFAULT_MIN_DAYS,
    *,
    daily_drawdowns=None,
    n_paths: int = DEFAULT_PATHS,
    horizon: int = DEFAULT_HORIZON,
    block: int = DEFAULT_BLOCK,
    live_months: int = DEFAULT_LIVE_MONTHS,
    scale: float = 1.0,
    seed: int = 7,
    restart: bool = True,
):
    """Monte Carlo FTMO-EV simulator.

    Parameters
    ----------
    daily_returns : array-like
        Fractional day-over-day equity returns (close-to-close).
    fee, account, split : float
        Challenge fee (€), account size (€), profit split to trader (0–1).
    phase1_target, phase2_target : float
        Profit targets as fraction of account start (0.10 / 0.05).
    max_daily_loss, max_dd : float
        Static limits as fraction of *initial* account (0.05 / 0.10).
        Daily loss includes floating P&L when ``daily_drawdowns`` is given.
    min_days : int
        Minimum trading days in a phase before a pass counts.
    daily_drawdowns : array-like or None
        Intraday max loss as fraction of *initial* account (same length as
        returns). If None, proxy = max(0, −r) × equity_frac (close-only).
    n_paths, horizon, block : int
        Bootstrap paths, trading days per path, contiguous block length.
    live_months : int
        Funded window used for ``p_survive`` (≈ ``live_months * block`` days).
    scale : float
        Multiplier on returns (and drawdowns) — position-size knob.
    seed : int
        RNG seed for reproducibility.
    restart : bool
        If True (default), breach → new fee + phase 1 restart (q1-style EV).
        If False, path ends on first breach (single-attempt EV).

    Returns
    -------
    dict
        p_pass_1 : float
            P(ever pass phase 1) over the horizon.
        p_pass_2 : float
            P(ever get funded = pass phase 1+2).
        p_survive : float
            P(no breach in first ``live_months`` of funded | funded and
            the full live window was observed). Paths funded so late that
            ``live_months`` cannot finish before ``horizon`` are
            right-censored and **excluded** (they must not count as
            survived). NaN if no eligible funded path remains.
        exp_payout_monthly : float
            Expected trader payout €/month over the horizon (cash incl. fee
            refund, fees not subtracted) = mean(cash) / (horizon / block).
        net_ev : float
            Expected net € over the full horizon = mean(cash − fees).
            Divide by (horizon / block) for €/month net.

        Extra diagnostics (stable, documented): attempts_mean, p_net_loss,
        breach12_given_funded, first_pay_months_med, horizon_months,
        n_funded, n_survive_eligible, n_funded_incomplete.
    """
    r = np.asarray(daily_returns, dtype=float).ravel()
    if r.size < 2:
        raise ValueError("daily_returns needs at least 2 observations")
    if daily_drawdowns is None:
        # Close-only proxy: loss fraction of initial ≈ max(0,−r) × eq_frac,
        # applied inside the loop (eq-dependent). Pre-store raw negative r.
        d = None
    else:
        d = np.asarray(daily_drawdowns, dtype=float).ravel()
        if d.size != r.size:
            raise ValueError("daily_drawdowns must match daily_returns length")

    rng = np.random.default_rng(seed)
    n = r.size
    n_blocks = horizon // block + 1
    starts = rng.integers(0, n, size=(n_paths, n_blocks))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(n_paths, -1)[:, :horizon] % n
    R = r[idx] * scale
    D = None if d is None else d[idx] * scale

    floor = 1.0 - max_dd
    phase = np.ones(n_paths, dtype=int)          # 1, 2, 3=funded
    eq = np.ones(n_paths, dtype=float)           # fraction of initial
    days_in = np.zeros(n_paths, dtype=int)
    fees = np.full(n_paths, fee, dtype=float)
    cash = np.zeros(n_paths, dtype=float)
    refunded = np.zeros(n_paths, dtype=bool)
    attempts = np.ones(n_paths, dtype=float)
    passed1 = np.zeros(n_paths, dtype=bool)
    funded_ever = np.zeros(n_paths, dtype=bool)
    funded_day = np.full(n_paths, -1, dtype=int)
    breach_live = np.zeros(n_paths, dtype=bool)
    first_pay = np.full(n_paths, -1, dtype=int)
    since_pay = np.zeros(n_paths, dtype=int)
    live_days = live_months * block
    active = np.ones(n_paths, dtype=bool)        # False after terminal breach if not restart

    for day in range(horizon):
        rr = R[:, day]
        # Daily loss as fraction of *initial* account
        if D is None:
            # Proxy: loss from day-start equity, scaled to initial (= eq_frac × (−r)+)
            dd = np.maximum(0.0, -rr) * eq
        else:
            dd = D[:, day]

        # Breach on trough before applying close, and on close through floor
        breach = active & ((dd >= max_daily_loss) | (eq - dd <= floor))
        eq = np.where(active, eq * (1.0 + rr), eq)
        breach |= active & (eq <= floor)

        days_in = np.where(active, days_in + 1, days_in)

        was_funded = phase == 3
        in_live_window = (funded_day >= 0) & (day - funded_day < live_days)
        breach_live |= breach & was_funded & in_live_window

        if restart:
            fees += fee * breach
            attempts += breach
            phase[breach] = 1
            eq[breach] = 1.0
            days_in[breach] = 0
            refunded[breach] = False
            since_pay[breach] = 0
            # funded_ever / funded_day kept (ever-funded stats)
        else:
            active &= ~breach
            # freeze breached paths
            eq = np.where(breach, eq, eq)

        ok = active & ~breach
        p1 = ok & (phase == 1) & (eq >= 1.0 + phase1_target) & (days_in >= min_days)
        phase[p1] = 2
        eq[p1] = 1.0
        days_in[p1] = 0
        passed1 |= p1 | (phase >= 2)

        p2 = ok & (phase == 2) & (eq >= 1.0 + phase2_target) & (days_in >= min_days) & ~p1
        phase[p2] = 3
        eq[p2] = 1.0
        days_in[p2] = 0
        since_pay[p2] = 0
        newly = p2 & ~funded_ever
        funded_ever |= p2
        funded_day[newly] = day
        passed1 |= p2

        f = ok & (phase == 3) & ~p2
        since_pay[f] += 1
        pay = f & (since_pay >= block) & (eq > 1.0)
        amount = np.where(pay, (eq - 1.0) * account * split, 0.0)
        cash += amount
        ref = pay & ~refunded
        cash += np.where(ref, fee, 0.0)
        refunded |= ref
        first_pay[(first_pay < 0) & pay] = day
        eq[pay] = 1.0
        since_pay[pay] = 0

    horizon_months = horizon / block
    net = cash - fees
    fp = first_pay[first_pay >= 0]
    # Right-censoring fix (U2): late-funded paths that never finish
    # live_months must not inflate p_survive. Eligible = funded and
    # (completed full live window OR breached during the observed live
    # portion — a breach is definitive even if the window is short).
    n_funded = int(funded_ever.sum())
    incomplete = (
        funded_ever
        & (funded_day >= 0)
        & (funded_day + live_days > horizon)
        & ~breach_live
    )
    eligible = funded_ever & ~incomplete
    n_eligible = int(eligible.sum())
    n_incomplete = int(incomplete.sum())
    if n_eligible > 0:
        p_survive = float((~breach_live)[eligible].mean())
        breach12 = float(breach_live[eligible].mean())
    else:
        p_survive = float("nan")
        breach12 = float("nan")

    return {
        "p_pass_1": float(passed1.mean()),
        "p_pass_2": float(funded_ever.mean()),
        "p_survive": p_survive,
        "exp_payout_monthly": float(cash.mean() / horizon_months),
        "net_ev": float(net.mean()),
        # diagnostics
        "net_ev_monthly": float(net.mean() / horizon_months),
        "attempts_mean": float(attempts.mean()),
        "p_net_loss": float((net < 0).mean()),
        "breach12_given_funded": breach12,
        "first_pay_months_med": float(np.median(fp) / block) if len(fp) else float("nan"),
        "horizon_months": float(horizon_months),
        "n_funded": n_funded,
        "n_survive_eligible": n_eligible,
        "n_funded_incomplete": n_incomplete,
        "fee": float(fee),
        "account": float(account),
        "split": float(split),
        "scale": float(scale),
        "n_paths": int(n_paths),
        "restart": bool(restart),
    }


def _synthetic_returns(n: int = 504, mu: float = 0.0008, sigma: float = 0.008, seed: int = 0):
    """Mild positive-drift Gaussian days for smoke tests (not a real edge)."""
    rng = np.random.default_rng(seed)
    return rng.normal(mu, sigma, size=n)


def _fmt(out: dict) -> str:
    surv = (
        f"p_survive={out['p_survive']*100:.1f}%"
        if np.isfinite(out["p_survive"])
        else "p_survive=nan"
    )
    lines = [
        f"p_pass_1={out['p_pass_1']*100:.1f}%  p_pass_2={out['p_pass_2']*100:.1f}%  {surv}",
        f"exp_payout_monthly=€{out['exp_payout_monthly']:,.0f}  "
        f"net_ev=€{out['net_ev']:,.0f}  net_ev_monthly=€{out['net_ev_monthly']:,.0f}",
        f"attempts_mean={out['attempts_mean']:.2f}  p_net_loss={out['p_net_loss']*100:.1f}%  "
        f"first_pay_months_med={out['first_pay_months_med']}",
        f"n_funded={out.get('n_funded', '?')}  n_survive_eligible={out.get('n_survive_eligible', '?')}  "
        f"n_funded_incomplete={out.get('n_funded_incomplete', '?')}",
    ]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="FTMO-EV Monte Carlo (engine/ftmo.py)")
    ap.add_argument("--csv", default=None, help="daily equity CSV (start_balance;min_equity;end_equity)")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--fee", type=float, default=DEFAULT_FEE)
    ap.add_argument("--account", type=float, default=DEFAULT_ACCOUNT)
    ap.add_argument("--split", type=float, default=DEFAULT_SPLIT)
    ap.add_argument("--paths", type=int, default=5000, help="paths (default 5000 for smoke; API default 20000)")
    ap.add_argument("--horizon", type=int, default=DEFAULT_HORIZON)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--no-restart", action="store_true")
    a = ap.parse_args(argv)

    if a.csv:
        rets, dd = load_daily_equity_csv(a.csv, a.account)
        print(f"loaded {a.csv}: {len(rets)} days, mean {rets.mean()*1e4:+.2f} bp/day")
        out = ftmo_ev(
            rets, fee=a.fee, account=a.account, split=a.split,
            daily_drawdowns=dd, n_paths=a.paths, horizon=a.horizon,
            scale=a.scale, seed=a.seed, restart=not a.no_restart,
        )
    else:
        rets = _synthetic_returns()
        print(f"synthetic returns: {len(rets)} days, mean {rets.mean()*1e4:+.2f} bp/day, "
              f"vol {rets.std()*np.sqrt(252)*100:.1f}%/yr")
        out = ftmo_ev(
            rets, fee=a.fee, account=a.account, split=a.split,
            n_paths=a.paths, horizon=a.horizon, scale=a.scale, seed=a.seed,
            restart=not a.no_restart,
        )
    print(_fmt(out))
    print("dict keys:", sorted(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1:])
