# Scoped MP4 subtitle review — v05

- Media: `/Users/diplomat/ytvideos/channels/paper_detour/videos/045_edmund_fitzgerald_last_voyage/Work/render_visual_v05/previews/edmund_fitzgerald_full_film_en_visual_v05.mp4`
- SHA-256: `6d6154c731fb253ed00aebf13574d9b07197a1ff5c77eef35074411bb2ed9996`
- Reviewer: coordinator (self-review), 2026-11-05
- Scope: frame-accurate subtitle placement; targeted investigation of synchronization warnings. This is not independent review or whole-film audio listening.

## Technical extraction

The exact MP4 passed the helper's stream metadata, complete audio/video decode and frame extraction checks. Technical helper verdict remains `UNVERIFIED`, since extracted frames still require human inspection. It extracted 545 planned frames covering all 45 scene intervals and 152 subtitle groups. Exact machine report: `report.json`; contact sheets: `scene_sheet_1.jpg`–`scene_sheet_3.jpg` and `cue_sheet_1.jpg`–`cue_sheet_4.jpg`.

## Actual visual inspection

I visually inspected all three 15-scene contact sheets (one midpoint per scene) and all four 40-group contact sheets (one actual midpoint frame per subtitle group, final sheet covers the remaining 32). I also compared group midpoints with scene midpoints. Across these 197 actual frames, captions remain visible within the image and their baseline stays consistent. I found no caption clipped off-frame and no systematic overlap with faces or action objects. Subtitle text over the ore-hold cutaway (groups 5–6) is low in frame and does not obscure the central cargo or people; the cutaway labels remain partly visible. This visual sample passes placement and legibility at the displayed contact-sheet scale. It does not inspect every frame or device crop.

## Synchronization finding

The retained provider word map and independent WhisperX estimate disagree by more than 0.15 s for 53 of 581 word onsets. This is an investigation flag, not proof that the provider timing is wrong: the second alignment is itself automatic and can place a word differently. The diagnostic also marks an ASR span overlapping detected quiet for “We” at 208.806–209.226 s, which further shows why silence detection alone cannot resolve the word. I could not listen to the audio in this review environment. Therefore `audible_sync` remains `UNVERIFIED`; no timings were changed based only on automatic estimates. User approval of the MP4 is preserved separately and is not recorded as an audio-listening claim.

## Result

`visual_placement=PASS` for the coverage above. `audible_sync=UNVERIFIED`. No media, subtitles or edit was changed; thus the existing MP4 hash and its user approval remain current. The mandatory full audible sync check is still open for release readiness.
