from monte_carlo_ftmo import load_monthly_returns, simulate
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "MR_t2_l3.csv"
rets = load_monthly_returns(path)
print(f"{path}: {len(rets)} months")
for bs in [1, 3, 6, 9, 12, 18]:
    r = simulate(rets, block_size=bs, n_sims=30000)
    print(f"block_size={bs:2d}mo: phase1={r['phase1_pass']*100:5.1f}%  funded={r['funded']*100:5.1f}%  live_income={r['live_income_ok_given_attempt']*100:5.1f}%")
