#!/usr/bin/env python3
"""D-092.1 TRAIN pre-screen: N180 UK100 5d morning fade + N181 JP225 1d afternoon fade.

Dead books not reused:
  UK100 N107 Lon-AM impulse → FRA40 afternoon; N138 GER/UK XS 15:30→21:00.
  JP225 N105 Tokyo-AM → Lon 08:00→14:00 continuation; N139 JP/HK XS 03:00→08:00.
Gates 3x C-048 COSTS_FTMO.csv (79d09e0), not alle. No 2025+ in the PnL.
Session-flat, swap nights 0. No thr-grid.

Clone bar: agree>=0.90 OR (agree>=0.85 AND cover>=0.70)
OR |z|>=0.90 OR (agree>=0.98 and n_both>=30).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n180_n181_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2024-12-31 23:59:59")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70
AGREE_HARD = 0.90
Z_CLONE = 0.90
AGREE_EXACT = 0.98
EXACT_MIN_N = 30

COSTS_RT = {"UK100cash": 1.42, "JP225cash": 1.51}
GATE_180 = 3.0 * COSTS_RT["UK100cash"]  # 4.26
GATE_181 = 3.0 * COSTS_RT["JP225cash"]  # 4.53
HIST_YEARS = {"UK100cash": 5.73, "JP225cash": 5.74}
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


def verdict(trades, gate, rt, label, instrument, notes, hist_years):
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
        "history_years": hist_years,
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
    uk = load_m5("UK100cash")
    jp = load_m5("JP225cash")
    t180, pos180, ret5, meta180 = session_prior(uk, 5, True, 9, 0, 12, 30)
    t181, pos181, ret1, meta181 = session_prior(jp, 1, True, 15, 0, 20, 0)

    def stamp(meta, sym, sess):
        meta["rt_in_costs_ftmo_csv"] = True
        meta["gate_file"] = "C-048 79d09e0 COSTS_FTMO.csv appended row; not COSTS_FTMO_alle"
        meta["d094a"] = (
            f"FTMO M5 file span {HIST_YEARS[sym]}y (>=5.73). "
            f"PnL through 2024-12-31 only ({TRADED_YEARS_TO_2024}y). 2025+ not loaded."
        )
        meta["history_years"] = HIST_YEARS[sym]
        meta["symbol_list"] = f"SymbolList_FTMO.csv {sym}"
        meta["swap_nights"] = 0
        meta["no_2025_plus"] = True
        meta["session"] = sess
    stamp(meta180, "UK100cash", "prior 5d return fade; entry 09:00 flat 12:30 CET")
    stamp(meta181, "JP225cash", "prior 1d return fade; entry 15:00 flat 20:00 CET")

    n138 = load_side_csv(ROOT / "results/R2/n138_n139_prescreen/n138_trades_train.csv")
    n139 = load_side_csv(ROOT / "results/R2/n138_n139_prescreen/n139_trades_train.csv")
    n107 = load_side_csv(ROOT / "results/R2/n106_n107_prescreen/n107_trades_train.csv")
    n105 = load_side_csv(ROOT / "results/R2/n104_n105_prescreen/n105_trades_train.csv")
    # N138 +1 is long GER / short UK, so the UK leg is the opposite sign.
    uk_leg = -n138
    jp_leg = n139

    peers_180 = {
        "N138_UK_leg": (uk_leg, None, True),
        "N107_UK_impulse_to_FRA": (n107, None, True),
        "N181_JP_1d_fade": (pos181, ret1, True),
    }
    c180 = {n: clone_sign(n, pos180, p, binding=b, z_c=ret5, z_p=z) for n, (p, z, b) in peers_180.items()}
    peers_181 = {
        "N139_JP_leg": (jp_leg, None, True),
        "N105_Tokyo_to_Lon": (n105, None, True),
        "N180_UK_5d_fade": (pos180, ret5, True),
    }
    c181 = {n: clone_sign(n, pos181, p, binding=b, z_c=ret1, z_p=z) for n, (p, z, b) in peers_181.items()}

    s180 = verdict(
        t180, GATE_180, COSTS_RT["UK100cash"], "N180", "UK100cash",
        "UK100_PRIOR5D_MORNING_FADE fade prior 5d, session-flat 09:00→12:30; "
        f"gate 3*{COSTS_RT['UK100cash']}={GATE_180:.2f} from C-048 COSTS_FTMO.csv; "
        "not N107 Lon-AM→FRA afternoon and not N138 15:30→21:00 XS; "
        "swap nights 0; M5 5.73y; PnL through 2024-12-31; NEW_FAMILY CW",
        HIST_YEARS["UK100cash"],
    )
    s180["meta"] = meta180
    s180["gate_source"] = "C-048 79d09e0 COSTS_FTMO.csv UK100cash rondreis_bp 1.42 × 3 = 4.26"
    apply_clone(s180, c180)
    s180["clone"] = c180

    s181 = verdict(
        t181, GATE_181, COSTS_RT["JP225cash"], "N181", "JP225cash",
        "JP225_PRIOR1D_AFTERNOON_FADE fade prior 1d, session-flat 15:00→20:00; "
        f"gate 3*{COSTS_RT['JP225cash']}={GATE_181:.2f} from C-048 COSTS_FTMO.csv; "
        "not N105 Tokyo-AM→Lon 08:00→14:00 and not N139 Asia XS 03:00→08:00; "
        "swap nights 0; M5 5.74y; PnL through 2024-12-31; NEW_FAMILY CX",
        HIST_YEARS["JP225cash"],
    )
    s181["meta"] = meta181
    s181["gate_source"] = "C-048 79d09e0 COSTS_FTMO.csv JP225cash rondreis_bp 1.51 × 3 = 4.53"
    apply_clone(s181, c181)
    s181["clone"] = c181

    pd.DataFrame(t180).to_csv(OUT / "n180_trades_train.csv", index=False)
    pd.DataFrame(t181).to_csv(OUT / "n181_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N180": pub(s180),
        "N181": pub(s181),
        "N180_clones": c180,
        "N181_clones": c181,
        "not_screened": {
            "HK50cash": "Cleared its own clone bar in the pre-check but was not needed once UK100 and JP225 both cleared.",
            "AUS200cash": "Cleared its own clone bar in the pre-check. Same-rule agree with UK100 was about 0.75, under 0.85, but left unused.",
            "USDSEK_USDNOK_USDZAR": "M5 4.74y. Not screened.",
            "USDHKD": "Not given an id.",
        },
        "gates": {"N180": round(GATE_180, 4), "N181": round(GATE_181, 4)},
        "costs_rt": COSTS_RT,
        "pnl_through": "2024-12-31",
        "no_2025_plus": True,
        "min_n": MIN_N,
        "no_thr_grid": True,
        "trial_count_unchanged": 471,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N180/N181 pre-screen (through 2024-12-31, no 2025+)\n\n"
        f"- **N180 UK100 5d morning fade**: N={s180['n']} mean={s180['mean_bruto_bp']} "
        f"netto={s180.get('netto_bp')} gate={s180['gate_bp']} → **{s180['verdict']}** "
        f"years={s180.get('years')} hits={s180.get('clone_hits')}\n"
        f"- **N181 JP225 1d afternoon fade**: N={s181['n']} mean={s181['mean_bruto_bp']} "
        f"netto={s181.get('netto_bp')} gate={s181['gate_bp']} → **{s181['verdict']}** "
        f"years={s181.get('years')} hits={s181.get('clone_hits')}\n"
    )
    print(json.dumps({"N180": pub(s180), "N181": pub(s181)}, indent=2, default=str))
    for label, clones in (("180", c180), ("181", c181)):
        print("---", label)
        for k, v in clones.items():
            print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "z_corr_train", "clone")})


if __name__ == "__main__":
    main()
