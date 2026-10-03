#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N172 USOIL 5d swing reversal + N173 USDCAD 1d swing continuation.

Both session-flat. Gates frozen from COSTS_FTMO.csv before PnL.
No thr-grid. No soft-pass. N<150 is UNDERPOWERED.

N170 FRA40 NY-impulse fade and N171 BTC EU-morning fade were filed OPEN on
4005235 and are not screened here: NY impulse fade and BTC/ETH are barred,
and their stated gates are not COSTS_FTMO.csv rows.

Clone bar: agree>=0.90 OR (agree>=0.85 AND cover>=0.70) OR |z|>=0.90
OR (agree>=0.98 and n_both>=30).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n172_n173_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
WARM = pd.Timestamp("2020-06-01")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70
AGREE_HARD = 0.90
Z_CLONE = 0.90
AGREE_EXACT = 0.98
EXACT_MIN_N = 30

COSTS_RT = {"USOILcash": 3.34, "USDCAD": 0.80}
GATE_172 = 3.0 * COSTS_RT["USOILcash"]  # 10.02
GATE_173 = 3.0 * COSTS_RT["USDCAD"]  # 2.40


def load_m5(sym: str) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    df = pd.read_csv(path, sep=";", compression="gzip", comment="#", usecols=["time", "close"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[(df["time"] >= WARM) & (df["time"] <= TRAIN_END)].reset_index(drop=True)
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


def session_from_prior_ret(df, lookback: int, fade: bool):
    """Sign of the prior completed lookback-day return. Session 15:30→21:00.
    fade=True → opposite sign (reversal). No threshold."""
    dc = daily_last(df)
    ret = dc / dc.shift(lookback) - 1.0
    groups = by_day(df)
    days = sorted(d for d in groups if TRAIN_START <= d <= TRAIN_END)
    trades = []
    pos = {}
    n_sig = 0
    n_skip = 0
    for day in days:
        prior = ret[ret.index < day].dropna()
        if prior.empty or prior.iloc[-1] == 0 or not np.isfinite(prior.iloc[-1]):
            continue
        if (day - prior.index[-1]).days > 5:
            continue
        n_sig += 1
        raw = float(prior.iloc[-1])
        side = (-1.0 if raw > 0 else 1.0) if fade else (1.0 if raw > 0 else -1.0)
        g = groups[day]
        ent = first_bar(g, day, 15, 30)
        ex = last_le(g, day, 21, 0)
        if ent is None or ex is None or ex["time"] <= ent["time"]:
            n_skip += 1
            continue
        p_ent, p_ex = px(ent), px(ex)
        if p_ent is None or p_ex is None:
            n_skip += 1
            continue
        bruto = side * 1e4 * (p_ex / p_ent - 1.0)
        pos[day] = side
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(prior.index[-1]).date()),
                "side": int(side),
                "prior_ret": round(raw, 6),
                "entry": str(ent["time"]),
                "exit": str(ex["time"]),
                "bruto_bp": float(bruto),
            }
        )
    meta = {
        "n_signal_days": n_sig,
        "n_skip_missing_bar": n_skip,
        "n_trades": len(trades),
        "swap_bp": 0,
        "swap_nights": 0,
        "overnight": False,
        "hold": "session-flat 15:30→21:00",
        "threshold": None,
    }
    return trades, pd.Series(pos, dtype=float).sort_index(), ret, meta


def impulse_pos(df, h0, m0, h1, m1, thr, fade) -> pd.Series:
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        if day < TRAIN_START or day > TRAIN_END:
            continue
        b0 = first_bar(g, day, h0, m0, 15)
        b1 = first_bar(g, day, h1, m1, 15)
        p0, p1 = px(b0), px(b1)
        if p0 is None or p1 is None:
            continue
        move = 1e4 * (p1 / p0 - 1.0)
        if abs(move) < thr:
            continue
        s = 1.0 if move > 0 else -1.0
        pos[day] = -s if fade else s
    return pd.Series(pos, dtype=float).sort_index()


def mom_pos(dc: pd.Series, lookback: int, hold: int, long_only: bool) -> pd.Series:
    dates = list(dc.index)
    pos = {}
    i = lookback
    while i + hold < len(dates):
        t = dates[i]
        if t > TRAIN_END:
            break
        c0 = float(dc.iloc[i])
        cl = float(dc.iloc[i - lookback])
        if cl <= 0 or c0 <= 0:
            i += 1
            continue
        ret = c0 / cl - 1.0
        if ret > 0:
            side = 1.0
        elif ret < 0 and not long_only:
            side = -1.0
        else:
            i += 1
            continue
        if t >= TRAIN_START:
            for k in range(hold):
                if i + k < len(dates) and dates[i + k] <= TRAIN_END:
                    pos[dates[i + k]] = side
        i += hold
    return pd.Series(pos, dtype=float).sort_index()


