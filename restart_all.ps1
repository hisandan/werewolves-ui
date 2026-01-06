Write-Host "🛑 Killing old processes..."
Get-Process python, uvicorn -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "⏳ Waiting 3 seconds..."
Start-Sleep -Seconds 3

Write-Host "🚀 Starting Backend (Green Agent)..."
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\backend\start_local_game.ps1"

Write-Host "🚀 Starting Agents (Purple Agents)..."
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\backend\start_agents.ps1"

Write-Host "🚀 Starting Frontend..."
Set-Location "$PSScriptRoot\frontend"
Start-Process python -ArgumentList "-m http.server 8080" -WindowStyle Minimized

Write-Host "✅ SYSTEM RESTARTED. Go to http://localhost:8080"
