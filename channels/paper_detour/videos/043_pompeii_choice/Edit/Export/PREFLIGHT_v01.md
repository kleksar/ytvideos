# Export preflight v01

- Timeline: `Edit/plan_v04.json`, SHA-256 `51b20bdd90fb2e272bbd0280f8f4a49697d2559a6978a0cbde318c13f341bf4e`; 1083 exclusive frames at 30 fps = 36.100 s. Eight scenes; each is 4–5.6 s.
- Input audio measured by FFprobe: 36.080000 s. Renderer requires coverage of 36.100 s with 40 ms tolerance; source is about 20 ms shorter, within tolerance. The final timeline ends at 36.100 s.
- Eight source images are 941×1672 RGB and upscale to 1440×2560; upscaling adds no detail.
- Subtitle map: `Edit/word_times_v04.json`, generated from v05 TTS and alignment source; 81 tokens. Automatic timing has not been checked against playback.
- Plan-only validation passed. Reviewed caption midpoint sheet: `Work/paper043-prod-v02/scratch/plancheck_v03/caption_composite_contact_v01.png`.
- Output: `/Users/diplomat/ytvideos/channels/paper_detour/videos/043_pompeii_choice/Work/paper043-prod-v02/previews/043_pompeii_choice_EN_review_v01.mp4`; destination was absent at preflight. Active owned run `paper043-prod-v02`; no other writer is recorded for the destination.
- Encoder availability: `h264_videotoolbox` checked; FFmpeg build: `ffmpeg version 8.1.2 Copyright (c) 2000-2026 the FFmpeg developers`. Exact submitted arguments will be saved as `render_command.json`.
- Audio contract: AAC-LC mono, 44,100 Hz, 192 kbit/s; source MP3 mono 44,100 Hz.
- No YouTube upload or metadata mutation before acceptance of the exact MP4 and packaging.
