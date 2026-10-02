"""N87 gate — US30cash opening-gap fade, intradag-flat
PREREG: PREREG_FTMO_N87.md (CEO commit 42821c9 on claude/ftmo-trading-strategy-98mplz)
Tijdinterpretatie: brokerservertijd rechtstreeks uit CSV (SH=1 per CEO pre-screen).
"""
import gzip
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── kosten ────────────────────────────────────────────────────────────────────
RT_BP      = 0.45   # roundtrip intradag (spread_med; geen commissie, intradag-flat)
GATE       = 3 * RT_BP   # 1.35 bp
SWAP_STRESS_FACTOR = 1.50  # stress = 1.5× spread (geen swap; stress = 1.5×RT)
# intradag-flat → geen swap

# ── train / test splits ───────────────────────────────────────────────────────
TRAIN_START = "2021-01-01"
TRAIN_END   = "2023-12-31"
TEST_START  = "2024-01-01"
TEST_END    = "2024-12-31"

GAP_THRESHOLD = 30.0  # bp

# ── NW-t helper ───────────────────────────────────────────────────────────────

def nw_t(series, L=5):
    """Newey-West t met L=5 (dag-niveau)."""
    x = np.asarray(series, dtype=float)
    n = len(x)
    if n < 2:
        return np.nan
    mu = x.mean()
    e  = x - mu
    gamma0 = (e ** 2).mean()
    long_run_var = gamma0
    for lag in range(1, L + 1):
        w = 1 - lag / (L + 1)
        gamma_lag = (e[lag:] * e[:-lag]).mean()
        long_run_var += 2 * w * gamma_lag
    if long_run_var <= 0:
        return np.nan
    se = np.sqrt(long_run_var / n)
    return mu / se


# ── data inladen ──────────────────────────────────────────────────────────────

def load_m5() -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / "US30cash.csv.gz"
    with gzip.open(path, "rt") as f:
        df = pd.read_csv(f, sep=";", comment="#", skip_blank_lines=True)
    df["dt"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df = df.sort_values("dt").reset_index(drop=True)
    return df


# ── trades berekenen ──────────────────────────────────────────────────────────

def compute_trades(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = df["dt"].dt.date
    df["hhmm"] = df["dt"].dt.hour * 100 + df["dt"].dt.minute

    records = []
    dates = sorted(df["date"].unique())

    for i, today in enumerate(dates):
        if i == 0:
            continue  # need previous day
        prev_day = dates[i - 1]

        today_rows = df[df["date"] == today]
        prev_rows  = df[df["date"] == prev_day]

        # prev_close: last bar close ≤ 23:00 van vorige dag
        prev_eligible = prev_rows[prev_rows["hhmm"] <= 2300]
        if prev_eligible.empty:
            continue
        prev_close = prev_eligible.iloc[-1]["close"]

        # day_open: first bar open ≥ 08:00 van vandaag
        open_eligible = today_rows[today_rows["hhmm"] >= 800]
        if open_eligible.empty:
            continue
        entry_bar = open_eligible.iloc[0]
        entry_price = entry_bar["open"]

        # gap berekenen
        gap_bp = 1e4 * (entry_price - prev_close) / prev_close

        if abs(gap_bp) <= GAP_THRESHOLD:
            continue  # geen trade

        direction = -1 if gap_bp > GAP_THRESHOLD else 1  # SHORT als gap omhoog

        # day_exit: last bar close ≤ 22:55 van vandaag
        exit_eligible = today_rows[today_rows["hhmm"] <= 2255]
        if exit_eligible.empty:
            continue
        exit_price = exit_eligible.iloc[-1]["close"]

        # gross return in bp (vanuit entry)
        gross_bp = 1e4 * direction * (exit_price - entry_price) / entry_price

        records.append({
            "date":     today,
            "gap_bp":   gap_bp,
            "direction": direction,
            "gross_bp": gross_bp,
        })

    trades = pd.DataFrame(records)
    if trades.empty:
        return trades
    trades["netto_bp"] = trades["gross_bp"] - RT_BP
    trades["date"]     = pd.to_datetime(trades["date"])
    return trades


# ── gate + statistieken ────────────────────────────────────────────────────────

def gate_stats(trades: pd.DataFrame, label: str):
    n     = len(trades)
    mean_bruto = trades["gross_bp"].mean() if n > 0 else np.nan
    mean_netto = trades["netto_bp"].mean() if n > 0 else np.nan
    t_nw  = nw_t(trades["netto_bp"]) if n > 0 else np.nan

    gate_pass = (n >= 150) and (mean_bruto >= GATE)
    # stress gate: RT×1.5 = 0.675 bp; threshold 3×0.675 = 2.025 bp (gaat ook door als mean > dat)
    stress_pass = mean_bruto >= (3 * RT_BP * SWAP_STRESS_FACTOR) if n >= 150 else False

    print(f"\n=== {label} (N={n}) ===")
    print(f"  mean bruto: {mean_bruto:.4f} bp | gate ({GATE:.2f} bp): {'PASS' if gate_pass else 'FAIL'}")
    print(f"  mean netto: {mean_netto:.4f} bp")
    print(f"  stress gate (>={3*RT_BP*SWAP_STRESS_FACTOR:.4f} bp): {'PASS' if stress_pass else 'FAIL'}")
    print(f"  NW t (L=5): {t_nw:.4f}")
    return {
        "label": label,
        "N": n,
        "mean_bruto_bp": round(mean_bruto, 4),
        "gate_pass": gate_pass,
        "stress_pass": stress_pass,
        "mean_netto_bp": round(mean_netto, 4),
        "t_nw_L5": round(t_nw, 4) if not np.isnan(t_nw) else None,
    }


def main():
    print("Loading US30cash M5 data ...")
    df = load_m5()
    print(f"  Loaded {len(df)} bars, {df['dt'].min()} → {df['dt'].max()}")

    trades = compute_trades(df)
    print(f"  Total trades (all dates): {len(trades)}")

    train = trades[(trades["date"] >= TRAIN_START) & (trades["date"] <= TRAIN_END)]
    test  = trades[(trades["date"] >= TEST_START)  & (trades["date"] <= TEST_END)]

    stats_train = gate_stats(train, "Train 2021-2023")
    stats_test  = gate_stats(test,  "Test 2024")

    # Formele toets (PASS vereist beide)
    formal_pass = (
        stats_train["gate_pass"]
        and stats_test is not None
        and (stats_train["t_nw_L5"] or 0) >= 2.0
        and (stats_test["t_nw_L5"]  or 0) >= 2.0
        and stats_train["mean_netto_bp"] > 0
        and stats_test["mean_netto_bp"]  > 0
    )

    print("\n=== UITKOMST ===")
    if not stats_train["gate_pass"]:
        outcome = "FAIL_COST_GATE"
        counts_trial = False
    elif formal_pass:
        outcome = "PASS"
        counts_trial = True
    else:
        outcome = "FAIL_T"
        counts_trial = True

    print(f"  Outcome:        {outcome}")
    print(f"  counts_as_trial: {counts_trial}")
    print(f"  Train gate:     {'PASS' if stats_train['gate_pass'] else 'FAIL'}")
    print(f"  Train t (NW):   {stats_train['t_nw_L5']}")
    print(f"  Test t (NW):    {stats_test['t_nw_L5']}")

    return outcome, counts_trial, stats_train, stats_test


if __name__ == "__main__":
    main()
