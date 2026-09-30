"""J2: drie hypothesen uit VOORSTEL_G.md (US100 gap-continuatie, XAU ORB Londen, GER40 ORB met US-filter)."""
from datetime import timedelta
from zoneinfo import ZoneInfo
import b4_sim
from b4_sim import NY, SYMS, cost_frac, load, run_orb, sessions
from c2_leadlag import evaluate

def gap_cont():
    sess = sessions("US100cash"); out = []; prev = None
    for d, s in sess:
        if prev is not None and len(s) >= 12:
            gap = s[0][1] / prev - 1
            if abs(gap) > 0.005:
                side = 1 if gap > 0 else -1
                out.append((d, side * (s[11][4] - s[0][1]) / s[0][1] - cost_frac(side, s[0], s[11], s[0][1], 0.0)))
        prev = s[-1][4]
    return out

def xau_london():
    b4_sim.SYMS["XAU_LON"] = ("Europe/London", (8, 0), (16, 30), SYMS["XAUUSD"][3])
    orig = b4_sim.load
    b4_sim.load = lambda sym: orig("XAUUSD" if sym == "XAU_LON" else sym)
    try:
        return [(d, n) for d, n, _ in run_orb(sessions("XAU_LON"), SYMS["XAUUSD"][3])]
    finally:
        b4_sim.load = orig

def ger40_filtered():
    # US500-prijs op servertijd, om het rendement vorige US-slot -> einde GER40-OR te bepalen
    us = {b[0]: b[4] for b in load("US500cash")}
    us_keys = sorted(us)
    import bisect
    def us_at(server_t):
        i = bisect.bisect_right(us_keys, server_t) - 1
        return us[us_keys[i]] if i >= 0 else None
    us_sess = dict(sessions("US500cash"))
    ger = sessions("GER40cash"); out = []
    for d, s in ger:
        prev_us = [x for x in us_sess if x < d]
        if not prev_us or len(s) < 8: continue
        us_close = us_sess[prev_us[-1]][-1][4]
        or_end_server = (s[5][0] + timedelta(minutes=5)).astimezone(NY).replace(tzinfo=None) + timedelta(hours=7)
        u = us_at(or_end_server)
        if not u: continue
        direction = 1 if u > us_close else -1
        tr = run_orb([(d, s)], SYMS["GER40cash"][3])
        for dd, net, R in tr:
            # bepaal richting van de ORB-trade: herbereken via teken van (slot - OR-grens) is niet beschikbaar; run_orb geeft
            # alleen netto rendement → richting afleiden uit de eerste doorbraak-bar
            hi = max(b[2] for b in s[:6]); lo = min(b[3] for b in s[:6])
            first = next((b for b in s[6:] if b[2] > hi or b[3] < lo), None)
            if first is None: continue
            side = 1 if first[2] > hi and not first[3] < lo else (-1 if first[3] < lo and not first[2] > hi else 1)
            if side == direction:
                out.append((dd, net))
    return out

if __name__ == "__main__":
    evaluate("(1) US100 gap-continuatie", gap_cont())
    evaluate("(2) XAU ORB Londen", xau_london())
    evaluate("(3) GER40 ORB + US-filter", ger40_filtered())
