#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N144 XPT_XPD_PGM_XS + N145 BTC_ETH_CRYPTO_XS.

Honest gates are computed BEFORE any train PnL, from the COSTS convention
(all-hours M5 median spread, 2024-01-01..2026-09-30, spread>0) plus the
commission the file's own contract size implies. Session medians are logged
and are NOT the gate (using them would cheapen XPT/XPD vs COSTS).

  N144 metals, not in COSTS_FTMO.csv. Spread measured here (reproduces the
  stated 23.63 / 43.94). Commission = €2/lot/side at EURUSD 1.04 on the
  cost-window median close — the same assumption COSTS states for XAG
  ("aangenomen als XAU"; MT5-deals). Contract=100 from the gz header.
  Swap 0 (session-flat).

  N145 crypto, in SymbolList_FTMO as Crypto I CFD, M5 from 2021-01-01.
  Stated BTC 0.17 bp kept zero-spread bars (6.3% of 2024-26); those are
  dropped. Commission 0.0325%/side = 3.25 bp (FTMO crypto schedule that
  set ETH contract=10, which is the gz header). Not the N45 18 bp placeholder.
  Swap 0.

Clone bar (precommitted in the VOORSTELs; decided before the run):
  FAIL_CLONE if |z Pearson| >= 0.90, or
  (sign agree on both-active >= 0.85 AND cover >= 0.70).
  A clone is not a PASS. No thr-grid. No soft gate. No US500 rewrite.
  No metal-oil rewrite.

Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0.
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n144_n145_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
COST_START = pd.Timestamp("2024-01-01")
COST_END = pd.Timestamp("2026-09-30 23:59:59")
MIN_N = 150
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70
EURUSD_REF = 1.04
METAL_EUR_PER_SIDE = 2.0
CRYPTO_COMM_BP_PER_SIDE = 3.25  # 0.0325% of notional


