param([string]$FromDate, [string]$ToDate, [string]$Tag)
$combos = @(
    @{TP=2; LB=1}, @{TP=2; LB=2}, @{TP=2; LB=3}, @{TP=2; LB=4},
    @{TP=3; LB=1}, @{TP=3; LB=2}, @{TP=3; LB=3}, @{TP=3; LB=4},
    @{TP=4; LB=1}, @{TP=4; LB=2}, @{TP=4; LB=3}, @{TP=4; LB=4}
)
foreach ($c in $combos) {
    $out = "$($Tag)_t$($c.TP)_l$($c.LB).csv"
    Write-Output "=== $out ==="
    & "C:\Users\sandro_cassino\vm_run_momentum.ps1" -FromDate $FromDate -ToDate $ToDate -TopN $c.TP -LookbackMonths $c.LB -ExposureFrac 0.30 -OutCsv $out
}
