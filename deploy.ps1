# Заливка статики на VPS. Пример:
#   .\deploy.ps1 -Vps 85.209.3.56 -Key "$env:USERPROFILE\.ssh\vps_ai"
param(
  [Parameter(Mandatory = $true)][string]$Vps,
  [string]$User = "root",
  [string]$Target = "/var/www/dima404",
  [int]$Port = 22,
  [string]$Key = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$remote = "$User@$Vps"

$sshArgs = @("-p", $Port, "-o", "BatchMode=yes")
$scpArgs = @("-P", $Port)
if ($Key) {
  $sshArgs += @("-i", $Key)
  $scpArgs += @("-i", $Key)
}

Write-Host "==> создаю каталог $Target" -ForegroundColor Cyan
& ssh @sshArgs $remote "mkdir -p $Target"

Write-Host "==> копирую файлы" -ForegroundColor Cyan
& scp @scpArgs -r "$root\index.html" "$root\404.html" "$root\assets" "${remote}:$Target/"

Write-Host "==> ставлю права" -ForegroundColor Cyan
& ssh @sshArgs $remote "find $Target -type d -exec chmod 755 {} + && find $Target -type f -exec chmod 644 {} +"

Write-Host "Готово. Проверь: http://$Vps/" -ForegroundColor Green
