#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N174 COFFEE 1d reversal + N175 COCOA open-hour continuation.

Soft commodities. Not CORN. Not the DBA basket. Not a rewrite of N172/N173.
Gates are 3× the measured round-trip in origin/main COSTS_FTMO_alle.csv
(these names are absent from COSTS_FTMO.csv). Commission is 0 and marked
NIET bevestigd, so the gate is a spread floor, not a guessed number.
D1 history starts 2023-01-19 (<5y): a cost-gate pass would still not be PASS.

No thr-grid. Clone bar: agree>=0.90 OR (agree>=0.85 AND cover>=0.70)
OR |z|>=0.90 OR (agree>=0.98 and n_both>=30).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n174_n175_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70
AGREE_HARD = 0.90
Z_CLONE = 0.90
AGREE_EXACT = 0.98
EXACT_MIN_N = 30

# origin/main COSTS_FTMO_alle.csv rondreis_bp (spread med; commission 0 unconfirmed)
COSTS_RT = {"COFFEE.c": 9.05, "COCOA.c": 19.68}
GATE_174 = 3.0 * COSTS_RT["COFFEE.c"]  # 27.15
GATE_175 = 3.0 * COSTS_RT["COCOA.c"]  # 59.04
HIST_START = pd.Timestamp("2023-01-19")
ASOF = pd.Timestamp("2026-10-04")
HIST_YEARS = round(float((ASOF - HIST_START).days) / 365.25, 2)


def load_m5(sym: str) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    df = pd.read_csv(path, sep=";", compression="gzip", comment="#", usecols=["time", "close"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[df["time"] <= TRAIN_END].reset_index(drop=True)
    return df[["time", "close"]]


def load_daily_close(sym: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    df = pd.read_csv(pd.io.common.StringIO("\n".join(body)), sep=";")
    s = pd.Series(
        pd.to_numeric(df["adjclose"], errors="coerce").values,
        index=pd.to_datetime(df["date"]),
    )
    return s.dropna().sort_index()


def daily_last(df: pd.DataFrame) -> pd.Series:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    s = d.groupby("day")["close"].last().sort_index()
    return s[s > 0]


def by_day(df: pd.DataFrame) -> dict:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    return {day: g for day, g in d.groupby("day", sort=False)}


def first_bar(g, day, h, m=0, span=20):
    t0 = day + pd.Timedelta(hours=h, minutes=m)
    exact = g[g["time"] == t0]
    if len(exact):
        return exact.iloc[0]
    win = g[(g["time"] >= t0) & (g["time"] <= t0 + pd.Timedelta(minutes=span))]
    return win.iloc[0] if len(win) else None


def last_le(g, day, h, m=0):
    t = day + pd.Timedelta(hours=h, minutes=m)
    win = g[(g["time"] >= day) & (g["time"] <= t)]
    return win.iloc[-1] if len(win) else None


def px(bar):
    if bar is None:
        return None
    p = float(bar["close"])
    return p if p > 0 else None


def session_prior(df, lookback: int, fade: bool, eh, em, xh, xm):
    dc = daily_last(df)
    ret = dc / dc.shift(lookback) - 1.0
    groups = by_day(df)
    trades = []
    pos = {}
    n_sig = 0
    n_skip = 0
    for day in sorted(d for d in groups if TRAIN_START <= d <= TRAIN_END):
        prior = ret[ret.index < day].dropna()
        if prior.empty or float(prior.iloc[-1]) == 0 or not np.isfinite(prior.iloc[-1]):
            continue
        if (day - prior.index[-1]).days > 6:
            continue
        n_sig += 1
        raw = float(prior.iloc[-1])
        side = (-1.0 if raw > 0 else 1.0) if fade else (1.0 if raw > 0 else -1.0)
        g = groups[day]
        ent = first_bar(g, day, eh, em)
        ex = last_le(g, day, xh, xm)
        if ent is None or ex is None or ex["time"] <= ent["time"]:
            n_skip += 1
            continue
        p0, p1 = px(ent), px(ex)
        if p0 is None or p1 is None:
            n_skip += 1
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(prior.index[-1]).date()),
                "side": int(side),
                "prior_ret": round(raw, 6),
                "entry": str(ent["time"]),
                "exit": str(ex["time"]),
                "bruto_bp": float(side * 1e4 * (p1 / p0 - 1.0)),
            }
        )
        pos[day] = side
    meta = {
        "n_signal_days": n_sig,
        "n_skip_missing_bar": n_skip,
        "n_trades": len(trades),
        "swap_nights": 0,
        "overnight": False,
        "threshold": None,
    }
    return trades, pd.Series(pos, dtype=float).sort_index(), ret, meta


