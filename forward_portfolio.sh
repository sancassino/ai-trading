#!/bin/bash
# Forward-papier portefeuilles (D-050, PREREG_PORT): na data-update (22:05) en F3b (22:15). Cron 22:25 UTC ma–vr.
cd /home/sandro_cassino/ai-trading || exit 1
git pull -q --rebase --autostash origin main || true
.venv/bin/python forward_portfolio.py >> forward/portfolio_cron.log 2>&1
git add forward/portfolio_daily.csv forward/portfolio2_daily.csv forward/portfolio_tracking.log forward/portfolio_cron.log 2>/dev/null
git commit -q -m "forward: portefeuille-papier $(date -u +%F)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || exit 0
for i in 1 2 3; do git push -q origin HEAD:main && break; git pull -q --rebase --autostash origin main; sleep 20; done
