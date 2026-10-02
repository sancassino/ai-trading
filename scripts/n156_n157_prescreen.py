#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N156 XAU/GER40 + N157 XAU/US100.

Gates frozen from COSTS_FTMO.csv before any train PnL.

  N156 XAUUSD RT 0.83 + GER40cash RT 0.72 = 1.55 → gate 3× = 4.65 bp.
  N157 XAUUSD RT 0.83 + US100cash RT 0.66 = 1.49 → gate 3× = 4.47 bp.

Session-flat 15:30→21:00 CET. Swap in the gate is 0. A two-sided book
cannot lock a receiving overnight side (long-XAU 2.15).

Both books fade the ratio: z>+1.5 → short leg A (XAU) + long leg B;
z<-1.5 → long XAU + short leg B. Threshold frozen. No thr-grid.

Clone bar (precommitted; decided before the run):
  FAIL_CLONE if |z Pearson| >= 0.90, or
  (sign agree on both-active >= 0.85 AND cover >= 0.70).
  A clone is not a PASS. N157 is FAIL_CLONE if it is a twin of N156.

Must-not-equal (binding):
  N156: N95 XAU Lon→NY vs the XAU leg, N146 AUD/XAU z40, N140 XAU/UKOIL z40,
        N133 GLD→US500 gold day-sign vs the XAU leg, N149 EUR/GER40 z40,
        N154 US100/GER40, N150 XAG/US30, N75 XAU/XAG, and N157.
  N157: N156, N92 US100 NY-2h vs the US100 leg, N148 USDJPY/US100 z40,
        N81 short-US100 vs the US100 leg, N154, N150, N133 gold day-sign,
        N75, N146.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n156_n157_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70

COSTS_RT = {
    "XAUUSD": 0.83,
    "GER40cash": 0.72,
    "US100cash": 0.66,
}
GATE_156 = 3.0 * (COSTS_RT["XAUUSD"] + COSTS_RT["GER40cash"])  # 4.65
GATE_157 = 3.0 * (COSTS_RT["XAUUSD"] + COSTS_RT["US100cash"])  # 4.47


def load_m5(sym: str, start, end) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    df = pd.read_csv(path, sep=";", compression="gzip", comment="#")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[(df["time"] >= start) & (df["time"] <= end)].reset_index(drop=True)
    return df[["time", "close"]]


def load_daily_close(sym: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(pd.io.common.StringIO("\n".join(body)), sep=sep)
    cols = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols.get("date") or cols.get("observation_date")
    cc = cols.get("adjclose") or cols.get("close")
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.DatetimeIndex(
            pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False))
        ).normalize(),
        name=sym,
    )
    s = s[~s.index.duplicated(keep="last")].sort_index().dropna()
    return s[s.index <= TRAIN_END]


def first_bar_at(g, day, h, m=0, span_min=15):
    t0 = day + pd.Timedelta(hours=h, minutes=m)
    t1 = t0 + pd.Timedelta(minutes=span_min)
    exact = g[g["time"] == t0]
    if len(exact):
        return exact.iloc[0]
    win = g[(g["time"] >= t0) & (g["time"] <= t1)]
    return win.iloc[0] if len(win) else None


def last_bar_le(g, day, h, m=0):
    t = day + pd.Timedelta(hours=h, minutes=m)
    win = g[g["time"] <= t]
    return win.iloc[-1] if len(win) else None


def daily_close_22(df: pd.DataFrame) -> pd.Series:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    cut = d["day"] + pd.Timedelta(hours=22)
    sub = d[d["time"] <= cut]
    s = sub.groupby("day")["close"].last().sort_index()
    return s[s > 0]


def zscore(sig: pd.Series, window: int) -> pd.Series:
    mu = sig.rolling(window, min_periods=window).mean()
    sd = sig.rolling(window, min_periods=window).std(ddof=0).replace(0, np.nan)
    return (sig - mu) / sd


def by_day(df: pd.DataFrame) -> dict:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    return {day: g for day, g in d.groupby("day", sort=False)}


def leg_ret_bp(g, day, side: int, h0, m0, h1, m1):
    b0 = first_bar_at(g, day, h0, m0, 15)
    b1 = last_bar_le(g, day, h1, m1)
    if b0 is None or b1 is None:
        return None
    if b1["time"] <= b0["time"]:
        return None
    p0 = float(b0["close"])
    p1 = float(b1["close"])
    if p0 <= 0 or p1 <= 0:
        return None
    return side * 1e4 * (p1 / p0 - 1.0)


