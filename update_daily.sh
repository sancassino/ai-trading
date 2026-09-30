#!/bin/bash
# Dagelijkse data-update (D-050): incrementeel data/daily bijwerken, QA-checksums, commit + push (met rebase). Cron 22:05 UTC ma–vr.
cd /home/sandro_cassino/ai-trading || exit 1
git pull -q --rebase --autostash origin main || true
.venv/bin/python update_daily.py >> results/update_daily.log 2>&1
sha256sum data/daily/*.csv > data/CHECKSUMS_daily.sha256
git add data/daily data/CHECKSUMS_daily.sha256 results/update_daily.log forward/data_snapshots
git commit -q -m "data/daily: dagelijkse update $(date -u +%F)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || exit 0
for i in 1 2 3; do git push -q origin HEAD:main && break; git pull -q --rebase --autostash origin main; sleep 20; done