def open_hour_cont(df):
    """COCOA liquidity open 12:00→13:30 continuation, flat 17:00. Sign only."""
    groups = by_day(df)
    trades = []
    pos = {}
    n_sig = 0
    n_skip = 0
    for day in sorted(d for d in groups if TRAIN_START <= d <= TRAIN_END):
        g = groups[day]
        b0 = first_bar(g, day, 12, 0)
        b1 = first_bar(g, day, 13, 30)
        ex = last_le(g, day, 17, 0)
        p0, p_sig = px(b0), px(b1)
        if p0 is None or p_sig is None or ex is None:
            continue
        move = p_sig / p0 - 1.0
        if move == 0 or not np.isfinite(move):
            continue
        n_sig += 1
        if ex["time"] <= b1["time"]:
            n_skip += 1
            continue
        p1 = px(ex)
        if p1 is None:
            n_skip += 1
            continue
        side = 1.0 if move > 0 else -1.0
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(day).date()),
                "side": int(side),
                "prior_ret": round(float(move), 6),
                "entry": str(b1["time"]),
                "exit": str(ex["time"]),
                "bruto_bp": float(side * 1e4 * (p1 / p_sig - 1.0)),
            }
        )
        pos[day] = side
    meta = {
        "n_signal_days": n_sig,
        "n_skip_missing_bar": n_skip,
        "n_trades": len(trades),
        "swap_nights": 0,
        "overnight": False,
        "threshold": None,
    }
    return trades, pd.Series(pos, dtype=float).sort_index(), meta


def dba_combo_pos() -> pd.Series:
    s = load_daily_close("DBA")
    z = (s - s.rolling(120, min_periods=120).mean()) / s.rolling(120, min_periods=120).std(ddof=0)
    d20 = s / s.shift(20) - 1.0
    pos = pd.Series(0.0, index=s.index)
    pos[(z > 0.5) & (d20 > 0)] = 1.0
    pos[(z < -0.5) & (d20 < 0)] = -1.0
    return pos[(pos.index >= TRAIN_START) & (pos.index <= TRAIN_END)]


def clone_sign(name, cand, peer, binding=True, z_c=None, z_p=None) -> dict:
    c = cand.astype(float)
    p_raw = peer.sort_index().astype(float) if peer is not None and len(peer) else pd.Series(dtype=float)
    rows = []
    for dt, cv in c.items():
        if dt in p_raw.index:
            pv = p_raw.loc[dt]
            pv = float(pv.iloc[0] if hasattr(pv, "iloc") else pv)
        else:
            prev = p_raw[p_raw.index < dt]
            pv = float(prev.iloc[-1]) if len(prev) else 0.0
        rows.append((dt, float(cv), pv))
    both = pd.DataFrame(rows, columns=["date", "c", "p"]).set_index("date")
    active = both[both["c"] != 0]
    both_on = active[active["p"] != 0]
    agree = float((np.sign(both_on["c"]) == np.sign(both_on["p"])).mean()) if len(both_on) else None
    cover = float(len(both_on) / len(active)) if len(active) else None
    corr = None
    if z_c is not None and z_p is not None:
        zz = z_c.rename("c").to_frame().join(z_p.rename("p"), how="inner").dropna()
        zz = zz[(zz.index >= TRAIN_START) & (zz.index <= TRAIN_END)]
        if len(zz) > 30:
            corr = float(zz["c"].corr(zz["p"]))
    is_clone = False
    if corr is not None and abs(corr) >= Z_CLONE:
        is_clone = True
    if agree is not None and agree >= AGREE_HARD:
        is_clone = True
    if agree is not None and cover is not None and agree >= AGREE_CLONE and cover >= COVER_CLONE:
        is_clone = True
    if agree is not None and agree >= AGREE_EXACT and len(both_on) >= EXACT_MIN_N:
        is_clone = True
    return {
        "peer": name,
        "z_corr_train": None if corr is None else round(corr, 4),
        "sign_agree_both_active": None if agree is None else round(agree, 4),
        "both_active_over_cand": None if cover is None else round(cover, 4),
        "n_cand_active": int(len(active)),
        "n_both_active": int(len(both_on)),
        "clone": bool(is_clone and binding),
        "clone_raw": bool(is_clone),
        "binding": binding,
    }


