# Paper Detour 041 — Dune origin, FFmpeg storyboard v01

Status: active remake plan for the accepted English Short. Narration v04, voice-only master, scene order, and the three accepted accent phrases are retained. Timings are conformed to the FFmpeg 4–6 second composition rule. No story rewrite or fact-check.

Canvas: 1440×2560, 30 fps, 1587 frames (52.9 s). Direct cuts. Each still is a whole image with subtle horizontal pan and zoom only; no depth/parallax, segmentation, or restored backgrounds. S12 uses byte-identical S01.

| Scene | Timeline | Composition and narration coverage | Whole-image motion | Accent |
|---|---:|---|---|---|
| S01 | 0–120f · 0–4.0s | Road blocked by dunes; first sentence and start of Forest Service response. | left_to_right + in | No cue |
| S02 | 120–240f · 4.0–8.0s | Hands plant beachgrass; response and investigation setup. | right_to_left + out | GRASS · 172–224f |
| S03 | 240–360f · 8.0–12.0s | Notebook, dune cross-section, visible roots; Herbert investigates. | left_to_right + in | No cue |
| S04 | 360–495f · 12.0–16.5s | Layered dunes echo ocean waves. | right_to_left + out | No cue |
| S05 | 495–630f · 16.5–21.0s | Desk and desert model; the slow-wave beat moves into study. | left_to_right + in | No cue |
| S06 | 630–765f · 21.0–25.5s | Notes curl into a planet; study and notes grow beyond an article. | right_to_left + out | No cue |
| S07 | 765–945f · 25.5–31.5s | Full desert planet and miniature settlements; imagined environment. | left_to_right + in | No cue |
| S08 | 945–1107f · 31.5–36.9s | Planet among anonymous rejected envelopes; continues through name reveal. | right_to_left + out | ARRAKIS · 1078–1131f; crosses cut |
| S09 | 1107–1227f · 36.9–40.9s | Lit manuscript and symbolic press; publishers, then Chilton. | left_to_right + in | ARRAKIS continues to 1131f |
| S10 | 1227–1347f · 40.9–44.9s | Paper engine and repair manuals; Chilton context. | right_to_left + out | No cue |
| S11 | 1347–1467f · 44.9–48.9s | Amber paper desert planet in deep blue; title reveal. | left_to_right + in | DUNE · 1450–1491f; crosses cut |
| S12 | 1467–1587f · 48.9–52.9s | Exact S01 still returns; Earth problem loops into opening. | right_to_left + out | DUNE continues to 1491f |

Word timing source: `Source/Voice/en_v04_lawrence/voice_en.alignment.json`; exact 133-token map in `Source/Subtitles/word_times_en_v01.json`. The 54 reviewed transcript groups remain exact and are explicitly supplied to FFmpeg (maximum three words). The first subtitle state begins at frame 0, remains present through pauses and ends at frame 1587; only the currently spoken word is yellow.

Accents use the Paper cream-paper/ochre cut-letter treatment, optical center `[0.5, 0.16]`, equal visible height, and one top-center anchor. Cue PNG positions come from the caption helper. ARRAKIS and DUNE cross a cut; both scene compositions were included in the static preflight sheet.
