#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N154 US100/GER40 + N155 US30/UKOIL.

Gates frozen from COSTS_FTMO.csv before any train PnL.

  N154 US100cash RT 0.66 + GER40cash RT 0.72 = 1.38 → gate 3× = 4.14 bp.
  N155 US30cash RT 0.45 + UKOILcash RT 2.71 = 3.16 → gate 3× = 9.48 bp.

Session-flat 15:30→21:00 CET. Swap in the gate is 0. A two-sided book
cannot lock a receiving overnight side (UKOIL short pays ~27 bp).

Both books fade the ratio: z>+1.5 → short leg A + long leg B;
z<-1.5 → long leg A + short leg B. Threshold frozen. No thr-grid.

Clone bar (precommitted; decided before the run):
  FAIL_CLONE if |z Pearson| >= 0.90, or
  (sign agree on both-active >= 0.85 AND cover >= 0.70).
  A clone is not a PASS.

Must-not-equal (binding):
  N154: US30/US500 z40 (N142), US100/US500 z40, GER40/UK100 z40 (N138),
        EU50/UK100 z40, EUR/GER40 z40 (N149), N81 one-sided US100 sign,
        N103 GER-AM day-sign vs the GER leg, N92 US100 NY-2h vs the
        US100 leg, and N155.
  N155: UKOIL/USOIL z40 (N136), XAU/UKOIL z40 (N140), XAG/UKOIL z40 (N141),
        GBP/UKOIL z40 (N147), US30/US500 z40 (N142), XAG/US30 z40 (N150),
        CRACK HEATOIL/BRENT z60, UKOIL-OVN vs the oil leg, N98 USOIL
        morning sign vs the oil leg, and N154.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n154_n155_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70

COSTS_RT = {
    "US100cash": 0.66,
    "GER40cash": 0.72,
    "US30cash": 0.45,
    "UKOILcash": 2.71,
}
GATE_154 = 3.0 * (COSTS_RT["US100cash"] + COSTS_RT["GER40cash"])  # 4.14
GATE_155 = 3.0 * (COSTS_RT["US30cash"] + COSTS_RT["UKOILcash"])  # 9.48


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


def ukoil_ovn_pos(uk: pd.DataFrame, daily: pd.Series) -> pd.Series:
    """N80: |gap|≥40 bp at 08:00 vs prior ≤22:00 close → continuation."""
    g = uk.copy()
    g["day"] = g["time"].dt.normalize()
    pos = pd.Series(0.0, index=daily.index)
    days = list(daily.index)
    for i in range(1, len(days)):
        day = days[i]
        cref = float(daily.iloc[i - 1])
        gd = g[g["day"] == day]
        if gd.empty or cref <= 0:
            continue
        b = first_bar_at(gd, day, 8, 0, 15)
        if b is None:
            continue
        gap = 1e4 * (float(b["close"]) / cref - 1.0)
        if gap >= 40:
            pos.loc[day] = 1.0
        elif gap <= -40:
            pos.loc[day] = -1.0
    return pos


