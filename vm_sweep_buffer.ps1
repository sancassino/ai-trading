param([string]$Symbol, [string]$FromDate, [int]$TP = 26)
$buffers = @(2, 5, 8, 12)
foreach ($b in $buffers) {
    $tag = "$($Symbol.Replace('.',''))_BUF$($b)_TP$TP"
    Write-Output "=== $tag ==="
    & "C:\Users\sandro_cassino\vm_run_test.ps1" -Symbol $Symbol -FromDate $FromDate -TF PERIOD_W1 -TrendPeriod $TP -ATRStopMult 15 -UseTrendExit true -ExitBufferPct $b -EntryBufferPct 1 -OutCsv "$tag.csv"
}
