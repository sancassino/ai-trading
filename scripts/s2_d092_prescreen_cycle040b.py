#!/usr/bin/env python3
"""D-092.1 extra non-clones — Strateeg-2 ~03:50 Europe/Amsterdam.
  D) OPEN_RECLAIM — US30/US100: 15:30–15:45 drive, 15:45–16:00 reclaim through open → trade reclaim; flat 17:30.
     ≠ N1 (no reclaim), ≠ Failed-OR (OR-break fail), ≠ N5 gap-fill.
  E) GER_MID_FADE — GER40: fade 09:00→13:00 extension ≥0.45×ATR back to open; flat 15:00 (vóór US/N11).
     ≠ N9 (pre-XETRA→open), ≠ N11 XETRA ORB, ≠ GER40_OPEN drive, ≠ N6 close.
  F) JP_TOKYO_FADE — JP225: fade 01:00–04:00 Tokyo extension ≥0.45×ATR to Asia open; flat 07:30 vóór London.
     ≠ F5-JP225-ORB / A1; Asia-only daily-flat.
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
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_0340b"


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
    h, l, c = g["high"].max(), g["low"].min(), g["close"].last()
    prev_c = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.rolling(n, min_periods=n).mean().shift(1)
    return {d: float(v) for d, v in atr.items() if pd.notna(v) and v > 0}


def bar_at(g, day0, hh, mm):
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


def sim_open_reclaim(g, atr_map):
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 15, 30)
    b15 = bar_at(g, day0, 15, 45)
    b30 = bar_at(g, day0, 16, 0)
    if b0 is None or b15 is None or b30 is None:
        return None
    p_open = float(b0["open"])
    p15 = float(b15["close"])
    entry = float(b30["close"])
    if p_open <= 0:
        return None
    drive1 = 1e4 * (p15 - p_open) / p_open
    atr_bp = 1e4 * atr / p_open
    if abs(drive1) < 0.20 * atr_bp:
        return None
    # reclaim: 16:00 close back through open opposite to first drive
    if drive1 > 0 and entry < p_open:
        side = -1  # failed upside drive → short
    elif drive1 < 0 and entry > p_open:
        side = 1
    else:
        return None
    win = g[(g["time"] >= day0 + pd.Timedelta(hours=15, minutes=30)) &
            (g["time"] <= day0 + pd.Timedelta(hours=16, minutes=0))]
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    # target: beyond open by 0.5× first-drive magnitude (positive skew via stop tight)
    drive_px = abs(p15 - p_open)
    if side == 1:
        stop = wlo - 0.10 * wr
        target = p_open + 0.50 * drive_px
    else:
        stop = whi + 0.10 * wr
        target = p_open - 0.50 * drive_px
    after = g[(g["time"] > day0 + pd.Timedelta(hours=16, minutes=0)) &
              (g["time"] <= day0 + pd.Timedelta(hours=17, minutes=30))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "drive1": drive1, "atr_bp": atr_bp}


def sim_ger_mid_fade(g, atr_map):
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b_open = bar_at(g, day0, 9, 0)
    b_entry = bar_at(g, day0, 13, 0)
    if b_open is None or b_entry is None:
        return None
    p_open = float(b_open["open"])
    entry = float(b_entry["close"])
    if p_open <= 0:
        return None
    morn_bp = 1e4 * (entry - p_open) / p_open
    atr_bp = 1e4 * atr / p_open
    if abs(morn_bp) < 0.45 * atr_bp:
        return None
    side = -1 if morn_bp > 0 else 1
    win = g[(g["time"] >= day0 + pd.Timedelta(hours=9, minutes=0)) &
            (g["time"] <= day0 + pd.Timedelta(hours=13, minutes=0))]
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    if side == 1:
        stop = wlo - 0.15 * wr
        target = p_open
    else:
        stop = whi + 0.15 * wr
        target = p_open
    after = g[(g["time"] > day0 + pd.Timedelta(hours=13, minutes=0)) &
              (g["time"] <= day0 + pd.Timedelta(hours=15, minutes=0))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "morn_bp": morn_bp, "atr_bp": atr_bp}


def sim_jp_tokyo_fade(g, atr_map):
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b_open = bar_at(g, day0, 1, 0)  # Tokyo cash ~01:00 AMS winter-ish proxy on CFD
    b_entry = bar_at(g, day0, 4, 0)
    if b_open is None or b_entry is None:
        return None
    p_open = float(b_open["open"])
    entry = float(b_entry["close"])
    if p_open <= 0:
        return None
    ext_bp = 1e4 * (entry - p_open) / p_open
    atr_bp = 1e4 * atr / p_open
    if abs(ext_bp) < 0.45 * atr_bp:
        return None
    side = -1 if ext_bp > 0 else 1
    win = g[(g["time"] >= day0 + pd.Timedelta(hours=1, minutes=0)) &
            (g["time"] <= day0 + pd.Timedelta(hours=4, minutes=0))]
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    if side == 1:
        stop = wlo - 0.15 * wr
        target = p_open
    else:
        stop = whi + 0.15 * wr
        target = p_open
    after = g[(g["time"] > day0 + pd.Timedelta(hours=4, minutes=0)) &
              (g["time"] <= day0 + pd.Timedelta(hours=7, minutes=30))]
    out = walk_exit(after, side, entry, stop, target)
    if out is None:
        return None
    exit_px, reason = out
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "bruto_bp": bruto_bp, "reason": reason,
            "ext_bp": ext_bp, "atr_bp": atr_bp}


def run_idea(name, symbols_rt, sim_fn):
    rows, per = [], []
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
        per.append({"idea": name, "symbol": sym, "n": n, "mean_bruto_bp": mean,
                    "gate_3x_rt": gate, "rt": rt, "pass": bool(n >= 30 and mean >= gate),
                    "skew": float(d["bruto_bp"].skew()) if n > 2 else float("nan")})
        rows.extend(sym_rows)
    all_df = pd.DataFrame(rows)
    n = len(all_df)
    mean = float(all_df["bruto_bp"].mean()) if n else float("nan")
    if n:
        w = all_df.groupby("symbol").size()
        w_rt = sum(w[s] * symbols_rt[s] for s in w.index) / n
        gate_p = 3.0 * w_rt
    else:
        w_rt = gate_p = float("nan")
    summary = {
        "idea": name, "n_pooled": n, "mean_bruto_bp": mean, "weighted_rt": w_rt,
        "gate_3x_wrt": gate_p, "pass_pooled_n150": bool(n >= 150 and mean >= gate_p),
        "mean_ge_gate": bool(n >= 1 and mean >= gate_p) if n else False,
        "per_symbol": per, "skew": float(all_df["bruto_bp"].skew()) if n > 2 else float("nan"),
    }
    return summary, all_df


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ideas = [
        ("OPEN_RECLAIM", {"US30cash": 0.45, "US100cash": 0.66}, sim_open_reclaim),
        ("GER_MID_FADE", {"GER40cash": 0.72}, sim_ger_mid_fade),
        ("JP_TOKYO_FADE", {"JP225cash": 1.51}, sim_jp_tokyo_fade),
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
    lines = ["# Strateeg-2 D-092.1 pre-screens cycle_0340b — 2026-10-01 ~03:50 Europe/Amsterdam", "",
             "Train 2021–2023. Gate mean≥3×RT and N≥150. Reserve untouched.", "",
             "| Idee | N | mean bruto | gate | skew | PASS? |",
             "|------|--:|----------:|-----:|-----:|:-----:|"]
    for s in all_sum:
        lines.append(f"| {s['idea']} | {s['n_pooled']} | {s['mean_bruto_bp']:.2f} bp | {s['gate_3x_wrt']:.2f} bp | {s['skew']:.2f} | {'PASS' if s['pass_pooled_n150'] else 'FAIL'} |")
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print("WROTE", OUT)

if __name__ == "__main__":
    main()