def crack_z_pos():
    ho = load_daily_close("HEATOIL_F")
    br = load_daily_close("BRENT_F")
    crack = (ho / br).dropna()
    crack = crack[(crack.index >= TRAIN_START - pd.Timedelta(days=180)) & (crack.index <= TRAIN_END)]
    z60 = zscore(crack, 60)
    pos = pd.Series(0.0, index=crack.index)
    pos[z60 > 0.5] = -1.0
    pos[z60 < -0.5] = 1.0
    return z60, pos


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
        "US100cash", "GER40cash", "US30cash", "UKOILcash",
        "US500cash", "UK100cash", "EU50cash", "EURUSD",
        "USOILcash", "XAUUSD", "XAGUSD", "GBPUSD",
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
    hist_154 = td["US100cash"] < 150 or td["GER40cash"] < 150
    hist_155 = td["US30cash"] < 150 or td["UKOILcash"] < 150

    t154, _, z154, pos154, meta154 = screen_xs(
        cache["US100cash"], cache["GER40cash"], 15, 30, 21, 0, "us100", "ger", thr=1.5
    )
    t155, _, z155, pos155, meta155 = screen_xs(
        cache["US30cash"], cache["UKOILcash"], 15, 30, 21, 0, "us30", "ukoil", thr=1.5
    )
    meta154["train_days"] = {"US100cash": td["US100cash"], "GER40cash": td["GER40cash"]}
    meta155["train_days"] = {"US30cash": td["US30cash"], "UKOILcash": td["UKOILcash"]}
    for meta in (meta154, meta155):
        meta["rt_in_costs"] = True
        meta["swap_bp"] = 0
        meta["session"] = "15:30-21:00 CET cheapest side (overnight swap excluded)"

    z_u30, pos_u30 = ratio_z_pos(cache, "US30cash", "US500cash")
    z_nq, pos_nq = ratio_z_pos(cache, "US100cash", "US500cash")
    z_geuk, pos_geuk = ratio_z_pos(cache, "GER40cash", "UK100cash")
    z_euuk, pos_euuk = ratio_z_pos(cache, "EU50cash", "UK100cash")
    z_eurger, pos_eurger = ratio_z_pos(cache, "EURUSD", "GER40cash")
    z_oils, pos_oils = ratio_z_pos(cache, "UKOILcash", "USOILcash")
    z_xauoil, pos_xauoil = ratio_z_pos(cache, "XAUUSD", "UKOILcash")
    z_xagoil, pos_xagoil = ratio_z_pos(cache, "XAGUSD", "UKOILcash")
    z_gbpoil, pos_gbpoil = ratio_z_pos(cache, "GBPUSD", "UKOILcash")
    z_xagus, pos_xagus = ratio_z_pos(cache, "XAGUSD", "US30cash")
    z_ck, pos_ck = crack_z_pos()

    pos_n81 = n81_us100_pos(cache)
    pos_n103 = impulse_pos(cache["GER40cash"], 8, 0, 12, 0, 40)
    pos_n92 = ny2h_pos(cache["US100cash"])
    pos_n98 = impulse_pos(cache["USOILcash"], 8, 0, 12, 0, 40)
    pos_ovn = ukoil_ovn_pos(cache["UKOILcash"], daily_close_22(cache["UKOILcash"]))

    # side +1 = long first leg. GER leg of N154 is the opposite. Oil leg of N155 too.
    us100_leg = pos154.rename("us100_leg")
    ger_leg = (-pos154).rename("ger_leg")
    us30_leg = pos155.rename("us30_leg")
    oil_leg = (-pos155).rename("oil_leg")

    c154 = bundle(z154, pos154, [
        ("US30_US500_z40_N142", z_u30, pos_u30, True),
        ("US100_US500_z40", z_nq, pos_nq, True),
        ("GER40_UK100_z40_N138", z_geuk, pos_geuk, True),
        ("EU50_UK100_z40", z_euuk, pos_euuk, True),
        ("EUR_GER40_z40_N149", z_eurger, pos_eurger, True),
        ("US30_UKOIL_N155", z155, pos155, True),
    ])
    c154["N81_short_US100_vs_US100_leg"] = leg_clone("N81_short_US100_vs_US100_leg", us100_leg, pos_n81)
    c154["N103_GER_AM_vs_GER_leg"] = leg_clone("N103_GER_AM_vs_GER_leg", ger_leg, pos_n103)
    c154["N92_US100_NY2H_vs_US100_leg"] = leg_clone("N92_US100_NY2H_vs_US100_leg", us100_leg, pos_n92)
    c154["N138_sign"] = leg_clone("N138_sign", pos154, pos_geuk)
    c154["N149_sign"] = leg_clone("N149_sign", pos154, pos_eurger)
    c154["N142_sign"] = leg_clone("N142_sign", pos154, pos_u30)
    c154["N155_sign"] = leg_clone("N155_sign", pos154, pos155)

    c155 = bundle(z155, pos155, [
        ("UKOIL_USOIL_z40_N136", z_oils, pos_oils, True),
        ("XAU_UKOIL_z40_N140", z_xauoil, pos_xauoil, True),
        ("XAG_UKOIL_z40_N141", z_xagoil, pos_xagoil, True),
        ("GBP_UKOIL_z40_N147", z_gbpoil, pos_gbpoil, True),
        ("US30_US500_z40_N142", z_u30, pos_u30, True),
        ("XAG_US30_z40_N150", z_xagus, pos_xagus, True),
        ("CRACK_z60", z_ck, pos_ck, True),
        ("US100_GER40_N154", z154, pos154, True),
    ])
    c155["UKOIL_OVN_vs_oil_leg"] = leg_clone("UKOIL_OVN_vs_oil_leg", oil_leg, pos_ovn)
    c155["N98_USOIL_AM_vs_oil_leg"] = leg_clone("N98_USOIL_AM_vs_oil_leg", oil_leg, pos_n98)
    c155["N140_sign"] = leg_clone("N140_sign", pos155, pos_xauoil)
    c155["N141_sign"] = leg_clone("N141_sign", pos155, pos_xagoil)
    c155["N147_sign"] = leg_clone("N147_sign", pos155, pos_gbpoil)
    c155["N136_sign"] = leg_clone("N136_sign", pos155, pos_oils)
    c155["N142_sign"] = leg_clone("N142_sign", pos155, pos_u30)
    c155["N150_sign"] = leg_clone("N150_sign", pos155, pos_xagus)
    c155["N154_sign"] = leg_clone("N154_sign", pos155, pos154)

    s154 = verdict(
        t154, GATE_154, "N154", "US100cash+GER40cash",
        (
            "US100_GER40_TRANSATLANTIC_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['US100cash']}+{COSTS_RT['GER40cash']}); swap 0; NEW_FAMILY BW"
        ),
        history_missing=hist_154,
    )
    s154["meta"] = meta154
    s154["costs_rt"] = {"US100cash": COSTS_RT["US100cash"], "GER40cash": COSTS_RT["GER40cash"]}
    s154["rt_in_costs"] = True
    apply_clone(s154, c154)
    s154["clone"] = c154

    s155 = verdict(
        t155, GATE_155, "N155", "US30cash+UKOILcash",
        (
            "US30_UKOIL_INDUSTRIAL_CRUDE_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['US30cash']}+{COSTS_RT['UKOILcash']}); swap 0; NEW_FAMILY BX"
        ),
        history_missing=hist_155,
    )
    s155["meta"] = meta155
    s155["costs_rt"] = {"US30cash": COSTS_RT["US30cash"], "UKOILcash": COSTS_RT["UKOILcash"]}
    s155["rt_in_costs"] = True
    apply_clone(s155, c155)
    s155["clone"] = c155

    pd.DataFrame(t154).to_csv(OUT / "n154_trades_train.csv", index=False)
    pd.DataFrame(t155).to_csv(OUT / "n155_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N154": pub(s154),
        "N155": pub(s155),
        "N154_clones": c154,
        "N155_clones": c155,
        "gates": {"N154": round(GATE_154, 4), "N155": round(GATE_155, 4)},
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
        "# D-092.1 N154/N155 pre-screen (train 2021–2023)\n\n"
        + line("N154 US100_GER40_TRANSATLANTIC_XS", s154)
        + line("N155 US30_UKOIL_INDUSTRIAL_CRUDE_XS", s155)
        + "\nGates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. "
        + "No thr-grid. No 2024+ selection. No softer session spread. No single-leg rewrite.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N154": pub(s154), "N155": pub(s155)}, indent=2, default=str))
    print("---CLONES154---")
    for k, v in c154.items():
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "clone", "n_both_active")})
    print("---CLONES155---")
    for k, v in c155.items():
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "clone", "n_both_active")})


if __name__ == "__main__":
    main()
