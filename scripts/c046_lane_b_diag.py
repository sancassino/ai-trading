#!/usr/bin/env python3
"""C-046 — absorb main v106 + Faraday 0019de4; Lane-B diag N168/N169 (0 CTO trials).

Faraday tip 0019de4 (~00:03 CEST 2026-10-04): S2 885090b cycle_2344 LQD/EWY →
N166 FAIL_CLONE (HYG) / N167 FAIL; absorb C-045; OPEN N168 US30_EUROPE_INVENTORY_FADE (CK)
/ N169 GBPUSD_LONDON_FIX_RESIDUAL_FADE (CL). N166/N167 already D-092.1 screened — not re-run.
Main NEXT_STEPS v106 (03ac200) still lists OPEN empty / Faraday tip 218eb11 — CTO absorbs
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
OUT = ROOT / "results/cto/c046_absorb_v106_n168_n169"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")
# Honest COSTS_FTMO.csv
RT_US30 = 0.45
RT_GBPUSD = 0.70
GATE_168 = 1.35  # 3.0 * RT_US30
GATE_169 = 2.10  # 3.0 * RT_GBPUSD
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
    """Return (pnls, sides, days, meta) for impulse-fade.
    sig_hm = (h0, m0, h1, m1) signal window start→end; entry at end bar; exit_hm = (xh, xm).
    """
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
        side = -1 if move > 0 else 1  # fade
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

    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    us500 = load_m5("data/m5gz/US500cash.csv.gz")
    us100 = load_m5("data/m5gz/US100cash.csv.gz")
    gbpusd = load_m5("data/m5gz/GBPUSD.csv.gz")
    eurusd = load_m5("data/m5gz/EURUSD.csv.gz")
    audusd = load_m5("data/m5gz/AUDUSD.csv.gz")

    # N168: US30 Europe inventory fade — impulse 09:00→12:00, fade, flat 15:00; thr ±25
    p168, s168, d168, m168 = screen_fade(us30, 25.0, (9, 0, 12, 0), (15, 0))
    # Same-window twins: US500 / US100 09:00→12:00 fade flat 15:00 (VOORSTEL future clone bar)
    # Also peer shapes: N20 = US30 PM continuation 18:00–21:00 (opposite window — check for completeness
    # but not same-window); N87 gap at cash open; N162 cash-close — different windows, so only
    # same-window index twins + a N20-style PM window as non-clone reference.
    p500, s500, d500, _ = screen_fade(us500, 25.0, (9, 0, 12, 0), (15, 0))
    p100, s100, d100, _ = screen_fade(us100, 25.0, (9, 0, 12, 0), (15, 0))
    # N20-like: US30 PM continuation window (not fade) — VOORSTEL says FAIL_CLONE if agree/cover vs N20;
    # N20 is continuation 18:00–21:00. For fade-vs-continuation sign agree we compare fade sides vs
    # a PM impulse-continuation side on same days when both fire — use PM impulse 18:00→20:00 as proxy.
    p_n20, s_n20, d_n20, _ = screen_fade(us30, 25.0, (18, 0, 20, 0), (21, 0))  # fade proxy of PM window
    # N162-like cash-close: 15:30→17:00 fade flat 21:00
    p_n162, s_n162, d_n162, _ = screen_fade(us30, 25.0, (15, 30, 17, 0), (21, 0))
    # N87-like gap: use 15:30 open bar vs prior close is hard without overnight — skip; VOORSTEL bars
    # N87 as different entry (cash open). Same-window twins are the binding clone bar.
    cand168 = sign_series(d168, s168)
    twin500 = clone_check(cand168, sign_series(d500, s500), "US500_europe_same_window_twin")
    twin100 = clone_check(cand168, sign_series(d100, s100), "US100_europe_same_window_twin")
    peer_n20 = clone_check(cand168, sign_series(d_n20, s_n20), "US30_PM_window_N20_proxy")
    peer_n162 = clone_check(cand168, sign_series(d_n162, s_n162), "US30_cash_close_N162_proxy")
    clones168 = [c["peer"] for c in (twin500, twin100, peer_n20, peer_n162) if c["clone"]]

    r168 = trade_stats(
        p168, GATE_168, "N168_US30_EUROPE_INVENTORY_FADE",
        notes=(
            f"NEW_FAMILY CK; US30cash impulse 09:00→12:00 fade ±25bp; "
            f"entry@12:00 flat 15:00; gate=3×{RT_US30}={GATE_168} (COSTS honest); "
            f"Europe session-flat before cash open; ≠ N20/N87/N162; twins US500/US100 same-window"
        ),
        years=years_from(p168, d168),
        n_long=int(sum(1 for s in s168 if s > 0)),
        n_short=int(sum(1 for s in s168 if s < 0)),
        meta={
            **m168,
            "session": "signal 09:00→12:00 entry at 12:00 flat 15:00 CET",
            "swap_bp": 0,
            "rt": RT_US30,
            "gate_source": "COSTS_FTMO.csv US30cash RT 0.45 × 3",
        },
        clone_hits=clones168,
    )
    r168["clone_detail"] = [twin500, twin100, peer_n20, peer_n162]

    # N169: GBPUSD London fix residual — impulse 17:00→18:00, fade, flat 20:30; thr ±15
    p169, s169, d169, m169 = screen_fade(gbpusd, 15.0, (17, 0, 18, 0), (20, 30))
    p_eur, s_eur, d_eur, _ = screen_fade(eurusd, 15.0, (17, 0, 18, 0), (20, 30))
    p_aud, s_aud, d_aud, _ = screen_fade(audusd, 15.0, (17, 0, 18, 0), (20, 30))
    # N29-like midday: GBPUSD fade flat by 15:00 — proxy impulse 11:00→13:00 flat 15:00
    p_n29, s_n29, d_n29, _ = screen_fade(gbpusd, 15.0, (11, 0, 13, 0), (15, 0))
    # N38-like London morning cont ends 14:30 — proxy impulse 08:00→11:00 flat 14:30
    p_n38, s_n38, d_n38, _ = screen_fade(gbpusd, 15.0, (8, 0, 11, 0), (14, 30))
    cand169 = sign_series(d169, s169)
    twin_eur = clone_check(cand169, sign_series(d_eur, s_eur), "EURUSD_fix_same_window_twin")
    twin_aud = clone_check(cand169, sign_series(d_aud, s_aud), "AUDUSD_fix_same_window_twin")
    peer_n29 = clone_check(cand169, sign_series(d_n29, s_n29), "GBPUSD_midday_N29_proxy")
    peer_n38 = clone_check(cand169, sign_series(d_n38, s_n38), "GBPUSD_morning_N38_proxy")
    clones169 = [c["peer"] for c in (twin_eur, twin_aud, peer_n29, peer_n38) if c["clone"]]

    r169 = trade_stats(
        p169, GATE_169, "N169_GBPUSD_LONDON_FIX_RESIDUAL_FADE",
        notes=(
            f"NEW_FAMILY CL; GBPUSD impulse 17:00→18:00 fade ±15bp; "
            f"entry@18:00 flat 20:30; gate=3×{RT_GBPUSD}={GATE_169} (COSTS honest; not US500 2.34); "
            f"session-flat; ≠ N29/N38/N46/N163; twins EURUSD/AUDUSD same-window; no swap credit as alpha"
        ),
        years=years_from(p169, d169),
        n_long=int(sum(1 for s in s169 if s > 0)),
        n_short=int(sum(1 for s in s169 if s < 0)),
        meta={
            **m169,
            "session": "signal 17:00→18:00 entry at 18:00 flat 20:30 broker",
            "swap_bp": 0,
            "rt": RT_GBPUSD,
            "gate_source": "COSTS_FTMO.csv GBPUSD RT 0.70 × 3",
            "swap_credit_not_alpha": True,
        },
        clone_hits=clones169,
    )
    r169["clone_detail"] = [twin_eur, twin_aud, peer_n29, peer_n38]

    rows = [r168, r169]
    flat = []
    for r in rows:
        row = {k: v for k, v in r.items() if k not in ("years", "meta", "clone_detail", "clone_hits")}
        row["clone_hits"] = ";".join(r.get("clone_hits") or [])
        for y, v in (r.get("years") or {}).items():
            row[f"y{y}"] = v
        for mk, mv in (r.get("meta") or {}).items():
            row[f"meta_{mk}"] = mv
        flat.append(row)
    pd.DataFrame(flat).to_csv(OUT / "c046_family_diag.csv", index=False)

    pd.DataFrame({"day": d168, "side": s168, "pnl_bp": p168}).to_csv(OUT / "n168_trades_train.csv", index=False)
    pd.DataFrame({"day": d169, "side": s169, "pnl_bp": p169}).to_csv(OUT / "n169_trades_train.csv", index=False)

    board = {
        "c": "C-046",
        "when": "2026-10-04 ~00:05 Europe/Amsterdam",
        "absorb": {
            "main": "03ac200 NEXT_STEPS v106 (Manager ~23:37; C-045 N164/N165 DIAG_FAIL; OPEN empty; TRIAL 471; Faraday tip still 218eb11)",
            "faraday": "0019de4 — S2 885090b; N166 FAIL_CLONE (HYG) / N167 FAIL; absorb C-045; OPEN N168 US30_EUROPE_INVENTORY_FADE CK / N169 GBPUSD_LONDON_FIX_RESIDUAL_FADE CL",
            "u2": "c5a0a4d D-090 IDLE cycle 23:45; absorb v106; hold TRIAL 471; no live PREREG",
            "s2": "885090b cycle_2344 LQD+EWY packed; Lane-B mapped → N166 FAIL_CLONE / N167 FAIL",
            "prior_cto": "71d3b5e C-045 N164/N165 DIAG_FAIL; OPEN empty",
            "ceo": "7cb6731 no new D-* after D-104",
        },
        "faraday_n166_n167": {
            "N166": "FAIL_CLONE HYG mom_confirm agree 0.95 cover 0.78; mean +7.59 ≥ gate 2.34; no PREREG",
            "N167": "FAIL mean −1.10 < gate 1.89; no PREREG",
            "note": "Faraday D-092.1 already screened; CTO does not re-screen",
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
            "bar N75–N167 + LQD/IG-credit / HYG twin / EWY→EUR + prior; "
            "N168/N169 = NEW_FAMILY CK/CL"
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

    (OUT / "c046_board.json").write_text(json.dumps(board, indent=2, default=_ser))
    lines = [
        "# C-046 — absorb main v106 + Faraday 0019de4; Lane-B diag N168/N169 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 471. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.",
        "",
        "## Absorb",
        "",
        "- Main `03ac200` NEXT_STEPS **v106** (~23:37): C-045 N164/N165 DIAG_FAIL; OPEN empty; U2 IDLE TRIAL 471; Faraday tip still `218eb11`.",
        "- Faraday `0019de4` (~00:03): S2 `885090b` → **N166 FAIL_CLONE** (HYG) / **N167 FAIL**; absorb C-045; OPEN **N168 US30_EUROPE_INVENTORY_FADE CK** / **N169 GBPUSD_LONDON_FIX_RESIDUAL_FADE CL**.",
        "- U2 `c5a0a4d` (~23:45): IDLE/HOLD absorb v106; TRIAL **471**; no live PREREG.",
        "- S2 `885090b` LQD+EWY consumed via N166/N167. Prior CTO C-045 `71d3b5e`. CEO `7cb6731` no new D-*. Reserve 2025+ untouched.",
        "",
        "## Faraday N166/N167 (not re-screened)",
        "",
        "- **N166** LQD→US500: FAIL_CLONE (HYG agree 0.95 cover 0.78); mean +7.59 ≥ 2.34 — NEW_FAMILY CI dead.",
        "- **N167** EWY→EURUSD: FAIL (mean −1.10 < 1.89) — NEW_FAMILY CJ dead.",
        "",
        "## Lane-B diagnostic N168/N169 (train 2021–2023; ≤2024; 0 CTO trials)",
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
        f"- N168 vs US500 europe same-window: {twin500}",
        f"- N168 vs US100 europe same-window: {twin100}",
        f"- N168 vs US30 PM N20-proxy: {peer_n20}",
        f"- N168 vs US30 cash-close N162-proxy: {peer_n162}",
        f"- N169 vs EURUSD fix same-window: {twin_eur}",
        f"- N169 vs AUDUSD fix same-window: {twin_aud}",
        f"- N169 vs GBPUSD midday N29-proxy: {peer_n29}",
        f"- N169 vs GBPUSD morning N38-proxy: {peer_n38}",
        "",
        "### Notes",
        "",
        "- N168: US30cash Europe inventory impulse 09:00→12:00 fade ±25 bp; entry@12:00 flat 15:00; gate=1.35 (3×RT 0.45); NEW_FAMILY CK.",
        "- N169: GBPUSD London-fix residual impulse 17:00→18:00 fade ±15 bp; entry@18:00 flat 20:30; gate=2.10 (3×RT 0.70; not US500 2.34); NEW_FAMILY CL.",
        "- Formal OPEN after this cycle depends on DIAG verdicts.",
        "- No thr-grid / no overnight / no soft gate / no twin remap / no 2025+.",
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
    (OUT / "c046_report.md").write_text("\n".join(lines) + "\n")

    print(json.dumps({r["label"]: {"verdict": r["verdict"], "n": r["n"], "mean": r["mean_bp"], "gate": r["gate_bp"], "day_t": r["day_t"], "clones": r["clone_hits"], "years": r["years"], "clone_detail": r.get("clone_detail")} for r in rows}, indent=2, default=_ser))
    print("promote:", promote)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
