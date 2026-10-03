#!/usr/bin/env python3
"""D-092.1 TRAIN pre-screen: N178 AUDJPY 5d reversal + N179 EURAUD 1d fade.

Not a redo of N176/N177. EURAUD is a 1-day fade, not N177's 1-day continuation.
Gates are 3x C-048 COSTS_FTMO.csv round-trip (79d09e0), not alle.
No 2025+ bar enters the signal or the PnL. Session-flat, swap nights 0.
No thr-grid.

Clone bar: agree>=0.90 OR (agree>=0.85 AND cover>=0.70)
OR |z|>=0.90 OR (agree>=0.98 and n_both>=30).
The two books must agree under 0.85.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n178_n179_prescreen"
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
COSTS_RT = {"AUDJPY": 1.57, "EURAUD": 1.11}
GATE_178 = 3.0 * COSTS_RT["AUDJPY"]  # 4.71
GATE_179 = 3.0 * COSTS_RT["EURAUD"]  # 3.33
HIST_YEARS = 5.74
TRADED_YEARS_TO_2024 = 3.99


def load_m5(sym: str) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    df = pd.read_csv(path, sep=";", compression="gzip", comment="#", usecols=["time", "close"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
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


def n66_short_hold(df) -> pd.Series:
    """Dead EURAUD book: short-only 20d momentum, hold 10 sessions (N66 / FX_EUR_SHORT)."""
    dc = daily_last(df)
    r20 = dc / dc.shift(20) - 1.0
    idx = list(dc.index)
    pos = {}
    for i, dt in enumerate(idx):
        if i < 20 or not np.isfinite(r20.iloc[i]):
            continue
        if float(r20.iloc[i]) < 0:
            for d in idx[i : i + 10]:
                pos[d] = -1.0
    return pd.Series(pos, dtype=float).sort_index()


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
    aud = load_m5("AUDJPY")
    eau = load_m5("EURAUD")
    t178, pos178, ret5, meta178 = session_prior(aud, 5, True, 8, 0, 16, 0)
    t179, pos179, ret1, meta179 = session_prior(eau, 1, True, 8, 0, 16, 0)
    pos66 = n66_short_hold(eau)

    d094 = (
        f"FTMO M5 file 2021-01-04 → 2026-10-01 is {HIST_YEARS}y (≥5.73). "
        f"PnL and signals use only bars through 2024-12-31 ({TRADED_YEARS_TO_2024}y). "
        "2025+ reserve not read into the book. C-048 79d09e0."
    )
    meta178["session"] = "prior 5d return fade; entry 08:00 flat 16:00 CET"
    meta179["session"] = "prior 1d return fade; entry 08:00 flat 16:00 CET"
    for meta, sym in ((meta178, "AUDJPY"), (meta179, "EURAUD")):
        meta["rt_in_costs_ftmo_csv"] = True
        meta["gate_file"] = "C-048 79d09e0 COSTS_FTMO.csv appended row; not COSTS_FTMO_alle"
        meta["d094a"] = d094
        meta["history_years"] = HIST_YEARS
        meta["symbol_list"] = f"SymbolList_FTMO.csv {sym}"
        meta["swap_nights"] = 0
        meta["no_2025_plus"] = True

    n152 = load_side_csv(ROOT / "results/R2/n152_n153_prescreen/n152_trades_train.csv")
    n153 = load_side_csv(ROOT / "results/R2/n152_n153_prescreen/n153_trades_train.csv")
    n176 = load_side_csv(ROOT / "results/R2/n176_n177_prescreen/n176_trades_train.csv")
    n177 = load_side_csv(ROOT / "results/R2/n176_n177_prescreen/n177_trades_train.csv")
    n58 = load_side_csv(ROOT / "results/R2/n58_n62_prescreen/N58_trades.csv", hold_expand=10)
    z152 = None
    zdf = pd.read_csv(ROOT / "results/R2/n152_n153_prescreen/n152_trades_train.csv")
    if "z40" in zdf.columns:
        zdf["date"] = pd.to_datetime(zdf["date"])
        z152 = pd.Series(zdf["z40"].astype(float).values, index=zdf["date"].dt.normalize()).sort_index()

    peers_178 = {
        "N152_GBP_NZD_XS": (n152, z152, True),
        "N153_EUR_CAD_XS": (n153, None, True),
        "N176_GBPCAD_5d_fade": (n176, None, True),
        "N177_EURNOK_1d_cont": (n177, None, True),
        "N58_AUDJPY_LO_20_10": (n58, None, True),
        "N66_EURAUD_SO_20_10_rebuilt": (pos66, None, True),
        "N179_EURAUD_1d_fade": (pos179, ret1, True),
    }
    c178 = {n: clone_sign(n, pos178, p, binding=b, z_c=ret5, z_p=z) for n, (p, z, b) in peers_178.items()}
    peers_179 = {
        "N152_GBP_NZD_XS": (n152, z152, True),
        "N153_EUR_CAD_XS": (n153, None, True),
        "N176_GBPCAD_5d_fade": (n176, None, True),
        "N177_EURNOK_1d_cont": (n177, None, True),
        "N58_AUDJPY_LO_20_10": (n58, None, True),
        "N66_EURAUD_SO_20_10_rebuilt": (pos66, None, True),
        "N178_AUDJPY_5d_fade": (pos178, ret5, True),
    }
    c179 = {n: clone_sign(n, pos179, p, binding=b, z_c=ret1, z_p=z) for n, (p, z, b) in peers_179.items()}

    s178 = verdict(
        t178, GATE_178, COSTS_RT["AUDJPY"], "N178", "AUDJPY",
        "AUDJPY_PRIOR5D_REVERSAL fade prior 5d return, session-flat 08:00→16:00; "
        f"gate 3*{COSTS_RT['AUDJPY']}={GATE_178:.2f} from C-048 COSTS_FTMO.csv (not alle); "
        "swap nights 0 (long credit -0.24 not used); not N58 20/10 LO; "
        "not N176 (agree under 0.85); M5 file 5.74y; PnL through 2024-12-31 only; NEW_FAMILY CU",
    )
    s178["meta"] = meta178
    s178["gate_source"] = "C-048 79d09e0 COSTS_FTMO.csv AUDJPY rondreis_bp 1.57 × 3 = 4.71"
    apply_clone(s178, c178)
    s178["clone"] = c178

    s179 = verdict(
        t179, GATE_179, COSTS_RT["EURAUD"], "N179", "EURAUD",
        "EURAUD_PRIOR1D_FADE fade prior 1d return, session-flat 08:00→16:00; "
        f"gate 3*{COSTS_RT['EURAUD']}={GATE_179:.2f} from C-048 COSTS_FTMO.csv (not alle); "
        "swap nights 0 (short credit -0.20 not used); not N177 1d continuation; "
        "not N66 overnight-short TSMOM; not a twin of N178; M5 file 5.74y; PnL through 2024-12-31 only; NEW_FAMILY CV",
    )
    s179["meta"] = meta179
    s179["gate_source"] = "C-048 79d09e0 COSTS_FTMO.csv EURAUD rondreis_bp 1.11 × 3 = 3.33"
    apply_clone(s179, c179)
    s179["clone"] = c179

    pd.DataFrame(t178).to_csv(OUT / "n178_trades_train.csv", index=False)
    pd.DataFrame(t179).to_csv(OUT / "n179_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N178": pub(s178),
        "N179": pub(s179),
        "N178_clones": c178,
        "N179_clones": c179,
        "discarded_before_id": {
            "USDSEK": "v114; M5 4.74y. Not screened.",
            "USDNOK": "v114; M5 4.74y. Not screened.",
            "USDZAR": "v114; M5 4.74y. Not screened.",
            "USDHKD": "Not given an id. 08:00-16:00 oracle |move| 1.91 bp < gate 2.52. Full-day ceiling 3.23 bp.",
            "UK100_JP225_HK50_AUS200": "Not used. AUDJPY and EURAUD both cleared history and the clone bar.",
            "EURAUD_prior1d_continuation": "Same rule as N177 agreed 0.68. Not reused.",
        },
        "gates": {"N178": round(GATE_178, 4), "N179": round(GATE_179, 4)},
        "costs_rt": COSTS_RT,
        "history_years_m5_file": HIST_YEARS,
        "pnl_through": "2024-12-31",
        "no_2025_plus": True,
        "train": "2021-01-01..2024-12-31; 2025+ not loaded",
        "min_n": MIN_N,
        "no_thr_grid": True,
        "trial_count_unchanged": 471,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))
    md = (
        "# D-092.1 N178/N179 pre-screen (through 2024-12-31, no 2025+)\n\n"
        "C-048 gates. Not a redo of N176/N177. EURAUD is a 1d fade, not N177's continuation.\n\n"
        f"- **N178 AUDJPY 5d reversal**: N={s178['n']} mean={s178['mean_bruto_bp']} "
        f"netto={s178.get('netto_bp')} gate={s178['gate_bp']} → **{s178['verdict']}** "
        f"years={s178.get('years')} L/S={s178.get('n_long')}/{s178.get('n_short')} "
        f"hits={s178.get('clone_hits')}\n"
        f"- **N179 EURAUD 1d fade**: N={s179['n']} mean={s179['mean_bruto_bp']} "
        f"netto={s179.get('netto_bp')} gate={s179['gate_bp']} → **{s179['verdict']}** "
        f"years={s179.get('years')} L/S={s179.get('n_long')}/{s179.get('n_short')} "
        f"hits={s179.get('clone_hits')}\n\n"
        "Session-flat, swap nights 0. No thr-grid. No OPEN filed.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N178": pub(s178), "N179": pub(s179)}, indent=2, default=str))
    for label, clones in (("178", c178), ("179", c179)):
        print("---", label)
        for k, v in clones.items():
            print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "z_corr_train", "clone")})


if __name__ == "__main__":
    main()
