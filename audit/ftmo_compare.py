#!/usr/bin/env python3
"""
audit/ftmo_compare.py — AUDITOR independent validation of engine/ftmo.py (D-087).

Own mini-implementation (< 50 lines, no import from engine/), compared against
CTO's ftmo_ev() on the same block-bootstrap synthetic paths.

FTMO 2-Step rules verified:
  1. 5% daily loss limit on initial account (static), incl. floating P&L via
     close-only proxy: dd = max(0, -r) * eq_fraction
  2. 10% max drawdown: static floor = 1 - 0.10 = 0.90 (fraction of initial)
  3. Phase 1: reach equity >= 1.10 without breach, in >= 4 trading days
  4. Phase 2: from equity reset 1.0, reach >= 1.05 without breach, >= 4 days
"""
import sys
import numpy as np


# ── Auditor's independent mini-implementation ────────────────────────────────
# 44 executable lines (excluding blank lines / comments)

def ftmo_mini(
    daily_returns,
    phase1_target: float = 0.10,
    phase2_target: float = 0.05,
    max_daily_loss: float = 0.05,
    max_dd: float = 0.10,
    min_days: int = 4,
    n_paths: int = 20_000,
    horizon: int = 504,
    block: int = 21,
    seed: int = 42,
    scale: float = 1.0,
) -> dict:
    r = np.asarray(daily_returns, float).ravel()
    if r.size < 2:
        raise ValueError("need >= 2 returns")
    floor = 1.0 - max_dd                         # 0.90 static floor

    rng = np.random.default_rng(seed)
    n = r.size
    n_blk = horizon // block + 1
    starts = rng.integers(0, n, size=(n_paths, n_blk))
    idx = (
        (starts[:, :, None] + np.arange(block)[None, None, :])
        .reshape(n_paths, -1)[:, :horizon] % n
    )
    R = r[idx] * scale

    phase   = np.ones(n_paths, dtype=int)        # 1=phase1, 2=phase2, 3=funded
    eq      = np.ones(n_paths, float)            # equity as fraction of initial
    days_in = np.zeros(n_paths, int)
    passed1 = np.zeros(n_paths, bool)            # ever passed phase 1
    funded  = np.zeros(n_paths, bool)            # ever became funded

    for day in range(horizon):
        rr = R[:, day]

        # Trough proxy: day-start equity × |loss|, as fraction of initial
        dd = np.maximum(0.0, -rr) * eq

        # Breach: trough hits daily-loss limit OR floor before/at close
        breach = (dd >= max_daily_loss) | (eq - dd <= floor)
        eq    *= (1.0 + rr)
        breach |= (eq <= floor)                  # close-to-close below floor

        days_in += 1                             # increment before breach reset (CTO order)

        # Restart on breach
        phase[breach]   = 1
        eq[breach]      = 1.0
        days_in[breach] = 0

        ok = ~breach

        # Phase 1 pass
        p1 = ok & (phase == 1) & (eq >= 1.0 + phase1_target) & (days_in >= min_days)
        phase[p1]   = 2
        eq[p1]      = 1.0
        days_in[p1] = 0
        passed1    |= p1 | (phase >= 2)          # paths in ph2/funded have already passed ph1

        # Phase 2 pass → funded
        p2 = (ok & (phase == 2) & ~p1
              & (eq >= 1.0 + phase2_target) & (days_in >= min_days))
        phase[p2]   = 3
        eq[p2]      = 1.0
        days_in[p2] = 0
        funded     |= p2

    return {
        "p_pass_1": float(passed1.mean()),
        "p_pass_2": float(funded.mean()),
    }


# ── Synthetic return generators ──────────────────────────────────────────────

def _synth(n: int = 504, mu: float = 0.0008, sigma: float = 0.008, seed: int = 0):
    return np.random.default_rng(seed).normal(mu, sigma, size=n)


SCENARIOS = [
    # (label, mu/day, sigma/day, seed)
    ("drift+",  0.0008, 0.0080, 0),   # mild positive drift, normal vol (CTO smoke-test)
    ("flat",    0.0000, 0.0080, 1),   # zero drift
    ("high-vol",0.0008, 0.0180, 2),   # high vol → more breaches
    ("low-vol", 0.0006, 0.0040, 3),   # low vol → easier pass
    ("neg-drift",-0.0005,0.0080, 4),  # downward drift
]


if __name__ == "__main__":
    # Load CTO's ftmo_ev from extracted copy (no engine/ import from auditor branch)
    import importlib.util, os
    spec = importlib.util.spec_from_file_location("ftmo_cto", "/tmp/ftmo_cto.py")
    ftmo_cto_mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(ftmo_cto_mod)  # type: ignore
    ftmo_ev = ftmo_cto_mod.ftmo_ev

    header = (f"{'scenario':12s}  {'mini_p1':>8} {'mini_p2':>8}  "
              f"{'cto_p1':>8} {'cto_p2':>8}  {'Δp1':>8} {'Δp2':>8}  verdict")
    print(header)
    print("-" * len(header))

    rows = []
    for label, mu, sigma, rs in SCENARIOS:
        rets = _synth(504, mu, sigma, rs)
        SEED, N = 42, 20_000
        mini = ftmo_mini(rets, n_paths=N, seed=SEED)
        cto  = ftmo_ev(rets,  n_paths=N, seed=SEED)
        dp1  = abs(mini["p_pass_1"] - cto["p_pass_1"])
        dp2  = abs(mini["p_pass_2"] - cto["p_pass_2"])
        if dp1 < 0.05 and dp2 < 0.05:
            v = "PASS"
        elif dp1 < 0.10 and dp2 < 0.10:
            v = "TWIJFEL"
        else:
            v = "FAIL"
        print(f"{label:12s}  {mini['p_pass_1']:8.4f} {mini['p_pass_2']:8.4f}  "
              f"{cto['p_pass_1']:8.4f} {cto['p_pass_2']:8.4f}  "
              f"{dp1:8.4f} {dp2:8.4f}  {v}")
        rows.append((label, mini, cto, dp1, dp2, v))

    print()
    any_fail    = any(r[5] == "FAIL"    for r in rows)
    any_twijfel = any(r[5] == "TWIJFEL" for r in rows)
    if any_fail:
        print("OVERALL: FAIL — fundamental deviation detected")
    elif any_twijfel:
        print("OVERALL: TWIJFEL — moderate deviation, check seed/block-size")
    else:
        print("OVERALL: PASS — both implementations agree within 5% on all scenarios")
