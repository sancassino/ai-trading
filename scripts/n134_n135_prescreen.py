#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N134 XLF→US500 + N135 QUAL→US500.

Freeze (no thr-grid):
  N134: XLF z40/thr1.5 stress_buy → US500cash 15:30→21:00 CET (NEW_FAMILY BC)
  N135: QUAL z40/thr1.5 stress_buy → US500cash 15:30→21:00 CET (NEW_FAMILY BD)
Gate: 3 × US500 RT 0.78 = 2.34 bp; N ≥ 150; train 2021–2023 only.
Clone bar (precommitted): FAIL_CLONE if z Pearson ≥ 0.90, or
  (sign agreement on both-active ≥ 0.85 AND both-active/candidate-active ≥ 0.70).
  N134 vs SECTOR_DISP (XL* 10d cross-section std, z40, fade thr +1.0/−0.5).
  N135 vs EQW (SPX_EQW/SPX z40 stress_buy) and vs IWM (z40 stress_buy).
≠ HYG/EMB/SECTOR_DISP/XLU-XLI/MTUM/EQW/USMV/IWM.
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n134_n135_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE = 2.34


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
    return s[~s.index.duplicated(keep="last")].sort_index().dropna()


def load_m5(sym: str) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)


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


def session_flat_trade(us500_day_g, side: int):
    day = us500_day_g["day"].iloc[0]
    b_entry = first_bar_at(us500_day_g, day, 15, 30, 15)
    b_exit = last_bar_le(us500_day_g, day, 21, 0)
    if b_entry is None or b_exit is None:
        return None
    if b_exit["time"] <= b_entry["time"]:
        return None
    p0 = float(b_entry["close"])
    p1 = float(b_exit["close"])
    if p0 <= 0:
        return None
    return side * 1e4 * (p1 / p0 - 1.0)


def _trades_from_pos(pos: pd.Series, us500: pd.DataFrame):
    us = us500.copy()
    us["day"] = us["time"].dt.normalize()
    days = sorted(us["day"].unique())
    trades = []
    for day in days:
        prior = pos[pos.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        g = us[us["day"] == day]
        if g.empty:
            continue
        bruto = session_flat_trade(g, int(side))
        if bruto is None:
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "side": int(side),
                "bruto_bp": bruto,
                "signal_day": str(prior.index[-1].date()),
            }
        )
    return trades


def screen_stress_z40(sig: pd.Series, us500: pd.DataFrame):
    sig = sig.sort_index()
    z40 = (sig - sig.rolling(40, min_periods=40).mean()) / sig.rolling(
        40, min_periods=40
    ).std(ddof=0).replace(0, np.nan)
    pos = pd.Series(0.0, index=sig.index)
    pos[z40 > 1.5] = -1.0
    pos[z40 < -1.5] = 1.0
    return _trades_from_pos(pos, us500)


def screen_inverse_z120(sig: pd.Series, us500: pd.DataFrame):
    """Haven/tightening: uptrend → SHORT equity; downtrend → LONG."""
    sig = sig.sort_index()
    z120 = (sig - sig.rolling(120, min_periods=120).mean()) / sig.rolling(
        120, min_periods=120
    ).std(ddof=0).replace(0, np.nan)
    d20 = sig / sig.shift(20) - 1.0
    pos = pd.Series(0.0, index=sig.index)
    pos[(z120 > 0.5) & (d20 > 0)] = -1.0
    pos[(z120 < -0.5) & (d20 < 0)] = 1.0
    return _trades_from_pos(pos, us500)


SECTORS = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]


def z40_of(sig: pd.Series) -> pd.Series:
    sig = sig.sort_index()
    mu = sig.rolling(40, min_periods=40).mean()
    sd = sig.rolling(40, min_periods=40).std(ddof=0).replace(0, np.nan)
    return (sig - mu) / sd


def stress_pos(z: pd.Series, hi=1.5, lo=-1.5) -> pd.Series:
    pos = pd.Series(0.0, index=z.index)
    pos[z > hi] = -1.0
    pos[z < lo] = 1.0
    return pos


def sector_disp_pos(frames: dict) -> pd.Series:
    """N93-style proxy: 10d cross-sectional std of XL* returns, z40, disp_fade +1.0/−0.5."""
    rets = []
    for sym, s in frames.items():
        r = s.sort_index() / s.sort_index().shift(10) - 1.0
        rets.append(r.rename(sym))
    wide = pd.concat(rets, axis=1).dropna(how="any")
    disp = wide.std(axis=1, ddof=0)
    z = z40_of(disp)
    pos = pd.Series(0.0, index=z.index)
    pos[z > 1.0] = -1.0
    pos[z < -0.5] = 1.0
    return pos


def clone_report(name: str, z_cand: pd.Series, pos_cand: pd.Series, peers: dict) -> dict:
    """peers: name -> (z or None, pos)."""
    out = {}
    for peer, (z_p, pos_p) in peers.items():
        both = pos_cand.to_frame("c").join(pos_p.rename("p"), how="inner").dropna()
        # train window only for the decision
        both = both[(both.index >= TRAIN_START) & (both.index <= TRAIN_END)]
        active = both[both["c"] != 0]
        both_on = active[active["p"] != 0]
        agree = float((both_on["c"] == both_on["p"]).mean()) if len(both_on) else None
        cover = float(len(both_on) / len(active)) if len(active) else None
        corr = None
        if z_p is not None:
            zz = z_cand.to_frame("c").join(z_p.rename("p"), how="inner").dropna()
            zz = zz[(zz.index >= TRAIN_START) & (zz.index <= TRAIN_END)]
            if len(zz) > 30:
                corr = float(zz["c"].corr(zz["p"]))
        is_clone = False
        if corr is not None and corr >= 0.90:
            is_clone = True
        if agree is not None and cover is not None and agree >= 0.85 and cover >= 0.70:
            is_clone = True
        out[peer] = {
            "z_corr_train": None if corr is None else round(corr, 4),
            "sign_agree_both_active": None if agree is None else round(agree, 4),
            "both_active_over_cand": None if cover is None else round(cover, 4),
            "n_cand_active": int(len(active)),
            "n_both_active": int(len(both_on)),
            "clone": is_clone,
        }
    out["_any_clone"] = any(v.get("clone") for k, v in out.items() if not k.startswith("_"))
    return out


