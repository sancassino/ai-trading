param(
    [string]$Marker,
    [int]$Lines = 500
)
$logDir = 'C:\Users\sandro_cassino\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs'
$log = (Get-ChildItem $logDir | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
$c = Get-Content $log -Encoding Unicode
$idx = @()
for ($i = 0; $i -lt $c.Count; $i++) { if ($c[$i] -match [regex]::Escape($Marker)) { $idx += $i } }
if ($idx.Count -eq 0) { Write-Output "MARKER NOT FOUND"; exit }
$start = $idx[-1]
$end = [Math]::Min($start + $Lines, $c.Count - 1)
$c[$start..$end]
