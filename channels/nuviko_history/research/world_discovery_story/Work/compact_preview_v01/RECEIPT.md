# 1080p compact viewing copy

Source: `Edit/Previews/world_discovery_PREVIEW_v01.mp4`, SHA-256 c5097a4bd7d670848adfecd0d27b7a4140152079a817198eb591b498b72e5cd0, 1,246,584,450 bytes. Retained unchanged.

Copy: `Edit/Previews/world_discovery_PREVIEW_1080p_v01.mp4`, SHA-256 6043a4049d6abfdda67e30e0ca32b2a3feb56302abe041f6fc0e93c6e7af621c, 167,339,293 bytes. ffprobe reports container 493.771995 s, video 493.766667 s, 1920x1080 H.264 yuv420p; AAC stereo 44.1 kHz, 493.771995 s. The approximately 5 ms longer container/audio duration is from the AAC encode. `moov` precedes `mdat` (faststart). Both streams decoded completely using ffmpeg, exit 0 and empty `decode_errors.log`; a 292 s actual video frame was inspected for map/caption readability. No player playback or listening performed.

Encoding: `ffmpeg -hide_banner -loglevel warning -nostdin -n -i Edit/Previews/world_discovery_PREVIEW_v01.mp4 -map 0:v:0 -map 0:a:0 -vf scale=1920:1080:flags=lanczos -c:v libx264 -preset veryfast -b:v 2600k -maxrate 3500k -bufsize 7000k -pix_fmt yuv420p -fps_mode passthrough -c:a aac -b:a 160k -movflags +faststart Edit/Previews/world_discovery_PREVIEW_1080p_v01.mp4`.

This derivative inherits the source's unfinished visual/editorial and audio checks and its known frame gap around 05:47. It is a preview, not a final or upload-ready master. See `Work/preview_v01/QA_RECEIPT.md`.