def clone_sign(name, cand: pd.Series, peer: pd.Series, binding=True, z_c=None, z_p=None) -> dict:
    c = cand.astype(float)
    p_raw = peer.sort_index().astype(float) if peer is not None and len(peer) else pd.Series(dtype=float)
    aligned = []
    for dt, cv in c.items():
        if dt in p_raw.index:
            pv = p_raw.loc[dt]
            pv = float(pv.iloc[0] if hasattr(pv, "iloc") else pv)
            aligned.append((dt, float(cv), pv))
        else:
            prev = p_raw[p_raw.index < dt]
            aligned.append((dt, float(cv), float(prev.iloc[-1]) if len(prev) else 0.0))
    both = pd.DataFrame(aligned, columns=["date", "c", "p"]).set_index("date")
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
    }
    if n == 0:
        base["verdict"] = "DIAG_FAIL"
        return base
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    netto = mean - rt  # session-flat, one RT, credits not added
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
    dates = pd.to_datetime([t["date"] for t in trades])
    span_y = float((dates.max() - dates.min()).days) / 365.25 if len(dates) else 0.0
    base.update(
        {
            "mean_bruto_bp": round(mean, 4),
            "netto_bp": round(netto, 4),
            "median_bruto_bp": round(float(np.median(arr)), 4),
            "stress_gate_bp": round(gate * 1.5, 4),
            "stress_note": (
                "PASS_stress_informal"
                if mean >= gate * 1.5
                else "BELOW_stress_1.5x (info only; own gate is the cost gate)"
            ),
            "verdict": v,
            "hit_rate": round(float((arr > 0).mean()), 4),
            "n_long": int(sum(1 for t in trades if t["side"] > 0)),
            "n_short": int(sum(1 for t in trades if t["side"] < 0)),
            "years": years,
            "trade_span_years": round(span_y, 2),
        }
    )
    return base


def apply_clone(summary, clones):
    hit = [k for k, v in clones.items() if v.get("clone") and v.get("binding", True)]
    summary["clone_hits"] = hit
    if hit and summary["verdict"] != "DIAG_FAIL":
        summary["verdict"] = "FAIL_CLONE"
        if "CLONE" not in summary["notes"]:
            summary["notes"] += " | CLONE of " + ",".join(hit) + " — no PREREG"
    return summary


