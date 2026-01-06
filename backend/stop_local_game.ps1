Stop-Process -Name "python" -ErrorAction SilentlyContinue
Stop-Process -Name "uvicorn" -ErrorAction SilentlyContinue
Write-Host "Werewolf Arena Backend Stopped."
