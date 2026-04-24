# =============================================================================
# Windows one-click setup. Run from PowerShell inside the project folder:
#   > powershell -ExecutionPolicy Bypass -File .\setup.ps1
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Tickers_Financials setup ===" -ForegroundColor Cyan
Write-Host ""

# --- 0. Ensure ExecutionPolicy allows local scripts for CurrentUser ----------
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "Restricted" -or $policy -eq "AllSigned") {
    Write-Host "[..] ExecutionPolicy is '$policy' - setting CurrentUser to RemoteSigned so venv can activate later ..."
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "[OK] ExecutionPolicy = RemoteSigned (CurrentUser)"
} else {
    Write-Host "[OK] ExecutionPolicy (CurrentUser) = $policy"
}

# --- 1. Check Python ---------------------------------------------------------
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[X] Python not found in PATH." -ForegroundColor Red
    Write-Host "    Install from: https://www.python.org/downloads/ (tick 'Add python.exe to PATH')"
    exit 1
}

$pyver = & python --version
Write-Host "[OK] $pyver"
$currentPythonPath = (& python -c "import sys; print(sys.executable)").Trim()

# --- 2. Check existing venv - recreate if broken or foreign -----------------
$venvNeedsRecreate = $false
if (Test-Path "venv") {
    $cfgPath = "venv\pyvenv.cfg"
    if (-not (Test-Path $cfgPath)) {
        Write-Host "[!] ./venv exists but has no pyvenv.cfg - rebuilding."
        $venvNeedsRecreate = $true
    } else {
        $cfg = Get-Content $cfgPath
        $homeLine = $cfg | Where-Object { $_ -match "^\s*home\s*=" } | Select-Object -First 1
        if ($homeLine) {
            $homePath = ($homeLine -replace "^\s*home\s*=\s*", "").Trim()
            if (-not (Test-Path $homePath)) {
                Write-Host "[!] ./venv points to a non-existent Python at '$homePath' - rebuilding."
                $venvNeedsRecreate = $true
            }
        }
        if (-not $venvNeedsRecreate) {
            $venvPython = "venv\Scripts\python.exe"
            if (-not (Test-Path $venvPython)) {
                Write-Host "[!] ./venv\Scripts\python.exe missing - rebuilding."
                $venvNeedsRecreate = $true
            } else {
                try {
                    & $venvPython --version 2>&1 | Out-Null
                    if ($LASTEXITCODE -ne 0) { $venvNeedsRecreate = $true }
                } catch {
                    $venvNeedsRecreate = $true
                }
                if ($venvNeedsRecreate) {
                    Write-Host "[!] ./venv\Scripts\python.exe is not runnable - rebuilding."
                }
            }
        }
    }
}

if ($venvNeedsRecreate) {
    Write-Host "[..] Removing broken venv ..."
    Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
}

if (-not (Test-Path "venv")) {
    Write-Host "[..] Creating virtual environment in ./venv (using $currentPythonPath) ..."
    & python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[X] Failed to create venv." -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] venv created"
} else {
    Write-Host "[OK] venv is valid - reusing"
}

# --- 3. Use the venv python directly (avoids activation script issues) ------
$venvPython = (Resolve-Path "venv\Scripts\python.exe").Path
Write-Host "[OK] Using venv python: $venvPython"

# --- 4. Upgrade pip ---------------------------------------------------------
Write-Host "[..] Upgrading pip ..."
& $venvPython -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[X] pip upgrade failed." -ForegroundColor Red
    exit 1
}

# --- 5. Install dependencies ------------------------------------------------
Write-Host "[..] Installing dependencies from requirements.txt (this takes ~2 min) ..."
& $venvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[X] pip install failed." -ForegroundColor Red
    Write-Host "    Common cause: Python $pyver is too new and some packages" -ForegroundColor Yellow
    Write-Host "    (pyarrow, pandas, numpy) don't yet have wheels for it." -ForegroundColor Yellow
    Write-Host "    Install Python 3.12 or 3.13 from python.org and run:" -ForegroundColor Yellow
    Write-Host "      Remove-Item -Recurse -Force venv" -ForegroundColor Yellow
    Write-Host "      py -3.12 -m venv venv" -ForegroundColor Yellow
    Write-Host "      .\setup.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "=== Setup complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Activate the venv:               .\venv\Scripts\Activate.ps1"
Write-Host "  2. Run the friendly dashboard:      streamlit run app.py"
Write-Host "  3. Or run the strategy scripts:     python -m finviz_us.strategies_run"
Write-Host ""
Write-Host "Open in VSCode:                       code ."
Write-Host "(then accept the 'Install recommended extensions' prompt)"
Write-Host ""
