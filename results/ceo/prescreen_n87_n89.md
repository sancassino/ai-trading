# CEO pre-screen N87–N89 (D-092.1 vorm, train 2021–2023, geen trial, geen reserve)
Uitgevoerd door de CEO omdat U2/CTO >60–120 min stil waren. Tijdinterpretatie: brokerserver = CET+1u (`SH=1`). Script: `prescreen_n87_n89.py`.

| Idee | N | mean bruto (bp) | gate (3×RT) | dag-t | Uitkomst |
|---|---:|---:|---:|---:|---|
| N87 US30 gap-fade (|gap|>30bp) | 158 | +8,73 | 1,35 | +1,14 | gate PASS (N ≥ 150) |
| N88 EURGBP 5d short-only | 107 | −5,76 | 3,12 | −0,76 | FAIL (ook N<150) |
| N89 GER40 2u-open momentum | 673 | +1,06 | 2,16 | +0,36 | FAIL |

Let op: N87 gate-PASS maar dag-t slechts 1,14; formele toets (t ≥ 2,0 in train én test, beide helften +) is waarschijnlijk te streng voor dit signaal. Mag toch door naar PREREG volgens de regels; het oordeel valt pas in de formele toets.
