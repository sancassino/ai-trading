param(
    [string]$FromDate = "2018.01.01",
    [string]$ToDate = "2026.09.24",
    [int]$LookbackMonths = 1,
    [int]$TopN = 3,
    [double]$ExposureFrac = 0.53,
    [string]$UseInverseVolWeight = "false",
    [double]$MaxLegWeight = 1.0,
    [string]$SelectBottom = "false",
    [int]$RegimeSMAMonths = 0,
    [string]$RegimeSymbol = "US500.cash",
    [double]$DailyGuardPct = 0,
    [double]$TotalGuardPct = 0,
    [string]$UniverseList = "",
    [string]$RankByRiskAdj = "false",
    [int]$MaxWait = 180,
    [string]$OutCsv = "MomentumRotation_output.csv"
)

$dataFolder = "C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
$iniPath = "$dataFolder\tester_mom_$([guid]::NewGuid().ToString('N').Substring(0,8)).ini"

$ini = @"
[Tester]
Expert=MomentumRotation
Symbol=US500.cash
Period=D1
Model=1
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
LookbackMonths=$LookbackMonths
TopN=$TopN
ExposureFrac=$ExposureFrac
UseInverseVolWeight=$UseInverseVolWeight
MaxLegWeight=$MaxLegWeight
SelectBottom=$SelectBottom
RegimeSMAMonths=$RegimeSMAMonths
RegimeSymbol=$RegimeSymbol
DailyGuardPct=$DailyGuardPct
TotalGuardPct=$TotalGuardPct
UniverseList=$UniverseList
RankByRiskAdj=$RankByRiskAdj
MagicNumber=20260925
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
$maxWait = $MaxWait
$waited = 0
while (-not (Test-Path $commonFile) -and $waited -lt $maxWait) { Start-Sleep -Seconds 5; $waited += 5 }
Start-Sleep -Seconds 3
if (Test-Path $commonFile) { Write-Output "DONE: $OutCsv ($((Get-Item $commonFile).Length) bytes) after $waited s" } else { Write-Output "TIMEOUT" }
Remove-Item $iniPath -Force -ErrorAction SilentlyContinue
