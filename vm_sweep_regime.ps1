param([string]$Symbol, [string]$FromDate)
$periods = @(13, 26, 39, 52, 78)
foreach ($p in $periods) {
    $tag = "$($Symbol.Replace('.',''))_REGIME_W$p"
    Write-Output "=== $tag ==="
    & "C:\Users\sandro_cassino\vm_run_test.ps1" -Symbol $Symbol -FromDate $FromDate -TF PERIOD_W1 -TrendPeriod $p -ATRStopMult 15 -UseTrendExit true -OutCsv "$tag.csv"
}
