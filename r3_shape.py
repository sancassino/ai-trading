"""R3: invloed van de rendementsvorm op de vereiste Sharpe onder FTMO (PREREG_R3.md)."""
import numpy as np
import q1b_products as qb

N, SIG = 100_000, 0.10 / np.sqrt(252)
rng = np.random.default_rng(21)
def shapes():
    k = 1.78
    g = rng.gamma(k, 1.0, N)
    t3 = rng.standard_t(3, N) / np.sqrt(3.0)
    e = rng.standard_normal(N); h = np.empty(N); z_g = np.empty(N); h[0] = 1.0
    for i in range(N):
        if i: h[i] = 0.05 + 0.10 * z_g[i - 1] ** 2 + 0.85 * h[i - 1]
        z_g[i] = e[i] * np.sqrt(h[i])
    z_g /= z_g.std()
    return {"normaal": rng.standard_normal(N), "pos. scheef": (g - k) / np.sqrt(k), "neg. scheef": -(g - k) / np.sqrt(k),
            "dikke staarten": t3 / t3.std(), "vol-clustering": z_g}
def main():
    srs = [1, 1.5, 2, 3, 4]
    for name, z in shapes().items():
        z = (z - z.mean()) / z.std()
        sk = float(((z - z.mean()) ** 3).mean())
        res = {p: [] for p in ("2step", "scaling")}
        for sr in srs:
            r = sr * 0.10 / 252 + SIG * z
            d = 1.2 * np.maximum(0.0, -r)
            for p in res:
                t, net, ploss, fund = qb.best(r, d, p)
                res[p].append(net)
        line = f"{name:<15} (skew {sk:+.2f}) "
        for p, vals in res.items():
            req = []
            for target in (500, 900):
                v = next((s0 + (target - v0) / (v1 - v0) * (s1 - s0) for s0, v0, s1, v1 in zip(srs, vals, srs[1:], vals[1:]) if v0 < target <= v1), None)
                req.append(f"{v:.1f}" if v else (">4" if vals[-1] < target else "<1"))
            line += f"| {p}: " + " ".join(f"SR{s}:€{v:,.0f}" for s, v in zip(srs, vals)) + f" → €500 SR {req[0]}, €900 SR {req[1]} "
        print(line, flush=True)
if __name__ == "__main__":
    main()
