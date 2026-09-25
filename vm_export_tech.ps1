$syms = @("AAPL","MSFT","AMZN","GOOG","META","NVDA","TSLA")
foreach ($s in $syms) {
    $out = "$($s)_rates.csv"
    Write-Output "=== $s ==="
    & "C:\Users\sandro_cassino\vm_export_rates.ps1" -Symbol $s -FromDate 2015.01.01 -ToDate 2026.09.24 -OutCsv $out
}
