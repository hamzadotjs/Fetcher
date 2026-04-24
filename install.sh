#!/usr/bin/env bash

set -euo pipefail

# --- helpers ---
log()  { echo -e "\033[1;34m[INFO]\033[0m $*"; }
ok()   { echo -e "\033[1;32m[OK]\033[0m   $*"; }
err()  { echo -e "\033[1;31m[ERR]\033[0m  $*" >&2; exit 1; }

# detect package manager once
detect_pm() {
    if command -v pacman &> /dev/null; then
        PM="pacman"
    elif command -v apt &> /dev/null; then
        PM="apt"
    elif command -v dnf &> /dev/null; then
        PM="dnf"
    else
        err "Unsupported package manager. Install dependencies manually."
    fi
}

install_pkg() {
    case "$PM" in
        pacman) sudo pacman -S --noconfirm --needed "$@" ;;
        apt)    sudo apt update -y && sudo apt install -y "$@" ;;
        dnf)    sudo dnf install -y "$@" ;;
    esac
}

require_cmd() {
    command -v "$1" &> /dev/null
}

# --- start ---
log "Detecting environment..."
detect_pm

# ensure we're in repo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

[ -f "fetcher.py" ] || err "fetcher.py not found in $SCRIPT_DIR"

# 1. Python
if ! require_cmd python3; then
    log "Installing Python..."
    install_pkg python3
else
    ok "Python already installed"
fi

# 2. pipx
if ! require_cmd pipx; then
    log "Installing pipx..."
    if [ "$PM" = "pacman" ]; then
        install_pkg python-pipx
    else
        install_pkg pipx
    fi
    pipx ensurepath
    ok "pipx installed (restart shell later if needed)"
else
    ok "pipx already installed"
fi

# 3. build deps (best effort)
if [ "$PM" = "apt" ]; then
    log "Installing build dependencies..."
    install_pkg python3-venv build-essential || true
fi

# 4. pyinstaller
log "Setting up PyInstaller..."
pipx install pyinstaller --force

PYINSTALLER="$HOME/.local/bin/pyinstaller"
[ -x "$PYINSTALLER" ] || err "PyInstaller not found after install"

# 5. build
log "Compiling Fetcher..."
"$PYINSTALLER" --onefile fetcher.py

# 6. install binary
log "Installing binary..."
mkdir -p "$HOME/.local/bin"
ln -sf "$SCRIPT_DIR/dist/fetcher" "$HOME/.local/bin/fetcher"

ok "Installation complete!"
echo
echo "Run: source ~/.bashrc (or ~/.zshrc)"
echo "Then: fetcher 🚀"
