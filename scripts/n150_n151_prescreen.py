#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N150 XAG_US30 + N151 EURJPY_USDCHF.

Gates frozen from COSTS_FTMO.csv before any train PnL.

  N150 XAGUSD RT 5.07 + US30cash RT 0.45 = 5.52 → gate 3× = 16.56 bp.
  N151 EURJPY RT 1.10 + USDCHF RT 1.01 = 2.11 → gate 3× = 6.33 bp.

Session-flat 15:30→21:00 CET is the cheap side: swap is 0 and is in the
gate as 0. A two-sided overnight book cannot lock the receiving side.

Clone bar (precommitted in the VOORSTELs; decided before the run):
  FAIL_CLONE if |z Pearson| >= 0.90, or
  (sign agree on both-active >= 0.85 AND cover >= 0.70).
  A clone is not a PASS. No thr-grid. No soft gate. No single-leg rewrite.
  No inline replacement screen: a clone FAILs and the refill is a later OPEN,
  not a third family fished inside this run.

Must-not-equal (binding):
  N150: N113 SLV/GLD z40 thr±1.0, N141 XAG/UKOIL z40, N142 US30/US500 z40,
        CPER level z40, CuAu COPPER/GOLD z40, XAU/XAG z40, USDJPY/US100 z40,
        N75 one-sided, N133 GLD haven vs the US30 leg, N151.
  N151: USDCHF/USDJPY z40 (the inline FAIL_CLONE book), USDJPY/US100 z40,
        EUR/GER40 z40, N28 EURJPY London-impulse vs the EURJPY leg,
        L60 FX-med (EURJPY and USDCHF 60d LO) vs the matching leg,
        EURNZD 5d LO vs the EURJPY leg, AUDCAD 5d LO (CAD/AUD),
        N148, N150.

Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0. Threshold ±1.5 frozen.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n150_n151_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70

COSTS_RT = {
    "XAGUSD": 5.07,
    "US30cash": 0.45,
    "EURJPY": 1.10,
    "USDCHF": 1.01,
}
GATE_150 = 3.0 * (COSTS_RT["XAGUSD"] + COSTS_RT["US30cash"])  # 16.56
GATE_151 = 3.0 * (COSTS_RT["EURJPY"] + COSTS_RT["USDCHF"])  # 6.33


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