def screen_xs(a, b, h0, m0, h1, m1, name_a, name_b, thr=1.5):
    """Opposite legs. side +1 = long A / short B (z < -thr)."""
    ca = daily_close_22(a)
    cb = daily_close_22(b)
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = (both["a"] / both["b"]).rename("ratio")
    z40 = zscore(ratio, 40)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z40 > thr] = -1.0
    pos[z40 < -thr] = 1.0
    ga = by_day(a)
    gb = by_day(b)
    trades = []
    days = list(pos.index)
    n_sig = 0
    n_skip_bar = 0
    for i in range(1, len(days)):
        sig_day = days[i - 1]
        day = days[i]
        if day < TRAIN_START or day > TRAIN_END:
            continue
        side = float(pos.loc[sig_day])
        if side == 0.0 or not np.isfinite(side):
            continue
        n_sig += 1
        gda = ga.get(day)
        gdb = gb.get(day)
        if gda is None or gdb is None:
            n_skip_bar += 1
            continue
        r_a = leg_ret_bp(gda, day, int(side), h0, m0, h1, m1)
        r_b = leg_ret_bp(gdb, day, int(-side), h0, m0, h1, m1)
        if r_a is None or r_b is None:
            n_skip_bar += 1
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(sig_day).date()),
                "side": int(side),
                f"{name_a}_bp": r_a,
                f"{name_b}_bp": r_b,
                "bruto_bp": r_a + r_b,
                "z40": None if not np.isfinite(z40.loc[sig_day]) else round(float(z40.loc[sig_day]), 4),
            }
        )
    meta = {
        "n_signal_days": n_sig,
        "n_skip_missing_bar": n_skip_bar,
        "n_ratio_days": int(len(ratio)),
        "ratio_first": str(pd.Timestamp(ratio.index.min()).date()) if len(ratio) else None,
        "ratio_last": str(pd.Timestamp(ratio.index.max()).date()) if len(ratio) else None,
        "b_sign": -1,
    }
    return trades, ratio, z40, pos, meta


