#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N146 AUD_XAU_COMMODITY_XS + N147 GBP_UKOIL_PETRO_XS.

Gates are the COSTS_FTMO.csv round-trips, frozen before any train PnL.
Not a session-median and not a softer number.

  N146 AUDUSD RT 1.22 + XAUUSD RT 0.83 = 2.05 → gate 3× = 6.15 bp.
  N147 GBPUSD RT 0.70 + UKOILcash RT 2.71 = 3.41 → gate 3× = 10.23 bp.

Session-flat 15:30→21:00 CET is the cheapest side: swap is 0 and is in the
gate as 0. Overnight would add a positive cost on at least one side
(UKOIL short 27.03; AUD both sides >0; XAU long 2.15; GBP both >0).

Clone bar (precommitted in the VOORSTELs; decided before the run):
  FAIL_CLONE if |z Pearson| >= 0.90, or
  (sign agree on both-active >= 0.85 AND cover >= 0.70).
  A clone is not a PASS. No thr-grid. No soft gate. No single-leg rewrite.

Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0. Threshold ±1.5 frozen.
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n146_n147_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70

# COSTS_FTMO.csv roundtrip_intraday_bp. Frozen. Not remeasured.
COSTS_RT = {
    "AUDUSD": 1.22,
    "XAUUSD": 0.83,
    "GBPUSD": 0.70,
    "UKOILcash": 2.71,
    "USOILcash": 3.34,
    "XAGUSD": 5.07,
}
GATE_146 = 3.0 * (COSTS_RT["AUDUSD"] + COSTS_RT["XAUUSD"])  # 6.15
GATE_147 = 3.0 * (COSTS_RT["GBPUSD"] + COSTS_RT["UKOILcash"])  # 10.23


def load_m5(sym: str, start, end) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[(df["time"] >= start) & (df["time"] <= end)].reset_index(drop=True)
    return df


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


def n75_pos(xau, xag) -> pd.Series:
    ca = daily_close_22(xau)
    cb = daily_close_22(xag)
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    r = np.log(both["a"] / both["b"])
    z = zscore(r, 20)
    pos = pd.Series(0.0, index=r.index)
    pos[z < -1.0] = 1.0
    return pos


def n91_aud_day_sign(aud: pd.DataFrame) -> pd.Series:
    """N91: ret5>0 → long AUD. Day-sign dated on the signal day. Long-only."""
    c = daily_close_22(aud)
    ret5 = c / c.shift(5) - 1.0
    pos = pd.Series(0.0, index=c.index)
    pos[ret5 > 0] = 1.0
    return pos


