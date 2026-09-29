#!/bin/bash
# Uurlijkse check op een nieuwe supervisor-opdracht. Meldt NIEUW als:
#  - een remote branch (≠ main) een NEXT_STEPS.md bevat die nog niet verwerkt is, of
#  - NEXT_STEPS.md op origin/main een andere inhoud heeft dan de laatst verwerkte.
# Verwerkte versies (blob-hashes) staan in .git/next_steps_seen (niet in de repo).
# Gebruik: ./check_next_steps.sh [--mark <blob-hash>]
cd "$(dirname "$0")"
SEEN=.git/next_steps_seen; touch $SEEN
if [ "$1" = "--mark" ]; then echo "$2" >> $SEEN; exit 0; fi
git fetch -q --prune origin || { echo "FOUT: git fetch mislukt"; exit 2; }
found=0
for ref in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin | grep -v -e '^origin$' -e 'origin/HEAD'); do
  blob=$(git rev-parse -q --verify "$ref:NEXT_STEPS.md" 2>/dev/null) || continue
  grep -qx "$blob" $SEEN && continue
  echo "NIEUW: $ref bevat NEXT_STEPS.md (blob $blob, commit $(git log -1 --format='%h %ci %s' $ref))"; found=1
done
[ $found = 0 ] && echo "GEEN nieuwe NEXT_STEPS ($(date '+%Y-%m-%d %H:%M'))"
exit 0
