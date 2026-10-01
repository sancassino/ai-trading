# S2 D-092.1 cycle_1140 (D-094 FREEZE OFF + D-097/D-100)

Train proxy daily 2010-01-01 → 2023-12-31; 2024 holdout unused; 2025+ sealed.
D-097 gate = max(3×RT, 50 bp). Non-overlapping holds. Overnight = D-100 cheap side only.

| Idee | Symbool | N | mean bruto | gate | outcome | skew | hit |
|------|---------|--:|----------:|-----:|---------|------|-----|
| SOY_SHORT_TSMOM | SOYBEAN.c / SOY_F | 189 | -17.8409 | 50.0 | **FAIL** | 0.5054 | 0.4444 |
| COFFEE_LONG_TSMOM | COFFEE.c / COFFEE_F | 191 | 44.7632 | 50.0 | **FAIL** | 0.7132 | 0.4869 |
| USDCHF_LONG_TSMOM | USDCHF / FX_USDCHF | 192 | -3.3213 | 50.0 | **FAIL** | 0.202 | 0.4896 |
| XAU_SHORT_TSMOM | XAUUSD / GOLD_F | 191 | -23.2898 | 50.0 | **FAIL** | -0.0436 | 0.4555 |
| USDCAD_LONG_TSMOM | USDCAD / FX_USDCAD | 200 | 1.9693 | 50.0 | **FAIL** | 0.3727 | 0.51 |
