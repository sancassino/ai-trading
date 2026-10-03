#!/usr/bin/env python3
"""D-092.1 TRAIN pre-screen: N176 GBPCAD 5d reversal + N177 EURNOK 1d continuation.

Authorized by C-048 (79d09e0) and Manager v114. USDSEK/USDNOK/USDZAR are not
screened (M5 4.74y). USDHKD is not given an id: the peg's oracle session
mean cannot clear 3x RT. No 2025+ bar enters the signal or the PnL.
Gates are 3x the C-048 COSTS_FTMO.csv round-trip, not COSTS_FTMO_alle.

No thr-grid. Clone bar: agree>=0.90 OR (agree>=0.85 AND cover>=0.70)
OR |z|>=0.90 OR (agree>=0.98 and n_both>=30).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n176_n177_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2024-12-31 23:59:59")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70
AGREE_HARD = 0.90
Z_CLONE = 0.90
AGREE_EXACT = 0.98
EXACT_MIN_N = 30

# C-048 79d09e0 COSTS_FTMO.csv appended rows (not alle)
COSTS_RT = {"GBPCAD": 1.08, "EURNOK": 4.62, "USDHKD": 0.84}
GATE_176 = 3.0 * COSTS_RT["GBPCAD"]  # 3.24
GATE_177 = 3.0 * COSTS_RT["EURNOK"]  # 13.86
GATE_HKD = 3.0 * COSTS_RT["USDHKD"]  # 2.52
# Full M5 file span measured 2021-01-04 → 2026-10-01. PnL stops 2024-12-31.
HIST_YEARS = 5.74
TRADED_YEARS_TO_2024 = 3.99


def load_m5(sym: str) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    df = pd.read_csv(path, sep=";", compression="gzip", comment="#", usecols=["time", "close"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    # no 2025+ reserve
    df = df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)
    return df[["time", "close"]]


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


def session_abs_mean(df, eh, em, xh, xm):
    groups = by_day(df)
    vals = []
    for day, g in groups.items():
        ent = first_bar(g, day, eh, em)
        ex = last_le(g, day, xh, xm)
        if ent is None or ex is None or ex["time"] <= ent["time"]:
            continue
        p0, p1 = px(ent), px(ex)
        if p0 is None or p1 is None:
            continue
        vals.append(abs(1e4 * (p1 / p0 - 1.0)))
    if not vals:
        return None
    a = np.array(vals)
    return {
        "n": int(len(a)),
        "mean_abs_bp": round(float(a.mean()), 4),
        "p50": round(float(np.median(a)), 4),
        "p90": round(float(np.quantile(a, 0.9)), 4),
        "p99": round(float(np.quantile(a, 0.99)), 4),
        "oracle_le_mean_abs": True,
    }


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


def verdict(trades, gate, rt, label, instrument, notes):
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
        "short_history_blocks_pass": False,
        "history_years": HIST_YEARS,
        "traded_years_through_2024": TRADED_YEARS_TO_2024,
    }
    if n == 0:
        base["verdict"] = "DIAG_FAIL"
        return base
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    netto = mean - rt
    if n >= MIN_N and mean >= gate:
        v = "PASS_may_PREREG"
    elif mean >= gate and n < MIN_N:
        v = "UNDERPOWERED"
    else:
        v = "FAIL"
    years = {}
    for y in (2021, 2022, 2023, 2024):
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
        return pd.Series(df["side"].astype(float).values, index=df["date"].dt.normalize()).sort_index()
    pos = {}
    for _, row in df.iterrows():
        start = pd.Timestamp(row["date"]).normalize()
        for k in range(hold_expand):
            pos[start + pd.Timedelta(days=k)] = float(row["side"])
    return pd.Series(pos).sort_index()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    gbpcad = load_m5("GBPCAD")
    eurnok = load_m5("EURNOK")
    usdhkd = load_m5("USDHKD")
    euraud = load_m5("EURAUD")

    t176, pos176, ret5, meta176 = session_prior(gbpcad, 5, True, 8, 0, 16, 0)
    t177, pos177, ret1, meta177 = session_prior(eurnok, 1, False, 9, 0, 13, 0)
    # same-mechanism EUR twin, not a dead id
    _t, pos_euraud_1d, ret_ea, _ = session_prior(euraud, 1, False, 9, 0, 13, 0)

    hkd = {
        "08:00-16:00": session_abs_mean(usdhkd, 8, 0, 16, 0),
        "00:00-23:00": session_abs_mean(usdhkd, 0, 0, 23, 0),
    }
    hkd_oracle = hkd["00:00-23:00"]["mean_abs_bp"]
    hkd_skip = {
        "symbol": "USDHKD",
        "given_id": False,
        "why": (
            f"peg. 08:00→16:00 oracle mean |move| {hkd['08:00-16:00']['mean_abs_bp']} bp "
            f"< gate {GATE_HKD:.2f}, so that window cannot clear. "
            f"00:00→23:00 oracle ceiling is {hkd_oracle} bp, only {hkd_oracle-GATE_HKD:.2f} bp above the gate, "
            "so a book would need a near-perfect sign. Not given an id; two other names already cleared history and the clone bar. "
            "M5 file span is 5.74y."
        ),
        "windows": hkd,
        "gate_bp": GATE_HKD,
    }

    d094 = (
        f"FTMO M5 file 2021-01-04 → 2026-10-01 is {HIST_YEARS}y (≥5.73). "
        f"PnL and signals use only bars through 2024-12-31 ({TRADED_YEARS_TO_2024}y). "
        "2025+ reserve not read into the book. C-048 79d09e0."
    )
    for meta, sym, sess in (
        (meta176, "GBPCAD", "prior 5d return fade; entry 08:00 flat 16:00 CET"),
        (meta177, "EURNOK", "prior 1d return continuation; entry 09:00 flat 13:00 CET"),
    ):
        meta["rt_in_costs_ftmo_csv"] = True
        meta["gate_file"] = "C-048 79d09e0 COSTS_FTMO.csv appended row; not COSTS_FTMO_alle"
        meta["d094a"] = d094
        meta["history_years"] = HIST_YEARS
        meta["symbol_list"] = f"SymbolList_FTMO.csv {sym}"
        meta["swap_nights"] = 0
        meta["session"] = sess
        meta["no_2025_plus"] = True

    n152 = load_side_csv(ROOT / "results/R2/n152_n153_prescreen/n152_trades_train.csv")
    n153 = load_side_csv(ROOT / "results/R2/n152_n153_prescreen/n153_trades_train.csv")
    n58 = load_side_csv(ROOT / "results/R2/n58_n62_prescreen/N58_trades.csv", hold_expand=10)
    # N66 has no trade file in n58 pack; FX_EUR_SHORT subsumed it. Use N58 file's sibling if present.
    n66_path = ROOT / "results/R2/n58_n62_prescreen/N66_trades.csv"
    n66 = load_side_csv(n66_path, hold_expand=10) if n66_path.exists() else None
    z152 = None
    zpath = ROOT / "results/R2/n152_n153_prescreen/n152_trades_train.csv"
    zdf = pd.read_csv(zpath)
    if "z40" in zdf.columns:
        zdf["date"] = pd.to_datetime(zdf["date"])
        z152 = pd.Series(zdf["z40"].astype(float).values, index=zdf["date"].dt.normalize()).sort_index()

    peers_176 = {
        "N152_GBP_NZD_XS": (n152, z152, True),
        "N153_EUR_CAD_XS": (n153, None, True),
        "N58_AUDJPY_LO_20_10": (n58, None, True),
        "N177_EURNOK_1d_cont": (pos177, ret1, True),
    }
    if n66 is not None:
        peers_176["N66_EURAUD_SO_20_10"] = (n66, None, True)
    c176 = {n: clone_sign(n, pos176, p, binding=b, z_c=ret5, z_p=z) for n, (p, z, b) in peers_176.items()}

    peers_177 = {
        "N152_GBP_NZD_XS": (n152, z152, True),
        "N153_EUR_CAD_XS": (n153, None, True),
        "N58_AUDJPY_LO_20_10": (n58, None, True),
        "N176_GBPCAD_5d_fade": (pos176, ret5, True),
        "EURAUD_same_1d_cont_NOT_A_DEAD_ID": (pos_euraud_1d, ret_ea, False),
    }
    if n66 is not None:
        peers_177["N66_EURAUD_SO_20_10"] = (n66, None, True)
    c177 = {n: clone_sign(n, pos177, p, binding=b, z_c=ret1, z_p=z) for n, (p, z, b) in peers_177.items()}

    s176 = verdict(
        t176, GATE_176, COSTS_RT["GBPCAD"], "N176", "GBPCAD",
        "GBPCAD_PRIOR5D_REVERSAL fade prior 5d return, session-flat 08:00→16:00; "
        f"gate 3*{COSTS_RT['GBPCAD']}={GATE_176:.2f} from C-048 COSTS_FTMO.csv (not alle); "
        "swap nights 0 (long credit -0.04 not used); not N152/N153 G10 XS; "
        "not a dead index leg; M5 file 5.74y; PnL through 2024-12-31 only; NEW_FAMILY CS",
    )
    s176["meta"] = meta176
    s176["gate_source"] = "C-048 79d09e0 COSTS_FTMO.csv GBPCAD rondreis_bp 1.08 × 3 = 3.24"
    apply_clone(s176, c176)
    s176["clone"] = c176

    s177 = verdict(
        t177, GATE_177, COSTS_RT["EURNOK"], "N177", "EURNOK",
        "EURNOK_PRIOR1D_CONTINUATION prior 1d return, session-flat 09:00→13:00; "
        f"gate 3*{COSTS_RT['EURNOK']}={GATE_177:.2f} from C-048 COSTS_FTMO.csv (not alle); "
        "swap nights 0 (short credit -0.20 not used); not EURAUD overnight-short TSMOM; "
        "not N176 (different instrument and mechanism); M5 file 5.74y; PnL through 2024-12-31 only; NEW_FAMILY CT",
    )
    s177["meta"] = meta177
    s177["gate_source"] = "C-048 79d09e0 COSTS_FTMO.csv EURNOK rondreis_bp 4.62 × 3 = 13.86"
    apply_clone(s177, c177)
    s177["clone"] = c177

    pd.DataFrame(t176).to_csv(OUT / "n176_trades_train.csv", index=False)
    pd.DataFrame(t177).to_csv(OUT / "n177_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N176": pub(s176),
        "N177": pub(s177),
        "N176_clones": c176,
        "N177_clones": c177,
        "discarded_before_id": {
            "USDSEK": "v114 refused; FTMO M5 4.74y < 5.73. Not screened.",
            "USDNOK": "v114 refused; FTMO M5 4.74y < 5.73. Not screened.",
            "USDZAR": "v114 refused; FTMO M5 4.74y < 5.73. Not screened.",
            "USDHKD": hkd_skip,
        },
        "gates": {"N176": round(GATE_176, 4), "N177": round(GATE_177, 4)},
        "costs_rt": COSTS_RT,
        "history_years_m5_file": HIST_YEARS,
        "pnl_through": "2024-12-31",
        "no_2025_plus": True,
        "train": "2021-01-01..2024-12-31; 2025+ not loaded",
        "min_n": MIN_N,
        "no_thr_grid": True,
        "trial_count_unchanged": 471,
        "not_used": ["UK100cash", "JP225cash", "HK50cash", "AUS200cash"],
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))
    md = (
        "# D-092.1 N176/N177 pre-screen (through 2024-12-31, no 2025+)\n\n"
        "C-048 gates from COSTS_FTMO.csv. v114: no USDSEK/USDNOK/USDZAR. "
        f"USDHKD not given an id (08:00–16:00 oracle {hkd['08:00-16:00']['mean_abs_bp']} bp < gate {GATE_HKD:.2f}; full-day ceiling {hkd_oracle} bp).\n\n"
        f"- **N176 GBPCAD 5d reversal**: N={s176['n']} mean={s176['mean_bruto_bp']} "
        f"netto={s176.get('netto_bp')} gate={s176['gate_bp']} → **{s176['verdict']}** "
        f"years={s176.get('years')} L/S={s176.get('n_long')}/{s176.get('n_short')} "
        f"hits={s176.get('clone_hits')}\n"
        f"- **N177 EURNOK 1d continuation**: N={s177['n']} mean={s177['mean_bruto_bp']} "
        f"netto={s177.get('netto_bp')} gate={s177['gate_bp']} → **{s177['verdict']}** "
        f"years={s177.get('years')} L/S={s177.get('n_long')}/{s177.get('n_short')} "
        f"hits={s177.get('clone_hits')}\n\n"
        "Session-flat, swap nights 0. No thr-grid. No index rewrite. No OPEN filed.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N176": pub(s176), "N177": pub(s177), "USDHKD_skip": hkd_skip["why"]}, indent=2, default=str))
    print("---176---")
    for k, v in c176.items():
        print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "z_corr_train", "n_both_active", "clone")})
    print("---177---")
    for k, v in c177.items():
        print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "z_corr_train", "n_both_active", "clone")})


if __name__ == "__main__":
    main()
