# Technical review for private staging

Exact media SHA-256: 5764ff61260e9d672a4fc89696d982954f0cae406d1a779e6bc3b75ea88c8faa; edit montage_v02. On 2026-11-05 ffmpeg -v error -i MEDIA -f null - decoded all audio and video and exited 0. ffprobe: H.264 High, yuv420p, 1440×2560, 30 fps, BT.709, AAC LC mono 44.1 kHz, duration 43.633333 s, consistent with contract. Previously examined MP4 contact frames and source images; full playback, audible sync and captions remain UNVERIFIED. Staging only; no claim of complete playback.
