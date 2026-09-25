param(
    [string]$Symbol,
    [string]$FromDate = "2000.01.01",
    [string]$ToDate = "2026.09.24",
    [double]$RiskPct = 1.0,
    [int]$TrendPeriod = 200,
    [double]$ATRStopMult = 3.0,
    [string]$UseTrendExit = "false",
    [string]$TF = "PERIOD_D1",
    [int]$BreakoutLookback = 0,
    [double]$ExitBufferPct = 0.0,
    [double]$EntryBufferPct = 0.0,
    [string]$OutCsv
)

$dataFolder = "C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
$iniPath = "$dataFolder\tester_$($Symbol)_$([guid]::NewGuid().ToString('N').Substring(0,8)).ini"

$ini = @"
[Tester]
Expert=TrendFollow_CrossAsset
Symbol=$Symbol
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
TF=$TF
TrendPeriod=$TrendPeriod
BreakoutLookback=$BreakoutLookback
ExitBufferPct=$ExitBufferPct
EntryBufferPct=$EntryBufferPct
ATRPeriod=20
ATRStopMult=$ATRStopMult
UseTrendExit=$UseTrendExit
RiskPct=$RiskPct
Slippage=5
MagicNumber=20260924
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

$maxWait = 180
$waited = 0
while (-not (Test-Path $commonFile) -and $waited -lt $maxWait) {
    Start-Sleep -Seconds 5
    $waited += 5
}
Start-Sleep -Seconds 3

if (Test-Path $commonFile) {
    Write-Output "DONE: $OutCsv ($((Get-Item $commonFile).Length) bytes) after $waited s"
} else {
    Write-Output "TIMEOUT: no output file after $maxWait s"
}
Remove-Item $iniPath -Force -ErrorAction SilentlyContinue
