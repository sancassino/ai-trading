$syms = @(
    @{S="US500.cash"; F="2017.01.01"},
    @{S="US100.cash"; F="2017.01.01"},
    @{S="US30.cash";  F="2017.01.01"},
    @{S="EU50.cash";  F="2017.01.01"},
    @{S="UK100.cash"; F="2017.01.01"},
    @{S="GER40.cash"; F="2017.01.01"}
)
foreach ($x in $syms) {
    $out = "$($x.S.Replace('.',''))_rates.csv"
    Write-Output "=== $($x.S) ==="
    & "C:\Users\sandro_cassino\vm_export_rates.ps1" -Symbol $x.S -FromDate $x.F -OutCsv $out
}
