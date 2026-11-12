# Paper Detour — SAM 2.1 Scene 01 pilot (macOS arm64)

Everything runs locally. Only software and weights are downloaded. Image never uploaded.

## Setup

Requires a native arm64 Python 3.10, 3.11 (recommended), or 3.12 already installed, plus `git`, `curl` and Xcode CLT. No global Python packages are modified.

```sh
# From the extracted bundle directory:
chmod +x setup_macos.sh
./setup_macos.sh
```

The installation target defaults to `~/paper-detour-sam2-local`; override using `PD_SAM2_HOME`. If Python 3.11 isn't available, use `PD_PYTHON=/path/to/native/python3.12 ./setup_macos.sh`. This command installs torch 2.5.1, torchvision 0.20.1, and SAM 2 with the CUDA extension disabled.

## Pilot

```sh
ROOT="$HOME/paper-detour-sam2-local"
# Edit prompts after checking coordinate_grid.png; examples are not verified masks.
"$ROOT/.venv/bin/python" sam2_scene01.py --image /path/to/master_v2_approved.png \
  --out "$ROOT/out/scene01" --grid-only
PYTORCH_ENABLE_MPS_FALLBACK=1 "$ROOT/.venv/bin/python" sam2_scene01.py \
  --image /path/to/master_v2_approved.png \
  --prompts prompts_scene01.example.json \
  --checkpoint "$ROOT/models/sam2.1_hiera_tiny.pt" \
  --out "$ROOT/out/scene01" --device mps
# Fallback, if MPS inference fails: repeat with --device cpu.
```

### Outputs
- `coordinate_grid.png` pixel grid for picking points and boxes
- `mask_{object}.png`: individual binary masks at original resolution
- `mask_MG.png`, `mask_FG.png`: binary union masks
- `MG.png`, `FG.png`: original RGB, alpha 0/255 at original coordinates
- `holes_exact.png`, `holes_inpaint_dilated.png`: areas requiring BG inpainting
- `preview_masks.png`: MG red, FG cyan, for prompt refinement

**Warning:** Coordinates in example JSON are approximate only; edit them after previewing. Binary masks aren't refined mattes. No BG inpainting or full composition verification is performed.

### Sources
- https://github.com/facebookresearch/sam2
- https://github.com/facebookresearch/sam2/blob/main/INSTALL.md
- https://github.com/facebookresearch/sam2/blob/main/sam2/sam2_image_predictor.py
- https://github.com/facebookresearch/sam2/blob/main/demo/README.md
- https://pytorch.org/get-started/previous-versions/
