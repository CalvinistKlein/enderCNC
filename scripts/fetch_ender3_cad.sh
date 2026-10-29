#!/usr/bin/env bash
set -euo pipefail

# Clones the official Creality Ender-3 CAD repository if not already present
REPO_TARGET="${1:-./ender3_cad_repo}"

if [ -d "$REPO_TARGET/Ender-3 Mechanical/STP" ]; then
  echo "[OK] Official Creality Ender-3 STEP repository already present at: $REPO_TARGET"
  exit 0
fi

echo "[INFO] Cloning official Creality Ender-3 CAD repository..."
git clone --depth 1 https://github.com/Creality3DPrinting/Ender-3.git "$REPO_TARGET"
echo "[OK] Cloned to $REPO_TARGET"
