$env:PYTHONPATH = "$PSScriptRoot\src"
$Count = 5

for ($i = 0; $i -lt $Count; $i++) {
    $Port = 8001 + $i
    $Name = "Player_$($i + 1)"
    Write-Host "Starting $Name on port $Port..."
    # Launch each agent in a separate window for visibility
    Start-Process python -ArgumentList "-m purple_agent.server --port $Port" -WorkingDirectory "$PSScriptRoot\src"
}
