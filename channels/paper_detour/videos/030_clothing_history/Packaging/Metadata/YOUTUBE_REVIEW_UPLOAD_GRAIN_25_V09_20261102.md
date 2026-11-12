# YouTube private review upload — grain 25% baseline v09

**Verified:** 2026-11-02  
**Purpose:** user comparison against the 50% grain test v08. This is a private review copy, not public release or approval as the public master.

## Palmier edit and local file

- Project `B1BA2D18`; source timeline v08 `479ECE26`; new isolated timeline v09 `B10FBA68`.
- Snapshot before the v09 change: `ABCA6C4B`.
- Grain clip `65FB718C`, mediaRef `9543F1E4`, full range `[0,5700)`: opacity restored from `0.50` to the v06 baseline `0.25`.
- Live timeline comparison: v09 matches accepted v06 after ignoring new IDs and the timeline name; compared with v08, the sole difference is Grain opacity (`0.50` → `0.25`). Accents (34), scenes (39), timing, and Mix remain the same.
- Palmier export job `F1489722-E5CC-482A-A5D8-157A9DA6A763`; final review file: `Edit/v09/PAPER_DETOUR_030_GRAIN_25_BASELINE_EN_v09.mp4`.
- SHA-256: `5a8f964fb8fc0bd29d98b4deca3792b61391507ee3e2262f852a63c11ca87868`; 255,856,197 bytes; 190.000 s, 1920×1080, 30 fps, H.264; AAC-LC stereo 48 kHz, 260,787 bit/s.
- QA: full audio/video decode passed. Final H.264 payload matches the native picture export; final AAC payload matches `Source/Audio/v06/accepted_v05_mix.m4a` bit-for-bit. Four actual frame pairs (frames 367, 1380, 2983, 4990) were inspected; v09 grain is visibly lower than v08, and text is legible in those samples. Full 1× playback and independent review were not performed.
- The first Palmier MP4 encoded a different AAC payload. It was not uploaded. The final review file stream-copies the accepted AAC mix into the native video without re-encoding either stream.

## YouTube readback

- Channel: Paper Detour (`UCMVfdfaNxV3ZkI3_J3Eejzw`)
- Video ID: `EUwJ5ES4UmY`
- Link: https://www.youtube.com/watch?v=EUwJ5ES4UmY
- Title: `Clothing Through the Ages — Grain 25% Baseline (Private Review v09)`
- Description: “Private review copy of the Paper Detour clothing-history film with the original full-frame grain restored to 25% opacity (the v06 baseline). Compared with private review v08 at 50%, only the grain strength differs; scenes, text, timing and the accepted audio are unchanged. Review export, not a public master.”
- API readback: `private`; upload status `processed`; processing status `succeeded`; duration `PT3M11S`; no failure or rejection reason. Metadata/audio language English (`en`); category ID `27`; tags none; made-for-kids false. Synthetic-media field was submitted as false; API readback did not return that field.
- No custom thumbnail, playlist entry, manual subtitle track, public release, or schedule was set.

Comparison copy v08 remains private at https://www.youtube.com/watch?v=2Ks3XDf4JwM. Both links are review copies and await the user's comparison.

Metadata: [`YOUTUBE_REVIEW_METADATA.json`](../../Edit/v09/QA/YOUTUBE_REVIEW_METADATA.json). QA: [`QA_REPORT.json`](../../Edit/v09/QA/QA_REPORT.json).
