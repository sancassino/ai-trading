#!/usr/bin/env python3
"""C-022 — D-097 / spoor 6: ≥10y daily-proxy TSMOM + XS-mom diagnostic screen (CTO).

Diagnostic only — NOT a PREREG trial.
- Reserve 2025+: untouched (hard cut ≤ 2024-12-31)
- No TRIALS.csv append
- Uses data/PROXY_MAP_FTMO.csv + data/daily/*.csv (spoor 6)
- Cost model: COSTS_FTMO.csv fuzzy match + category fallbacks (swap×nights)

Purpose: surface D-097.1 candidates (hold 5/10/20d, prefer ≥50 bp bruto/trade)
for Strateeg/S2 PREREG design after mechanism evidence on long proxies.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c022_d097_proxy_tsmom"
CAL_END = pd.Timestamp("2024-12-31")
# discovery window: prefer long history; report both full-proxy and 2015–2024 slice
SLICE_START = pd.Timestamp("2015-01-01")
MIN_YEARS = 8.0  # soft floor for reporting a row
LOOKBACKS = (20, 60, 120)
HOLDS = (5, 10, 20)
XS_LOOKBACK = 60
XS_HOLD = 20
XS_TOP_BOTTOM = 3  # long top-k / short bottom-k within universe

# Category fallback RT + overnight swap (bp). Conservative for agri/metals without FTMO row.
FALLBACK_COST = {
    "fx": {"rt": 1.0, "swap_long": 0.5, "swap_short": 0.5},
    "index": {"rt": 1.5, "swap_long": 1.5, "swap_short": 0.8},
    "commodity/metal": {"rt": 3.0, "swap_long": 2.0, "swap_short": 2.0},
    "stock": {"rt": 4.0, "swap_long": 1.0, "swap_short": 1.0},
    "crypto": {"rt": 8.0, "swap_long": 5.0, "swap_short": 5.0},
}


def _norm(s: str) -> str:
    return s.replace(".", "").replace("_", "").replace("-", "").lower()


def load_costs() -> dict[str, dict]:
    path = ROOT / "COSTS_FTMO.csv"
    df = pd.read_csv(path, sep=";", comment="#")
    out = {}
    for _, r in df.iterrows():
        out[_norm(str(r["symbol"]))] = {
            "rt": float(r["roundtrip_intraday_bp"]),
            "swap_long": float(r["swap_long_bp_per_nacht"]),
            "swap_short": float(r["swap_short_bp_per_nacht"]),
            "src": str(r["symbol"]),
        }
    # aliases
    aliases = {
        "usoilcash": "usoilcash",
        "ukoilcash": "ukoilcash",
        "xauusd": "xauusd",
        "xagusd": "xagusd",
        "ger40cash": "ger40cash",
        "us100cash": "us100cash",
        "us30cash": "us30cash",
        "us500cash": "us500cash",
    }
    # map PROXY ftmo names without 'cash' suffix variants already covered by _norm
    return out


def cost_for(ftmo_symbol: str, categorie: str, costs: dict) -> dict:
    n = _norm(ftmo_symbol)
    # try variants
    candidates = [
        n,
        _norm(ftmo_symbol.replace(".cash", "cash")),
        _norm(ftmo_symbol.replace(".c", "")),
        _norm(ftmo_symbol.split(".")[0] + "cash"),
    ]
    # oil aliases
    if "usoil" in n:
        candidates.append("usoilcash")
    if "ukoil" in n:
        candidates.append("ukoilcash")
    for c in candidates:
        if c in costs:
            d = dict(costs[c])
            d["match"] = d.pop("src")
            return d
    fb = FALLBACK_COST.get(categorie, FALLBACK_COST["index"])
    return {**fb, "match": f"fallback:{categorie}"}


def load_proxy_map() -> list[dict]:
    lines = [
        ln
        for ln in (ROOT / "data/PROXY_MAP_FTMO.csv").read_text().splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    return list(csv.DictReader(lines, delimiter=";"))


def load_px(proxy: str) -> pd.Series | None:
    path = ROOT / "data/daily" / f"{proxy}.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path, sep=";", comment="#")
    df.columns = [c.lower() for c in df.columns]
    if "date" not in df.columns or "close" not in df.columns:
        return None
    df["date"] = pd.to_datetime(df["date"])
    px_col = "adjclose" if "adjclose" in df.columns and df["adjclose"].notna().any() else "close"
    s = df.set_index("date")[px_col].astype(float).sort_index()
    s = s[~s.index.duplicated(keep="last")]
    s = s[s.index <= CAL_END]
    s = s.replace([np.inf, -np.inf], np.nan).dropna()
    s = s[s > 0]
    return s if len(s) > 300 else None


def tsmom_trades(px: pd.Series, lookback: int, hold: int, mode: str) -> pd.DataFrame:
    """mode: long_only | long_short. Signal = sign(px/px.shift(L)-1). Enter next day, exit after hold days."""
    ret_lb = px / px.shift(lookback) - 1.0
    sig = np.sign(ret_lb)
    if mode == "long_only":
        sig = sig.clip(lower=0)
    # trade on business days: rebalance every `hold` days
    dates = px.index
    rows = []
    i = lookback + 1
    while i + hold < len(dates):
        d_entry = dates[i]
        d_exit = dates[i + hold]
        s = float(sig.iloc[i - 1])  # signal known prior close
        if s == 0 or math.isnan(s):
            i += hold
            continue
        p0 = float(px.iloc[i])
        p1 = float(px.iloc[i + hold])
        if p0 <= 0 or p1 <= 0:
            i += hold
            continue
        bruto_bp = s * (p1 / p0 - 1.0) * 10_000.0
        rows.append(
            {
                "entry": d_entry,
                "exit": d_exit,
                "side": s,
                "bruto_bp": bruto_bp,
                "nights": hold,  # approx calendar nights ≈ hold for daily bars
            }
        )
        i += hold
    return pd.DataFrame(rows)


def summarize(trades: pd.DataFrame, rt: float, swap_long: float, swap_short: float) -> dict:
    if trades.empty:
        return {"n": 0}
    t = trades.copy()
    swap = np.where(t["side"] > 0, swap_long, swap_short)
    # swap cost: if swap_long > 0 it is a cost for longs (FTMO file convention: positive = you pay)
    t["cost_bp"] = rt + np.abs(swap) * t["nights"]  # abs: treat signed as magnitude cost; FTMO signs vary
    # better: use signed — positive swap_* means pay that many bp/night
    t["cost_bp"] = rt + np.where(t["side"] > 0, swap_long, swap_short) * t["nights"]
    # if receiving swap (negative), cost decreases
    t["net_bp"] = t["bruto_bp"] - t["cost_bp"]
    years = max((t["exit"].max() - t["entry"].min()).days / 365.25, 1e-6)
    mean_b = float(t["bruto_bp"].mean())
    mean_n = float(t["net_bp"].mean())
    # day-cluster approx: one obs per trade (non-overlapping)
    sd = float(t["net_bp"].std(ddof=1)) if len(t) > 2 else float("nan")
    tstat = mean_n / (sd / math.sqrt(len(t))) if sd and sd > 0 else float("nan")
    # split halves
    mid = t["entry"].min() + (t["entry"].max() - t["entry"].min()) / 2
    h1 = t[t["entry"] <= mid]["net_bp"]
    h2 = t[t["entry"] > mid]["net_bp"]

    def _t(x):
        if len(x) < 5:
            return float("nan")
        m = float(x.mean())
        s = float(x.std(ddof=1))
        return m / (s / math.sqrt(len(x))) if s > 0 else float("nan")

    return {
        "n": int(len(t)),
        "years": years,
        "trades_per_year": len(t) / years,
        "mean_bruto_bp": mean_b,
        "mean_net_bp": mean_n,
        "median_bruto_bp": float(t["bruto_bp"].median()),
        "hit_rate": float((t["bruto_bp"] > 0).mean()),
        "t_net": tstat,
        "t_h1": _t(h1),
        "t_h2": _t(h2),
        "mean_cost_bp": float(t["cost_bp"].mean()),
        "prescreen_50bp": mean_b >= 50.0,
        "gate_3x_cost": mean_b >= 3.0 * float(t["cost_bp"].mean()) if len(t) else False,
    }


def xs_mom_universe(
    series: dict[str, pd.Series], lookback: int, hold: int, k: int
) -> pd.DataFrame:
    """Equal-weight long top-k / short bottom-k cross-sectional mom; non-overlapping holds."""
    if len(series) < 2 * k:
        return pd.DataFrame()
    px = pd.DataFrame(series).sort_index().ffill(limit=3)
    # align common calendar
    px = px.dropna(how="all")
    dates = px.index
    rows = []
    i = lookback + 1
    while i + hold < len(dates):
        window = px.iloc[i - lookback - 1 : i]
        if window.shape[0] < lookback // 2:
            i += hold
            continue
        p0 = px.iloc[i]
        p1 = px.iloc[i + hold]
        mom = px.iloc[i - 1] / px.iloc[i - 1 - lookback] - 1.0
        valid = mom.dropna().index.intersection(p0.dropna().index).intersection(p1.dropna().index)
        if len(valid) < 2 * k:
            i += hold
            continue
        m = mom.loc[valid].sort_values()
        shorts = m.index[:k]
        longs = m.index[-k:]
        legs = []
        for sym in longs:
            legs.append((p1[sym] / p0[sym] - 1.0) * 10_000.0)
        for sym in shorts:
            legs.append(-(p1[sym] / p0[sym] - 1.0) * 10_000.0)
        bruto = float(np.mean(legs))
        rows.append(
            {
                "entry": dates[i],
                "exit": dates[i + hold],
                "side": 1.0,
                "bruto_bp": bruto,
                "nights": hold,
                "n_legs": len(legs),
            }
        )
        i += hold
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    costs = load_costs()
    rows_map = load_proxy_map()

    loaded: dict[str, dict] = {}
    for r in rows_map:
        if r.get("10j_plus") != "ja" or not r.get("proxy"):
            continue
        # skip compound FXBIS proxies without a file
        if "+" in r["proxy"]:
            continue
        px = load_px(r["proxy"])
        if px is None:
            continue
        years = float(r.get("jaren_tm_2024") or 0)
        if years < MIN_YEARS:
            continue
        cinfo = cost_for(r["ftmo_symbol"], r["categorie"], costs)
        loaded[r["ftmo_symbol"]] = {
            "categorie": r["categorie"],
            "proxy": r["proxy"],
            "years_meta": years,
            "px": px,
            "cost": cinfo,
        }

    solo_rows = []
    for sym, meta in sorted(loaded.items()):
        px_full = meta["px"]
        for slice_name, px in (
            ("full_to_2024", px_full),
            ("2015_2024", px_full[px_full.index >= SLICE_START]),
        ):
            if len(px) < 400:
                continue
            for lb in LOOKBACKS:
                for hold in HOLDS:
                    for mode in ("long_only", "long_short"):
                        tr = tsmom_trades(px, lb, hold, mode)
                        # cost: for long_short use average of long/short swap magnitude in summarize per trade
                        summ = summarize(
                            tr,
                            meta["cost"]["rt"],
                            meta["cost"]["swap_long"],
                            meta["cost"]["swap_short"],
                        )
                        if summ.get("n", 0) < 20:
                            continue
                        solo_rows.append(
                            {
                                "family": "TSMOM",
                                "ftmo_symbol": sym,
                                "categorie": meta["categorie"],
                                "proxy": meta["proxy"],
                                "slice": slice_name,
                                "lookback": lb,
                                "hold": hold,
                                "mode": mode,
                                "cost_match": meta["cost"]["match"],
                                "rt_bp": meta["cost"]["rt"],
                                **summ,
                            }
                        )

    # XS universes
    universes = {
        "commodities": [s for s, m in loaded.items() if m["categorie"] == "commodity/metal"],
        "indices": [s for s, m in loaded.items() if m["categorie"] == "index"],
        "fx_majors": [
            s
            for s, m in loaded.items()
            if m["categorie"] == "fx"
            and s
            in {
                "EURUSD",
                "GBPUSD",
                "USDJPY",
                "AUDUSD",
                "USDCAD",
                "USDCHF",
                "NZDUSD",
            }
        ],
    }
    xs_rows = []
    for uname, syms in universes.items():
        series = {s: loaded[s]["px"] for s in syms if s in loaded}
        # median category cost for approx net
        rts = [loaded[s]["cost"]["rt"] for s in series]
        swL = [loaded[s]["cost"]["swap_long"] for s in series]
        swS = [loaded[s]["cost"]["swap_short"] for s in series]
        rt = float(np.median(rts)) if rts else 3.0
        # portfolio: long+short legs ≈ 2× RT/k? use 2*rt for round-trip book approx / k averaging already in bruto
        # Approx book cost: each rebalance trades 2k legs; per book return we used mean of k long + k short
        # → charge ~rt + hold*mean(|swap|) as single-leg equivalent (bruto already averaged)
        swap_l = float(np.median(swL)) if swL else 2.0
        swap_s = float(np.median(swS)) if swS else 2.0
        for slice_name, cutter in (
            ("full_to_2024", lambda s: s),
            ("2015_2024", lambda s: s[s.index >= SLICE_START]),
        ):
            ser = {k: cutter(v) for k, v in series.items()}
            ser = {k: v for k, v in ser.items() if len(v) >= 400}
            tr = xs_mom_universe(ser, XS_LOOKBACK, XS_HOLD, XS_TOP_BOTTOM)
            # for XS use average of long/short swap
            if not tr.empty:
                tr = tr.copy()
                # approximate: half book long / half short → average swap
                avg_swap = 0.5 * (swap_l + swap_s)
                tr["side"] = 1.0
                # monkey-patch: pass avg as both
                summ = summarize(tr, rt * 2.0, avg_swap, avg_swap)  # 2× RT for L+S book
            else:
                summ = {"n": 0}
            if summ.get("n", 0) < 15:
                continue
            xs_rows.append(
                {
                    "family": "XS_MOM",
                    "ftmo_symbol": uname,
                    "categorie": uname,
                    "proxy": ",".join(sorted(ser.keys())),
                    "slice": slice_name,
                    "lookback": XS_LOOKBACK,
                    "hold": XS_HOLD,
                    "mode": f"L{XS_TOP_BOTTOM}/S{XS_TOP_BOTTOM}",
                    "cost_match": f"median_rt×2={rt*2:.2f}",
                    "rt_bp": rt * 2,
                    "n_names": len(ser),
                    **summ,
                }
            )

    solo = pd.DataFrame(solo_rows)
    xs = pd.DataFrame(xs_rows)
    all_df = pd.concat([solo, xs], ignore_index=True) if len(xs) else solo

    # Rank: prefer 2015–2024 slice, gate_3x or ≥50bp, both-half t>0, high mean net
    if not all_df.empty:
        all_df.to_csv(OUT / "screen_all.csv", index=False)
        focus = all_df[all_df["slice"] == "2015_2024"].copy()
        focus["score"] = (
            focus["mean_bruto_bp"].fillna(-1e9)
            + 10.0 * focus["prescreen_50bp"].astype(float)
            + 5.0 * focus["gate_3x_cost"].astype(float)
            + focus["t_net"].fillna(0)
        )
        focus = focus.sort_values("score", ascending=False)
        focus.to_csv(OUT / "screen_2015_2024_ranked.csv", index=False)
        # shortlist: bruto≥50 or gate_3x, t_net>1, t_h1>0, t_h2>0
        short = focus[
            (focus["prescreen_50bp"] | focus["gate_3x_cost"])
            & (focus["t_net"] > 1.0)
            & (focus["t_h1"] > 0)
            & (focus["t_h2"] > 0)
        ].head(40)
        short.to_csv(OUT / "shortlist.csv", index=False)
    else:
        focus = all_df
        short = all_df

    # Board + report
    n_loaded = len(loaded)
    top = short.head(15) if len(short) else focus.head(15)

    def _row_md(r):
        return (
            f"| {r.get('family')} | {r.get('ftmo_symbol')} | {r.get('mode')} | "
            f"L{r.get('lookback')}/H{r.get('hold')} | {r.get('n')} | "
            f"{r.get('mean_bruto_bp', float('nan')):.1f} | {r.get('mean_net_bp', float('nan')):.1f} | "
            f"{r.get('t_net', float('nan')):.2f} | {r.get('t_h1', float('nan')):.2f}/"
            f"{r.get('t_h2', float('nan')):.2f} | {r.get('trades_per_year', float('nan')):.1f} | "
            f"{r.get('cost_match')} |"
        )

    lines = [
        "# C-022 — D-097 proxy TSMOM / XS-mom diagnostic (CTO track 4/5 assist)",
        "",
        "- When: 2026-10-01 ~09:53 Europe/Amsterdam (CEST / UTC+2)",
        "- Branch: `grok/cto-1`",
        "- Reserve 2025+: **not used** (cut ≤2024-12-31)",
        "- Trials appended: **0**",
        f"- Proxies loaded (10j+, daily file, no compound FXBIS): **{n_loaded}**",
        "- Engine: daily close TSMOM + XS-mom; costs from `COSTS_FTMO.csv` + category fallback",
        "",
        "## Binding",
        "",
        "- Diagnostic / mechanism screen only — **not** a formal gate, **not** a PREREG.",
        "- Strateeg/S2 must freeze a rule in PREREG before U2 cost-gate on FTMO-M5.",
        "- D-094a (b): ≥10y proxy can underwrite mechanism; FTMO-M5 still needed for costs/execution.",
        "- Track-3 combine still **paused** until solo day-clust t≥2.0 on a formal PASS.",
        "",
        "## Coverage",
        "",
    ]
    from collections import Counter

    cat_c = Counter(m["categorie"] for m in loaded.values())
    for k, v in sorted(cat_c.items()):
        lines.append(f"- {k}: {v}")
    lines += [
        "",
        "## Shortlist (2015–2024; bruto≥50 **or** 3×cost; t_net>1; both halves t>0)",
        "",
        "| family | symbol/univ | mode | L/H | N | bruto bp | net bp | t_net | t_h1/h2 | tr/yr | cost |",
        "|---|---|---|---|---:|---:|---:|---:|---|---:|---|",
    ]
    if len(top):
        for _, r in top.iterrows():
            lines.append(_row_md(r))
    else:
        lines.append("| — | no row cleared shortlist filters | | | | | | | | | |")

    # drought note + best near-misses
    near = focus.head(10) if len(focus) else pd.DataFrame()
    lines += [
        "",
        "## Top 10 by score (even if shortlist empty)",
        "",
        "| family | symbol/univ | mode | L/H | N | bruto bp | net bp | t_net | t_h1/h2 | tr/yr | 50bp? |",
        "|---|---|---|---|---:|---:|---:|---:|---|---:|:---:|",
    ]
    for _, r in near.iterrows():
        lines.append(
            f"| {r.get('family')} | {r.get('ftmo_symbol')} | {r.get('mode')} | "
            f"L{r.get('lookback')}/H{r.get('hold')} | {r.get('n')} | "
            f"{r.get('mean_bruto_bp', float('nan')):.1f} | {r.get('mean_net_bp', float('nan')):.1f} | "
            f"{r.get('t_net', float('nan')):.2f} | {r.get('t_h1', float('nan')):.2f}/"
            f"{r.get('t_h2', float('nan')):.2f} | {r.get('trades_per_year', float('nan')):.1f} | "
            f"{'Y' if r.get('prescreen_50bp') else 'n'} |"
        )

    lines += [
        "",
        "## CTO guidance for Strateeg / S2",
        "",
        "1. Prefer shortlist rows with **hold 10–20d**, commodities/FX/index — not stock-CFD single names unless pooled.",
        "2. If shortlist empty: drought continues on classic TSMOM; next families = **carry/RV** (rate differentials), "
        "**vol-targeted CTA** (sign×vol scale), **regime-gated TSMOM** (200d filter as one frozen rule).",
        "3. Do **not** clone dead intradag N35–N44 / P1 / GBPJPY.",
        "4. Any PREREG must cite proxy file + years and D-094a reason (b) if FTMO-M5 <5y.",
        "",
        "## CTO next",
        "",
        "- Still idle on track-3 blends until formal solo t≥2 PASS.",
        "- On first U2 PASS under D-097: track-5 `recommend_scale` / `ftmo_ev`.",
        "",
        "Artefacts: `screen_all.csv`, `screen_2015_2024_ranked.csv`, `shortlist.csv`, `c022_board.json`.",
    ]
    (OUT / "c022_report.md").write_text("\n".join(lines) + "\n")

    board = {
        "cycle": "C-022",
        "when": "2026-10-01 ~09:53 Europe/Amsterdam (CEST / UTC+2)",
        "decision": "D-097",
        "reserve_2025": "untouched",
        "trials_appended": 0,
        "proxies_loaded": n_loaded,
        "categories": dict(cat_c),
        "solo_rows": int(len(solo)),
        "xs_rows": int(len(xs)),
        "shortlist_n": int(len(short)) if len(short) else 0,
        "shortlist_top": top.fillna(None).to_dict(orient="records") if len(top) else [],
        "track3": "PAUSED until solo formal t>=2",
        "note": "Diagnostic mechanism screen on spoor-6 daily proxies; not a PREREG/trial.",
    }
    (OUT / "c022_board.json").write_text(json.dumps(board, indent=2, default=str))
    print(json.dumps({k: board[k] for k in board if k != "shortlist_top"}, indent=2))
    print("shortlist_n", board["shortlist_n"])
    if len(top):
        print(top[["family", "ftmo_symbol", "mode", "lookback", "hold", "mean_bruto_bp", "mean_net_bp", "t_net"]].head(12).to_string(index=False))


if __name__ == "__main__":
    main()
