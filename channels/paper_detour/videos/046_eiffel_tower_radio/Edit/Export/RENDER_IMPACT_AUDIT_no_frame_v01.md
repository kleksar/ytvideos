# Paper 046 no-frame render impact audit

File: `Work/eiffel-remake-frame-20261105/previews/Paper_Detour_046_Eiffel_Tower_Radio_EN_no_frame_v01.mp4`; SHA-256 `70b5cd353a9394ba4239952195d108ef7e5db94fdf9f1e53f7ad4d6c9d667193`.

The renderer encoded a file but exited with `Stale delivery input: .../automation/ffmpeg_montage/montage.py`; no delivery receipt was produced. The frozen engine is `Work/eiffel-remake-frame-20261105/scratch/no-frame-render-v01/render_provenance/engine_0_montage.py`. A direct diff against the current engine shows removal of Paper Frame validation and frame-specific decoding, and addition of a final 300-frame end-screen exception for long Paper videos. The submitted plan is a Short with no overlays and no end-screen scene, so those changed branches do not alter its generated FFmpeg composition. This comparison does not itself establish export QA, create a delivery receipt or verify speech sync.

The encoded file reports 1440×2560 H.264, AAC and 114.266667 seconds via ffprobe. Settings preflight passed before encoding. Exact FFmpeg command and frozen provenance are preserved in the run directory.

The complete final MP4 was decoded with `ffmpeg -v error -i ... -f null -` and exited 0; this verifies decoding only. Audible synchronization and visual semantic review were not established by decoding.
