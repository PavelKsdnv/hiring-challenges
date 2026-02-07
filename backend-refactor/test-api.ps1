$base = "http://localhost:8000"
$pass = 0
$fail = 0

function Assert-Eq($label, $expected, $actual) {
    if ($expected -eq $actual) {
        Write-Host "  PASS: $label" -ForegroundColor Green
        $script:pass++
    } else {
        Write-Host "  FAIL: $label (expected '$expected', got '$actual')" -ForegroundColor Red
        $script:fail++
    }
}

function Assert-Contains($label, $needle, $haystack) {
    if ($haystack -like "*$needle*") {
        Write-Host "  PASS: $label" -ForegroundColor Green
        $script:pass++
    } else {
        Write-Host "  FAIL: $label (expected response to contain '$needle')" -ForegroundColor Red
        $script:fail++
    }
}

# Preflight
try {
    Invoke-RestMethod "$base/api/health" -TimeoutSec 3 | Out-Null
} catch {
    Write-Host "ERROR: Cannot reach $base - is the server running?" -ForegroundColor Red
    exit 1
}

# Test 1: Health endpoint
Write-Host "Test 1: Health endpoint"
$health = Invoke-RestMethod "$base/api/health"
Assert-Eq "status is ok" "ok" $health.status

# Test 2: Assets return correct signal fields
Write-Host "Test 2: Assets response uses snake_case signal fields"
$assets = Invoke-RestMethod "$base/api/v1/assets"
$raw = $assets | ConvertTo-Json -Depth 3
Assert-Contains "has signal_id field" "signal_id" $raw
Assert-Contains "has signal_name field" "signal_name" $raw
Assert-Contains "has asset_id on signal" "asset_id" $raw
Assert-Contains "has unit field" "unit" $raw

# Test 3: Assets count
Write-Host "Test 3: Assets count"
Assert-Eq "3 assets returned" 3 $assets.Count

# Test 4: Measurements v1 returns data
Write-Host "Test 4: Measurements v1 returns data"
$signalId = $assets[0].signals[0].signal_id
$measurements = Invoke-RestMethod "$base/api/v1/measurements?signalIds=$signalId&from=2021-11-01T00:00:00&to=2021-11-08T00:00:00"
Assert-Eq "260 measurements returned" 260 $measurements.Count

# Test 5: Measurements v2 stats are correct
Write-Host "Test 5: Measurement stats endpoint"
$stats = Invoke-RestMethod "$base/api/v2/measurements/stats/$signalId`?from=2021-11-01T00:00:00&to=2021-11-08T00:00:00"
Assert-Eq "stats count is 260" 260 $stats.count
Assert-Eq "stats mean is 114.69" 114.69 $stats.mean

# Test 6: Invalid date range returns 400
Write-Host "Test 6: Invalid date range returns 400"
try {
    Invoke-RestMethod "$base/api/v2/measurements/stats/$signalId`?from=2021-11-08T00:00:00&to=2021-11-01T00:00:00"
    Assert-Eq "returns 400" "400" "200"
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    Assert-Eq "returns 400" 400 $code
}

# Summary
Write-Host "`nResults: $pass passed, $fail failed"
if ($fail -gt 0) { exit 1 }
