#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: Strateeg VOORSTEL N41–N43."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n41_n43_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N, MIN_N = 14, 150

def load_m5(sym):
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"): f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open","high","low","close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
    return df[(df["time"]>=TRAIN_START)&(df["time"]<=TRAIN_END)].reset_index(drop=True)

def atr_map(m5):
    g = m5.set_index("time").resample("1D").agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
    tr = pd.concat([g["high"]-g["low"], (g["high"]-g["close"].shift()).abs(), (g["low"]-g["close"].shift()).abs()], axis=1).max(axis=1)
    g["atr"] = tr.rolling(ATR_N).mean()
    return g["atr"]

def prior_atr(atr, day):
    for k in range(1,10):
        a = atr.get(day - pd.Timedelta(days=k), np.nan)
        if a==a: return float(a)
    return float("nan")

def bar_at(g, day0, h, m=0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"]==t]
    return None if rows.empty else rows.iloc[0]

def manage(g, day0, entry_t, entry, side, stop, flat_h, flat_m=0):
    flat_t = day0 + pd.Timedelta(hours=flat_h, minutes=flat_m)
    path = g[(g["time"]>entry_t)&(g["time"]<=flat_t)]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    if stop==stop:
        for _, row in path.iterrows():
            hi, lo = float(row["high"]), float(row["low"])
            if side==1 and lo<=stop: return stop, "stop"
            if side==-1 and hi>=stop: return stop, "stop"
    return exit_px, "time"

def sim_n41(g, atr):
    if not (atr==atr) or atr<=0: return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0900, b1500, b1530 = bar_at(g,day0,9,0), bar_at(g,day0,15,0), bar_at(g,day0,15,30)
    if b0900 is None or b1500 is None or b1530 is None: return None
    c0, c1 = float(b0900["close"]), float(b1500["close"])
    if c0<=0: return None
    eu = 1e4*(c1-c0)/c0
    if abs(eu)<40: return None
    side = 1 if eu>0 else -1
    entry = float(b1530["close"]); entry_t = day0+pd.Timedelta(hours=15,minutes=30)
    stop = entry - side*atr
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 17, 0)
    return {"date":str(day0.date()),"side":side,"ret_sig":eu,"gross_bp":side*1e4*(exit_px-entry)/entry,"exit":hit}

def sim_n42(g, atr):
    if not (atr==atr) or atr<=0: return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0800, b1130 = bar_at(g,day0,8,0), bar_at(g,day0,11,30)
    if b0800 is None or b1130 is None: return None
    o0, o1 = float(b0800["open"]), float(b1130["open"])
    if o0<=0: return None
    ret = 1e4*(o1-o0)/o0
    if abs(ret)<35: return None
    side = 1 if ret>0 else -1
    entry = o1; entry_t = day0+pd.Timedelta(hours=11,minutes=30)
    stop = entry - side*0.5*atr
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 14, 30)
    return {"date":str(day0.date()),"side":side,"ret_sig":ret,"gross_bp":side*1e4*(exit_px-entry)/entry,"exit":hit}

def sim_n43(g, atr):
    if not (atr==atr) or atr<=0: return None
    day0 = g["time"].dt.normalize().iloc[0]
    b1530, b1600 = bar_at(g,day0,15,30), bar_at(g,day0,16,0)
    if b1530 is None or b1600 is None: return None
    c0, c1 = float(b1530["close"]), float(b1600["close"])
    if c0<=0: return None
    drive = 1e4*(c1-c0)/c0
    if abs(drive)<50: return None
    side = 1 if drive>0 else -1
    entry = c1; entry_t = day0+pd.Timedelta(hours=16,minutes=0)
    stop = entry - side*atr
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 18, 0)
    return {"date":str(day0.date()),"side":side,"ret_sig":drive,"gross_bp":side*1e4*(exit_px-entry)/entry,"exit":hit}

def run(sym, fn, rt, gate, lab):
    m5 = load_m5(sym); atr = atr_map(m5); trades=[]
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        if len(g)<10: continue
        r = fn(g, prior_atr(atr, day))
        if r: trades.append(r)
    df = pd.DataFrame(trades)
    if df.empty:
        return {"sleeve":lab,"symbol":sym,"n":0,"mean_gross_bp":None,"median_gross_bp":None,"gate_bp":gate,"rt_bp":rt,"power_n_ge_150":False,"gate_ok":False,"verdict":"FAIL","date_min":None,"date_max":None}, df
    mean=float(df["gross_bp"].mean()); med=float(df["gross_bp"].median()); n=int(len(df))
    ok = mean>=gate and n>=MIN_N
    return {"sleeve":lab,"symbol":sym,"n":n,"mean_gross_bp":mean,"median_gross_bp":med,"gate_bp":gate,"rt_bp":rt,"power_n_ge_150":n>=MIN_N,"gate_ok":mean>=gate,"verdict":"PASS" if ok else "FAIL","date_min":df["date"].min(),"date_max":df["date"].max()}, df

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    specs=[("US30cash",sim_n41,0.45,1.35,"N41"),("NZDUSD",sim_n42,1.85,5.55,"N42"),("UKOILcash",sim_n43,2.71,8.13,"N43")]
    rows=[]
    for sym,fn,rt,gate,lab in specs:
        meta,df=run(sym,fn,rt,gate,lab); rows.append(meta)
        if not df.empty: df.to_csv(OUT/f"{lab.lower()}_trades_train.csv", index=False)
        print(lab, meta["verdict"], "N=", meta["n"], "mean=", meta["mean_gross_bp"], "gate=", gate)
    summary={"window":"2021-01-01..2023-12-31","source":"VOORSTEL_PRESCREEN_N41..N43","reserve_2025_touched":False,"sleeves":rows}
    (OUT/"prescreen.json").write_text(json.dumps(summary, indent=2))
    lines=["# D-092.1 pre-screen N41–N43 TRAIN 2021–2023","","Source: Strateeg VOORSTEL N41–N43. Reserve 2025→ onaangeraakt.","","| Sleeve | N | mean bruto | gate | Uitkomst |","|--------|---|------------|------|----------|"]
    for r in rows:
        mean="n/a" if r["mean_gross_bp"] is None else f"{r['mean_gross_bp']:+.2f} bp"
        lines.append(f"| **{r['sleeve']}** | {r['n']} | {mean} | {r['gate_bp']} | **{r['verdict']}** |")
    lines += ["","No PREREG on FAIL. No TRIALS append."]
    (OUT/"prescreen.md").write_text("\n".join(lines)+"\n")

if __name__=="__main__":
    main()
