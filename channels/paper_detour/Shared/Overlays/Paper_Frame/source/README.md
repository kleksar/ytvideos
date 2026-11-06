# Paper Frame v03 source

`render_master_v03.py` and the three `assets/layer*.png` reproduce the user-approved thin frame. Along the straight sides each v02 layer uses a normal-width factor of 0.67 × 0.67, with a smooth corner blend; the three periods remain 16, 8 and 16/3 seconds. This is not a global scaling of the canvas.

Requires Python 3, NumPy, SciPy, Pillow and FFmpeg with `prores_ks`. From this directory, generate to new, non-existing paths:

```sh
python3 render_master_v03.py --width 2560 --height 1440 --duration 16 --output /absolute/path/paper-border-16x9-16s-v03.mov
python3 render_master_v03.py --width 1440 --height 2560 --duration 16 --output /absolute/path/paper-border-9x16-16s-v03.mov
```

The generator is configured for 30 fps, 480 frames and straight alpha, with no duplicate endpoint. Verify exact output against [validation](VALIDATION.md) before use. The previous v02 and v01 masters remain intact for existing projects.
