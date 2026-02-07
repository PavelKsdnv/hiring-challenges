$base = "http://localhost:8000"

Write-Host "=== Testing Health ==="
Invoke-RestMethod "$base/api/health" | ConvertTo-Json

Write-Host "`n=== Testing Assets API ==="
$assets = Invoke-RestMethod "$base/api/v1/assets"
$assets | ConvertTo-Json -Depth 1

$signalId = $assets[0].signals[0].SignalId
Write-Host "`n=== Found Signal ID: $signalId ==="

Write-Host "`n=== Testing Measurements v1 ==="
$measurements = Invoke-RestMethod "$base/api/v1/measurements?signalIds=$signalId&from=2021-11-01T00:00:00&to=2021-11-08T00:00:00"
$count = $measurements.Count
Write-Host "Measurements count: $count"

Write-Host "`n=== Testing Measurements v2 Stats ==="
Invoke-RestMethod "$base/api/v2/measurements/stats/$signalId`?from=2021-11-01T00:00:00&to=2021-11-08T00:00:00" | ConvertTo-Json -Depth 1