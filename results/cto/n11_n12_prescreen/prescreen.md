# D-092.1 CTO C-012 — N11 / N12 (train 2021–2023)

Source U2 `2ac8e86` / Strateeg `b374f0a`. CTO verified trades CSVs (mean/N).
Reserve 2025+ untouched. No TRIALS by CTO.

## GER40 RT correction (binding)

`COSTS_FTMO.csv` (S0 header) lists **GER40cash roundtrip = 0.72 bp** → D-092.1 gate **3×0.72 = 2.16 bp**.
N6 / VOORSTEL N9/N11 claim of ~1.40 bp (gate 4.20) is a **mis-citation** of that file.
S2-GER40_OPEN already used 0.72. Binding for GER40 intradag = **COSTS RT**, not the erroneous 1.40.

| Idee | N | mean bruto | Binding gate | VOORSTEL gate | Uitkomst |
|------|---|------------|--------------|---------------|----------|
| N11 GER40 XETRA ORB | 496 | +3.33 bp | **2.16** (COSTS) | 4.20 (erroneous) | **PASS_may_PREREG** (binding) |
| N12 XAU NY-Open Cont | 303 | +0.59 bp | 2.49 | 2.49 | **FAIL — geen PREREG** |

N11 caveat: median −14.0 bp (skew-fragile). Still one honest PREREG under correct costs.
N9 remains underpowered (N=61) even under 2.16 — no PREREG.
