# ---------------------------------------------------------------------------
# 06 - Masaustu dosyalarini tum makinelerde gunceller:
#   - komutlar.txt (GitHub'dan)
#   - "AES Lab Rehberi" kisayolu ve Chrome/Edge favorileri (LabGuideUrl)
#   - C:\Projeler icin aes-user yazma yetkisi (npm install yonetici gerektirmesin)
#
# AMI'yi yeniden almadan tum makinelere dagitmak icin kullanin.
# Not: GitHub raw icerigi birkac dakika onbellekte kalabilir.
# ---------------------------------------------------------------------------
param([string[]]$Only)
. "$PSScriptRoot\common.ps1"
Assert-Configured @("RepoRawBase", "WorkshopUser")

$instances = @(Get-WorkshopInstances -Only $Only | Where-Object { $_.State -eq "running" })
if ($instances.Count -eq 0) { throw "Calisan workshop instance'i bulunamadi." }

Wait-SsmOnline $instances

$script = @"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
`$dest = 'C:\Users\$WorkshopUser\Desktop\komutlar.txt'
Invoke-WebRequest -UseBasicParsing -Uri '$RepoRawBase/komutlar.txt' -OutFile `$dest
Write-Output "Guncellendi: `$dest (`$((Get-Item `$dest).Length) byte)"
`$guide = '$(if ($LabGuideUrl) { $LabGuideUrl } else { "https://aes-workshop-v3.onrender.com" })'
`$lnk = 'C:\Users\$WorkshopUser\Desktop\AES Lab Rehberi.url'
[IO.File]::WriteAllText(`$lnk, "[InternetShortcut]``r``nURL=`$guide``r``n")
Write-Output "Kisayol: `$lnk -> `$guide"
# Tarayici favorileri: konsol adresi masaustundeki AES Konsol kisayolundan okunur
`$console = ''
`$consoleLnk = 'C:\Users\$WorkshopUser\Desktop\AES Konsol.url'
if (Test-Path `$consoleLnk) {
    `$m = Select-String -Path `$consoleLnk -Pattern '^URL=(.+)$' | Select-Object -First 1
    if (`$m) { `$console = `$m.Matches[0].Groups[1].Value.Trim() }
}
`$bm = @(
    @{ toplevel_name = 'AES Workshop' },
    [ordered]@{ name = 'AES Konsol';      url = `$console },
    [ordered]@{ name = 'AES Lab Rehberi'; url = `$guide }
)
`$json = ConvertTo-Json -InputObject `$bm -Compress
foreach (`$key in @('HKLM:\SOFTWARE\Policies\Google\Chrome', 'HKLM:\SOFTWARE\Policies\Microsoft\Edge')) {
    New-Item -Path `$key -Force | Out-Null
    Set-ItemProperty -Path `$key -Name 'ManagedBookmarks'   -Value `$json -Type String
    Set-ItemProperty -Path `$key -Name 'BookmarkBarEnabled' -Value 1      -Type DWord
}
Write-Output "Tarayici favorileri: AES Konsol -> `$console, AES Lab Rehberi -> `$guide"
if (Test-Path 'C:\Projeler') {
    icacls.exe 'C:\Projeler' /grant '${WorkshopUser}:(OI)(CI)M' /T /C /Q | Out-Null
    Write-Output "C:\Projeler: $WorkshopUser icin yazma yetkisi verildi"
}
"@

Write-Host "==> Masaustu dosyalari guncelleniyor: $($instances.Count) makine" -ForegroundColor Cyan
$sent = Send-SsmScript -InstanceIds @($instances | ForEach-Object { $_.InstanceId }) -Script $script -Comment "update desktop" -ExecutionTimeoutSeconds 300
Wait-SsmCommands -Sent $sent -Instances $instances -TimeoutMinutes 10 | Out-Null
