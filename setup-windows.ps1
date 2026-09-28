[CmdletBinding()]
param(
    [switch]$SkipSync
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VirtualEnvironment = Join-Path $ProjectRoot ".venv"
$PyvenvConfig = Join-Path $VirtualEnvironment "pyvenv.cfg"
$WindowsPython = Join-Path $VirtualEnvironment "Scripts\python.exe"

Set-Location $ProjectRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv is not installed or is not on PATH. Install uv for Windows, reopen PowerShell, and run this script again."
}

if (Test-Path -LiteralPath $VirtualEnvironment) {
    $config = if (Test-Path -LiteralPath $PyvenvConfig) {
        Get-Content -LiteralPath $PyvenvConfig -Raw
    } else {
        ""
    }
    $isUnixEnvironment = $config -match '(?m)^home\s*=\s*/' -or $config -match 'linux'
    $isIncompleteWindowsEnvironment = -not (Test-Path -LiteralPath $PyvenvConfig) -or -not (Test-Path -LiteralPath $WindowsPython)

    if ($isUnixEnvironment -or $isIncompleteWindowsEnvironment) {
        Write-Host "Removing an incompatible or incomplete .venv..." -ForegroundColor Yellow

        # A WSL-created environment can contain a lib64 -> lib directory link.
        # Windows removes directory links with rmdir rather than Remove-Item.
        $lib64 = Join-Path $VirtualEnvironment "lib64"
        if (Test-Path -LiteralPath $lib64) {
            & cmd.exe /d /c "rmdir `"$lib64`""
            if ($LASTEXITCODE -ne 0 -and (Test-Path -LiteralPath $lib64)) {
                throw "Could not remove $lib64. Close terminals and editors using the environment, then run this script again."
            }
        }

        Remove-Item -LiteralPath $VirtualEnvironment -Recurse -Force
    }
}

if (-not $SkipSync) {
    Write-Host "Creating the Windows Python 3.12 environment..." -ForegroundColor Cyan
    & uv sync --locked --python 3.12
    if ($LASTEXITCODE -ne 0) {
        throw "uv sync failed with exit code $LASTEXITCODE."
    }
}

if (-not (Test-Path -LiteralPath $WindowsPython)) {
    throw "The Windows virtual environment was not created at $WindowsPython."
}

$envFile = Join-Path $ProjectRoot ".env"
$envExample = Join-Path $ProjectRoot ".env.example"
if (-not (Test-Path -LiteralPath $envFile) -and (Test-Path -LiteralPath $envExample)) {
    Copy-Item -LiteralPath $envExample -Destination $envFile
    Write-Host "Created .env from .env.example." -ForegroundColor Green
}

Write-Host "Running the offline Windows verification..." -ForegroundColor Cyan
& uv run python tools/verify_windows.py
if ($LASTEXITCODE -ne 0) {
    throw "Windows verification failed with exit code $LASTEXITCODE."
}

Write-Host ""
Write-Host "Windows environment is ready." -ForegroundColor Green
Write-Host "Use 'uv run <command>' from the repository root; activation is not required."
Write-Host "For the live model lessons, start Ollama and pull the models listed in workshop/README.md."