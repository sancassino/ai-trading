#!/usr/bin/env python3
"""C-043 — absorb main v103 + Faraday 78ee291; Lane-B diag N158/N159 (0 CTO trials).

Faraday tip 78ee291 (~01:48 CEST): N156 FAIL / N157 FAIL; OPEN N158 USOIL_NY_IMPULSE_FADE (CA)
/ N159 GER40_EUROPE_CLOSE_FADE (CB). Prior: N154 FAIL / N155 FAIL_CLONE / N152–N153 FAIL.
Main NEXT_STEPS v103 (ddb929c) still lists OPEN N154/N155 (stale vs Faraday).
U2 c2b7720 IDLE/HOLD TRIAL 470. Diagnostic screens only until DIAG_PASS → PREREG freeze.
Reserve 2025+ untouched. Train 2021–2023; hard cut ≤2024-12-31.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c043_absorb_v103_n158_n159"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")
RT_USOIL = 3.34
RT_GER40 = 0.72
GATE_158 = 3.0 * RT_USOIL  # 10.02
GATE_159 = 3.0 * RT_GER40  # 2.16
MIN_N = 150
THR = 40.0  # impulse bp threshold frozen


def load_m5(rel: str) -> pd.DataFrame:
    with gzip.open(ROOT / rel, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)]
    df = df[df["time"] <= HARD_CUT]
    return df.reset_index(drop=True)


def first_bar_in(g: pd.DataFrame, day, h: int, m0: int = 0, span_min: int = 15):
    t0 = day + pd.Timedelta(hours=h, minutes=m0)
    t1 = t0 + pd.Timedelta(minutes=span_min)
    exact = g[g["time"] == t0]
    if len(exact):
        return exact.iloc[0]
    win = g[(g["time"] >= t0) & (g["time"] <= t1)]
    return win.iloc[0] if len(win) else None


def last_bar_le(g: pd.DataFrame, day, h: int, m0: int = 0):
    t = day + pd.Timedelta(hours=h, minutes=m0)
    win = g[g["time"] <= t]
    return win.iloc[-1] if len(win) else None


def by_day(df: pd.DataFrame) -> dict:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    return {day: g for day, g in d.groupby("day", sort=False)}


def px(bar):
    if bar is None:
        return None
    p = float(bar["close"])
    return p if p > 0 else None


def trade_stats(pnls_bp, gate_bp, label, notes="", years=None, n_long=None, n_short=None, meta=None):
    arr = np.asarray(pnls_bp, dtype=float)
    arr = arr[np.isfinite(arr)]
    n = len(arr)
    mean = float(np.mean(arr)) if n else float("nan")
    med = float(np.median(arr)) if n else float("nan")
    if n >= 2 and float(np.std(arr, ddof=1)) > 0:
        t = mean / (float(np.std(arr, ddof=1)) / math.sqrt(n))
    else:
        t = float("nan")
    half = n // 2
    m1 = float(np.mean(arr[:half])) if half else float("nan")
    m2 = float(np.mean(arr[half:])) if n - half else float("nan")
    if n >= MIN_N and np.isfinite(mean) and mean >= gate_bp:
        verdict = "DIAG_PASS"
    elif n < MIN_N and np.isfinite(mean) and mean >= gate_bp:
        verdict = "UNDERPOWERED"
    else:
        verdict = "DIAG_FAIL"
    return {
        "label": label,
        "n": n,
        "mean_bp": round(mean, 3) if n else None,
        "median_bp": round(med, 3) if n else None,
        "day_t": round(t, 3) if n >= 2 else None,
        "h1_mean_bp": round(m1, 3) if half else None,
        "h2_mean_bp": round(m2, 3) if n - half else None,
        "n_long": n_long,
        "n_short": n_short,
        "gate_bp": gate_bp,
        "verdict": verdict,
        "years": years or {},
        "notes": notes,
        "meta": meta or {},
    }


def diag_impulse_fade(
    rel: str,
    gate: float,
    label: str,
    notes: str,
    sig_h0: int,
    sig_m0: int,
    sig_h1: int,
    sig_m1: int,
    entry_h: int | None,
    entry_m: int | None,
    exit_h: int,
    exit_m: int,
    entry_is_signal_end: bool = False,
):
    """Same-day one-leg impulse fade. thr ±40 bp frozen."""
    df = load_m5(rel)
    groups = by_day(df)
    pnls = []
    sides = []
    by_year: dict[str, list[float]] = {"2021": [], "2022": [], "2023": []}
    n_impulse = 0
    n_skip = 0
    for day in sorted(groups):
        if day < TRAIN_START or day > TRAIN_END:
            continue
        g = groups[day]
        b0 = first_bar_in(g, day, sig_h0, sig_m0, 15)
        b1 = first_bar_in(g, day, sig_h1, sig_m1, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0, p1 = px(b0), px(b1)
        if p0 is None or p1 is None:
            continue
        move = 1e4 * (p1 / p0 - 1.0)
        if abs(move) < THR:
            continue
        n_impulse += 1
        side = -1 if move > 0 else 1
        if entry_is_signal_end:
            ent = b1
        else:
            ent = first_bar_in(g, day, entry_h, entry_m, 15)  # type: ignore[arg-type]
        ex = last_bar_le(g, day, exit_h, exit_m)
        if ent is None or ex is None or ex["time"] <= ent["time"]:
            n_skip += 1
            continue
        p_ent, p_ex = px(ent), px(ex)
        if p_ent is None or p_ex is None:
            n_skip += 1
            continue
        if pd.Timestamp(ex["time"]).normalize() != pd.Timestamp(ent["time"]).normalize():
            n_skip += 1
            continue
        pnl = side * 1e4 * (p_ex / p_ent - 1.0)
        pnls.append(pnl)
        sides.append(side)
        y = str(pd.Timestamp(day).year)
        if y in by_year:
            by_year[y].append(pnl)
    years = {y: round(float(np.mean(v)), 3) for y, v in by_year.items() if v}
    n_long = int(sum(1 for s in sides if s > 0))
    n_short = int(sum(1 for s in sides if s < 0))
    return trade_stats(
        pnls,
        gate,
        label,
        notes,
        years=years,
        n_long=n_long,
        n_short=n_short,
        meta={"n_impulse_days": n_impulse, "n_skip_missing_bar": n_skip, "thr_bp": THR},
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [
        diag_impulse_fade(
            "data/m5gz/USOILcash.csv.gz",
            GATE_158,
            "N158_USOIL_NY_IMPULSE_FADE",
            (
                f"NEW_FAMILY CA; USOILcash impulse 15:30→17:00 fade ±{THR}bp; "
                f"entry@17:00 flat 21:00; gate=3×{RT_USOIL}={GATE_158}; session-flat; "
                f"≠ N22/N43/N80/N98/N136/N155/CRACK"
            ),
            15, 30, 17, 0,
            None, None,
            21, 0,
            entry_is_signal_end=True,
        ),
        diag_impulse_fade(
            "data/m5gz/GER40cash.csv.gz",
            GATE_159,
            "N159_GER40_EUROPE_CLOSE_FADE",
            (
                f"NEW_FAMILY CB; GER40cash impulse 12:00→15:00 fade ±{THR}bp; "
                f"entry 15:30 flat 17:30; gate=3×{RT_GER40}={GATE_159}; session-flat; "
                f"≠ N156/N149/N154/N138/N103/N40/N21"
            ),
            12, 0, 15, 0,
            15, 30,
            17, 30,
            entry_is_signal_end=False,
        ),
    ]
    flat = []
    for r in rows:
        row = {k: v for k, v in r.items() if k not in ("years", "meta")}
        for y, v in (r.get("years") or {}).items():
            row[f"y{y}"] = v
        for mk, mv in (r.get("meta") or {}).items():
            row[f"meta_{mk}"] = mv
        flat.append(row)
    pd.DataFrame(flat).to_csv(OUT / "c043_family_diag.csv", index=False)

    board = {
        "c": "C-043",
        "when": "2026-10-03 ~01:53 Europe/Amsterdam",
        "absorb": {
            "main": "ddb929c NEXT_STEPS v103 (Manager ~01:41; Faraday tip listed 9c4ee71 OPEN N154/N155 — stale)",
            "faraday": "78ee291 — N156 FAIL / N157 FAIL; OPEN N158/N159; prior N154 FAIL / N155 FAIL_CLONE / N152–N153 FAIL",
            "u2": "c2b7720 IDLE/HOLD absorb v103; TRIAL 470; screens-only N154/N155 (no PREREG)",
            "s2": "51b24bf cycle_0147 XLK_TECH_SECTOR_STRESS COST_OK→PROMOTE (Lane-A; Strateeg may pick up)",
            "prior_cto": "d5311f9 C-042 N150/N151 DIAG_FAIL; N143 PREREG retracted",
        },
        "freeze": "OFF",
        "trial_count": 470,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "track_3": "PAUSED",
        "live_prereg": None,
        "results": [{k: v for k, v in r.items() if k != "meta"} | {"meta": r.get("meta")} for r in rows],
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": (
            "cost-PASS→FAIL_T streak N100…N131 (≥5); pivot ON; "
            "bar N75–N157 + XAU-GER/XAU-US100/US100-GER/US30-UKOIL + prior; "
            "N158/N159 = NEW_FAMILY CA/CB"
        ),
    }
    # json-safe years already plain
    def _ser(obj):
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        raise TypeError(type(obj))

    (OUT / "c043_board.json").write_text(json.dumps(board, indent=2, default=_ser))
    lines = [
        "# C-043 — absorb main v103 + Faraday 78ee291; Lane-B diag N158/N159 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 470. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.",
        "",
        "## Absorb",
        "",
        "- Main `ddb929c` NEXT_STEPS **v103** (~01:41): Faraday tip listed `9c4ee71` N138–N153 FAIL; OPEN N154/N155 — stale vs Faraday tip `78ee291`.",
        "- Faraday `78ee291` (~01:48): **N156 FAIL** (−2.46 < 4.65) / **N157 FAIL** (−1.82 < 4.47); OPEN **N158 USOIL_NY_IMPULSE_FADE CA** / **N159 GER40_EUROPE_CLOSE_FADE CB**. Prior N154 FAIL / N155 FAIL_CLONE.",
        "- U2 `c2b7720` IDLE/HOLD absorb v103; TRIAL **470**. S2 `51b24bf` XLK_TECH_SECTOR_STRESS COST_OK→PROMOTE (Lane-A feed).",
        "- Prior CTO C-042 `d5311f9`: N150/N151 DIAG_FAIL; N143 retracted. Reserve 2025+ untouched.",
        "",
        "## Lane-B diagnostic N158/N159 (train 2021–2023; ≤2024; 0 CTO trials)",
        "",
        "| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | Verdict |",
        "|------|--------:|--:|-----:|------:|---:|---:|----:|-------|---------|",
    ]
    for r in rows:
        years = r.get("years") or {}
        ystr = "/".join(f"{y}:{years[y]}" for y in ("2021", "2022", "2023") if y in years)
        ls = f"{r.get('n_long')}/{r.get('n_short')}"
        lines.append(
            f"| {r['label']} | {r['mean_bp']} | {r['n']} | {r['gate_bp']} | {r['day_t']} | "
            f"{r['h1_mean_bp']} | {r['h2_mean_bp']} | {ls} | {ystr or '—'} | **{r['verdict']}** |"
        )
    lines += [
        "",
        "### Notes",
        "",
        "- N158: USOILcash NY-hour impulse 15:30→17:00 fade ±40 bp; entry@17:00 flat 21:00; gate=3×3.34=10.02; NEW_FAMILY CA.",
        "- N159: GER40cash Europe-close impulse 12:00→15:00 fade ±40 bp; entry 15:30 flat 17:30; gate=3×0.72=2.16; NEW_FAMILY CB.",
        "- Absorbed Faraday N152–N157 FAIL/FAIL_CLONE (no re-run). Formal OPEN after this cycle = empty if both DIAG_FAIL.",
        "- DIAG_PASS → CTO freezes PREREG for U2; else drop / Strateeg refill ≥2 NEW_FAMILY (D-094). S2 XLK available as Lane-A feed.",
        "- No thr-grid / no overnight / no soft gate / no second-leg remap.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c043_report.md").write_text("\n".join(lines))
    print(json.dumps({"results": [{k: r[k] for k in ("label", "n", "mean_bp", "gate_bp", "verdict", "years", "n_long", "n_short")} for r in rows]}, indent=2))


if __name__ == "__main__":
    main()
