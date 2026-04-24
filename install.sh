#!/usr/bin/env sh

#!/usr/bin/env bash

# Function to install packages based on the distro
install_pkg() {
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm "$1"
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y "$1"
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y "$1"
    else
        echo "❌ Error: Unsupported package manager. Install $1 manually."
        exit 1
    fi
}

echo "󰚰 Detecting environment..."

# 1. Ensure Python and Pip are present
if ! command -v python3 &> /dev/null; then
    install_pkg "python3"
fi

# 2. Ensure pipx is present (safest way to install pyinstaller)
if ! command -v pipx &> /dev/null; then
    if [[ -f /usr/bin/pacman ]]; then
        install_pkg "python-pipx"
    else
        install_pkg "pipx"
    fi
    pipx ensurepath
fi

# 3. Install PyInstaller via pipx
echo "󰄲 Setting up build tools..."
pipx install pyinstaller --force

# 4. Build the binary
echo "󰄲 Compiling Fetcher..."
~/.local/bin/pyinstaller --onefile fetcher.py

# 5. Create local bin and symlink
mkdir -p ~/.local/bin
ln -sf "$(pwd)/dist/fetcher" ~/.local/bin/fetcher

echo "󰄬 Setup complete. Restart your terminal or run: source ~/.zshrc"
echo "🚀 Type 'fetcher' to launch."
