param(
    [string]$Symbol,
    [string]$FromDate = "2004.01.01",
    [string]$ToDate = "2026.09.24"
)

$combos = @(
    @{TP=200; ATR=4.0},
    @{TP=200; ATR=6.0},
    @{TP=200; ATR=8.0},
    @{TP=150; ATR=6.0},
    @{TP=100; ATR=6.0}
)

foreach ($c in $combos) {
    $tag = "$($Symbol.Replace('.',''))_TP$($c.TP)_ATR$($c.ATR)"
    $out = "$tag.csv"
    Write-Output "=== $tag ==="
    & "C:\Users\sandro_cassino\vm_run_test.ps1" -Symbol $Symbol -FromDate $FromDate -ToDate $ToDate -TrendPeriod $c.TP -ATRStopMult $c.ATR -OutCsv $out
}
