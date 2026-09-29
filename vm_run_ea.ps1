# Generieke Strategy Tester-run: willekeurige EA + inputs (bestand met regels 'naam=waarde').
param(
    [string]$Expert, [string]$Symbol = "US500.cash", [string]$Period = "M1",
    [string]$FromDate = "2021.01.01", [string]$ToDate = "2026.09.24",
    [int]$Deposit = 80000, [string]$Currency = "EUR", [int]$Model = 1,
    [string]$InputsFile = "", [string]$OutCsv, [int]$MaxWait = 1800
)
$dataFolder = "C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
$iniPath = "$dataFolder\tester_ea_$([guid]::NewGuid().ToString('N').Substring(0,8)).ini"
$inputs = ""
if ($InputsFile -ne "" -and (Test-Path $InputsFile)) { $inputs = (Get-Content $InputsFile) -join "`r`n" }
$ini = @"
[Tester]
Expert=$Expert
Symbol=$Symbol
Period=$Period
Model=$Model
FromDate=$FromDate
ToDate=$ToDate
ForwardMode=0
Deposit=$Deposit
Currency=$Currency
Leverage=100
ExecutionMode=0
Optimization=0
ShutdownTerminal=1
Visual=0

[TesterInputs]
$inputs
DiagBestandsnaam=$OutCsv
"@
Set-Content -Path $iniPath -Value $ini -Encoding ASCII
Get-Process -Name terminal64,metatester64 -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3
$commonFile = "C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\Common\Files\$OutCsv"
if (Test-Path $commonFile) { Remove-Item $commonFile -Force }
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
    CommandLine = "`"C:\Program Files\MetaTrader 5\terminal64.exe`" /config:`"$iniPath`""
} | Out-Null
$waited = 0
while (-not (Test-Path $commonFile) -and $waited -lt $MaxWait) { Start-Sleep -Seconds 5; $waited += 5 }
Start-Sleep -Seconds 3
if (Test-Path $commonFile) { Write-Output "DONE: $OutCsv ($((Get-Item $commonFile).Length) bytes) after $waited s" } else { Write-Output "TIMEOUT" }
Remove-Item $iniPath -Force -ErrorAction SilentlyContinue
