"""G3/H1: NR7-opening-range-breakout (Crabel) op FTMO-M5, volgens VOORSTEL_F.md (H1)."""
import statistics
from b4_sim import SYMS, run_orb, sessions
from c2_leadlag import evaluate

def main():
    allt, base = [], []
    for s in SYMS:
        sess = sessions(s)
        ranges = [max(b[2] for b in x) - min(b[3] for b in x) for _, x in sess]
        nr7 = [i for i in range(7, len(sess)) if ranges[i - 1] <= min(ranges[i - 7:i])]
        sel = [sess[i] for i in nr7]
        t = run_orb(sel, SYMS[s][3])
        allt += [(d, n) for d, n, _ in t]
        base += [(d, n) for d, n, _ in run_orb(sess, SYMS[s][3])]
        print(f"  {s:<10} NR7-dagen {len(sel):>4} | trades {len(t):>4} | {statistics.mean([n for _, n, _ in t])*1e4 if t else float('nan'):+.2f} bp")
    evaluate("H1 NR7-ORB (gepoold)", allt)
    b = statistics.mean([n for _, n in base]) * 1e4; h = statistics.mean([n for _, n in allt]) * 1e4
    print(f"  bp/trade NR7 {h:+.2f} vs B4a {b:+.2f} → {'≥ 2×' if h >= 2 * b else '< 2×'} (eis ≥ 2×)")

if __name__ == "__main__":
    main()
