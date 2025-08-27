$ErrorActionPreference = "Stop"
Clear-Host
Write-Host ""
Write-Host "===== TOKRA SHIELD =====" -ForegroundColor Cyan
$envName = "tokra_shield_env"
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue) }
if (-not $py) { throw "Python not found in PATH." }
& $py.Source -m venv $envName
. ".\$envName\Scripts\Activate.ps1"
python -m pip install --upgrade pip | Out-Null

$wheel = Get-ChildItem -Path ".\dist" -Filter "tokra_shield-*.whl" -ErrorAction SilentlyContinue | Select-Object -Last 1
if ($wheel) {
  $job = Start-Job { param($w) pip install $w fastapi==0.116.1 uvicorn==0.35.0 } -ArgumentList $wheel.FullName
} else {
  $job = Start-Job { pip install "tokra-shield[api]" }
}
while ($job.State -eq "Running") {
  Start-Sleep -Milliseconds 150
  Write-Progress -Activity "Installing Tokra Shield" -Status "Please wait..." -PercentComplete 50
}
Receive-Job $job -Wait
Write-Progress -Activity "Installing Tokra Shield" -Completed
tokra-shield hello
Write-Host "`n[OK] To start API: tokra-shield run"
