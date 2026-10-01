#!/usr/bin/env python3
"""D-092.1 pre-screen ONLY — Strateeg-2 candidates (train 2021–2023).
mean bruto vs 3× RT. No test/reserve. No PREREG claim until PASS.
Ideas (non-clone vs dead set / FAIL screens):
  A) LUNCH_OPEN_FADE — US30/US100: fade morning move (open→17:00 AMS)
     toward session open; entry 17:00; flat 19:00. ≠ MIDDAY_VWAP / N1 / IB / VWAP_PB.
  B) UK_AM_FADE — UK100: fade London AM extension vs Asia anchor; flat 14:00.
     ≠ GER40_OPEN / N1 / XAU_AM_FADE (different instrument + window).
  C) EUR_NY_FADE — EURUSD: fade first 60m US-cash drive; flat 18:30.
     ≠ A5 London ORB / GS02 Asian fade / USDJPY handoff.
"""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
OUT = ROOT / "results" / "strateeg2_prescreen"


def load_m5(sym: str) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        # skip comment lines; first non-# is header or data
        pos = f.tell()
        first = f.readline()
        if first.startswith("#"):
            while True:
                pos = f.tell()
                line = f.readline()
                if not line.startswith("#"):
                    # line may be header
                    if "time" in line.lower() or "open" in line.lower():
                        pass  # header consumed
                    else:
                        f.seek(pos)
                    break
        else:
            f.seek(0)
        df = pd.read_csv(f, sep=";", header=None, names=["time", "open", "high", "low", "close", "spread"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M", errors="coerce")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["time", "close"]).sort_values("time").reset_index(drop=True)
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].copy()


def d1_atr_map(df: pd.DataFrame, n: int = 14) -> dict:
    g = df.groupby(df["time"].dt.normalize())
    o = g["open"].first()
    h = g["high"].max()
    l = g["low"].min()
    c = g["close"].last()
    prev_c = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.rolling(n, min_periods=n).mean()
    # map day -> prior ATR (no lookahead)
    atr_prior = atr.shift(1)
    return {d: float(v) for d, v in atr_prior.items() if pd.notna(v) and v > 0}


def bar_at(g: pd.DataFrame, day0, hh, mm):
    t = day0 + pd.Timedelta(hours=hh, minutes=mm)
    b = g[(g["time"] >= t) & (g["time"] < t + pd.Timedelta(minutes=5))]
    return None if b.empty else b.iloc[0]


def walk_exit(after, side, entry, stop, target=None):
    if after.empty:
        return None
    exit_px, reason = float(after.iloc[-1]["close"]), "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            if lo <= stop:
                return stop, "stop"
            if target is not None and hi >= target:
                return target, "target"
        else:
            if hi >= stop:
                return stop, "stop"
            if target is not None and lo <= target:
                return target, "target"
    return exit_px, reason


def sim_lunch_open_fade(g, atr_map):
    """A) Fade morning open→17:00 AMS move; entry 17:00; target open; flat 19:00."""
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b_open = bar_at(g, day0, 15, 30)
    b_entry = bar_at(g, day0, 17, 0)
    if b_open is None or b_entry is None:
        return None
    p_open = float(b_open["open"])
    entry = float(b_entry["close"])
    if p_open <= 0:
        return None
    morn_bp = 1e4 * (entry - p_open) / p_open
    atr_bp = 1e4 * atr / p_open
    if abs(morn_bp) < 0.40 * atr_bp:
        return None
    side = -1 if morn_bp > 0 else 1  # fade
    morn = g[(g["time"] >= day0 + pd.Timedelta(hours=15, minutes=30)) &
             (g["time"] <= day0 + pd.Timedelta(hours=17, minutes=0))]
    mhi, mlo = float(morn["high"].max()), float(morn["low"].min())
    mr = mhi - mlo
    if mr <= 0:
        return None
    if side == 1:  # long fade of down morning
        stop = mlo - 0.15 * mr
        target = p_open
    else:
        stop = mhi + 0.15 * mr
        target = p_open
    after = g[(g["time"] > day0 + pd.Timedelta(hours=17, minutes=0)) &
              (g["time"] <= day0 + pd.Timedelta(hours=19, minutes=0))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "morn_bp": morn_bp, "atr_bp": atr_bp}


def sim_uk_am_fade(g, atr_map):
    """B) UK100: Asia 00:00–08:00 anchor; London AM 08:00–11:30 extension fade; flat 14:00."""
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    asia = g[(g["time"] >= day0) & (g["time"] < day0 + pd.Timedelta(hours=8))]
    am = g[(g["time"] >= day0 + pd.Timedelta(hours=8)) &
           (g["time"] <= day0 + pd.Timedelta(hours=11, minutes=30))]
    b_entry = bar_at(g, day0, 11, 30)
    if asia.empty or am.empty or b_entry is None:
        return None
    asia_hi, asia_lo = float(asia["high"].max()), float(asia["low"].min())
    am_hi, am_lo = float(am["high"].max()), float(am["low"].min())
    p_ref = float(bar_at(g, day0, 8, 0)["open"]) if bar_at(g, day0, 8, 0) is not None else float(am.iloc[0]["open"])
    if p_ref <= 0 or asia_hi <= asia_lo:
        return None
    atr_bp = 1e4 * atr / p_ref
    up_ext = 1e4 * (am_hi - asia_hi) / asia_hi if am_hi > asia_hi else 0.0
    dn_ext = 1e4 * (asia_lo - am_lo) / asia_lo if am_lo < asia_lo else 0.0
    if up_ext < 0.50 * atr_bp and dn_ext < 0.50 * atr_bp:
        return None
    if up_ext >= dn_ext and up_ext >= 0.50 * atr_bp:
        side = -1
    elif dn_ext > up_ext and dn_ext >= 0.50 * atr_bp:
        side = 1
    else:
        return None
    entry = float(b_entry["close"])
    # stop beyond AM extreme
    if side == -1:
        stop = am_hi + 0.20 * (am_hi - am_lo + 1e-12)
        target = (asia_hi + asia_lo) / 2
    else:
        stop = am_lo - 0.20 * (am_hi - am_lo + 1e-12)
        target = (asia_hi + asia_lo) / 2
    after = g[(g["time"] > day0 + pd.Timedelta(hours=11, minutes=30)) &
              (g["time"] <= day0 + pd.Timedelta(hours=14, minutes=0))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "up_ext": up_ext, "dn_ext": dn_ext, "atr_bp": atr_bp}


def sim_eur_ny_fade(g, atr_map):
    """C) EURUSD: fade US cash first-hour drive (15:30–16:30); entry 16:30; flat 18:30."""
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 15, 30)
    b1 = bar_at(g, day0, 16, 30)
    if b0 is None or b1 is None:
        return None
    p0 = float(b0["open"])
    entry = float(b1["close"])
    if p0 <= 0:
        return None
    drive_bp = 1e4 * (entry - p0) / p0
    atr_bp = 1e4 * atr / p0
    if abs(drive_bp) < 0.35 * atr_bp:
        return None
    side = -1 if drive_bp > 0 else 1
    win = g[(g["time"] >= day0 + pd.Timedelta(hours=15, minutes=30)) &
            (g["time"] <= day0 + pd.Timedelta(hours=16, minutes=30))]
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    if side == 1:
        stop = wlo - 0.25 * wr
        target = p0
    else:
        stop = whi + 0.25 * wr
        target = p0
    after = g[(g["time"] > day0 + pd.Timedelta(hours=16, minutes=30)) &
              (g["time"] <= day0 + pd.Timedelta(hours=18, minutes=30))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "drive_bp": drive_bp, "atr_bp": atr_bp}


