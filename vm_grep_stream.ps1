param([string]$Pattern, [int]$MaxMatches = 30)
$logDir = 'C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs'
$log = (Get-ChildItem $logDir | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
Select-String -Path $log -Pattern $Pattern -Encoding Unicode | Select-Object -Last $MaxMatches | ForEach-Object { $_.Line }
