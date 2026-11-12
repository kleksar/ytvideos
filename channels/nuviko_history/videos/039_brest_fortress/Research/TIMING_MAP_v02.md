# Alignment-backed storyboard timing map v02

Derived from the exact character alignment for `Source/Voice/v02/voice_en.mp3` (measured duration 612.320 s). The timing map is `Edit/Preproduction/shot_map_v02.csv`, paired with `Storyboard/storyboard_v02.md`.

- 116 shot intervals; first start 0.000 s, final end 612.320 s.
- Machine checks: intervals are positive, ordered, contiguous, and cover the full MP3 duration. Shortest hold 3.040 s; longest hold 8.400 s.
- Starts are phrase-anchored to retained character alignment. This is an automated timing map, not a human listening review or final subtitle review.
- The provider's final character endpoint lies beyond the MP3 container duration; the last shot is clamped to 612.320 s.
- At 30 fps, 612.320 s is not an integer frame boundary. The export contract must set the final integer frame count and report the resulting duration without claiming exact equality with the MP3 duration.
- No generated image is assumed ready solely from its shot-map entry. Current manifest has 11 assets for 116 shot IDs; missing expected image files: 105.

- Selected images: 24 of 116 are present, creator-reviewed and hash-matched to the current map; 92 shots lack a ready exact source.
- Three older source PNGs (01.01, 01.05, 04.03) remain draft until their image-specific review is complete. Rejected replacements for 06.03 and 06.04 are retained in the manifest; the map points to accepted v02 replacements.
