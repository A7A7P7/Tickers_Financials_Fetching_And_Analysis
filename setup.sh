#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Unix (macOS / Linux / WSL) one-click setup.
#   $ chmod +x setup.sh && ./setup.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

echo
echo "=== Tickers_Financials setup ==="
echo

# ─── 1. Check Python ────────────────────────────────────────────────────────
if ! command -v python3 >/dev/null 2>&1; then
    echo "[X] python3 not found in PATH."
    echo "    Install Python 3.11+ from: https://www.python.org/downloads/"
    exit 1
fi

PYVER=$(python3 --version)
echo "[OK] $PYVER"

# ─── 2. Check existing venv — recreate if broken or foreign ────────────────
venv_needs_recreate=false
if [ -d "venv" ]; then
    if [ ! -f "venv/pyvenv.cfg" ]; then
        echo "[!] ./venv exists but has no pyvenv.cfg — rebuilding."
        venv_needs_recreate=true
    else
        # Grab the 'home' path from pyvenv.cfg
        home_path=$(grep -E "^\s*home\s*=" venv/pyvenv.cfg | head -n 1 | sed -E 's/^\s*home\s*=\s*//;s/\s*$//')
        if [ -n "$home_path" ] && [ ! -d "$home_path" ]; then
            echo "[!] ./venv points to a non-existent Python at '$home_path' — rebuilding."
            venv_needs_recreate=true
        fi
        if ! venv_needs_recreate && [ ! -x "venv/bin/python" ]; then
            echo "[!] ./venv/bin/python missing or not executable — rebuilding."
            venv_needs_recreate=true
        fi
        if ! $venv_needs_recreate; then
            if ! venv/bin/python --version >/dev/null 2>&1; then
                echo "[!] ./venv/bin/python is not runnable — rebuilding."
                venv_needs_recreate=true
            fi
        fi
    fi
fi

if $venv_needs_recreate; then
    echo "[..] Removing broken venv ..."
    rm -rf venv
fi

if [ ! -d "venv" ]; then
    echo "[..] Creating virtual environment in ./venv ..."
    python3 -m venv venv
    echo "[OK] venv created"
else
    echo "[OK] venv is valid — reusing"
fi

VENV_PY="$(pwd)/venv/bin/python"
echo "[OK] Using venv python: $VENV_PY"

# ─── 3. Upgrade pip ─────────────────────────────────────────────────────────
echo "[..] Upgrading pip ..."
"$VENV_PY" -m pip install --upgrade pip --quiet

# ─── 4. Install dependencies ────────────────────────────────────────────────
echo "[..] Installing dependencies from requirements.txt (this takes ~2 min) ..."
if ! "$VENV_PY" -m pip install -r requirements.txt; then
    echo
    echo "[X] pip install failed."
    echo "    Common cause: Python $PYVER is too new and some packages"
    echo "    (pyarrow, pandas, numpy) don't yet have wheels for it."
    echo "    Install Python 3.12 or 3.13 and re-run:"
    echo "      rm -rf venv"
    echo "      python3.12 -m venv venv"
    echo "      ./setup.sh"
    exit 1
fi

echo
echo "=== Setup complete ==="
echo
echo "Next steps:"
echo "  1. Activate the venv:               source venv/bin/activate"
echo "  2. Run the friendly dashboard:      streamlit run app.py"
echo "  3. Or run the strategy scripts:     python -m finviz_us.strategies_run"
echo
echo "Open in VSCode:                       code ."
echo "(then accept the 'Install recommended extensions' prompt)"
echo
