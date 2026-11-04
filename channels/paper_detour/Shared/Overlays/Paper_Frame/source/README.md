# Paper Frame source kit — current 16-second masters

The canonical generator is `render_master.py`; its default duration is 16 seconds. Use the new versioned ProRes masters below. They are local assets outside this source-only clone; supply a user-selected absolute output path when regenerating or using them. The older 8-second masters are preserved under their original filenames and are superseded for current work.

## Current masters

- Horizontal: `masters/paper-border-16x9-16s-v02.mov` — 2560×1440, 16:9.
- Vertical: `masters/paper-border-9x16-16s-v02.mov` — 1440×2560, 9:16.
- Both: 30 fps, 480 frames, exactly 16 seconds, ProRes 4444, straight alpha.
- The center is transparent; each outer edge is continuously opaque. The final frame is time 15.9667 seconds. Do not add a duplicate endpoint at 16 seconds.

The top and bottom layers move left to right; the side layers move top to bottom. Their periods are 16, 8, and 16/3 seconds (5⅓ seconds); together they repeat every 16 seconds. The second and third layer artwork is narrowed across the edge, not stretched along it. Layer order, shapes, amplitudes, direction and phase are fixed in the generator.

The vertical artwork is rotated from the same source PNGs rather than non-uniformly stretched. The center remains transparent; do not add a background to the master.

## Regenerate without overwriting prior masters

Python 3 with NumPy, SciPy and Pillow is required, along with FFmpeg built with `prores_ks`. Run these commands from the repository root using an environment that provides those dependencies:

```sh
python channels/paper_detour/Shared/Overlays/Paper_Frame/source/render_master.py \
  --width 2560 --height 1440 --duration 16 \
  --output /absolute/path/masters/paper-border-16x9-16s-v02.mov

python channels/paper_detour/Shared/Overlays/Paper_Frame/source/render_master.py \
  --width 1440 --height 2560 --duration 16 \
  --output /absolute/path/masters/paper-border-9x16-16s-v02.mov
```

Choose new versioned output names for later revisions. The renderer overwrites an existing output through FFmpeg, so confirm the target does not exist before running it.

## Composite into a video

Use the master matching the base video's exact aspect and dimensions. Loop it with `-stream_loop -1`, interpret its alpha as straight, and composite it over the already rendered picture. For audio-preserving output, render the video-only overlay first, then remux the original AAC stream separately through EOF without `-t`, `-shortest`, or a frame cap on the remux. See the project-level `Paper_Frame/README.md` for the full command and QA procedure.

The transparent alpha belongs to the ProRes master. The delivered H.264 `yuv420p` MP4 has no alpha channel; the paper edge is baked into the picture.