def daily_ratio_z_pos(sym_a, sym_b, window, thr):
    a = load_daily_close(sym_a)
    b = load_daily_close(sym_b)
    ratio = (a / b).dropna()
    ratio = ratio[(ratio.index >= TRAIN_START - pd.Timedelta(days=window * 3)) & (ratio.index <= TRAIN_END)]
    z = zscore(ratio, window)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def level_z_pos(sym, window, thr):
    s = load_daily_close(sym)
    s = s[(s.index >= TRAIN_START - pd.Timedelta(days=window * 3)) & (s.index <= TRAIN_END)]
    z = zscore(s, window)
    pos = pd.Series(0.0, index=s.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def impulse_pos(df, h0, m0, h1, m1, thr) -> pd.Series:
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, h0, m0, 15)
        b1 = first_bar_at(g, day, h1, m1, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0:
            continue
        move = 1e4 * (p1 / p0 - 1.0)
        if abs(move) < thr:
            continue
        pos[day] = 1.0 if move > 0 else -1.0
    return pd.Series(pos, dtype=float).sort_index()


def lo_ret_pos(close: pd.Series, lookback: int) -> pd.Series:
    ret = close / close.shift(lookback) - 1.0
    pos = pd.Series(0.0, index=close.index)
    pos[ret > 0] = 1.0
    return pos


def gld_haven_pos() -> pd.Series:
    """N133: GLD z120>0.5 and d20>0 → short US500 (−1); z120<-0.5 and d20<0 → long."""
    gld = load_daily_close("GLD")
    z120 = zscore(gld, 120)
    d20 = gld / gld.shift(20) - 1.0
    pos = pd.Series(0.0, index=gld.index)
    pos[(z120 > 0.5) & (d20 > 0)] = -1.0
    pos[(z120 < -0.5) & (d20 < 0)] = 1.0
    return pos


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
        "XAGUSD", "US30cash", "EURJPY", "USDCHF",
        "XAUUSD", "UKOILcash", "US500cash", "USDJPY", "US100cash",
        "EURUSD", "GER40cash", "EURNZD", "AUDCAD", "USDCAD",
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
    hist_150 = td["XAGUSD"] < 150 or td["US30cash"] < 150
    hist_151 = td["EURJPY"] < 150 or td["USDCHF"] < 150

    t150, _, z150, pos150, meta150 = screen_xs(
        cache["XAGUSD"], cache["US30cash"], 15, 30, 21, 0, "xag", "us30", thr=1.5
    )
    t151, _, z151, pos151, meta151 = screen_xs(
        cache["EURJPY"], cache["USDCHF"], 15, 30, 21, 0, "eurjpy", "usdchf", thr=1.5
    )
    meta150["train_days"] = {"XAGUSD": td["XAGUSD"], "US30cash": td["US30cash"]}
    meta151["train_days"] = {"EURJPY": td["EURJPY"], "USDCHF": td["USDCHF"]}
    for meta in (meta150, meta151):
        meta["rt_in_costs"] = True
        meta["swap_bp"] = 0
        meta["session"] = "15:30-21:00 CET cheapest side (overnight swap excluded)"

    z_xauxag, pos_xauxag = ratio_z_pos(cache, "XAUUSD", "XAGUSD", 40, 1.5)
    z_xaguk, pos_xaguk = ratio_z_pos(cache, "XAGUSD", "UKOILcash", 40, 1.5)
    z_u30, pos_u30 = ratio_z_pos(cache, "US30cash", "US500cash", 40, 1.5)
    z_jpyus, pos_jpyus = ratio_z_pos(cache, "USDJPY", "US100cash", 40, 1.5)
    z_chfjpy, pos_chfjpy = ratio_z_pos(cache, "USDCHF", "USDJPY", 40, 1.5)
    z_eurger, pos_eurger = ratio_z_pos(cache, "EURUSD", "GER40cash", 40, 1.5)

    ca = daily_close_22(cache["XAUUSD"])
    cag = daily_close_22(cache["XAGUSD"])
    both_m = pd.concat([ca.rename("a"), cag.rename("g")], axis=1).dropna()
    ln_r = np.log(both_m["a"] / both_m["g"])
    z20 = zscore(ln_r, 20)
    pos75 = pd.Series(0.0, index=ln_r.index)
    pos75[z20 < -1.0] = 1.0

    z_sg, pos_sg = daily_ratio_z_pos("SLV", "GLD", 40, 1.0)
    z_cper, pos_cper = level_z_pos("CPER", 40, 1.5)
    z_cuau, pos_cuau = daily_ratio_z_pos("COPPER_F", "GOLD_F", 40, 1.5)
    pos_gld = gld_haven_pos()

    pos_n28 = impulse_pos(cache["EURJPY"], 9, 0, 15, 30, 35.0)
    c_ej = daily_close_22(cache["EURJPY"])
    c_chf = daily_close_22(cache["USDCHF"])
    c_jpy = daily_close_22(cache["USDJPY"])
    c_cad = daily_close_22(cache["USDCAD"])
    c_nzd = daily_close_22(cache["EURNZD"])
    c_audcad = daily_close_22(cache["AUDCAD"])
    pos_ej_l60 = lo_ret_pos(c_ej, 60)
    pos_chf_l60 = lo_ret_pos(c_chf, 60)
    pos_jpy_l60 = lo_ret_pos(c_jpy, 60)
    pos_cad_l60 = lo_ret_pos(c_cad, 60)
    pos_eurnzd = lo_ret_pos(c_nzd, 5)
    pos_audcad = lo_ret_pos(c_audcad, 5)

    us30_leg = (-pos150).rename("us30_leg")
    xag_leg = pos150.rename("xag_leg")
    ej_leg = pos151.rename("eurjpy_leg")
    chf_leg = (-pos151).rename("usdchf_leg")

    c150 = bundle(z150, pos150, [
        ("SILVER_GOLD_N113", z_sg, pos_sg, True),
        ("XAG_UKOIL_N141", z_xaguk, pos_xaguk, True),
        ("US30_US500_N142", z_u30, pos_u30, True),
        ("CPER_N117", z_cper, pos_cper, True),
        ("CuAu_COPPER_GOLD", z_cuau, pos_cuau, True),
        ("XAU_XAG_z40", z_xauxag, pos_xauxag, True),
        ("USDJPY_US100_N148", z_jpyus, pos_jpyus, True),
        ("N75_XAU_XAG_onesided", None, pos75, True),
        ("EURJPY_USDCHF_N151", z151, pos151, True),
    ])
    c150["N133_GLD_vs_US30_leg"] = leg_clone("N133_GLD_vs_US30_leg", us30_leg, pos_gld)
    c150["N141_sign"] = leg_clone("N141_sign", pos150, pos_xaguk)
    c150["N142_sign"] = leg_clone("N142_sign", pos150, pos_u30)
    c150["N75_vs_XAG_leg"] = leg_clone("N75_vs_XAG_leg", xag_leg, pos75)

    c151 = bundle(z151, pos151, [
        ("USDCHF_USDJPY_inline", z_chfjpy, pos_chfjpy, True),
        ("USDJPY_US100_N148", z_jpyus, pos_jpyus, True),
        ("EUR_GER40_N149", z_eurger, pos_eurger, True),
        ("XAG_US30_N150", z150, pos150, True),
    ])
    c151["inline_USDCHF_USDJPY_sign"] = leg_clone("inline_USDCHF_USDJPY_sign", pos151, pos_chfjpy)
    c151["N28_EURJPY_Lon_vs_EURJPY_leg"] = leg_clone("N28_EURJPY_Lon_vs_EURJPY_leg", ej_leg, pos_n28)
    c151["EURJPY_L60_vs_EURJPY_leg"] = leg_clone("EURJPY_L60_vs_EURJPY_leg", ej_leg, pos_ej_l60)
    c151["USDCHF_L60_vs_USDCHF_leg"] = leg_clone("USDCHF_L60_vs_USDCHF_leg", chf_leg, pos_chf_l60)
    c151["USDJPY_L60_vs_EURJPY_leg"] = leg_clone("USDJPY_L60_vs_EURJPY_leg", ej_leg, pos_jpy_l60)
    c151["USDCAD_L60_vs_basket"] = leg_clone("USDCAD_L60_vs_basket", pos151, pos_cad_l60)
    c151["EURNZD_LO_5d_vs_EURJPY_leg"] = leg_clone("EURNZD_LO_5d_vs_EURJPY_leg", ej_leg, pos_eurnzd)
    c151["AUDCAD_LO_5d_vs_basket"] = leg_clone("AUDCAD_LO_5d_vs_basket", pos151, pos_audcad)
    c151["N148_sign"] = leg_clone("N148_sign", pos151, pos_jpyus)
    c151["N150_sign"] = leg_clone("N150_sign", pos151, pos150)

    s150 = verdict(
        t150, GATE_150, "N150", "XAGUSD+US30cash",
        (
            "XAGUSD_US30_METAL_INDUSTRIAL_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['XAGUSD']}+{COSTS_RT['US30cash']}); swap 0; NEW_FAMILY BS"
        ),
        history_missing=hist_150,
    )
    s150["meta"] = meta150
    s150["costs_rt"] = {"XAGUSD": COSTS_RT["XAGUSD"], "US30cash": COSTS_RT["US30cash"]}
    s150["rt_in_costs"] = True
    apply_clone(s150, c150)
    s150["clone"] = c150

    s151 = verdict(
        t151, GATE_151, "N151", "EURJPY+USDCHF",
        (
            "EURJPY_USDCHF_FUNDING_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['EURJPY']}+{COSTS_RT['USDCHF']}); swap 0; NEW_FAMILY BT"
        ),
        history_missing=hist_151,
    )
    s151["meta"] = meta151
    s151["costs_rt"] = {"EURJPY": COSTS_RT["EURJPY"], "USDCHF": COSTS_RT["USDCHF"]}
    s151["rt_in_costs"] = True
    apply_clone(s151, c151)
    s151["clone"] = c151

    pd.DataFrame(t150).to_csv(OUT / "n150_trades_train.csv", index=False)
    pd.DataFrame(t151).to_csv(OUT / "n151_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N150": pub(s150),
        "N151": pub(s151),
        "N150_clones": c150,
        "N151_clones": c151,
        "gates": {"N150": round(GATE_150, 4), "N151": round(GATE_151, 4)},
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
        "# D-092.1 N150/N151 pre-screen (train 2021–2023)\n\n"
        + line("N150 XAGUSD_US30_METAL_INDUSTRIAL_XS", s150)
        + line("N151 EURJPY_USDCHF_FUNDING_XS", s151)
        + "\nGates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. "
        + "No thr-grid. No 2024+ selection. No softer session spread. No inline replacement.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N150": pub(s150), "N151": pub(s151), "clones150": c150, "clones151": c151}, indent=2, default=str))


if __name__ == "__main__":
    main()
