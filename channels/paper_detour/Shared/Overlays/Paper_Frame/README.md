# Paper Frame — Paper Detour overlays

Transparent animated paper border for horizontal long films and vertical Shorts. This is a separate, post-scene overlay: it composites over the rendered video without changing story, scene motion, narration, or subtitle timing. Burned-in captions remain part of the source picture and stay below the frame layer.

## Source kit and masters

- Reproducible small source kit: [`source/`](source/): three layered PNG assets, `render_master.py`, the generation `README.md`, and the current `VALIDATION.md`. `source/SHA256SUMS.txt` records the copied files. The large ProRes masters are local assets outside the repository. Supply their local paths when rendering; the repo contains the generator and source kit, not the large MOVs.
- Current horizontal master: `masters/paper-border-16x9-16s-v02.mov`, **2560×1440**, 16:9.
- Current vertical master: `masters/paper-border-9x16-16s-v02.mov`, **1440×2560**, 9:16. Earlier 8-second masters remain preserved under their original names and are superseded.
- Both current masters: ProRes 4444, straight alpha, `yuva444p12le`, 30 fps, 480 frames / exactly 16 seconds. The center is fully transparent (`alpha=0`); the four outer edges remain opaque (`alpha=255`).
- Layer motion: top and bottom travel left to right; sides travel top to bottom. The second and third paper layers are narrowed across the edge without stretching their artwork along it. Layer periods are 16, 8, and 16/3 seconds (5⅓ s); together they repeat every 16 seconds. Frame 479 returns to frame 0 without a larger step than the ordinary adjacent-frame motion. See the current `source/VALIDATION.md` for measured results.

## Rebuild the transparent masters

From the repository root, with Python 3, NumPy, SciPy, Pillow, and an FFmpeg build with `prores_ks`:

```sh
python3 channels/paper_detour/Shared/Overlays/Paper_Frame/source/render_master.py \
  --width 2560 --height 1440 \
  --duration 16 \
  --output /absolute/local/path/paper-border-16x9-16s-v02.mov

python3 channels/paper_detour/Shared/Overlays/Paper_Frame/source/render_master.py \
  --width 1440 --height 2560 \
  --duration 16 \
  --output /absolute/local/path/paper-border-9x16-16s-v02.mov
```

The renderer uses the three PNGs in `source/assets/`. The default duration is 16 seconds (480 frames at 30 fps). Keep each layer period at 16, 8, and 16/3 seconds respectively; do not duplicate a 16-second endpoint frame. The vertical artwork is rotated from the source assets rather than stretched non-uniformly. Never overwrite the preserved 8-second masters.

## Add a frame to an existing MP4

Choose the master matching the video's aspect and exact canvas. Do not stretch the horizontal master into a portrait video or vice versa. The Paper long-film profile is 2560×1440 at 30 fps; the Short profile is 1440×2560 at 30 fps. `-stream_loop -1` repeats the 480-frame movie for the entire base-video duration. `alpha=straight` tells FFmpeg how to interpret the ProRes alpha. The source audio is mapped and stream-copied.

```sh
INPUT=/absolute/path/source.mp4
MASTER=/absolute/path/paper-border-16x9-16s-v02.mov
VIDEO_ONLY=/absolute/path/frame-video-only.mp4
OUTPUT=/absolute/path/review-with-paper-frame.mp4
FRAMES=6764

# Pass 1: composite and encode exactly the base video's frames without audio.
ffmpeg -hide_banner -n \
  -i "$INPUT" \
  -stream_loop -1 -i "$MASTER" \
  -filter_complex \
  "[0:v]fps=30,setpts=PTS-STARTPTS[base];[1:v]fps=30,setpts=PTS-STARTPTS,format=rgba[frame];[base][frame]overlay=0:0:alpha=straight:eof_action=pass:shortest=1:format=auto,format=yuv420p,setsar=1[v]" \
  -map "[v]" -an \
  -c:v h264_videotoolbox -b:v 20M -pix_fmt yuv420p \
  -r 30 -fps_mode cfr \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -frames:v "$FRAMES" -movflags +faststart "$VIDEO_ONLY"

# Pass 2: remux the original AAC to EOF; do not add -t, -shortest or a frame cap.
ffmpeg -hide_banner -n \
  -i "$VIDEO_ONLY" -i "$INPUT" \
  -map 0:v:0 -map 1:a:0 -map_metadata 1 -map_chapters 1 \
  -c copy -movflags +faststart "$OUTPUT"
```

For vertical output, set `MASTER` to `paper-border-9x16-16s-v02.mov`, dimensions to 1440×2560, and `FRAMES`/`DURATION` to that edit's actual exclusive end frame and frame count. Never overwrite the source MP4; use a new versioned output path. This process re-encodes the already-rendered H.264 picture to add the overlay, so it is a new lossy video generation. It leaves the AAC audio packets unchanged.

## Inspect and play an output

```sh
ffprobe -v error -show_streams -show_format -of json "$OUTPUT"
ffmpeg -v error -i "$OUTPUT" -map 0:v:0 -map 0:a:0 -f null -
open -a "QuickTime Player" "$OUTPUT"
```

The output should match the source edit's dimensions, aspect, 30 fps, frame count and duration; audio should retain its codec, profile, sample rate, channel count and packet data. Review frames at the start, middle, end, both sides of a 16-second loop boundary, and caption-bearing moments. Check that no caption is obscured or printed over the border.

## Alpha and final-file behavior

Transparency exists in the ProRes master, not in the delivered movie. FFmpeg composites the paper pixels over the source image and exports a regular H.264 `yuv420p` MP4. The final MP4 therefore contains no alpha channel; the border is baked into the picture. Do not remove the original MP4 or the transparent master when creating a review version.
