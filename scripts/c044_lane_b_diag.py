#!/usr/bin/env python3
"""C-044 — absorb main v104 + Faraday 7c1a880; Lane-B diag N162/N163 (0 CTO trials).

Faraday tip 7c1a880 (~02:02 CEST): N160 FAIL / N161 PASS→PREREG; OPEN N162 US500_CASH_CLOSE_FADE (CE)
/ N163 AUDUSD_NY_IMPULSE_FADE (CF). U2 03a1a1d then N161 FAIL_T TRIAL 471.
Main NEXT_STEPS v104 (95624bb) lists OPEN N162/N163 (VOORSTEL only; Faraday left
n162_n163_prescreen uncommitted — CTO independent diag).
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
OUT = ROOT / "results/cto/c044_absorb_v104_n162_n163"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")
RT_US500 = 0.78
RT_AUD = 1.22
GATE_162 = 3.0 * RT_US500  # 2.34
GATE_163 = 3.0 * RT_AUD  # 3.66
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70


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


def trade_stats(pnls_bp, gate_bp, label, notes="", years=None, n_long=None, n_short=None, meta=None, clone_hits=None):
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
    clones = list(clone_hits or [])
    if clones:
        verdict = "DIAG_FAIL_CLONE"
    elif n >= MIN_N and np.isfinite(mean) and mean >= gate_bp:
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
        "clone_hits": clones,
        "meta": meta or {},
    }


def screen_fade(df, thr, sig_hm, exit_hm):
    """Return (pnls, sides, days, meta) for impulse-fade."""
    groups = by_day(df)
    pnls, sides, days = [], [], []
    n_impulse = 0
    n_skip = 0
    h0, m0, h1, m1 = sig_hm
    xh, xm = exit_hm
    for day in sorted(groups):
        if day < TRAIN_START or day > TRAIN_END:
            continue
        g = groups[day]
        b0 = first_bar_in(g, day, h0, m0, 15)
        b1 = first_bar_in(g, day, h1, m1, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0, p1 = px(b0), px(b1)
        if p0 is None or p1 is None:
            continue
        move = 1e4 * (p1 / p0 - 1.0)
        if abs(move) < thr:
            continue
        n_impulse += 1
        side = -1 if move > 0 else 1
        ent = b1
        ex = last_bar_le(g, day, xh, xm)
        if ent is None or ex is None or ex["time"] <= ent["time"]:
            n_skip += 1
            continue
        if pd.Timestamp(ex["time"]).normalize() != pd.Timestamp(ent["time"]).normalize():
            n_skip += 1
            continue
        p_ent, p_ex = px(ent), px(ex)
        if p_ent is None or p_ex is None:
            n_skip += 1
            continue
        pnl = side * 1e4 * (p_ex / p_ent - 1.0)
        pnls.append(pnl)
        sides.append(side)
        days.append(pd.Timestamp(day))
    meta = {"n_impulse_days": n_impulse, "n_skip_missing_bar": n_skip, "thr_bp": thr, "n_trades": len(pnls)}
    return pnls, sides, days, meta


def sign_series(days, sides):
    return pd.Series(sides, index=pd.DatetimeIndex(days)).sort_index()


def clone_check(cand: pd.Series, peer: pd.Series, name: str):
    both = cand.index.intersection(peer.index)
    if len(cand) == 0 or len(both) == 0:
        return {"peer": name, "sign_agree": None, "cover": 0.0, "clone": False}
    agree = float((np.sign(cand.loc[both]) == np.sign(peer.loc[both])).mean())
    cover = float(len(both) / len(cand))
    return {
        "peer": name,
        "sign_agree": round(agree, 4),
        "cover": round(cover, 4),
        "n_cand": int(len(cand)),
        "n_both": int(len(both)),
        "clone": bool(agree >= AGREE_CLONE and cover >= COVER_CLONE),
    }


def years_from(pnls, days):
    by_year: dict[str, list[float]] = {"2021": [], "2022": [], "2023": []}
    for p, d in zip(pnls, days):
        y = str(pd.Timestamp(d).year)
        if y in by_year:
            by_year[y].append(p)
    return {y: round(float(np.mean(v)), 3) for y, v in by_year.items() if v}


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    us500 = load_m5("data/m5gz/US500cash.csv.gz")
    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    us100 = load_m5("data/m5gz/US100cash.csv.gz")
    aud = load_m5("data/m5gz/AUDUSD.csv.gz")
    nzd = load_m5("data/m5gz/NZDUSD.csv.gz")

    # N162: US500 19:00→20:30 fade ±25, flat 21:00
    p162, s162, d162, m162 = screen_fade(us500, 25.0, (19, 0, 20, 30), (21, 0))
    # Twin barred: same window on US30 / US100
    p30, s30, d30, _ = screen_fade(us30, 25.0, (19, 0, 20, 30), (21, 0))
    p100, s100, d100, _ = screen_fade(us100, 25.0, (19, 0, 20, 30), (21, 0))
    cand162 = sign_series(d162, s162)
    twin30 = clone_check(cand162, sign_series(d30, s30), "US30_same_window_twin_BARRED")
    twin100 = clone_check(cand162, sign_series(d100, s100), "US100_same_window_twin_BARRED")
    clones162 = [c["peer"] for c in (twin30, twin100) if c["clone"]]

    r162 = trade_stats(
        p162, GATE_162, "N162_US500_CASH_CLOSE_FADE",
        notes=(
            f"NEW_FAMILY CE; US500cash impulse 19:00→20:30 fade ±25bp; "
            f"entry@20:30 flat 21:00; gate=3×{RT_US500}={GATE_162}; session-flat; "
            f"≠ N24/N92/N87/N159; twins US30/US100 same-window BARRED"
        ),
        years=years_from(p162, d162),
        n_long=int(sum(1 for s in s162 if s > 0)),
        n_short=int(sum(1 for s in s162 if s < 0)),
        meta={**m162, "session": "signal 19:00→20:30 entry at 20:30 flat 21:00 CET", "swap_bp": 0},
        clone_hits=clones162,
    )
    r162["clone_detail"] = [twin30, twin100]

    # N163: AUD 15:30→17:00 fade ±20, flat 21:00
    p163, s163, d163, m163 = screen_fade(aud, 20.0, (15, 30, 17, 0), (21, 0))
    p_nzd, s_nzd, d_nzd, _ = screen_fade(nzd, 20.0, (15, 30, 17, 0), (21, 0))
    cand163 = sign_series(d163, s163)
    twin_nzd = clone_check(cand163, sign_series(d_nzd, s_nzd), "NZD_same_window_twin_BARRED")
    clones163 = [c["peer"] for c in (twin_nzd,) if c["clone"]]

    r163 = trade_stats(
        p163, GATE_163, "N163_AUDUSD_NY_IMPULSE_FADE",
        notes=(
            f"NEW_FAMILY CF; AUDUSD impulse 15:30→17:00 fade ±20bp; "
            f"entry@17:00 flat 21:00; gate=3×{RT_AUD}={GATE_163} (NOT US500 2.34); "
            f"session-flat; ≠ N146/N84/N91/GS02; NZD same-window twin BARRED"
        ),
        years=years_from(p163, d163),
        n_long=int(sum(1 for s in s163 if s > 0)),
        n_short=int(sum(1 for s in s163 if s < 0)),
        meta={**m163, "session": "signal 15:30→17:00 entry at 17:00 flat 21:00 CET", "swap_bp": 0, "gate_is_not_us500": True},
        clone_hits=clones163,
    )
    r163["clone_detail"] = [twin_nzd]

    rows = [r162, r163]
    flat = []
    for r in rows:
        row = {k: v for k, v in r.items() if k not in ("years", "meta", "clone_detail", "clone_hits")}
        row["clone_hits"] = ";".join(r.get("clone_hits") or [])
        for y, v in (r.get("years") or {}).items():
            row[f"y{y}"] = v
        for mk, mv in (r.get("meta") or {}).items():
            row[f"meta_{mk}"] = mv
        flat.append(row)
    pd.DataFrame(flat).to_csv(OUT / "c044_family_diag.csv", index=False)

    # trade CSVs for audit
    pd.DataFrame({"day": d162, "side": s162, "pnl_bp": p162}).to_csv(OUT / "n162_trades_train.csv", index=False)
    pd.DataFrame({"day": d163, "side": s163, "pnl_bp": p163}).to_csv(OUT / "n163_trades_train.csv", index=False)

    board = {
        "c": "C-044",
        "when": "2026-10-03 ~22:57 Europe/Amsterdam",
        "absorb": {
            "main": "95624bb NEXT_STEPS v104 (Manager ~02:07; Faraday 7c1a880 N154–N160 FAIL + N161 PASS→PREREG; U2 N161 FAIL_T TRIAL 471; OPEN N162/N163)",
            "faraday": "7c1a880 — N160 FAIL / N161 PASS→PREREG; OPEN N162/N163; prior N154–N159 FAIL/FAIL_CLONE; WT left n162_n163_prescreen uncommitted (FAIL_CLONE both)",
            "u2": "03a1a1d N161 XLK_TECH_SECTOR_STRESS FAIL_T TRIAL 470→471; IDLE/HOLD; no live PREREG",
            "s2": "51b24bf cycle_0147 XLK_TECH_SECTOR_STRESS (consumed → N161 FAIL_T)",
            "prior_cto": "c27849d C-043 N158/N159 DIAG_FAIL; OPEN note stale vs Faraday 7c1a880",
        },
        "freeze": "OFF",
        "trial_count": 471,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "track_3": "PAUSED",
        "live_prereg": None,
        "results": [
            {k: v for k, v in r.items() if k != "meta"} | {"meta": r.get("meta")}
            for r in rows
        ],
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": (
            "cost-PASS→FAIL_T streak N100…N131 + N161 (≥5); pivot ON; "
            "bar N75–N163 + US500 cash-close / AUD NY-fade + US30/US100 same-window / NZD same-window twins + prior; "
            "N162/N163 = NEW_FAMILY CE/CF"
        ),
        "agrees_faraday_uncommitted": {
            "N162": "FAIL_CLONE mean~-0.31 n=217 gate 2.34; twins US30/US100",
            "N163": "FAIL_CLONE mean~-1.67 n=296 gate 3.66; twin NZD",
        },
    }

    def _ser(obj):
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, pd.Timestamp):
            return str(obj)
        raise TypeError(type(obj))

    (OUT / "c044_board.json").write_text(json.dumps(board, indent=2, default=_ser))
    lines = [
        "# C-044 — absorb main v104 + Faraday 7c1a880; Lane-B diag N162/N163 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 471. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.",
        "",
        "## Absorb",
        "",
        "- Main `95624bb` NEXT_STEPS **v104** (~02:07): Faraday tip `7c1a880` N154–N160 FAIL + N161 PASS→PREREG; U2 `03a1a1d` N161 FAIL_T **TRIAL 471**; OPEN N162/N163; C-043.",
        "- Faraday `7c1a880` (~02:02): **N160 FAIL** (−7.15 < 15.21) / **N161 PASS→PREREG** (then FAIL_T @ U2); OPEN **N162 US500_CASH_CLOSE_FADE CE** / **N163 AUDUSD_NY_IMPULSE_FADE CF**. WT left `results/R2/n162_n163_prescreen/` uncommitted (both FAIL_CLONE).",
        "- U2 `03a1a1d` (~02:04): **N161 FAIL_T** (TRIAL **470→471**); IDLE/HOLD; no live PREREG.",
        "- S2 `51b24bf` XLK_TECH consumed via N161. Prior CTO C-043 `c27849d`: N158/N159 DIAG_FAIL. Reserve 2025+ untouched.",
        "- Catch-up: prior CTO routine ~22:25 CEST FAILED; this cycle absorbs ~21h of teammate tips.",
        "",
        "## Lane-B diagnostic N162/N163 (train 2021–2023; ≤2024; 0 CTO trials)",
        "",
        "| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | clones | Verdict |",
        "|------|--------:|--:|-----:|------:|---:|---:|----:|-------|--------|---------|",
    ]
    for r in rows:
        years = r.get("years") or {}
        ystr = "/".join(f"{y}:{years[y]}" for y in ("2021", "2022", "2023") if y in years)
        ls = f"{r.get('n_long')}/{r.get('n_short')}"
        ch = ",".join(r.get("clone_hits") or []) or "—"
        lines.append(
            f"| {r['label']} | {r['mean_bp']} | {r['n']} | {r['gate_bp']} | {r['day_t']} | "
            f"{r['h1_mean_bp']} | {r['h2_mean_bp']} | {ls} | {ystr or '—'} | {ch} | **{r['verdict']}** |"
        )
    lines += [
        "",
        "### Clone detail",
        "",
        f"- N162 vs US30 same-window: {twin30}",
        f"- N162 vs US100 same-window: {twin100}",
        f"- N163 vs NZD same-window: {twin_nzd}",
        "",
        "### Notes",
        "",
        "- N162: US500cash cash-close impulse 19:00→20:30 fade ±25 bp; entry@20:30 flat 21:00; gate=3×0.78=2.34; NEW_FAMILY CE.",
        "- N163: AUDUSD NY-hour impulse 15:30→17:00 fade ±20 bp; entry@17:00 flat 21:00; gate=3×1.22=3.66 (NOT US500 2.34); NEW_FAMILY CF.",
        "- Absorbed Faraday N154–N161 FAIL/FAIL_CLONE/FAIL_T (no re-run). Formal OPEN after this cycle = **empty**.",
        "- Agrees Faraday uncommitted WT prescreen (both FAIL_CLONE + mean < gate).",
        "- No thr-grid / no overnight / no soft gate / no twin remap / no PREREG.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c044_report.md").write_text("\n".join(lines))
    print(json.dumps({
        "results": [
            {k: r[k] for k in ("label", "n", "mean_bp", "gate_bp", "verdict", "years", "n_long", "n_short", "clone_hits")}
            for r in rows
        ]
    }, indent=2))


if __name__ == "__main__":
    main()