def load_m5(sym: str, start, end) -> tuple[pd.DataFrame, float]:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        point = 0.01
        contract = None
        if first.startswith("#"):
            if "point=" in first:
                point = float(first.split("point=")[1].split(";")[0])
            if "contract=" in first:
                contract = float(first.split("contract=")[1].split(";")[0])
        else:
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    if "spread" in df.columns:
        df["spread"] = pd.to_numeric(df["spread"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[(df["time"] >= start) & (df["time"] <= end)].reset_index(drop=True)
    df.attrs["point"] = point
    df.attrs["contract"] = contract
    return df, point


def load_daily_close(sym: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
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


def honest_rt(sym: str, kind: str) -> dict:
    """COSTS-convention RT. kind is 'metal' or 'crypto'. Gate inputs only."""
    df, point = load_m5(sym, COST_START, COST_END)
    contract = df.attrs.get("contract")
    close = df["close"]
    spread = df["spread"]
    bp = spread * point / close * 1e4
    ok = (spread > 0) & (close > 0) & np.isfinite(bp)
    hm = df["time"].dt.hour * 60 + df["time"].dt.minute
    sess = ok & (hm >= 15 * 60 + 30) & (hm <= 21 * 60)
    med = float(np.median(bp[ok]))
    med_close = float(close[ok].median())
    if kind == "metal":
        comm_side = METAL_EUR_PER_SIDE * EURUSD_REF / (med_close * contract) * 1e4
        comm_src = "EUR2/lot/side at EURUSD 1.04 on cost-window median close (COSTS XAG assumption)"
    else:
        comm_side = CRYPTO_COMM_BP_PER_SIDE
        comm_src = "FTMO crypto 0.0325%/side (gz contract matches the Jul 2025 schedule)"
    rt = med + 2.0 * comm_side
    return {
        "symbol": sym,
        "point": point,
        "contract": contract,
        "n_bars": int(len(df)),
        "zero_spread_share": round(float((spread <= 0).mean()), 4),
        "spread_med_all_hours_bp": round(med, 4),
        "spread_med_session_1530_2100_bp": round(float(np.median(bp[sess])), 4),
        "median_close": round(med_close, 4),
        "comm_bp_per_side": round(float(comm_side), 4),
        "comm_source": comm_src,
        "rt_bp": round(float(rt), 4),
        "session_not_used_in_gate": True,
    }


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


def level_z_pos(sym, window, thr):
    s = load_daily_close(sym)
    z = zscore(s, window)
    pos = pd.Series(0.0, index=s.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


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


def n45_eth_pos(eth: pd.DataFrame) -> pd.Series:
    """N45: |asia 00:00→08:00| >= 300 bp → side = sign. Position dated that day."""
    groups = by_day(eth)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, 0, 0, 15)
        b1 = first_bar_at(g, day, 8, 0, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0:
            continue
        move = 1e4 * (p1 / p0 - 1.0)
        if abs(move) < 300:
            continue
        pos[day] = 1.0 if move > 0 else -1.0
    return pd.Series(pos, dtype=float).sort_index()


def btc_orb_day_sign(btc: pd.DataFrame) -> pd.Series:
    """BTC cash-open ORB day-sign: sign of 15:30→16:00. Peer only, not a trade."""
    groups = by_day(btc)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, 15, 30, 15)
        b1 = first_bar_at(g, day, 16, 0, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0 or p1 == p0:
            continue
        pos[day] = 1.0 if p1 > p0 else -1.0
    return pd.Series(pos, dtype=float).sort_index()


def n75_pos(xau, xag) -> pd.Series:
    """N75: z20 of ln(XAU/XAG) < -1 → long the ratio (+1). One side only."""
    ca = daily_close_22(xau)
    cb = daily_close_22(xag)
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    r = np.log(both["a"] / both["b"])
    z = zscore(r, 20)
    pos = pd.Series(0.0, index=r.index)
    pos[z < -1.0] = 1.0
    return pos


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
    if hit and summary["verdict"] == "PASS_may_PREREG":
        summary["verdict"] = "FAIL_CLONE"
        summary["notes"] += " | CLONE of " + ",".join(hit) + " — no PREREG"
    elif hit:
        # still record; a fail that is also a clone stays FAIL unless the
        # numeric bar is the reason we would have passed. Mark FAIL_CLONE
        # only when the mean would otherwise clear, matching N143.
        if summary.get("mean_bruto_bp") is not None and summary["mean_bruto_bp"] >= summary["gate_bp"]:
            summary["verdict"] = "FAIL_CLONE"
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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # Costs first. No train prices in this block.
    rt = {
        "XPTUSD": honest_rt("XPTUSD", "metal"),
        "XPDUSD": honest_rt("XPDUSD", "metal"),
        "BTCUSD": honest_rt("BTCUSD", "crypto"),
        "ETHUSD": honest_rt("ETHUSD", "crypto"),
    }
    gate_144 = 3.0 * (rt["XPTUSD"]["rt_bp"] + rt["XPDUSD"]["rt_bp"])
    gate_145 = 3.0 * (rt["BTCUSD"]["rt_bp"] + rt["ETHUSD"]["rt_bp"])

    need = ("XPTUSD", "XPDUSD", "BTCUSD", "ETHUSD", "XAUUSD", "XAGUSD", "UKOILcash")
    cache = {}
    for s in need:
        df, _ = load_m5(s, TRAIN_START, TRAIN_END)
        cache[s] = df

    # symbol_history says XPT D1 bars=0. M5 is the screen. DIAG only if a leg
    # has no train bars.
    xpt_days = int(cache["XPTUSD"]["time"].dt.normalize().nunique()) if len(cache["XPTUSD"]) else 0
    xpd_days = int(cache["XPDUSD"]["time"].dt.normalize().nunique()) if len(cache["XPDUSD"]) else 0
    btc_days = int(cache["BTCUSD"]["time"].dt.normalize().nunique()) if len(cache["BTCUSD"]) else 0
    eth_days = int(cache["ETHUSD"]["time"].dt.normalize().nunique()) if len(cache["ETHUSD"]) else 0
    hist_144 = xpt_days < 150 or xpd_days < 150
    hist_145 = btc_days < 150 or eth_days < 150

    t144, ratio144, z144, pos144, meta144 = screen_xs(
        cache["XPTUSD"], cache["XPDUSD"], 15, 30, 21, 0, "xpt", "xpd", thr=1.5
    )
    t145, ratio145, z145, pos145, meta145 = screen_xs(
        cache["BTCUSD"], cache["ETHUSD"], 15, 30, 21, 0, "btc", "eth", thr=1.5
    )
    meta144["train_days_xpt"] = xpt_days
    meta144["train_days_xpd"] = xpd_days
    meta144["symbol_history_XPT_d1_bars"] = 0
    meta144["symbol_history_note"] = "symbol_history_FTMO.csv XPTUSD first_d1='-' bars=0; M5 gz is populated"
    meta145["train_days_btc"] = btc_days
    meta145["train_days_eth"] = eth_days
    meta145["in_symbol_list"] = True
    meta145["in_costs_ftmo"] = False

    z_auag, pos_auag = ratio_z_pos(cache, "XAUUSD", "XAGUSD", 40, 1.5)
    z_auoil, pos_auoil = ratio_z_pos(cache, "XAUUSD", "UKOILcash", 40, 1.5)
    z_pplt, pos_pplt = level_z_pos("PPLT", 40, 1.5)
    z_gld, pos_gld = level_z_pos("GLD", 40, 1.5)
    # N113 SLV/GLD z40 thr ±1.0 fade. Position sign matches the ratio fade
    # (z>+1 → short the ratio), which is also the US500 side in that PREREG.
    slv = load_daily_close("SLV")
    gld = load_daily_close("GLD")
    sg = (slv / gld).dropna()
    z_n113 = zscore(sg, 40)
    pos_n113 = pd.Series(0.0, index=sg.index)
    pos_n113[z_n113 > 1.0] = -1.0
    pos_n113[z_n113 < -1.0] = 1.0
    pos_n75 = n75_pos(cache["XAUUSD"], cache["XAGUSD"])
    pos_n45 = n45_eth_pos(cache["ETHUSD"])
    pos_orb = btc_orb_day_sign(cache["BTCUSD"])

    c144 = bundle(z144, pos144, [
        ("XAU_XAG_z40", z_auag, pos_auag, True),
        ("XAU_UKOIL_z40_N140", z_auoil, pos_auoil, True),
        ("PPLT_z40_N129", z_pplt, pos_pplt, True),
        ("GLD_z40", z_gld, pos_gld, True),
        ("N145_BTC_ETH", z145, pos145, True),
    ])
    for key, peer in (
        ("N75_XAU_XAG_one_side", pos_n75),
        ("N113_SLV_GLD_fade", pos_n113),
    ):
        rec = clone_pair(key, None, pos144, None, peer.reindex(pos144.index).fillna(0.0))
        rec["binding"] = True
        c144[key] = rec

    c145 = bundle(z145, pos145, [
        ("XPT_XPD_z40_N144", z144, pos144, True),
        ("XAU_XAG_z40", z_auag, pos_auag, True),
    ])
    # ETH leg of N145 is the opposite of the basket side.
    eth_leg = (-pos145).rename("eth_leg")
    rec = clone_pair("N45_ETH_asia_cont_vs_ETH_leg", None, eth_leg, None, pos_n45.reindex(eth_leg.index).fillna(0.0))
    rec["binding"] = True
    c145["N45_ETH_asia_cont_vs_ETH_leg"] = rec
    rec = clone_pair("BTC_ORB_1530_1600_vs_BTC_leg", None, pos145, None, pos_orb.reindex(pos145.index).fillna(0.0))
    rec["binding"] = True
    c145["BTC_ORB_1530_1600_vs_BTC_leg"] = rec

    s144 = verdict(
        t144, gate_144, "N144", "XPTUSD+XPDUSD",
        (
            f"XPT_XPD_PGM_XS z40/±1.5 both legs 15:30→21:00; "
            f"honest gate 3*({rt['XPTUSD']['rt_bp']}+{rt['XPDUSD']['rt_bp']}); "
            f"stated est was 202.71 spread-only; swap 0; NEW_FAMILY BM"
        ),
        history_missing=hist_144,
    )
    s144["meta"] = meta144
    s144["rt"] = {"XPTUSD": rt["XPTUSD"], "XPDUSD": rt["XPDUSD"]}
    s144["stated_gate_bp"] = 202.71
    s144["rt_in_costs"] = False
    apply_clone(s144, c144)
    s144["clone"] = c144

    s145 = verdict(
        t145, gate_145, "N145", "BTCUSD+ETHUSD",
        (
            f"BTC_ETH_CRYPTO_XS z40/±1.5 both legs 15:30→21:00; "
            f"honest gate 3*({rt['BTCUSD']['rt_bp']}+{rt['ETHUSD']['rt_bp']}); "
            f"stated est was 23.25 (BTC median kept spread=0); swap 0; NEW_FAMILY BN; "
            f"both legs in SymbolList_FTMO Crypto I CFD; M5 from 2021-01-01"
        ),
        history_missing=hist_145,
    )
    s145["meta"] = meta145
    s145["rt"] = {"BTCUSD": rt["BTCUSD"], "ETHUSD": rt["ETHUSD"]}
    s145["stated_gate_bp"] = 23.25
    s145["rt_in_costs"] = False
    apply_clone(s145, c145)
    s145["clone"] = c145

    pd.DataFrame(t144).to_csv(OUT / "n144_trades_train.csv", index=False)
    pd.DataFrame(t145).to_csv(OUT / "n145_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N144": pub(s144),
        "N145": pub(s145),
        "N144_clones": c144,
        "N145_clones": c145,
        "gates": {"N144": round(gate_144, 4), "N145": round(gate_145, 4), "stated": {"N144": 202.71, "N145": 23.25}},
        "rt": rt,
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "session": "15:30-21:00 CET",
        "no_thr_grid": True,
        "no_2024_in_signal": True,
        "cost_sample": "2024-01-01..2026-09-30 all hours, spread>0",
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} stated={s.get('stated_gate_bp')} "
            f"→ **{s['verdict']}** years={s.get('years')} "
            f"L/S={s.get('n_long_basket')}/{s.get('n_short_basket')} "
            f"hits={s.get('clone_hits')} meta={s.get('meta')}\n"
        )

    md = (
        "# D-092.1 N144/N145 pre-screen (train 2021–2023)\n\n"
        + line("N144 XPT_XPD_PGM_XS", s144)
        + line("N145 BTC_ETH_CRYPTO_XS", s145)
        + "\nHonest RT = all-hours median spread (spread>0, 2024-01-01..2026-09-30) "
        + "+ commission. Session medians logged, not used. No thr-grid. No 2024+ selection.\n"
        + f"\nRT XPT {rt['XPTUSD']['rt_bp']} (spread {rt['XPTUSD']['spread_med_all_hours_bp']} "
        + f"+ 2×{rt['XPTUSD']['comm_bp_per_side']}) / "
        + f"XPD {rt['XPDUSD']['rt_bp']} (spread {rt['XPDUSD']['spread_med_all_hours_bp']} "
        + f"+ 2×{rt['XPDUSD']['comm_bp_per_side']}).\n"
        + f"RT BTC {rt['BTCUSD']['rt_bp']} (spread {rt['BTCUSD']['spread_med_all_hours_bp']} "
        + f"+ 2×{rt['BTCUSD']['comm_bp_per_side']}; zero-spread share {rt['BTCUSD']['zero_spread_share']}) / "
        + f"ETH {rt['ETHUSD']['rt_bp']} (spread {rt['ETHUSD']['spread_med_all_hours_bp']} "
        + f"+ 2×{rt['ETHUSD']['comm_bp_per_side']}).\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N144": pub(s144), "N145": pub(s145), "gates": summary["gates"]}, indent=2, default=str))


if __name__ == "__main__":
    main()
