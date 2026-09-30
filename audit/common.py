"""AUDIT_1 — eigen data-laag (geen import van engine/ of catalogus/). Leest ruwe data/daily/*.csv en data/fred/DTB3.csv."""
import numpy as np, pandas as pd

def load(name, col="adjclose", path="data/daily"):
    df = pd.read_csv(f"{path}/{name}.csv", sep=";", comment="#", parse_dates=["date"])
    s = df.set_index("date")[col].astype(float)
    return s[~s.index.duplicated()].sort_index()

def rf_daily_pct():
    """DTB3 (FRED, % /jr) dagelijks; na laatste datum US3M. Eigen implementatie."""
    d = pd.read_csv("data/fred/DTB3.csv", parse_dates=["observation_date"])
    d["DTB3"] = pd.to_numeric(d["DTB3"], errors="coerce")
    s = d.dropna().set_index("observation_date")["DTB3"]
    return s
