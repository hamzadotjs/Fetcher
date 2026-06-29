#!/usr/bin/env bash
set -e

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Regular layout preview:"
echo
python3 "$SRC_DIR/main.py"
echo
read -rp "Use this layout? [y/N] " use_regular

if [[ "$use_regular" =~ ^[Yy]$ ]]; then
    target="$SRC_DIR/regular"
else
    echo
    echo "==> Nitch layout preview:"
    echo
    python3 "$SRC_DIR/nitch.py"
    echo
    read -rp "Use the nitch layout instead? [y/N] " use_nitch
    if [[ "$use_nitch" =~ ^[Yy]$ ]]; then
        target="$SRC_DIR/nitch"
    else
        echo "Neither layout picked. Aborting, nothing installed."
        exit 1
    fi
fi
if [[ "$use_regular" =~ ^[Yy]$ ]]; then
    sed -i 's/^fetcher = .*/fetcher = "main:main"/' "$SRC_DIR/pyproject.toml"
else
    sed -i 's/^fetcher = .*/fetcher = "nitch:main"/' "$SRC_DIR/pyproject.toml"
fi

pipx install -e "$SRC_DIR"
echo "Done. Run 'fetcher'."
