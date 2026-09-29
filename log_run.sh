#!/bin/bash
# Voegt een entry toe aan RUNLOG.md en commit + pusht alles (incl. results/).
# Gebruik: ./log_run.sh "Titel" "Getest: ...\nResultaat: ...\nVolgende stap: ..."
set -e
cd "$(dirname "$0")"
[ -f RUNLOG.md ] || printf '# RUNLOG\n\nKort verslag per run/test, nieuwste onderaan.\n' > RUNLOG.md
printf '\n## %s — %s\n\n%b\n' "$(date '+%Y-%m-%d %H:%M')" "$1" "$2" >> RUNLOG.md
git add -A
git commit -q -m "RUNLOG: $1" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q origin HEAD:main
git log --oneline -1
