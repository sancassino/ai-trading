"""N8 (geen trial): power van de S3-beslisregel, dag-blok-bootstrap (21 d) uit de FTMO-ORB-trades 2021–26 van de S3-symbolen."""
import math
from collections import defaultdict
import numpy as np

SYMS = ["US500cash", "US100cash", "GER40cash", "XAUUSD"]
by = defaultdict(lambda: np.zeros((4, 2)))
for line in open("results/b4/B4_a_ORB_trades.csv"):
    if line[0].isdigit():
        d, s, n, _ = line.strip().split(";")
        if s in SYMS:
            by[d][SYMS.index(s)] += (float(n), 1)
days = sorted(by); A = np.array([by[d] for d in days])          # (dagen, 4, [som, aantal])
cnt = A[:, :, 1].sum(); mu = A[:, :, 0].sum() / cnt
ref = [d for d in days]; m2426 = sum(by[d][:, 0].sum() for d in days if d >= "2024") / sum(by[d][:, 1].sum() for d in days if d >= "2024")
print(f"FTMO 2021–26, S3-symbolen: {len(days)} dagen, {int(cnt)} trades, gemiddeld {mu*1e4:+.2f} bp; 2024–26 {m2426*1e4:+.2f} bp "
      f"→ 'blijvend'-voorwaarden (≥ 0,9 bp én 2024–26 ≥ 0): {'JA' if mu*1e4 >= 0.9 and m2426 >= 0 else 'NEE'}")
COST = 0.7e-4
worlds = {"effect 2021–26-niveau": 0.0, "effect gehalveerd": 0.5 * mu, "nul (bruto 0, netto −kosten)": mu + COST}
rng = np.random.default_rng(8)
def sim(shift, years, thr, n=3000):
    L = 252 * years; res = defaultdict(int)
    for _ in range(n):
        st = rng.integers(0, len(A), L // 21 + 1)
        idx = ((st[:, None] + np.arange(21)[None, :]).ravel() % len(A))[:L]
        X = A[idx].copy(); X[:, :, 0] -= shift * X[:, :, 1]
        has = X[:, :, 1].sum(1) > 0
        dm = X[has, :, 0].sum(1) / X[has, :, 1].sum(1)
        t = dm.mean() / dm.std(ddof=1) * math.sqrt(len(dm))
        mean = X[:, :, 0].sum() / X[:, :, 1].sum()
        h = L // 2; m1 = X[:h, :, 0].sum() / X[:h, :, 1].sum(); m2 = X[h:, :, 0].sum() / X[h:, :, 1].sum()
        pos3 = sum(X[:, k, 0].sum() > 0 for k in range(3))
        if t >= thr and m1 > 0 and m2 > 0 and mean >= 0.9e-4 and pos3 >= 2:
            res["bevestigd"] += 1
        elif t < 1 or mean <= 0.5e-4:
            res["verworpen"] += 1
        else:
            res["onbeslist"] += 1
    return {k: res[k] / n for k in ("bevestigd", "onbeslist", "verworpen")}
for years in (9, 10):
    for thr, lab in ((2.5, "(A) t ≥ 2,5"), (2.0, "(B) eenzijdig t ≥ 2,0")):
        for w, sh in worlds.items():
            p = sim(sh, years, thr)
            print(f"{years} jaar | {lab:<22} | {w:<30} | bevestigd {p['bevestigd']*100:4.0f}% | onbeslist {p['onbeslist']*100:4.0f}% | verworpen {p['verworpen']*100:4.0f}%", flush=True)