def daily_file_years(name: str) -> float:
    path = ROOT / "data" / "daily" / name
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#") and not ln.lower().startswith("date")]
    if len(body) < 2:
        return 0.0
    d0 = pd.Timestamp(body[0].split(";")[0].replace(".", "-")[:10])
    d1 = pd.Timestamp(body[-1].split(";")[0].replace(".", "-")[:10])
    return float((d1 - d0).days) / 365.25


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    books = {s: load_m5(s) for s in ("USOILcash", "UKOILcash", "USDCAD", "USDJPY")}
    dc = {s: daily_last(books[s]) for s in books}

    t172, pos172, ret5_oil, meta172 = session_from_prior_ret(books["USOILcash"], 5, fade=True)
    t173, pos173, ret1_cad, meta173 = session_from_prior_ret(books["USDCAD"], 1, fade=False)
    # same-rule UKOIL reversal (not a dead id; informational, not binding)
    _t_uk, pos_uk, ret5_uk, _ = session_from_prior_ret(books["UKOILcash"], 5, fade=True)

    meta172["rt_in_costs"] = True
    meta173["rt_in_costs"] = True
    meta172["symbol_list"] = "SymbolList_FTMO.csv USOIL.cash; symbol_history_FTMO first_d1 2020-12-31 bars 1482"
    meta173["symbol_list"] = "SymbolList_FTMO.csv USDCAD Forex"
    meta172["d094a_years"] = round((pd.Timestamp("2026-10-04") - pd.Timestamp("2020-12-31")).days / 365.25, 2)
    meta173["d094a_years"] = round(daily_file_years("USDCAD.csv"), 2)
    meta172["d094a"] = (
        f"USOILcash on the FTMO symbol list; D1 history from 2020-12-31 "
        f"({meta172['d094a_years']}y through 2026-10-04, >=5y). Train book is 2021-2023."
    )
    meta173["d094a"] = (
        f"USDCAD on the FTMO symbol list; daily file span {meta173['d094a_years']}y (>=5y). "
        "Train book is 2021-2023."
    )
    meta172["session"] = "prior 5d return fade; entry 15:30 flat 21:00 CET"
    meta173["session"] = "prior 1d return continuation; entry 15:30 flat 21:00 CET"
    meta173["swap_long_credit_not_in_gate"] = -0.09
    meta173["swap_short_not_in_gate_because_zero_nights"] = 0.98
    meta172["oil_swap_unreliable_not_used"] = "session-flat; long credit -5.40 and short 24.53 not in the gate"

    ret20_oil = dc["USOILcash"] / dc["USOILcash"].shift(20) - 1.0
    ret10_jpy = dc["USDJPY"] / dc["USDJPY"].shift(10) - 1.0
    ret20_cad = dc["USDCAD"] / dc["USDCAD"].shift(20) - 1.0
    ret60_cad = dc["USDCAD"] / dc["USDCAD"].shift(60) - 1.0

    peers_172 = {
        "N50_USOIL_TSMOM20_10_LO": (mom_pos(dc["USOILcash"], 20, 10, True), ret20_oil, True),
        "N49_UKOIL_TSMOM20_10_LO": (mom_pos(dc["UKOILcash"], 20, 10, True), None, True),
        "N158_USOIL_NY_IMPULSE_FADE": (impulse_pos(books["USOILcash"], 15, 30, 17, 0, 40, True), None, True),
        "N22_UKOIL_LonAM_fade": (impulse_pos(books["UKOILcash"], 9, 0, 12, 0, 40, True), None, True),
        "N43_UKOIL_NY_cont": (impulse_pos(books["UKOILcash"], 15, 30, 16, 0, 50, False), None, True),
        "N98_USOIL_LonAM_sign": (impulse_pos(books["USOILcash"], 8, 0, 12, 0, 40, False), None, True),
        "UKOIL_same_rule_5d_reversal_NOT_A_DEAD_ID": (pos_uk, ret5_uk, False),
        "N173_USDCAD_1d_cont": (pos173, ret1_cad, True),
    }
    c172 = {}
    for name, (p, z, binding) in peers_172.items():
        c172[name] = clone_sign(name, pos172, p, binding=binding, z_c=ret5_oil, z_p=z)

    r60_lo = pd.Series(np.where(ret60_cad.dropna() > 0, 1.0, 0.0), index=ret60_cad.dropna().index)
    r20_lo = pd.Series(np.where(ret20_cad.dropna() > 0, 1.0, 0.0), index=ret20_cad.dropna().index)
    peers_173 = {
        "N33_USDCAD_Lon_cont_proxy": (impulse_pos(books["USDCAD"], 8, 0, 12, 0, 35, False), None, True),
        "N48_USDJPY_ret10_sign": (np.sign(ret10_jpy.dropna()), ret10_jpy, True),
        "USDCAD_ret20_LO_N73_family": (r20_lo, ret20_cad, True),
        "USDCAD_ret60_LO_L60_family": (r60_lo, ret60_cad, True),
        "N172_USOIL_5d_reversal": (pos172, ret5_oil, True),
    }
    c173 = {}
    for name, (p, z, binding) in peers_173.items():
        c173[name] = clone_sign(name, pos173, p, binding=binding, z_c=ret1_cad, z_p=z)

    s172 = verdict(
        t172, GATE_172, COSTS_RT["USOILcash"], "N172", "USOILcash",
        "USOIL_PRIOR5D_SWING_REVERSAL sign of prior 5d return, fade, session-flat 15:30→21:00; "
        f"honest COSTS gate 3*{COSTS_RT['USOILcash']}={GATE_172:.2f}; swap nights 0 "
        "(oil swap specs not used); no threshold; not NY-impulse fade (signal is the prior 5d, "
        "entry at 15:30 not after a 15:30–17:00 impulse); not UKOIL overnight; not Brent–WTI; "
        "NEW_FAMILY CO",
    )
    s172["meta"] = meta172
    s172["costs_rt"] = COSTS_RT["USOILcash"]
    s172["gate_source"] = "honest COSTS_FTMO.csv roundtrip_intraday_bp 3.34 × 3 = 10.02"
    apply_clone(s172, c172)
    s172["clone"] = c172

    s173 = verdict(
        t173, GATE_173, COSTS_RT["USDCAD"], "N173", "USDCAD",
        "USDCAD_PRIOR1D_SWING_CONTINUATION sign of prior 1d return, same sign, session-flat 15:30→21:00; "
        f"honest COSTS gate 3*{COSTS_RT['USDCAD']}={GATE_173:.2f} (not the US500 2.34 gate); "
        "swap nights 0 inside the gate; long swap credit -0.09 is not alpha and is not subtracted; "
        "not L60; not a G10 cross; not N33's London-morning window; NEW_FAMILY CP",
    )
    s173["meta"] = meta173
    s173["costs_rt"] = COSTS_RT["USDCAD"]
    s173["gate_source"] = "honest COSTS_FTMO.csv roundtrip_intraday_bp 0.80 × 3 = 2.40; swap nights 0; credit not subtracted"
    s173["swap"] = {
        "nights": 0,
        "long_bp_credit": -0.09,
        "short_bp": 0.98,
        "in_gate_bp": 0.0,
        "credit_treated_as_alpha": False,
    }
    apply_clone(s173, c173)
    s173["clone"] = c173

    pd.DataFrame(t172).to_csv(OUT / "n172_trades_train.csv", index=False)
    pd.DataFrame(t173).to_csv(OUT / "n173_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N172": pub(s172),
        "N173": pub(s173),
        "N172_clones": c172,
        "N173_clones": c173,
        "gates": {"N172": round(GATE_172, 4), "N173": round(GATE_173, 4)},
        "costs_rt": COSTS_RT,
        "clone_rule": {
            "sign_agree_hard_ge": AGREE_HARD,
            "sign_agree_ge": AGREE_CLONE,
            "cover_ge": COVER_CLONE,
            "z_corr_ge": Z_CLONE,
            "agree_exact_ge": AGREE_EXACT,
            "agree_exact_min_n": EXACT_MIN_N,
        },
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap_nights": 0,
        "no_thr_grid": True,
        "no_2024_in_signal": True,
        "discarded_before_id": {
            "USDJPY_rate_carry_5d_LO": "agree 1.00 cover 0.92 vs N53/N67/L60 — clone, no id",
            "USDCAD_rate_carry_LO": "agree 1.00 cover 0.93 vs L60 — clone, no id",
            "GBP_rate_carry_LO": "agree 1.00 cover 0.94 vs ret20 LO — clone, no id",
            "UKOIL_same_5d_reversal": "agree 0.97 cover 0.77 vs this USOIL rule — twin market, not a second id",
            "XAU_5d_reversal": "same mechanism as N172; not filed",
            "N170_FRA40_as_filed": "NY impulse fade + gate not in COSTS_FTMO.csv — discarded, not cost-screened",
            "N171_BTC_as_filed": "BTC/ETH barred — discarded, not cost-screened",
        },
        "trial_count_unchanged": 471,
        "tip_seen": "4005235 filed unscreened N170/N171; those mechanisms do not clear the bar",
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} netto={s.get('netto_bp')} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} "
            f"→ **{s['verdict']}** years={s.get('years')} span={s.get('trade_span_years')} "
            f"L/S={s.get('n_long')}/{s.get('n_short')} "
            f"hits={s.get('clone_hits')} meta_skip={s.get('meta', {}).get('n_skip_missing_bar')}\n"
        )

    md = (
        "# D-092.1 N172/N173 pre-screen (train 2021–2023)\n\n"
        "Commodity swing + FX swing. Session-flat. Not N170 FRA40 NY-impulse (barred; not screened). "
        "Not N171 BTC (barred; not screened). Not a rate-carry (those cloned L60/N53 before an id).\n\n"
        + line("N172 USOIL prior-5d swing reversal session-flat", s172)
        + line("N173 USDCAD prior-1d swing continuation session-flat", s173)
        + "\nGates from COSTS_FTMO.csv round-trips. N172 RT 3.34 × 3 = 10.02. "
        + "N173 RT 0.80 × 3 = 2.40, not the US500 gate. "
        + "Session-flat so swap nights = 0. USDCAD long swap credit −0.09 is not alpha. "
        + "Oil swap specs are not used. No thr-grid. No 2024+ selection.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N172": pub(s172), "N173": pub(s173)}, indent=2, default=str))
    print("---CLONES172---")
    for k, v in c172.items():
        flag = "CLONE" if v["clone"] else ("raw" if v["clone_raw"] else "")
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "n_both_active", "binding")}, flag)
    print("---CLONES173---")
    for k, v in c173.items():
        flag = "CLONE" if v["clone"] else ("raw" if v["clone_raw"] else "")
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "n_both_active", "binding")}, flag)


if __name__ == "__main__":
    main()
