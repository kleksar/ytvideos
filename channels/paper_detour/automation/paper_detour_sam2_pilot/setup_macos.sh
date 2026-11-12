#!/usr/bin/env bash
set -euo pipefail

# Everything installed under one user-owned directory, no global pip changes.
ROOT="${PD_SAM2_HOME:-$HOME/paper-detour-sam2-local}"
PYTHON="${PD_PYTHON:-python3.11}"
SAM2_COMMIT="3a7889d905e38ca043c9b5a571ec1635bab678ac"
mkdir -p "$ROOT/cache/pip" "$ROOT/cache/xdg" "$ROOT/cache/torch" "$ROOT/models"
export PIP_CACHE_DIR="$ROOT/cache/pip"
export XDG_CACHE_HOME="$ROOT/cache/xdg"
export TORCH_HOME="$ROOT/cache/torch"

"$PYTHON" - <<'PY'
import platform, sys
print("Interpreter:", sys.version, platform.machine())
assert sys.version_info[:2] in {(3, 10), (3, 11), (3, 12)}, "Use Python 3.10/3.11/3.12"
assert platform.machine() == "arm64", "Use native arm64 Python, not Rosetta x86_64"
PY

if [ ! -f "$ROOT/.venv/bin/python" ]; then
    "$PYTHON" -m venv "$ROOT/.venv"
fi
VENV_PY="$ROOT/.venv/bin/python"
"$VENV_PY" -m pip install --upgrade pip 'setuptools>=61' wheel
"$VENV_PY" -m pip install torch==2.5.1 torchvision==0.20.1 numpy==1.26.4 'pillow>=9.4.0'

if [ ! -d "$ROOT/sam2/.git" ]; then
    git clone https://github.com/facebookresearch/sam2.git "$ROOT/sam2"
fi
git -C "$ROOT/sam2" fetch --depth 1 origin "$SAM2_COMMIT"
git -C "$ROOT/sam2" checkout --detach "$SAM2_COMMIT"
test "$(git -C "$ROOT/sam2" rev-parse HEAD)" = "$SAM2_COMMIT"
test -f "$ROOT/sam2/sam2/configs/sam2.1/sam2.1_hiera_t.yaml"
SAM2_BUILD_CUDA=0 "$VENV_PY" -m pip install --no-build-isolation -e "$ROOT/sam2"

CHECKPOINT="$ROOT/models/sam2.1_hiera_tiny.pt"
if [ ! -s "$CHECKPOINT" ]; then
    curl --fail --location --retry 3 \
      --output "$CHECKPOINT" \
      https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_tiny.pt
fi

git -C "$ROOT/sam2" rev-parse HEAD > "$ROOT/sam2.commit"
shasum -a 256 "$CHECKPOINT" > "$ROOT/checkpoint.sha256"
"$VENV_PY" -m pip freeze > "$ROOT/requirements.lock.txt"
"$VENV_PY" - <<'PY'
import torch, torchvision
print('torch:', torch.__version__, 'torchvision:', torchvision.__version__)
print('mps available:', torch.backends.mps.is_available())
PY
printf '\nInstalled in: %s\n' "$ROOT"
printf 'Use --device cpu if MPS fails. Installation alone does not validate inference.\n'
