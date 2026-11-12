# Subtitle preparation attempt — EN v01

- Montage input: `Edit/Timeline/montage_manifest_en_v01.json`, original voice/text/alignment v01.
- Paper long-video style: single-line ChalkboardSE Bold; measured usable width is 1298 px at the final 2560×1440 canvas.
- Result: automatic sentence grouping cannot produce a syntax-safe one-line grouping for the long NTSB theory sentence; the full name “National Transportation Safety Board” also exceeds the measured width as one group. Subtitle preparation did not produce a renderer-ready contract or a render.
- A v02 English production wording candidate and Extra High receipt exist, but the TTS call returned HTTP 401 and created no matching voice/alignment. It is not used by v01 audio.
- The sidecar SRT build covers the v01 transcript; timing mapping and playback remain UNVERIFIED.
- Next dependency: obtain an available authorized synthesis request for the v02 wording (or another exact, width-safe production adaptation), then regenerate voice alignment, full mix, word map, scene timings and subtitles before render.