def verdict(trades, gate, label, instrument, notes=""):
    n = len(trades)
    if n == 0:
        return {
            "id": label,
            "instrument": instrument,
            "n": 0,
            "mean_bruto_bp": None,
            "gate_bp": gate,
            "verdict": "FAIL",
            "notes": notes,
        }
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    if n >= MIN_N and mean >= gate:
        v = "PASS_may_PREREG"
    elif mean >= gate and n < MIN_N:
        v = "UNDERPOWERED"
    else:
        v = "FAIL"
    return {
        "id": label,
        "instrument": instrument,
        "n": n,
        "mean_bruto_bp": round(mean, 4),
        "median_bruto_bp": round(float(np.median(arr)), 4),
        "gate_bp": gate,
        "stress_gate_bp": round(gate * 1.5, 4),
        "stress_note": (
            "PASS_stress_informal"
            if mean >= gate * 1.5
            else "BELOW_stress_1.5x (info only; D-092.1 cost-gate is binding)"
        ),
        "verdict": v,
        "hit_rate": round(float((arr > 0).mean()), 4),
        "n_long": int(sum(1 for t in trades if t["side"] > 0)),
        "n_short": int(sum(1 for t in trades if t["side"] < 0)),
        "years": {
            str(y): round(
                float(np.mean([t["bruto_bp"] for t in trades if t["date"].startswith(str(y))])),
                4,
            )
            for y in (2021, 2022, 2023)
            if any(t["date"].startswith(str(y)) for t in trades)
        },
        "notes": notes,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    xlf = load_daily_close("XLF")
    qual = load_daily_close("QUAL")
    iwm = load_daily_close("IWM")
    eqw = load_daily_close("SPX_EQW") / load_daily_close("SPX")
    eqw.name = "EQW_RATIO"
    sectors = {s: load_daily_close(s) for s in SECTORS}
    us500 = load_m5("US500cash")

    z_xlf = z40_of(xlf)
    z_qual = z40_of(qual)
    z_iwm = z40_of(iwm)
    z_eqw = z40_of(eqw)
    pos_xlf = stress_pos(z_xlf)
    pos_qual = stress_pos(z_qual)
    pos_iwm = stress_pos(z_iwm)
    pos_eqw = stress_pos(z_eqw)
    pos_disp = sector_disp_pos(sectors)
    # defensive ratio as extra note (not the mandated clone bar)
    z_xlu_xli = z40_of(sectors["XLU"] / sectors["XLI"])

    c134 = clone_report(
        "N134", z_xlf, pos_xlf,
        {"SECTOR_DISP": (None, pos_disp), "XLU_XLI": (z_xlu_xli, stress_pos(z_xlu_xli))},
    )
    c135 = clone_report(
        "N135", z_qual, pos_qual,
        {"EQW": (z_eqw, pos_eqw), "IWM": (z_iwm, pos_iwm)},
    )

    t134 = screen_stress_z40(xlf, us500)
    t135 = screen_stress_z40(qual, us500)
    s134 = verdict(
        t134, GATE, "N134", "US500cash",
        "XLF_FINANCIAL z40/thr1.5 stress_buy; NEW_FAMILY BC; D-100 session-flat; ≠SECTOR_DISP/HYG/XLU-XLI",
    )
    s135 = verdict(
        t135, GATE, "N135", "US500cash",
        "QUAL_QUALITY z40/thr1.5 stress_buy; NEW_FAMILY BD; D-100 session-flat; ≠EQW/IWM/MTUM/USMV",
    )
    # Clone overrides a cost PASS. Cost numbers stay visible; verdict becomes FAIL_CLONE.
    s134["clone"] = c134
    s135["clone"] = c135
    if c134.get("_any_clone"):
        s134["verdict"] = "FAIL_CLONE"
        s134["notes"] += " | CLONE of barred family — not a valid OPEN; no PREREG"
    if c135.get("_any_clone"):
        s135["verdict"] = "FAIL_CLONE"
        s135["notes"] += " | CLONE of barred family — not a valid OPEN; no PREREG"

    pd.DataFrame(t134).to_csv(OUT / "n134_trades_train.csv", index=False)
    pd.DataFrame(t135).to_csv(OUT / "n135_trades_train.csv", index=False)
    summary = {"N134": s134, "N135": s135, "clone_rule": {
        "z_corr_ge": 0.90,
        "sign_agree_ge": 0.85,
        "both_over_cand_ge": 0.70,
        "sector_disp_proxy": "XL* 10d xs-std z40 fade +1.0/-0.5 (XLC/XLRE absent)",
    }}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} → **{s['verdict']}** "
            f"years={s.get('years')} long/short={s.get('n_long')}/{s.get('n_short')} "
            f"stress={s.get('stress_note')} clone={s.get('clone')}\n"
        )
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N134/N135 pre-screen (train 2021–2023)\n\n"
        + line("N134 XLF_FINANCIAL→US500", s134)
        + line("N135 QUAL_QUALITY→US500", s135)
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
