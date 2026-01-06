$env:PYTHONPATH = "$PSScriptRoot\src"
Write-Host "Starting Werewolf Arena Backend..."
# Remove -NoNewWindow to ensure visibility
Start-Process python -ArgumentList "-m uvicorn green_agent.server:app --host 0.0.0.0 --port 8000 --reload" -WorkingDirectory "$PSScriptRoot\src"