def n22_ukoil_day_sign(oil: pd.DataFrame) -> pd.Series:
    """N22: lon 09:00→12:00 ≥±40 bp → fade at the day. UKOIL day-sign."""
    groups = by_day(oil)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, 9, 0, 15)
        b1 = first_bar_at(g, day, 12, 0, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0:
            continue
        lon = 1e4 * (p1 / p0 - 1.0)
        if lon >= 40:
            pos[day] = -1.0
        elif lon <= -40:
            pos[day] = 1.0
    return pd.Series(pos, dtype=float).sort_index()


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
        # Precommitted bar: a clone is FAIL_CLONE even when the mean is under the gate
        # (same labeling as N141). Not a PASS.
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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    need = ("AUDUSD", "XAUUSD", "GBPUSD", "UKOILcash", "USOILcash", "XAGUSD")
    cache = {}
    for s in need:
        cache[s] = load_m5(s, TRAIN_START, TRAIN_END)

    days = {s: int(cache[s]["time"].dt.normalize().nunique()) if len(cache[s]) else 0 for s in need}
    hist_146 = days["AUDUSD"] < 150 or days["XAUUSD"] < 150
    hist_147 = days["GBPUSD"] < 150 or days["UKOILcash"] < 150

    t146, _, z146, pos146, meta146 = screen_xs(
        cache["AUDUSD"], cache["XAUUSD"], 15, 30, 21, 0, "aud", "xau", thr=1.5
    )
    t147, _, z147, pos147, meta147 = screen_xs(
        cache["GBPUSD"], cache["UKOILcash"], 15, 30, 21, 0, "gbp", "ukoil", thr=1.5
    )
    meta146["train_days"] = {"AUDUSD": days["AUDUSD"], "XAUUSD": days["XAUUSD"]}
    meta147["train_days"] = {"GBPUSD": days["GBPUSD"], "UKOILcash": days["UKOILcash"]}
    meta146["rt_in_costs"] = True
    meta147["rt_in_costs"] = True
    meta146["swap_bp"] = 0
    meta147["swap_bp"] = 0
    meta146["session"] = "15:30-21:00 CET cheapest side (overnight swap excluded)"
    meta147["session"] = "15:30-21:00 CET cheapest side (UKOIL short swap 27.03 not in alpha)"

    z_auag, pos_auag = ratio_z_pos(cache, "XAUUSD", "XAGUSD", 40, 1.5)
    z_auoil, pos_auoil = ratio_z_pos(cache, "XAUUSD", "UKOILcash", 40, 1.5)
    z_oils, pos_oils = ratio_z_pos(cache, "UKOILcash", "USOILcash", 40, 1.5)
    z_gld, pos_gld = level_z_pos("GLD", 40, 1.5)
    pos_n75 = n75_pos(cache["XAUUSD"], cache["XAGUSD"])
    pos_n91 = n91_aud_day_sign(cache["AUDUSD"])
    pos_n22 = n22_ukoil_day_sign(cache["UKOILcash"])

    c146 = bundle(z146, pos146, [
        ("XAU_XAG_z40", z_auag, pos_auag, True),
        ("XAU_UKOIL_z40_N140", z_auoil, pos_auoil, True),
        ("GLD_z40", z_gld, pos_gld, True),
        ("GBP_UKOIL_z40_N147", z147, pos147, True),
    ])
    # AUD leg of the basket is `pos` itself (+1 = long AUD).
    rec = clone_pair("N75_XAU_XAG_one_side", None, pos146, None, pos_n75.reindex(pos146.index).fillna(0.0))
    rec["binding"] = True
    c146["N75_XAU_XAG_one_side"] = rec
    rec = clone_pair("N140_XAU_UKOIL_sign", None, pos146, None, pos_auoil.reindex(pos146.index).fillna(0.0))
    rec["binding"] = True
    c146["N140_XAU_UKOIL_sign"] = rec
    rec = clone_pair("N91_AUD_day_sign", None, pos146, None, pos_n91.reindex(pos146.index).fillna(0.0))
    rec["binding"] = True
    c146["N91_AUD_day_sign"] = rec

    c147 = bundle(z147, pos147, [
        ("UKOIL_USOIL_z40_N136", z_oils, pos_oils, True),
        ("XAU_UKOIL_z40_N140", z_auoil, pos_auoil, True),
        ("AUD_XAU_z40_N146", z146, pos146, True),
    ])
    rec = clone_pair("N136_BRENT_WTI_sign", None, pos147, None, pos_oils.reindex(pos147.index).fillna(0.0))
    rec["binding"] = True
    c147["N136_BRENT_WTI_sign"] = rec
    rec = clone_pair("N140_XAU_UKOIL_sign", None, pos147, None, pos_auoil.reindex(pos147.index).fillna(0.0))
    rec["binding"] = True
    c147["N140_XAU_UKOIL_sign"] = rec
    # UKOIL leg is the opposite of the basket side.
    oil_leg = (-pos147).rename("ukoil_leg")
    rec = clone_pair("N22_UKOIL_LonNY_day_sign", None, oil_leg, None, pos_n22.reindex(oil_leg.index).fillna(0.0))
    rec["binding"] = True
    c147["N22_UKOIL_LonNY_day_sign"] = rec

    s146 = verdict(
        t146, GATE_146, "N146", "AUDUSD+XAUUSD",
        (
            "AUD_XAU_COMMODITY_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['AUDUSD']}+{COSTS_RT['XAUUSD']}); swap 0; NEW_FAMILY BO"
        ),
        history_missing=hist_146,
    )
    s146["meta"] = meta146
    s146["costs_rt"] = {"AUDUSD": COSTS_RT["AUDUSD"], "XAUUSD": COSTS_RT["XAUUSD"]}
    s146["rt_in_costs"] = True
    apply_clone(s146, c146)
    s146["clone"] = c146

    s147 = verdict(
        t147, GATE_147, "N147", "GBPUSD+UKOILcash",
        (
            "GBP_UKOIL_PETRO_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['GBPUSD']}+{COSTS_RT['UKOILcash']}); swap 0; NEW_FAMILY BP"
        ),
        history_missing=hist_147,
    )
    s147["meta"] = meta147
    s147["costs_rt"] = {"GBPUSD": COSTS_RT["GBPUSD"], "UKOILcash": COSTS_RT["UKOILcash"]}
    s147["rt_in_costs"] = True
    apply_clone(s147, c147)
    s147["clone"] = c147

    pd.DataFrame(t146).to_csv(OUT / "n146_trades_train.csv", index=False)
    pd.DataFrame(t147).to_csv(OUT / "n147_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N146": pub(s146),
        "N147": pub(s147),
        "N146_clones": c146,
        "N147_clones": c147,
        "gates": {"N146": round(GATE_146, 4), "N147": round(GATE_147, 4)},
        "costs_rt": COSTS_RT,
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "session": "15:30-21:00 CET",
        "no_thr_grid": True,
        "no_2024_in_signal": True,
        "gate_source": "COSTS_FTMO.csv roundtrip_intraday_bp; not a session median",
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
        "# D-092.1 N146/N147 pre-screen (train 2021–2023)\n\n"
        + line("N146 AUD_XAU_COMMODITY_XS", s146)
        + line("N147 GBP_UKOIL_PETRO_XS", s147)
        + "\nGates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. "
        + "No thr-grid. No 2024+ selection. No softer session spread.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N146": pub(s146), "N147": pub(s147), "clones146": c146, "clones147": c147}, indent=2, default=str))


if __name__ == "__main__":
    main()
