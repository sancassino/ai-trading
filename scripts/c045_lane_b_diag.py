#!/usr/bin/env python3
"""C-045 — absorb main v105 + Faraday 218eb11; Lane-B diag N164/N165 (0 CTO trials).

Faraday tip 218eb11 (~23:23 CEST): absorb C-044 N161 FAIL_T + N162/N163 DIAG_FAIL_CLONE;
OPEN N164 US2000_NY_IMPULSE_FADE (CG) / N165 EURCHF_LONDON_HAVEN_FADE (CH).
Main NEXT_STEPS v105 (31af9f2) still lists OPEN empty / Faraday tip 7c1a880 — CTO absorbs
newer Faraday OPEN independently.
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
OUT = ROOT / "results/cto/c045_absorb_v105_n164_n165"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")
RT_US2000 = 3.14  # est; not in COSTS_FTMO — U2 remeasure before PREREG
RT_EURCHF = 1.15  # est; not in COSTS_FTMO — U2 remeasure before PREREG
GATE_164 = 3.0 * RT_US2000  # 9.42 → VOORSTEL says 9.43 (3×3.14 rounded)
GATE_165 = 3.0 * RT_EURCHF  # 3.45
# Use VOORSTEL stated gates exactly
GATE_164 = 9.43
GATE_165 = 3.45
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

    us2000 = load_m5("data/m5gz/US2000cash.csv.gz")
    us500 = load_m5("data/m5gz/US500cash.csv.gz")
    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    us100 = load_m5("data/m5gz/US100cash.csv.gz")
    eurchf = load_m5("data/m5gz/EURCHF.csv.gz")
    gbpchf = load_m5("data/m5gz/GBPCHF.csv.gz")
    usdchf = load_m5("data/m5gz/USDCHF.csv.gz")
    audchf = load_m5("data/m5gz/AUDCHF.csv.gz")

    # N164: US2000 15:30→17:00 fade ±35, flat 21:00
    p164, s164, d164, m164 = screen_fade(us2000, 35.0, (15, 30, 17, 0), (21, 0))
    # Same-window twins BARRED: US500 / US100 / US30 15:30→17:00 fade (use same thr scale? VOORSTEL says
    # future clone bar vs same-window fade — use thr 35 for index twins for apples-to-apples sign agree;
    # also check thr-25 large-cap scale as sensitivity is not needed for clone — same threshold family).
    p500, s500, d500, _ = screen_fade(us500, 35.0, (15, 30, 17, 0), (21, 0))
    p30, s30, d30, _ = screen_fade(us30, 35.0, (15, 30, 17, 0), (21, 0))
    p100, s100, d100, _ = screen_fade(us100, 35.0, (15, 30, 17, 0), (21, 0))
    cand164 = sign_series(d164, s164)
    twin500 = clone_check(cand164, sign_series(d500, s500), "US500_same_window_twin_BARRED")
    twin30 = clone_check(cand164, sign_series(d30, s30), "US30_same_window_twin_BARRED")
    twin100 = clone_check(cand164, sign_series(d100, s100), "US100_same_window_twin_BARRED")
    clones164 = [c["peer"] for c in (twin500, twin30, twin100) if c["clone"]]

    r164 = trade_stats(
        p164, GATE_164, "N164_US2000_NY_IMPULSE_FADE",
        notes=(
            f"NEW_FAMILY CG; US2000cash impulse 15:30→17:00 fade ±35bp; "
            f"entry@17:00 flat 21:00; gate=3×{RT_US2000}est={GATE_164} (not in COSTS); "
            f"session-flat; ≠ N119/N162/N92/N161; twins US500/US30/US100 same-window BARRED"
        ),
        years=years_from(p164, d164),
        n_long=int(sum(1 for s in s164 if s > 0)),
        n_short=int(sum(1 for s in s164 if s < 0)),
        meta={**m164, "session": "signal 15:30→17:00 entry at 17:00 flat 21:00 CET", "swap_bp": 0, "rt_est": RT_US2000},
        clone_hits=clones164,
    )
    r164["clone_detail"] = [twin500, twin30, twin100]

    # N165: EURCHF 08:00→11:30 fade ±15, flat 15:00
    p165, s165, d165, m165 = screen_fade(eurchf, 15.0, (8, 0, 11, 30), (15, 0))
    p_gbp, s_gbp, d_gbp, _ = screen_fade(gbpchf, 15.0, (8, 0, 11, 30), (15, 0))
    p_usd, s_usd, d_usd, _ = screen_fade(usdchf, 15.0, (8, 0, 11, 30), (15, 0))
    p_aud, s_aud, d_aud, _ = screen_fade(audchf, 15.0, (8, 0, 11, 30), (15, 0))
    cand165 = sign_series(d165, s165)
    twin_gbp = clone_check(cand165, sign_series(d_gbp, s_gbp), "GBPCHF_same_window_twin_BARRED")
    twin_usd = clone_check(cand165, sign_series(d_usd, s_usd), "USDCHF_same_window_twin_BARRED")
    twin_aud = clone_check(cand165, sign_series(d_aud, s_aud), "AUDCHF_same_window_twin_BARRED")
    clones165 = [c["peer"] for c in (twin_gbp, twin_usd, twin_aud) if c["clone"]]

    r165 = trade_stats(
        p165, GATE_165, "N165_EURCHF_LONDON_HAVEN_FADE",
        notes=(
            f"NEW_FAMILY CH; EURCHF impulse 08:00→11:30 fade ±15bp; "
            f"entry@11:30 flat 15:00; gate=3×{RT_EURCHF}est={GATE_165} (not in COSTS); "
            f"Europe session-flat; ≠ N104/CADCHF/N163/N151; twins GBPCHF/USDCHF/AUDCHF BARRED"
        ),
        years=years_from(p165, d165),
        n_long=int(sum(1 for s in s165 if s > 0)),
        n_short=int(sum(1 for s in s165 if s < 0)),
        meta={**m165, "session": "signal 08:00→11:30 entry at 11:30 flat 15:00 CET", "swap_bp": 0, "rt_est": RT_EURCHF},
        clone_hits=clones165,
    )
    r165["clone_detail"] = [twin_gbp, twin_usd, twin_aud]

    rows = [r164, r165]
    flat = []
    for r in rows:
        row = {k: v for k, v in r.items() if k not in ("years", "meta", "clone_detail", "clone_hits")}
        row["clone_hits"] = ";".join(r.get("clone_hits") or [])
        for y, v in (r.get("years") or {}).items():
            row[f"y{y}"] = v
        for mk, mv in (r.get("meta") or {}).items():
            row[f"meta_{mk}"] = mv
        flat.append(row)
    pd.DataFrame(flat).to_csv(OUT / "c045_family_diag.csv", index=False)

    pd.DataFrame({"day": d164, "side": s164, "pnl_bp": p164}).to_csv(OUT / "n164_trades_train.csv", index=False)
    pd.DataFrame({"day": d165, "side": s165, "pnl_bp": p165}).to_csv(OUT / "n165_trades_train.csv", index=False)

    board = {
        "c": "C-045",
        "when": "2026-10-03 ~23:30 Europe/Amsterdam",
        "absorb": {
            "main": "31af9f2 NEXT_STEPS v105 (Manager ~23:09; C-044 N162/N163 DIAG_FAIL_CLONE; OPEN empty; TRIAL 471; Faraday tip still 7c1a880)",
            "faraday": "218eb11 — absorb C-044; OPEN N164 US2000_NY_IMPULSE_FADE CG / N165 EURCHF_LONDON_HAVEN_FADE CH; commit n162_n163_prescreen FAIL_CLONE",
            "u2": "69c1a34 D-090 IDLE cycle 23:15; hold TRIAL 471; tip after 03a1a1d N161 FAIL_T; no live PREREG",
            "s2": "51b24bf cycle_0147 XLK_TECH consumed via N161 FAIL_T",
            "prior_cto": "02ed02b C-044 N162/N163 DIAG_FAIL_CLONE; OPEN empty",
            "ceo": "7cb6731 no new D-* after D-104",
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
            "bar N75–N165 + US2000 NY-impulse / EURCHF London-haven + US500/US30/US100 same-window "
            "+ GBPCHF/USDCHF/AUDCHF same-window twins + prior; N164/N165 = NEW_FAMILY CG/CH"
        ),
    }

    def _ser(obj):
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, pd.Timestamp):
            return str(obj)
        raise TypeError(type(obj))

    (OUT / "c045_board.json").write_text(json.dumps(board, indent=2, default=_ser))
    lines = [
        "# C-045 — absorb main v105 + Faraday 218eb11; Lane-B diag N164/N165 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 471. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.",
        "",
        "## Absorb",
        "",
        "- Main `31af9f2` NEXT_STEPS **v105** (~23:09): C-044 N162/N163 DIAG_FAIL_CLONE; OPEN empty; U2 IDLE TRIAL 471; Faraday tip still `7c1a880`.",
        "- Faraday `218eb11` (~23:23): absorb C-044; OPEN **N164 US2000_NY_IMPULSE_FADE CG** / **N165 EURCHF_LONDON_HAVEN_FADE CH**; commit n162_n163_prescreen (FAIL_CLONE both).",
        "- U2 `69c1a34` (~23:15): IDLE/HOLD absorb v105; TRIAL **471**; no live PREREG (after N161 FAIL_T `03a1a1d`).",
        "- S2 `51b24bf` XLK consumed. Prior CTO C-044 `02ed02b`. CEO `7cb6731` no new D-*. Reserve 2025+ untouched.",
        "",
        "## Lane-B diagnostic N164/N165 (train 2021–2023; ≤2024; 0 CTO trials)",
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
        f"- N164 vs US500 same-window: {twin500}",
        f"- N164 vs US30 same-window: {twin30}",
        f"- N164 vs US100 same-window: {twin100}",
        f"- N165 vs GBPCHF same-window: {twin_gbp}",
        f"- N165 vs USDCHF same-window: {twin_usd}",
        f"- N165 vs AUDCHF same-window: {twin_aud}",
        "",
        "### Notes",
        "",
        "- N164: US2000cash NY-hour impulse 15:30→17:00 fade ±35 bp; entry@17:00 flat 21:00; gate=9.43 (3×RT_est 3.14; not in COSTS); NEW_FAMILY CG.",
        "- N165: EURCHF London-AM impulse 08:00→11:30 fade ±15 bp; entry@11:30 flat 15:00; gate=3.45 (3×RT_est 1.15; not in COSTS); NEW_FAMILY CH.",
        "- Formal OPEN after this cycle = **empty** (neither DIAG_PASS) OR promote if DIAG_PASS.",
        "- No thr-grid / no overnight / no soft gate / no twin remap.",
        "",
        "## Verdict summary",
        "",
    ]
    for r in rows:
        lines.append(f"- **{r['label']}**: **{r['verdict']}** (n={r['n']}, mean={r['mean_bp']}, gate={r['gate_bp']})")
    promote = board["promote_to_prereg"]
    lines.append("")
    lines.append(f"**Promote to PREREG:** {promote if promote else 'none'}.")
    lines.append("")
    (OUT / "c045_report.md").write_text("\n".join(lines) + "\n")

    print(json.dumps({r["label"]: {"verdict": r["verdict"], "n": r["n"], "mean": r["mean_bp"], "gate": r["gate_bp"], "clones": r["clone_hits"]} for r in rows}, indent=2))
    print("promote:", promote)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