def run_idea(name, symbols_rt, sim_fn):
    rows = []
    per = []
    for sym, rt in symbols_rt.items():
        df = load_m5(sym)
        atr_map = d1_atr_map(df)
        sym_rows = []
        for _, g in df.groupby(df["time"].dt.normalize()):
            r = sim_fn(g, atr_map)
            if r:
                r["symbol"] = sym
                sym_rows.append(r)
        d = pd.DataFrame(sym_rows)
        n = len(d)
        mean = float(d["bruto_bp"].mean()) if n else float("nan")
        gate = 3.0 * rt
        ok = bool(n >= 30 and mean >= gate)
        per.append({"idea": name, "symbol": sym, "n": n, "mean_bruto_bp": mean, "gate_3x_rt": gate, "rt": rt, "pass": ok})
        rows.extend(sym_rows)
    all_df = pd.DataFrame(rows)
    n = len(all_df)
    mean = float(all_df["bruto_bp"].mean()) if n else float("nan")
    # pooled gate = 3× mean RT weighted by trade count per sym
    if n:
        w = all_df.groupby("symbol").size()
        rt_map = {s: symbols_rt[s] for s in w.index}
        w_rt = sum(w[s] * rt_map[s] for s in w.index) / n
        gate_p = 3.0 * w_rt
    else:
        gate_p = float("nan")
        w_rt = float("nan")
    pooled_pass = bool(n >= 80 and mean >= gate_p)
    summary = {
        "idea": name,
        "n_pooled": n,
        "mean_bruto_bp": mean,
        "weighted_rt": w_rt,
        "gate_3x_wrt": gate_p,
        "pass_pooled": pooled_pass,
        "per_symbol": per,
        "skew": float(all_df["bruto_bp"].skew()) if n > 2 else float("nan"),
    }
    return summary, all_df


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ideas = [
        ("LUNCH_OPEN_FADE", {"US30cash": 0.45, "US100cash": 0.66}, sim_lunch_open_fade),
        ("UK_AM_FADE", {"UK100cash": 1.42}, sim_uk_am_fade),
        ("EUR_NY_FADE", {"EURUSD": 0.63}, sim_eur_ny_fade),
    ]
    all_sum = []
    for name, rts, fn in ideas:
        summary, trades = run_idea(name, rts, fn)
        all_sum.append(summary)
        trades.to_csv(OUT / f"{name}_trades_train.csv", index=False)
        print(json.dumps({k: summary[k] for k in summary if k != "per_symbol"}, indent=2))
        for p in summary["per_symbol"]:
            print(" ", p)
        print("---")
    with open(OUT / "prescreen_summary.json", "w") as f:
        json.dump(all_sum, f, indent=2, default=str)
    # markdown
    lines = ["# Strateeg-2 D-092.1 pre-screens — 2026-10-01 ~02:45 Europe/Amsterdam", "",
             "Train 2021–2023 only. Gate: mean bruto ≥ 3× RT. Reserve 2025→ untouched.", "",
             "| Idee | N | mean bruto | gate | PASS? |",
             "|------|--:|----------:|-----:|:-----:|"]
    for s in all_sum:
        lines.append(f"| {s['idea']} | {s['n_pooled']} | {s['mean_bruto_bp']:.2f} bp | {s['gate_3x_wrt']:.2f} bp | {'PASS' if s['pass_pooled'] else 'FAIL'} |")
    lines.append("")
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print("WROTE", OUT / "prescreen_summary.json")


if __name__ == "__main__":
    main()
