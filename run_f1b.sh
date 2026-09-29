#!/bin/bash
# F1b: 3 varianten x 4 schalen voor RSI2Sleeve
S=/tmp/claude-1001/-home-sandro-cassino-ai-trading/a42a5805-4eb4-4c9d-a275-83c4a128786d/scratchpad
for V in cap guard both; do for SC in 0.8 1.0 1.5 2.0; do
  N="F1b_${V}_s${SC}.csv"; [ -f results/f/$N ] && continue
  LF=$(awk "BEGIN{printf \"%.5f\", $SC/6}")
  MIP=0; DG=0; [ $V = cap ] && MIP=2; [ $V = guard ] && DG=3; [ $V = both ] && MIP=2 && DG=3
  printf "LegFrac=$LF\nMaxIndexPositions=$MIP\nDayGuardPct=$DG\n" > $S/in_f1b.txt
  ./run_ea.sh RSI2Sleeve $N $S/in_f1b.txt | grep -v SWEEP_DONE
done; done; echo SWEEP_DONE
