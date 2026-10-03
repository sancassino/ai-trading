#!/usr/bin/env python3
"""D-092.1 TRAIN pre-screen: N182 HK50 5d Europe fade + N183 AUS200 afternoon 1d fade.

Dead books not reused:
  HK50 N64 short-only TSMOM 20→10; N139 JP/HK Asia XS 03:00→08:00 (HK leg).
  AUS200 N61 short-only TSMOM 20→10; N108 Asia-AM → Lon 08:00→12:00 continuation.
Gates 3x C-048 COSTS_FTMO.csv (79d09e0), not alle. No 2025+ in the PnL.
Session-flat, swap nights 0. No thr-grid. Not a redo of N180/N181.

Clone bar: agree>=0.90 OR (agree>=0.85 AND cover>=0.70)
OR |z|>=0.90 OR (agree>=0.98 and n_both>=30).
Mutual agree and agree vs N180/N181 must stay under 0.85.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n182_n183_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2024-12-31 23:59:59")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70
AGREE_HARD = 0.90
Z_CLONE = 0.90
AGREE_EXACT = 0.98
EXACT_MIN_N = 30

COSTS_RT = {"HK50cash": 2.63, "AUS200cash": 1.36}
GATE_182 = 3.0 * COSTS_RT["HK50cash"]  # 7.89
GATE_183 = 3.0 * COSTS_RT["AUS200cash"]  # 4.08
HIST_YEARS = {"HK50cash": 5.74, "AUS200cash": 5.74}
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
    hk = load_m5("HK50cash")
    aus = load_m5("AUS200cash")
    t182, pos182, ret5, meta182 = session_prior(hk, 5, True, 9, 0, 15, 0)
    t183, pos183, ret1, meta183 = session_prior(aus, 1, True, 14, 0, 18, 0)

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
    stamp(meta182, "HK50cash", "prior 5d return fade; entry 09:00 flat 15:00 CET")
    stamp(meta183, "AUS200cash", "prior 1d return fade; entry 14:00 flat 18:00 CET")

    n139 = load_side_csv(ROOT / "results/R2/n138_n139_prescreen/n139_trades_train.csv")
    n64 = load_side_csv(ROOT / "results/R2/n58_n62_prescreen/N64_trades.csv", hold_expand=10)
    n108 = load_side_csv(ROOT / "results/R2/n108_n109_prescreen/n108_trades_train.csv")
    n61 = load_side_csv(ROOT / "results/R2/n58_n62_prescreen/N61_trades.csv", hold_expand=10)
    n180 = load_side_csv(ROOT / "results/R2/n180_n181_prescreen/n180_trades_train.csv")
    n181 = load_side_csv(ROOT / "results/R2/n180_n181_prescreen/n181_trades_train.csv")
    # N139 +1 is long JP / short HK, so the HK leg is the opposite sign.
    hk_leg = -n139

    peers_182 = {
        "N139_HK_leg": (hk_leg, None, True),
        "N64_HK50_SO_20_10": (n64, None, True),
        "N180_UK_5d_fade": (n180, None, True),
        "N181_JP_1d_fade": (n181, None, True),
        "N183_AUS_1d_fade": (pos183, ret1, True),
    }
    c182 = {n: clone_sign(n, pos182, p, binding=b, z_c=ret5, z_p=z) for n, (p, z, b) in peers_182.items()}
    peers_183 = {
        "N108_Asia_to_Lon": (n108, None, True),
        "N61_AUS_SO_20_10": (n61, None, True),
        "N180_UK_5d_fade": (n180, None, True),
        "N181_JP_1d_fade": (n181, None, True),
        "N182_HK_5d_fade": (pos182, ret5, True),
    }
    c183 = {n: clone_sign(n, pos183, p, binding=b, z_c=ret1, z_p=z) for n, (p, z, b) in peers_183.items()}

    s182 = verdict(
        t182, GATE_182, COSTS_RT["HK50cash"], "N182", "HK50cash",
        "HK50_PRIOR5D_EUROPE_FADE fade prior 5d, session-flat 09:00→15:00; "
        f"gate 3*{COSTS_RT['HK50cash']}={GATE_182:.2f} from C-048 COSTS_FTMO.csv; "
        "not N64 20/10 short and not N139 Asia XS 03:00→08:00; "
        "swap nights 0; M5 5.74y; PnL through 2024-12-31; NEW_FAMILY CY",
        HIST_YEARS["HK50cash"],
    )
    s182["meta"] = meta182
    s182["gate_source"] = "C-048 79d09e0 COSTS_FTMO.csv HK50cash rondreis_bp 2.63 × 3 = 7.89"
    apply_clone(s182, c182)
    s182["clone"] = c182

    s183 = verdict(
        t183, GATE_183, COSTS_RT["AUS200cash"], "N183", "AUS200cash",
        "AUS200_PRIOR1D_AFTERNOON_FADE fade prior 1d, session-flat 14:00→18:00; "
        f"gate 3*{COSTS_RT['AUS200cash']}={GATE_183:.2f} from C-048 COSTS_FTMO.csv; "
        "not N108 Asia-AM→Lon 08:00→12:00 and not N61 20/10 short; "
        "swap nights 0; M5 5.74y; PnL through 2024-12-31; NEW_FAMILY CZ",
        HIST_YEARS["AUS200cash"],
    )
    s183["meta"] = meta183
    s183["gate_source"] = "C-048 79d09e0 COSTS_FTMO.csv AUS200cash rondreis_bp 1.36 × 3 = 4.08"
    apply_clone(s183, c183)
    s183["clone"] = c183

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    # Assign ids only if the final books stay under the clone bar.
    if s182["verdict"] == "FAIL_CLONE" or s183["verdict"] == "FAIL_CLONE":
        summary = {
            "discarded": {"N182_candidate": pub(s182), "N183_candidate": pub(s183)},
            "N182_clones": c182,
            "N183_clones": c183,
            "ids_assigned": False,
            "trial_count_unchanged": 471,
        }
        (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))
        print("CLONE_DISCARD")
        print(json.dumps(summary["discarded"], indent=2, default=str))
        return

    pd.DataFrame(t182).to_csv(OUT / "n182_trades_train.csv", index=False)
    pd.DataFrame(t183).to_csv(OUT / "n183_trades_train.csv", index=False)
    summary = {
        "N182": pub(s182),
        "N183": pub(s183),
        "N182_clones": c182,
        "N183_clones": c183,
        "gates": {"N182": round(GATE_182, 4), "N183": round(GATE_183, 4)},
        "costs_rt": COSTS_RT,
        "pnl_through": "2024-12-31",
        "no_2025_plus": True,
        "min_n": MIN_N,
        "no_thr_grid": True,
        "trial_count_unchanged": 471,
        "closes_c048_nine": True,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N182/N183 pre-screen (through 2024-12-31, no 2025+)\n\n"
        f"- **N182 HK50 5d Europe fade**: N={s182['n']} mean={s182['mean_bruto_bp']} "
        f"netto={s182.get('netto_bp')} gate={s182['gate_bp']} → **{s182['verdict']}** "
        f"years={s182.get('years')} hits={s182.get('clone_hits')}\n"
        f"- **N183 AUS200 afternoon 1d fade**: N={s183['n']} mean={s183['mean_bruto_bp']} "
        f"netto={s183.get('netto_bp')} gate={s183['gate_bp']} → **{s183['verdict']}** "
        f"years={s183.get('years')} hits={s183.get('clone_hits')}\n"
    )
    print(json.dumps({"N182": pub(s182), "N183": pub(s183)}, indent=2, default=str))
    for label, clones in (("182", c182), ("183", c183)):
        print("---", label)
        for k, v in clones.items():
            print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "z_corr_train", "clone")})


if __name__ == "__main__":
    main()
