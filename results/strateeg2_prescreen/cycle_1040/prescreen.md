# S2 D-092.1 cycle_1040 (D-094 FREEZE OFF + D-097/D-099)

Train proxy daily 2010-01-01 → 2023-12-31; 2024 holdout unused; 2025+ sealed.
D-097 gate = max(3×RT, 50 bp). Non-overlapping holds.

| Idee | Symbool | N | mean bruto | gate | outcome | skew | hit |
|------|---------|--:|----------:|-----:|---------|------|-----|
| XCU_HV_TSMOM | XCUUSD / COPPER_F | 113 | -9.6819 | 50.0 | **FAIL** | 0.1994 | 0.4425 |
| CORN_PLANT_MOM | CORN.c / CORN_F | 64 | -83.502 | 64.71 | **FAIL** | 0.2588 | 0.4219 |
| WHEAT_WINTER_MOM | WHEAT.c / WHEAT_F | 59 | -11.3323 | 56.61 | **FAIL** | 0.5274 | 0.4407 |
| HK50_SWING_TSMOM | HK50cash / HSI | 199 | -13.1966 | 50.0 | **FAIL** | -0.5393 | 0.5025 |
| GBPAUD_SWING20 | GBPAUD / FXBIS | 509 | -0.2461 | 50.0 | **FAIL** | -0.6837 | 0.5128 |
