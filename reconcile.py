"""Vergelijk maandrendementen van twee dag-equity-logs (bv. Python-sim vs MT5).
Gebruik: python3 reconcile.py a_daily.csv b_daily.csv"""
import sys, statistics
from walk_forward import monthly_returns
a, b = monthly_returns(sys.argv[1]), monthly_returns(sys.argv[2])
ms = sorted(set(a) & set(b))
x, y = [a[m] for m in ms], [b[m] for m in ms]
corr = statistics.correlation(x, y)
tot = lambda r: __import__("math").prod(1 + v for v in r) - 1
print(f"{len(ms)} maanden | correlatie maandrendement {corr:.3f} | totaal A {tot(x)*100:+.1f}% vs B {tot(y)*100:+.1f}% | "
      f"verschil {abs(tot(x)-tot(y))/max(abs(tot(y)),1e-9)*100:.0f}% van B")
diffs = sorted(zip(ms, x, y), key=lambda t: -abs(t[1] - t[2]))[:6]
print("grootste afwijkingen:", " ".join(f"{m}:{p*100:+.1f}/{q*100:+.1f}" for m, p, q in diffs))
