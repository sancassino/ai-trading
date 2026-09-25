param([string]$Symbol, [string]$FromDate = "2004.01.01")
$combos = @(
    @{TP=200; BO=55;  ATR=4.0},
    @{TP=100; BO=100; ATR=5.0},
    @{TP=50;  BO=20;  ATR=4.0}
)
foreach ($c in $combos) {
    $tag = "$($Symbol.Replace('.',''))_DON_TP$($c.TP)_BO$($c.BO)_ATR$($c.ATR)"
    Write-Output "=== $tag ==="
    & "C:\Users\sandro_cassino\vm_run_test.ps1" -Symbol $Symbol -FromDate $FromDate -TrendPeriod $c.TP -BreakoutLookback $c.BO -ATRStopMult $c.ATR -OutCsv "$tag.csv"
}
