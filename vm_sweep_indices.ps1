$symbols = @("US500.cash","US100.cash","US30.cash","EU50.cash","UK100.cash","GER40.cash","USOIL.cash")
foreach ($s in $symbols) {
    $tag = "$($s.Replace('.',''))_TP150_ATR6"
    $out = "$tag.csv"
    Write-Output "=== $tag ==="
    & "C:\Users\sandro_cassino\vm_run_test.ps1" -Symbol $s -FromDate "2015.01.01" -ToDate "2026.09.24" -TrendPeriod 150 -ATRStopMult 6.0 -OutCsv $out
}
