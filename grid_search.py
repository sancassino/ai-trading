from momentum_rotation_daily import run

results = []
for lookback in [1, 2, 3, 4, 6, 9, 12]:
    for top_n in [1, 2, 3, 4, 5]:
        r = run(lookback, top_n, 1.0)
        if r['n_months'] < 20:
            continue
        # size to the binding constraint: 5% single-day loss OR 10% static floor
        worst_day_pct = abs(r['worst_day'][1]) / 100000
        floor_pct = r['static_dd_from_start']
        max_exposure_day = 0.05 / worst_day_pct if worst_day_pct > 0 else 1.0
        max_exposure_floor = 0.10 / floor_pct if floor_pct > 0 else 1.0
        safe_exposure = min(1.0, max_exposure_day, max_exposure_floor) * 0.9  # 10% safety margin
        r_scaled = run(lookback, top_n, safe_exposure)
        results.append((lookback, top_n, safe_exposure, r_scaled['avg_month'], r_scaled['static_dd_from_start'],
                         abs(r_scaled['worst_day'][1])/100000, sum(1 for y in r_scaled['years'] if r_scaled['years'][y]>0), len(r_scaled['years'])))

results.sort(key=lambda x: -x[3])
print(f"{'lookback':>8} {'top_n':>6} {'exposure':>9} {'avg/mo':>10} {'staticDD':>9} {'worstday':>9} {'yrs+':>6}")
for row in results:
    print(f"{row[0]:>8} {row[1]:>6} {row[2]*100:>8.1f}% ${row[3]:>8,.0f} {row[4]*100:>8.1f}% {row[5]*100:>8.1f}% {row[6]}/{row[7]}")