def verdict(trades, gate, rt, label, instrument, notes, short_history: bool):
    n = len(trades)
    base = {
        "id": label,
        "instrument": instrument,
        "n": n,
        "mean_bruto_bp": None,
        "netto_bp": None,
        "gate_bp": round(float(gate), 4),
        "rt_bp": rt,
        "verdict": "FAIL",
        "notes": notes,
        "short_history_blocks_pass": short_history,
        "history_years": HIST_YEARS,
    }
    if n == 0:
        base["verdict"] = "DIAG_FAIL"
        return base
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    netto = mean - rt
    if n >= MIN_N and mean >= gate and not short_history:
        v = "PASS_may_PREREG"
    elif n >= MIN_N and mean >= gate and short_history:
        v = "NO_PASS_SHORT_HISTORY"
    elif mean >= gate and n < MIN_N:
        v = "UNDERPOWERED"
    else:
        v = "FAIL"
    years = {}
    for y in (2021, 2022, 2023):
        ys = [t["bruto_bp"] for t in trades if t["date"].startswith(str(y))]
        if ys:
            years[str(y)] = round(float(np.mean(ys)), 4)
    dates = pd.to_datetime([t["date"] for t in trades])
    span = float((dates.max() - dates.min()).days) / 365.25 if len(dates) else 0.0
    base.update(
        {
            "mean_bruto_bp": round(mean, 4),
            "netto_bp": round(netto, 4),
            "median_bruto_bp": round(float(np.median(arr)), 4),
            "stress_gate_bp": round(gate * 1.5, 4),
            "stress_note": "BELOW_stress_1.5x (info only)" if mean < gate * 1.5 else "PASS_stress_informal",
            "verdict": v,
            "hit_rate": round(float((arr > 0).mean()), 4),
            "n_long": int(sum(1 for t in trades if t["side"] > 0)),
            "n_short": int(sum(1 for t in trades if t["side"] < 0)),
            "years": years,
            "trade_span_years": round(span, 2),
        }
    )
    return base


def apply_clone(summary, clones):
    hit = [k for k, v in clones.items() if v.get("clone") and v.get("binding", True)]
    summary["clone_hits"] = hit
    if hit and summary["verdict"] not in ("DIAG_FAIL",):
        summary["verdict"] = "FAIL_CLONE"
        if "CLONE" not in summary["notes"]:
            summary["notes"] += " | CLONE of " + ",".join(hit)
    return summary


