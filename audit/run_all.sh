#!/bin/sh
# AUDIT_1 — reproduceer alle auditresultaten (vanuit repo-root; vereist numpy pandas scipy statsmodels; data ≤ 2024-12-31 via audit/common.py)
mkdir -p audit/out
for s in rep_petf rep_sens2 rep_drift rep_phase stat_bh stat_t stat_alpha datacheck calendar_check forward_lastday; do
  python3 audit/$s.py 2>&1 | grep -v -E "Warning|new =|warnings" > audit/out/$s.txt
done
