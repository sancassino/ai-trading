"""D1: EURUSD-intradagseizoen met vaste vensters, exact volgens PREREG_D1.md."""
from collections import defaultdict
from datetime import timedelta
from zoneinfo import ZoneInfo

from b4_sim import NY, cost_frac, load
from c2_leadlag import evaluate

LON = ZoneInfo("Europe/London")
COMM = 0.0000225


def window(side, start_hm, last_hm):
    by_day = defaultdict(dict)
    for b in load("EURUSD"):
        t = (b[0] - timedelta(hours=7)).replace(tzinfo=NY).astimezone(LON)
        by_day[t.date()][(t.hour, t.minute)] = (t,) + b[1:]
    out = []
    for d, bars in sorted(by_day.items()):
        if start_hm in bars and last_hm in bars:
            eb, xb = bars[start_hm], bars[last_hm]
            net = side * (xb[4] - eb[1]) / eb[1] - cost_frac(side, eb, xb, eb[1], COMM)
            out.append((d, net))
    return out


if __name__ == "__main__":
    evaluate("(i) short EUR 08-12 LON", window(-1, (8, 0), (11, 55)))
    evaluate("(ii) long EUR 14-18 LON", window(1, (14, 0), (17, 55)))
