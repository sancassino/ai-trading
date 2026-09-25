param([string]$Name)
$dataFolder = "C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
$mq5 = "$dataFolder\MQL5\Experts\$Name.mq5"
Get-Process -Name terminal64,metatester64 -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2
Start-Process -FilePath "C:\Program Files\MetaTrader 5\metaeditor64.exe" -ArgumentList "/compile:`"$mq5`" /log" -Wait
Start-Sleep -Seconds 2
$ex5 = "$dataFolder\MQL5\Experts\$Name.ex5"
Write-Output "EX5 exists: $(Test-Path $ex5)"
