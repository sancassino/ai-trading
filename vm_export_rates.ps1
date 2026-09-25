param([string]$Symbol, [string]$FromDate = "2015.01.01", [string]$ToDate = "2026.09.24", [string]$OutCsv)

$dataFolder = "C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
$iniPath = "$dataFolder\exp_$($Symbol.Replace('.',''))_$([guid]::NewGuid().ToString('N').Substring(0,6)).ini"

$ini = @"
[Tester]
Expert=ExportRates
Symbol=$Symbol
Period=D1
Model=2
FromDate=$FromDate
ToDate=$ToDate
ForwardMode=0
Deposit=100000
Currency=USD
Leverage=100
ExecutionMode=0
Optimization=0
ShutdownTerminal=1
Visual=0

[TesterInputs]
OutFile=$OutCsv
"@

Set-Content -Path $iniPath -Value $ini -Encoding ASCII
Get-Process -Name terminal64,metatester64 -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3
$commonFile = "C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\Common\Files\$OutCsv"
if (Test-Path $commonFile) { Remove-Item $commonFile -Force }
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
    CommandLine = "`"C:\Program Files\MetaTrader 5\terminal64.exe`" /config:`"$iniPath`""
} | Out-Null
$maxWait = 60
$waited = 0
while (-not (Test-Path $commonFile) -and $waited -lt $maxWait) { Start-Sleep -Seconds 3; $waited += 3 }
Start-Sleep -Seconds 2
if (Test-Path $commonFile) { Write-Output "DONE: $OutCsv after $waited s" } else { Write-Output "TIMEOUT" }
Remove-Item $iniPath -Force -ErrorAction SilentlyContinue
