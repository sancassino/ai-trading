"""Statistiek voor strategie-evaluatie: Sharpe met standaardfout/CI, t-stat, gedeflateerde Sharpe,
minimale trackrecordlengte en benodigde Sharpe voor een FTMO-inkomensdoel.

Bronnen: Lo (2002) "The Statistics of Sharpe Ratios"; Mertens (2002) SE met scheefheid/kurtosis;
Bailey & López de Prado (2012, 2014) "The Sharpe Ratio Efficient Frontier" / "The Deflated Sharpe Ratio".

CLI: python3 stats_tools.py <dagreeks.csv> [...] [--trials 300,30]
     python3 stats_tools.py --required 880 [--account 80000 --max-dd 0.10 --p-ruin 0.05]
Dagreeks-formaat: date;start_balance;start_equity;min_equity;end_equity (zoals *_daily.csv).
"""
import argparse
import csv
import math
import random
import statistics
from statistics import NormalDist

N01 = NormalDist()
EULER = 0.5772156649


def daily_returns(path):
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter=";") if r.get("date")]
    eq = [float(r["end_equity"]) for r in rows]
    return [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]


def moments(x):
    m = statistics.mean(x)
    s = statistics.pstdev(x)
    n = len(x)
    skew = sum((v - m) ** 3 for v in x) / n / s ** 3
    kurt = sum((v - m) ** 4 for v in x) / n / s ** 4
    return m, s, skew, kurt


def sharpe(x, periods=252):
    """(jaarlijkse SR, per-periode SR)"""
    m, s, _, _ = moments(x)
    sr = m / s if s > 0 else 0.0
    return sr * math.sqrt(periods), sr


def sharpe_se(x, periods=252):
    """SE van de jaarlijkse Sharpe (Mertens: incl. scheefheid en kurtosis)."""
    _, s, g3, g4 = moments(x)
    sr = sharpe(x, periods)[1]
    var = (1 - g3 * sr + (g4 - 1) / 4 * sr ** 2) / (len(x) - 1)
    return math.sqrt(var) * math.sqrt(periods)


def t_stat(x):
    m, s, _, _ = moments(x)
    return m / s * math.sqrt(len(x)) if s > 0 else 0.0


def bootstrap_ci(x, periods=252, block=21, n=2000, seed=1, alpha=0.05):
    """Stationaire block-bootstrap (Politis-Romano) van de jaarlijkse Sharpe."""
    rng = random.Random(seed)
    T = len(x)
    p = 1 / block
    out = []
    for _ in range(n):
        sample = []
        i = rng.randrange(T)
        while len(sample) < T:
            sample.append(x[i])
            i = rng.randrange(T) if rng.random() < p else (i + 1) % T
        out.append(sharpe(sample, periods)[0])
    out.sort()
    return out[int(alpha / 2 * n)], out[int((1 - alpha / 2) * n) - 1]


def expected_max_sr(n_trials, sr_var):
    """Verwachte maximale (per-periode) SR onder H0 bij n_trials onafhankelijke pogingen."""
    if n_trials <= 1:
        return 0.0
    return math.sqrt(sr_var) * ((1 - EULER) * N01.inv_cdf(1 - 1 / n_trials)
                                + EULER * N01.inv_cdf(1 - 1 / (n_trials * math.e)))


def deflated_sharpe(x, n_trials, sr_var=None):
    """Kans dat de ware SR > 0 na correctie voor n_trials (Bailey & López de Prado 2014).
    sr_var = variantie van de per-periode SR over de trials; default: variantie van de schatter."""
    _, _, g3, g4 = moments(x)
    sr = sharpe(x)[1]
    T = len(x)
    if sr_var is None:
        sr_var = (1 - g3 * sr + (g4 - 1) / 4 * sr ** 2) / (T - 1)
    sr0 = expected_max_sr(n_trials, sr_var)
    z = (sr - sr0) * math.sqrt(T - 1) / math.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr ** 2)
    return N01.cdf(z), sr0 * math.sqrt(252)


def min_track_record(x, sr_star=0.0, alpha=0.05):
    """Minimale lengte (in jaren) om SR > sr_star (jaarlijks) met 1-alpha zekerheid aan te tonen."""
    _, _, g3, g4 = moments(x)
    sr = sharpe(x)[1]
    srs = sr_star / math.sqrt(252)
    if sr <= srs:
        return float("inf")
    n = 1 + (1 - g3 * sr + (g4 - 1) / 4 * sr ** 2) * (N01.inv_cdf(1 - alpha) / (sr - srs)) ** 2
    return n / 252


def required_sharpe(target_eur_per_month, account=80000, max_dd=0.10, p_ruin=0.05):
    """Benodigde jaarlijkse Sharpe: rendement mu = 12*doel/account, en de kans om ooit max_dd onder
    de start te komen (Brownse beweging met drift) = exp(-2 mu D / sigma^2) <= p_ruin.
    Met sigma = mu/SR volgt SR >= sqrt(mu * ln(1/p) / (2 D)). Geeft (SR, mu, sigma)."""
    mu = 12 * target_eur_per_month / account
    sr = math.sqrt(mu * math.log(1 / p_ruin) / (2 * max_dd))
    return sr, mu, mu / sr


def report(path, trials):
    x = daily_returns(path)
    sr = sharpe(x)[0]
    lo, hi = bootstrap_ci(x)
    parts = [f"{path.split('/')[-1]:<44} T={len(x)/252:4.1f}jr SR {sr:+.2f} ±{sharpe_se(x):.2f} "
             f"[{lo:+.2f},{hi:+.2f}] t {t_stat(x):+.2f} minTRL {min_track_record(x):5.1f}jr"]
    for n in trials:
        dsr, sr0 = deflated_sharpe(x, n)
        parts.append(f"DSR(N={n}) {dsr:.2f} (SR0 {sr0:.2f})")
    print(" | ".join(parts))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--trials", default="300,30")
    ap.add_argument("--required", type=float)
    ap.add_argument("--account", type=float, default=80000)
    ap.add_argument("--max-dd", type=float, default=0.10)
    ap.add_argument("--p-ruin", type=float, default=0.05)
    a = ap.parse_args()
    if a.required:
        sr, mu, sig = required_sharpe(a.required, a.account, a.max_dd, a.p_ruin)
        print(f"doel €{a.required:,.0f}/mnd op €{a.account:,.0f}: rendement {mu*100:.1f}%/jr, "
              f"benodigde Sharpe ≥ {sr:.2f} bij vol ≤ {sig*100:.1f}% (P(−{a.max_dd*100:.0f}%) ≤ {a.p_ruin*100:.0f}%)")
    for f in a.files:
        report(f, [int(t) for t in a.trials.split(",")])