def load_side_csv(path, hold_expand=None):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    if hold_expand is None:
        return pd.Series(df["side"].astype(float).values, index=df["date"]).sort_index()
    pos = {}
    for _, row in df.iterrows():
        start = row["date"]
        for k in range(hold_expand):
            pos[start + pd.Timedelta(days=k)] = float(row["side"])
    return pd.Series(pos).sort_index()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    coffee = load_m5("COFFEE.c")
    cocoa = load_m5("COCOA.c")
    t174, pos174, ret1, meta174 = session_prior(coffee, 1, True, 14, 0, 19, 0)
    t175, pos175, meta175 = open_hour_cont(cocoa)
    # same-rule cocoa 1d fade is a twin market check, not a dead id
    _t, pos_cocoa_1d, _, _ = session_prior(cocoa, 1, True, 14, 0, 19, 0)

    hist_note = (
        f"symbol_history_FTMO first_d1 2023-01-19; {HIST_YEARS}y through 2026-10-04 "
        "(<5y). Shorter-history exception: screened, cannot be PASS."
    )
    for meta, sym in ((meta174, "COFFEE.c"), (meta175, "COCOA.c")):
        meta["rt_in_costs_ftmo_csv"] = False
        meta["gate_file"] = "origin/main COSTS_FTMO_alle.csv rondreis_bp; absent from COSTS_FTMO.csv"
        meta["commission_unconfirmed"] = True
        meta["commission_bp"] = 0.0
        meta["d094a"] = hist_note
        meta["history_years"] = HIST_YEARS
        meta["symbol_list"] = f"SymbolList_FTMO.csv {sym} Agriculture"
        meta["swap_nights"] = 0
    meta174["session"] = "prior 1d return fade; entry 14:00 flat 19:00 CET"
    meta175["session"] = "open-hour 12:00→13:30 continuation; entry 13:30 flat 17:00 CET"

    p172 = load_side_csv(ROOT / "results/R2/n172_n173_prescreen/n172_trades_train.csv")
    p173 = load_side_csv(ROOT / "results/R2/n172_n173_prescreen/n173_trades_train.csv")
    p50 = load_side_csv(ROOT / "results/R2/n45_n51_prescreen/N50_trades.csv", hold_expand=10)
    dba = dba_combo_pos()

    peers_174 = {
        "N172_USOIL_5d_reversal": (p172, None, True),
        "N173_USDCAD_1d_cont": (p173, None, True),
        "N50_USOIL_TSMOM_expanded": (p50, None, True),
        "N126_DBA_z120_d20": (dba, None, True),
        "COCOA_same_1d_fade_NOT_A_DEAD_ID": (pos_cocoa_1d, None, False),
        "N175_COCOA_open_cont": (pos175, None, True),
    }
    c174 = {n: clone_sign(n, pos174, p, binding=b, z_c=ret1, z_p=z) for n, (p, z, b) in peers_174.items()}
    peers_175 = {
        "N174_COFFEE_1d_fade": (pos174, ret1, True),
        "N172_USOIL_5d_reversal": (p172, None, True),
        "N50_USOIL_TSMOM_expanded": (p50, None, True),
        "N126_DBA_z120_d20": (dba, None, True),
        "N173_USDCAD_1d_cont": (p173, None, True),
    }
    c175 = {n: clone_sign(n, pos175, p, binding=b, z_c=None, z_p=z) for n, (p, z, b) in peers_175.items()}

    s174 = verdict(
        t174, GATE_174, COSTS_RT["COFFEE.c"], "N174", "COFFEE.c",
        "COFFEE_PRIOR1D_REVERSAL fade prior-day return, session-flat 14:00→19:00; "
        f"gate 3*{COSTS_RT['COFFEE.c']}={GATE_174:.2f} from COSTS_FTMO_alle rondreis "
        "(not in COSTS_FTMO.csv; commission 0 unconfirmed, so this is a spread floor); "
        f"history {HIST_YEARS}y from 2023-01-19 <5y so PASS is blocked; "
        "not CORN, not DBA basket, not N172 5d oil reversal; NEW_FAMILY CQ",
        short_history=True,
    )
    s174["meta"] = meta174
    s174["gate_source"] = (
        "origin/main COSTS_FTMO_alle.csv COFFEE.c rondreis_bp 9.05 × 3 = 27.15; "
        "commission 0 NIET bevestigd (spread floor). Absent from COSTS_FTMO.csv."
    )
    apply_clone(s174, c174)
    s174["clone"] = c174

    s175 = verdict(
        t175, GATE_175, COSTS_RT["COCOA.c"], "N175", "COCOA.c",
        "COCOA_OPEN_HOUR_CONTINUATION 12:00→13:30 sign, entry 13:30 flat 17:00; "
        f"gate 3*{COSTS_RT['COCOA.c']}={GATE_175:.2f} from COSTS_FTMO_alle rondreis "
        "(not in COSTS_FTMO.csv; commission 0 unconfirmed, spread floor); "
        f"history {HIST_YEARS}y from 2023-01-19 <5y so PASS is blocked; "
        "not the coffee 1d fade, not CORN, not DBA, not an NY-impulse fade; NEW_FAMILY CR",
        short_history=True,
    )
    s175["meta"] = meta175
    s175["gate_source"] = (
        "origin/main COSTS_FTMO_alle.csv COCOA.c rondreis_bp 19.68 × 3 = 59.04; "
        "commission 0 NIET bevestigd (spread floor). Absent from COSTS_FTMO.csv."
    )
    apply_clone(s175, c175)
    s175["clone"] = c175

    pd.DataFrame(t174).to_csv(OUT / "n174_trades_train.csv", index=False)
    pd.DataFrame(t175).to_csv(OUT / "n175_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N174": pub(s174),
        "N175": pub(s175),
        "N174_clones": c174,
        "N175_clones": c175,
        "gates": {"N174": round(GATE_174, 4), "N175": round(GATE_175, 4)},
        "costs_rt": COSTS_RT,
        "history_years": HIST_YEARS,
        "short_history_blocks_pass": True,
        "train": "2021-01-01..2023-12-31; M5 for these names starts 2023-01-19",
        "min_n": MIN_N,
        "no_thr_grid": True,
        "trial_count_unchanged": 471,
        "not_redone": ["N172", "N173", "N170", "N171"],
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))
    md = (
        "# D-092.1 N174/N175 pre-screen (train 2021–2023)\n\n"
        "Soft singles. Not CORN. Not DBA. History from 2023-01-19 is "
        f"**{HIST_YEARS}y < 5y**, so neither result can be PASS.\n\n"
        f"- **N174 COFFEE 1d reversal**: N={s174['n']} mean={s174['mean_bruto_bp']} "
        f"netto={s174.get('netto_bp')} gate={s174['gate_bp']} → **{s174['verdict']}** "
        f"years={s174.get('years')} L/S={s174.get('n_long')}/{s174.get('n_short')} "
        f"hits={s174.get('clone_hits')}\n"
        f"- **N175 COCOA open-hour continuation**: N={s175['n']} mean={s175['mean_bruto_bp']} "
        f"netto={s175.get('netto_bp')} gate={s175['gate_bp']} → **{s175['verdict']}** "
        f"years={s175.get('years')} L/S={s175.get('n_long')}/{s175.get('n_short')} "
        f"hits={s175.get('clone_hits')}\n\n"
        "Gates are 3× COSTS_FTMO_alle rondreis (main). Commission unconfirmed, so the gate is a spread floor. "
        "No thr-grid. No 2024+ selection.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N174": pub(s174), "N175": pub(s175)}, indent=2, default=str))
    print("---174---")
    for k, v in c174.items():
        print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "n_both_active", "binding", "clone")})
    print("---175---")
    for k, v in c175.items():
        print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "n_both_active", "binding", "clone")})


if __name__ == "__main__":
    main()
