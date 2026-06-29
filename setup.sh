#!/usr/bin/env bash
set -e

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Regular layout preview:"
echo
python3 "$SRC_DIR/regular/main.py"
echo
read -rp "Use this layout? [y/N] " use_regular

if [[ "$use_regular" =~ ^[Yy]$ ]]; then
    target="$SRC_DIR/regular"
else
    echo
    echo "==> Nitch layout preview:"
    echo
    python3 "$SRC_DIR/nitch/main.py"
    echo
    read -rp "Use the nitch layout instead? [y/N] " use_nitch
    if [[ "$use_nitch" =~ ^[Yy]$ ]]; then
        target="$SRC_DIR/nitch"
    else
        echo "Neither layout picked. Aborting, nothing installed."
        exit 1
    fi
fi

pipx install -e "$target"
echo "Done. Run 'fetcher'."
