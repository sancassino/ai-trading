"""AUDIT_1: test of het forward-papier een kunstmatig 'maandeinde' op de laatste beschikbare dag krijgt (engine.month_end: np.r_[..., True]).
Methode: monkeypatch engine.run_rule.load_daily zodat data na T wordt afgekapt; vergelijk het dagrendement van T met de volledige run."""
import sys; sys.path.insert(0, ".")
import numpy as np
from datetime import date
import engine.run_rule as E
import engine.forward as F
orig = E.load_daily
def run(cut):
    def ld(name, field="adjclose"):
        d = orig(name, field)
        if cut is None: return d
        k = d["date"] <= cut
        return {kk: (v[k] if isinstance(v, np.ndarray) else v) for kk, v in d.items()}
    E.load_daily = ld; F.load_daily = ld
    import catalogus._common as C
    try:
        return {r: F.series(*spec, start=date(2024, 1, 1), end=date(2024, 12, 31)) for r, spec in (("C52L", ("C52_allweather", "lang", "etf")), ("C02", ("C02_faber", "basis", "etf")))}
    finally:
        E.load_daily = orig; F.load_daily = orig
full = run(None)
for cut in (date(2024, 6, 14), date(2024, 6, 19), date(2024, 9, 18), date(2024, 11, 14), date(2024, 12, 13)):
    part = run(cut)
    for k in ("C52L", "C02"):
        d = max(part[k]); a, b = part[k][d][1], full[k][d][1]
        # verschil voor alle eerdere dagen
        prev = max(abs(part[k][x][1] - full[k][x][1]) for x in part[k] if x < d)
        print(f"{k:5s} afgekapt op {cut} (laatste rij {d}): dagrendement laatste dag {a*1e4:+8.3f} bp (volledige run {b*1e4:+8.3f} bp) verschil {(a-b)*1e4:+7.3f} bp; max verschil eerdere dagen {prev:.2e}")