def ratio_z_pos(cache, sym_a, sym_b, window=40, thr=1.5):
    ca = daily_close_22(cache[sym_a])
    cb = daily_close_22(cache[sym_b])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = both["a"] / both["b"]
    z = zscore(ratio, window)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def n95_xau_lon_ny(df) -> pd.Series:
    """N95: |XAU 08:00→11:00| >= 25 bp → continuation. Dated the impulse day."""
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, 8, 0, 15)
        b1 = first_bar_at(g, day, 11, 0, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0:
            continue
        am = 1e4 * (p1 / p0 - 1.0)
        if abs(am) < 25:
            continue
        pos[day] = 1.0 if am > 0 else -1.0
    return pd.Series(pos, dtype=float).sort_index()


def ny2h_pos(df) -> pd.Series:
    """N92: sign of US100 15:30→17:30."""
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, 15, 30, 15)
        b1 = first_bar_at(g, day, 17, 30, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0 or p1 == p0:
            continue
        pos[day] = 1.0 if p1 > p0 else -1.0
    return pd.Series(pos, dtype=float).sort_index()


def n81_us100_pos(cache) -> pd.Series:
    """N81: ln(US100/US500) z20 > +1 → short US100. Hostile side flat."""
    ca = daily_close_22(cache["US100cash"])
    cb = daily_close_22(cache["US500cash"])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    r = np.log(both["a"] / both["b"])
    z = zscore(r, 20)
    pos = pd.Series(0.0, index=r.index)
    pos[z > 1.0] = -1.0
    return pos


def n75_pos(cache) -> pd.Series:
    """N75: ln(XAU/XAG) z20 < -1 → long the ratio (long XAU / short XAG). One-sided."""
    ca = daily_close_22(cache["XAUUSD"])
    cb = daily_close_22(cache["XAGUSD"])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    r = np.log(both["a"] / both["b"])
    z = zscore(r, 20)
    pos = pd.Series(0.0, index=r.index)
    pos[z < -1.0] = 1.0
    return pos


def gld_haven():
    """N133: GLD z120+d20 inverse haven. Equity side and the gold-rich day-sign.

    Gold-rich (z120>0.5 and d20>0) → equity short (−1) and gold day-sign +1.
    Gold-cheap → equity long (+1) and gold day-sign −1.
    """
    gld = load_daily_close("GLD")
    z120 = zscore(gld, 120)
    d20 = gld / gld.shift(20) - 1.0
    equity = pd.Series(0.0, index=gld.index)
    equity[(z120 > 0.5) & (d20 > 0)] = -1.0
    equity[(z120 < -0.5) & (d20 < 0)] = 1.0
    gold_sign = -equity  # +1 on gold-rich days
    return z120, equity, gold_sign


def align(z, pos, index):
    if z is None:
        return None, pos.reindex(index).fillna(0.0)
    zz = z.reindex(index, method="ffill")
    pp = pos.reindex(index, method="ffill").fillna(0.0)
    return zz, pp


def clone_pair(name, z_c, pos_c, z_p, pos_p) -> dict:
    both = pos_c.to_frame("c").join(pos_p.rename("p"), how="inner").dropna()
    both = both[(both.index >= TRAIN_START) & (both.index <= TRAIN_END)]
    active = both[both["c"] != 0]
    both_on = active[active["p"] != 0]
    agree = float((both_on["c"] == both_on["p"]).mean()) if len(both_on) else None
    cover = float(len(both_on) / len(active)) if len(active) else None
    corr = None
    if z_c is not None and z_p is not None:
        zz = z_c.to_frame("c").join(z_p.rename("p"), how="inner").dropna()
        zz = zz[(zz.index >= TRAIN_START) & (zz.index <= TRAIN_END)]
        if len(zz) > 30:
            corr = float(zz["c"].corr(zz["p"]))
    is_clone = False
    if corr is not None and abs(corr) >= Z_CLONE:
        is_clone = True
    if agree is not None and cover is not None and agree >= AGREE_CLONE and cover >= COVER_CLONE:
        is_clone = True
    return {
        "peer": name,
        "z_corr_train": None if corr is None else round(corr, 4),
        "sign_agree_both_active": None if agree is None else round(agree, 4),
        "both_active_over_cand": None if cover is None else round(cover, 4),
        "n_cand_active": int(len(active)),
        "n_both_active": int(len(both_on)),
        "clone": is_clone,
    }


def verdict(trades, gate, label, instrument, notes, history_missing=False):
    n = len(trades)
    base = {
        "id": label,
        "instrument": instrument,
        "n": n,
        "mean_bruto_bp": None,
        "gate_bp": round(float(gate), 4),
        "verdict": "FAIL",
        "notes": notes,
    }
    if history_missing or n == 0:
        base["verdict"] = "DIAG_FAIL"
        return base
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    if n >= MIN_N and mean >= gate:
        v = "PASS_may_PREREG"
    elif mean >= gate and n < MIN_N:
        v = "UNDERPOWERED"
    else:
        v = "FAIL"
    years = {}
    for y in (2021, 2022, 2023):
        ys = [t["bruto_bp"] for t in trades if t["date"].startswith(str(y))]
        if ys:
            years[str(y)] = round(float(np.mean(ys)), 4)
    base.update(
        {
            "mean_bruto_bp": round(mean, 4),
            "median_bruto_bp": round(float(np.median(arr)), 4),
            "stress_gate_bp": round(gate * 1.5, 4),
            "stress_note": (
                "PASS_stress_informal"
                if mean >= gate * 1.5
                else "BELOW_stress_1.5x (info only; own gate is the cost gate)"
            ),
            "verdict": v,
            "hit_rate": round(float((arr > 0).mean()), 4),
            "n_long_basket": int(sum(1 for t in trades if t.get("side", 0) > 0)),
            "n_short_basket": int(sum(1 for t in trades if t.get("side", 0) < 0)),
            "years": years,
        }
    )
    return base


def apply_clone(summary, clones):
    hit = [k for k, v in clones.items() if v.get("clone") and v.get("binding", True)]
    summary["clone_hits"] = hit
    if hit:
        summary["verdict"] = "FAIL_CLONE"
        if "CLONE" not in summary["notes"]:
            summary["notes"] += " | CLONE of " + ",".join(hit) + " — no PREREG"
    return summary


def bundle(z_c, pos_c, peers):
    out = {}
    for name, z_p, pos_p, binding in peers:
        z_u, p_u = align(z_p, pos_p, pos_c.index)
        rec = clone_pair(name, z_c, pos_c, z_u, p_u)
        rec["binding"] = binding
        out[name] = rec
    return out


def leg_clone(name, leg, peer):
    rec = clone_pair(name, None, leg, None, peer.reindex(leg.index).fillna(0.0))
    rec["binding"] = True
    return rec


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    need = (
        "XAUUSD", "GER40cash", "US100cash", "US500cash", "US30cash",
        "UKOILcash", "AUDUSD", "EURUSD", "USDJPY", "XAGUSD",
    )
    cache = {}
    for s in need:
        cache[s] = load_m5(s, TRAIN_START - pd.Timedelta(days=120), TRAIN_END)

    def train_days(sym):
        t = cache[sym]["time"]
        m = (t >= TRAIN_START) & (t <= TRAIN_END)
        return int(t[m].dt.normalize().nunique())

    td = {s: train_days(s) for s in need}
    days = {s: int(cache[s]["time"].dt.normalize().nunique()) if len(cache[s]) else 0 for s in need}
    hist_156 = td["XAUUSD"] < 150 or td["GER40cash"] < 150
    hist_157 = td["XAUUSD"] < 150 or td["US100cash"] < 150

    t156, _, z156, pos156, meta156 = screen_xs(
        cache["XAUUSD"], cache["GER40cash"], 15, 30, 21, 0, "xau", "ger", thr=1.5
    )
    t157, _, z157, pos157, meta157 = screen_xs(
        cache["XAUUSD"], cache["US100cash"], 15, 30, 21, 0, "xau", "us100", thr=1.5
    )
    meta156["train_days"] = {"XAUUSD": td["XAUUSD"], "GER40cash": td["GER40cash"]}
    meta157["train_days"] = {"XAUUSD": td["XAUUSD"], "US100cash": td["US100cash"]}
    for meta in (meta156, meta157):
        meta["rt_in_costs"] = True
        meta["swap_bp"] = 0
        meta["session"] = "15:30-21:00 CET cheapest side (overnight swap excluded)"

    z_audxau, pos_audxau = ratio_z_pos(cache, "AUDUSD", "XAUUSD")
    z_xauoil, pos_xauoil = ratio_z_pos(cache, "XAUUSD", "UKOILcash")
    z_eurger, pos_eurger = ratio_z_pos(cache, "EURUSD", "GER40cash")
    z_usger, pos_usger = ratio_z_pos(cache, "US100cash", "GER40cash")
    z_xagus, pos_xagus = ratio_z_pos(cache, "XAGUSD", "US30cash")
    z_auag, pos_auag = ratio_z_pos(cache, "XAUUSD", "XAGUSD")
    z_jpyus, pos_jpyus = ratio_z_pos(cache, "USDJPY", "US100cash")
    z_gld, equity_gld, gold_sign = gld_haven()

    pos_n95 = n95_xau_lon_ny(cache["XAUUSD"])
    pos_n92 = ny2h_pos(cache["US100cash"])
    pos_n81 = n81_us100_pos(cache)
    pos_n75 = n75_pos(cache)

    # side +1 = long XAU. Index leg is the opposite.
    xau_leg_156 = pos156.rename("xau_leg")
    ger_leg_156 = (-pos156).rename("ger_leg")
    xau_leg_157 = pos157.rename("xau_leg")
    us100_leg_157 = (-pos157).rename("us100_leg")

    c156 = bundle(z156, pos156, [
        ("AUD_XAU_z40_N146", z_audxau, pos_audxau, True),
        ("XAU_UKOIL_z40_N140", z_xauoil, pos_xauoil, True),
        ("EUR_GER40_z40_N149", z_eurger, pos_eurger, True),
        ("US100_GER40_z40_N154", z_usger, pos_usger, True),
        ("XAG_US30_z40_N150", z_xagus, pos_xagus, True),
        ("XAU_XAG_z40_N75", z_auag, pos_auag, True),
        ("GLD_z120_N133", z_gld, equity_gld, True),
        ("XAU_US100_N157", z157, pos157, True),
    ])
    c156["N95_XAU_LonNY_vs_XAU_leg"] = leg_clone("N95_XAU_LonNY_vs_XAU_leg", xau_leg_156, pos_n95)
    c156["N133_gold_day_sign_vs_XAU_leg"] = leg_clone(
        "N133_gold_day_sign_vs_XAU_leg", xau_leg_156, gold_sign
    )
    c156["N133_equity_side_vs_XAU_leg"] = leg_clone(
        "N133_equity_side_vs_XAU_leg", xau_leg_156, equity_gld
    )
    c156["N146_sign"] = leg_clone("N146_sign", pos156, pos_audxau)
    c156["N140_sign"] = leg_clone("N140_sign", pos156, pos_xauoil)
    c156["N149_sign"] = leg_clone("N149_sign", pos156, pos_eurger)
    c156["N154_sign"] = leg_clone("N154_sign", pos156, pos_usger)
    c156["N150_sign"] = leg_clone("N150_sign", pos156, pos_xagus)
    c156["N75_sign"] = leg_clone("N75_sign", pos156, pos_n75)
    c156["N157_sign"] = leg_clone("N157_sign", pos156, pos157)

    c157 = bundle(z157, pos157, [
        ("XAU_GER40_N156", z156, pos156, True),
        ("USDJPY_US100_z40_N148", z_jpyus, pos_jpyus, True),
        ("US100_GER40_z40_N154", z_usger, pos_usger, True),
        ("XAG_US30_z40_N150", z_xagus, pos_xagus, True),
        ("XAU_XAG_z40_N75", z_auag, pos_auag, True),
        ("AUD_XAU_z40_N146", z_audxau, pos_audxau, True),
        ("GLD_z120_N133", z_gld, equity_gld, True),
    ])
    c157["N92_US100_NY2H_vs_US100_leg"] = leg_clone(
        "N92_US100_NY2H_vs_US100_leg", us100_leg_157, pos_n92
    )
    c157["N81_short_US100_vs_US100_leg"] = leg_clone(
        "N81_short_US100_vs_US100_leg", us100_leg_157, pos_n81
    )
    c157["N95_XAU_LonNY_vs_XAU_leg"] = leg_clone("N95_XAU_LonNY_vs_XAU_leg", xau_leg_157, pos_n95)
    c157["N133_gold_day_sign_vs_XAU_leg"] = leg_clone(
        "N133_gold_day_sign_vs_XAU_leg", xau_leg_157, gold_sign
    )
    c157["N148_sign"] = leg_clone("N148_sign", pos157, pos_jpyus)
    c157["N156_sign"] = leg_clone("N156_sign", pos157, pos156)
    c157["N154_sign"] = leg_clone("N154_sign", pos157, pos_usger)
    c157["N150_sign"] = leg_clone("N150_sign", pos157, pos_xagus)
    c157["N75_sign"] = leg_clone("N75_sign", pos157, pos_n75)
    c157["N146_sign"] = leg_clone("N146_sign", pos157, pos_audxau)

    s156 = verdict(
        t156, GATE_156, "N156", "XAUUSD+GER40cash",
        (
            "XAU_GER40_HAVEN_DAX_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['XAUUSD']}+{COSTS_RT['GER40cash']}); swap 0; NEW_FAMILY BY"
        ),
        history_missing=hist_156,
    )
    s156["meta"] = meta156
    s156["costs_rt"] = {"XAUUSD": COSTS_RT["XAUUSD"], "GER40cash": COSTS_RT["GER40cash"]}
    s156["rt_in_costs"] = True
    apply_clone(s156, c156)
    s156["clone"] = c156

    s157 = verdict(
        t157, GATE_157, "N157", "XAUUSD+US100cash",
        (
            "XAU_US100_HAVEN_NASDAQ_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['XAUUSD']}+{COSTS_RT['US100cash']}); swap 0; NEW_FAMILY BZ"
        ),
        history_missing=hist_157,
    )
    s157["meta"] = meta157
    s157["costs_rt"] = {"XAUUSD": COSTS_RT["XAUUSD"], "US100cash": COSTS_RT["US100cash"]}
    s157["rt_in_costs"] = True
    apply_clone(s157, c157)
    s157["clone"] = c157

    pd.DataFrame(t156).to_csv(OUT / "n156_trades_train.csv", index=False)
    pd.DataFrame(t157).to_csv(OUT / "n157_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N156": pub(s156),
        "N157": pub(s157),
        "N156_clones": c156,
        "N157_clones": c157,
        "gates": {"N156": round(GATE_156, 4), "N157": round(GATE_157, 4)},
        "costs_rt": COSTS_RT,
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "session": "15:30-21:00 CET",
        "no_thr_grid": True,
        "no_2024_in_signal": True,
        "no_inline_replacement": True,
        "gate_source": "COSTS_FTMO.csv roundtrip_intraday_bp; not a session median",
        "loaded_days_incl_warmup": days,
        "train_days": td,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} "
            f"→ **{s['verdict']}** years={s.get('years')} "
            f"L/S={s.get('n_long_basket')}/{s.get('n_short_basket')} "
            f"hits={s.get('clone_hits')} meta={s.get('meta')}\n"
        )

    md = (
        "# D-092.1 N156/N157 pre-screen (train 2021–2023)\n\n"
        + line("N156 XAU_GER40_HAVEN_DAX_XS", s156)
        + line("N157 XAU_US100_HAVEN_NASDAQ_XS", s157)
        + "\nGates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. "
        + "No thr-grid. No 2024+ selection. No softer session spread. No single-leg rewrite.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N156": pub(s156), "N157": pub(s157)}, indent=2, default=str))
    print("---CLONES156---")
    for k, v in c156.items():
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "clone", "n_both_active")})
    print("---CLONES157---")
    for k, v in c157.items():
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "clone", "n_both_active")})


if __name__ == "__main__":
    main()
