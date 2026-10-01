#!/usr/bin/env python3
"""D-092.1 pre-screen ONLY — Strateeg-2 hourly ~03:40 Europe/Amsterdam (2026-10-01).
Train 2021–2023. mean bruto vs 3× RT. No test/reserve. No PREREG until PASS + N≥150.

Non-clones vs dead set (LUNCH_OPEN/IB/MIDDAY/VWAP_PB/GER_US/N1–N6/N7–N10/N12/ORB/…):
  A) GAP_CONT_FADE — US30/US100: overnight gap continues first 45m → fade; flat 19:00.
     ≠ N5 (immediate gap-fill) / GS01 (gap continuation) / N1 (T+30 1.5×ATR).
  B) LATE_EXT_FADE — US30/US100: fade large open→20:00 extension; flat 21:55.
     ≠ N3 (close-drive *continuation* 20:30–21:55) — this is fade from 20:00.
  C) LONDON_WIDE_NY_FADE — EURUSD/GBPUSD: wide London range + outer close → fade to mid at NY open; flat 18:00.
     ≠ A5 London ORB breakout / GS02 Asian fade / EUR_NY_FADE (no London-range filter).
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
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_0340"


def load_m5(sym: str) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        first = f.readline()
        if first.startswith("#"):
            while True:
                pos = f.tell()
                line = f.readline()
                if not line.startswith("#"):
                    if "time" not in line.lower() and "open" not in line.lower():
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
    h = g["high"].max()
    l = g["low"].min()
    c = g["close"].last()
    prev_c = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.rolling(n, min_periods=n).mean().shift(1)
    return {d: float(v) for d, v in atr.items() if pd.notna(v) and v > 0}


def prior_close_map(df: pd.DataFrame) -> dict:
    c = df.groupby(df["time"].dt.normalize())["close"].last()
    return {d: float(v) for d, v in c.shift(1).items() if pd.notna(v)}


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


def sim_gap_cont_fade(g, atr_map, pc_map):
    """A) Gap continues first 45m RTH → fade; entry 16:15; flat 19:00."""
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    pc = pc_map.get(day0)
    if atr is None or pc is None or pc <= 0:
        return None
    b_open = bar_at(g, day0, 15, 30)
    b_entry = bar_at(g, day0, 16, 15)
    if b_open is None or b_entry is None:
        return None
    p_open = float(b_open["open"])
    entry = float(b_entry["close"])
    if p_open <= 0:
        return None
    gap_bp = 1e4 * (p_open - pc) / pc
    first_bp = 1e4 * (entry - p_open) / p_open
    atr_bp = 1e4 * atr / p_open
    if abs(gap_bp) < 15.0:  # ≥15 bp overnight gap
        return None
    if abs(first_bp) < 0.25 * atr_bp:
        return None
    if np.sign(gap_bp) != np.sign(first_bp):
        return None  # need continuation of gap
    side = -1 if gap_bp > 0 else 1  # fade
    win = g[(g["time"] >= day0 + pd.Timedelta(hours=15, minutes=30)) &
            (g["time"] <= day0 + pd.Timedelta(hours=16, minutes=15))]
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    if side == 1:
        stop = wlo - 0.15 * wr
        target = p_open  # back to cash open
    else:
        stop = whi + 0.15 * wr
        target = p_open
    after = g[(g["time"] > day0 + pd.Timedelta(hours=16, minutes=15)) &
              (g["time"] <= day0 + pd.Timedelta(hours=19, minutes=0))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "gap_bp": gap_bp, "first_bp": first_bp, "atr_bp": atr_bp}


def sim_late_ext_fade(g, atr_map, pc_map=None):
    """B) Fade open→20:00 extension ≥0.55×ATR; entry 20:00; flat 21:55."""
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b_open = bar_at(g, day0, 15, 30)
    b_entry = bar_at(g, day0, 20, 0)
    if b_open is None or b_entry is None:
        return None
    p_open = float(b_open["open"])
    entry = float(b_entry["close"])
    if p_open <= 0:
        return None
    sess_bp = 1e4 * (entry - p_open) / p_open
    atr_bp = 1e4 * atr / p_open
    if abs(sess_bp) < 0.55 * atr_bp:
        return None
    side = -1 if sess_bp > 0 else 1
    win = g[(g["time"] >= day0 + pd.Timedelta(hours=15, minutes=30)) &
            (g["time"] <= day0 + pd.Timedelta(hours=20, minutes=0))]
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    if side == 1:
        stop = wlo - 0.10 * wr
        target = p_open
    else:
        stop = whi + 0.10 * wr
        target = p_open
    after = g[(g["time"] > day0 + pd.Timedelta(hours=20, minutes=0)) &
              (g["time"] <= day0 + pd.Timedelta(hours=21, minutes=55))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "sess_bp": sess_bp, "atr_bp": atr_bp}


def sim_london_wide_ny_fade(g, atr_map, pc_map=None):
    """C) Wide London range + outer close → fade to mid at NY open; flat 18:00."""
    if len(g) < 50:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    london = g[(g["time"] >= day0 + pd.Timedelta(hours=9, minutes=0)) &
               (g["time"] < day0 + pd.Timedelta(hours=15, minutes=30))]
    b_entry = bar_at(g, day0, 15, 35)
    if london.empty or b_entry is None or len(london) < 20:
        return None
    lhi, llo = float(london["high"].max()), float(london["low"].min())
    lr = lhi - llo
    if lr <= 0:
        return None
    p_lopen = float(london.iloc[0]["open"])
    if p_lopen <= 0:
        return None
    atr_bp = 1e4 * atr / p_lopen
    range_bp = 1e4 * lr / p_lopen
    if range_bp < 0.70 * atr_bp:
        return None
    l_close = float(london.iloc[-1]["close"])
    pos = (l_close - llo) / lr  # 0=low, 1=high
    if pos >= 0.70:
        side = -1  # fade upper close
    elif pos <= 0.30:
        side = 1
    else:
        return None
    entry = float(b_entry["close"])
    mid = (lhi + llo) / 2
    if side == 1:
        stop = llo - 0.20 * lr
        target = mid
    else:
        stop = lhi + 0.20 * lr
        target = mid
    after = g[(g["time"] > day0 + pd.Timedelta(hours=15, minutes=35)) &
              (g["time"] <= day0 + pd.Timedelta(hours=18, minutes=0))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "range_bp": range_bp, "pos": pos, "atr_bp": atr_bp}


def run_idea(name, symbols_rt, sim_fn, needs_pc=False):
    rows = []
    per = []
    for sym, rt in symbols_rt.items():
        df = load_m5(sym)
        atr_map = d1_atr_map(df)
        pc_map = prior_close_map(df) if needs_pc else None
        sym_rows = []
        for _, g in df.groupby(df["time"].dt.normalize()):
            if needs_pc:
                r = sim_fn(g, atr_map, pc_map)
            else:
                r = sim_fn(g, atr_map)
            if r:
                r["symbol"] = sym
                sym_rows.append(r)
        d = pd.DataFrame(sym_rows)
        n = len(d)
        mean = float(d["bruto_bp"].mean()) if n else float("nan")
        gate = 3.0 * rt
        ok = bool(n >= 30 and mean >= gate)
        skew = float(d["bruto_bp"].skew()) if n > 2 else float("nan")
        per.append({"idea": name, "symbol": sym, "n": n, "mean_bruto_bp": mean,
                    "gate_3x_rt": gate, "rt": rt, "pass": ok, "skew": skew})
        rows.extend(sym_rows)
    all_df = pd.DataFrame(rows)
    n = len(all_df)
    mean = float(all_df["bruto_bp"].mean()) if n else float("nan")
    if n:
        w = all_df.groupby("symbol").size()
        w_rt = sum(w[s] * symbols_rt[s] for s in w.index) / n
        gate_p = 3.0 * w_rt
    else:
        gate_p = float("nan")
        w_rt = float("nan")
    # D-092.1: PASS for PREREG needs mean≥gate AND N≥150 (expected)
    pooled_pass = bool(n >= 150 and mean >= gate_p)
    summary = {
        "idea": name,
        "n_pooled": n,
        "mean_bruto_bp": mean,
        "weighted_rt": w_rt,
        "gate_3x_wrt": gate_p,
        "pass_pooled_n150": pooled_pass,
        "mean_ge_gate": bool(n >= 1 and mean >= gate_p) if n else False,
        "per_symbol": per,
        "skew": float(all_df["bruto_bp"].skew()) if n > 2 else float("nan"),
    }
    return summary, all_df


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ideas = [
        ("GAP_CONT_FADE", {"US30cash": 0.45, "US100cash": 0.66}, sim_gap_cont_fade, True),
        ("LATE_EXT_FADE", {"US30cash": 0.45, "US100cash": 0.66}, sim_late_ext_fade, False),
        ("LONDON_WIDE_NY_FADE", {"EURUSD": 0.63, "GBPUSD": 0.70}, sim_london_wide_ny_fade, False),
    ]
    all_sum = []
    for name, rts, fn, needs_pc in ideas:
        summary, trades = run_idea(name, rts, fn, needs_pc=needs_pc)
        all_sum.append(summary)
        trades.to_csv(OUT / f"{name}_trades_train.csv", index=False)
        print(json.dumps({k: summary[k] for k in summary if k != "per_symbol"}, indent=2))
        for p in summary["per_symbol"]:
            print(" ", p)
        print("---")
    with open(OUT / "prescreen_summary.json", "w") as f:
        json.dump(all_sum, f, indent=2, default=str)
    lines = [
        "# Strateeg-2 D-092.1 pre-screens — 2026-10-01 ~03:47 Europe/Amsterdam",
        "",
        "Train 2021–2023 only. Gate: mean bruto ≥ 3× RT **and** N≥150 for PREREG. Reserve 2025→ untouched.",
        "",
        "| Idee | N | mean bruto | gate | skew | PASS N≥150? |",
        "|------|--:|----------:|-----:|-----:|:-----------:|",
    ]
    for s in all_sum:
        mb = s["mean_bruto_bp"]
        gp = s["gate_3x_wrt"]
        sk = s["skew"]
        lines.append(
            f"| {s['idea']} | {s['n_pooled']} | {mb:.2f} bp | {gp:.2f} bp | {sk:.2f} | "
            f"{'PASS' if s['pass_pooled_n150'] else 'FAIL'} |"
        )
    lines.append("")
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
