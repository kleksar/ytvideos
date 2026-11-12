# Paper Detour 007 — final independent review v06

**File:** Deliverables/007_joshua_jessica_en_short_1080x1920_30fps_paper_foley_aac256_v06_20261101.mp4  
**SHA-256:** d05ed452d7b6950592c4847e4a5b87acd288fdadf00e4e33f31d536a18c2474ad8  
**Reviewer:** independent read-only AV reviewer  
**Result:** PASS in the checked scope

## Verified

- H.264 High, 1080×1920, 30 fps, 1344 frames / 44.8 s; AAC-LC stereo, 44.1 kHz, 256,022 bit/s measured by ffprobe.
- FFmpeg full decode passed. Measured −22.0 LUFS, LRA 2.4 LU, −4.1 dBTP.
- P12 55% starts appearing at f1030, is fully readable at f1036, and is visibly behind the laptop bezel during entrance/exit. It stays off the laptop screen. Clearance to the lamp is narrow but visibly non-overlapping.
- P12 title is hidden by f1163; P13 begins at f1164 with no title.
- Sampled f0, f1254 and f1343 show the same room/laptop composition. Blurred grayscale RMSE between f0 and f1343 is 0.00492. This supports a match in composition, not continuous motion.
- No obvious visual encoding artifact was seen in the checked frames.
- Audio-to-source correlation at sampled windows 1.0, 22.0, 34.6 and 44.55 seconds peaked at 0 ms. The P12 sample had 0.975 correlation, consistent with the added effect.
- AAC stream duration is 44.790 s; video/container duration is 44.800 s, a 10 ms tail difference.

## Not verified

Full-length normal-speed playback, continuous motion at the loop seam, and human listening were unavailable. Perceived narration quality, pronunciation, SFX attack/balance, and subjective loop sound remain unverified.
