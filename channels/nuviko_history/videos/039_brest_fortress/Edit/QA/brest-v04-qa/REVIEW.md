# Brest Fortress v04 — exact MP4 visual revision review

- **Media:** `/Users/diplomat/ytvideos/channels/nuviko_history/videos/039_brest_fortress/Work/render_en_v04/previews/039_brest_fortress_en_review_v04.mp4`
- **SHA-256:** `8946329fd7bfe34094938795e35db26e35c44bbc3d690e66e5df7f5e3b4736ef`
- **Edit:** `Edit/Production/v04/render_plan_v04.json`, frozen alongside `EXPORT_CONTRACT_v04.json`; edit, dependency and media hashes rechecked against the delivery sidecar. The renderer uses inline camera values in the render plan. The supporting `camera_plan_v04.json` has historical source-map/hash columns and does not supersede the inline render inputs.
- **Scope verdict:** requested picture corrections **PASS**; exact render technical verification **PASS**. Full internal AV/release profile **UNVERIFIED** (listening and complete cue placement checks outstanding). Review by the production coordinator; no independent reviewer.

| Check | Status | Evidence and scope |
|---|---|---|
| Stream metadata and saved settings | PASS | H.264, 2560×1440, 30 fps, progressive Rec.709, 18,370 frames; AAC-LC stereo at 44100 Hz. Duration 612.333333 s. Checked the exact file and 74 records in the delivery receipt plus frozen command and engine. |
| Full decode | PASS | VideoToolbox H.264 decode traversed the full video through the last selected frame (18,369), and AAC was decoded to null; FFmpeg error log empty. See `technical.json` for the exact argv and frame indices. |
| Scene pictures and cut samples | PASS | Inspected 361 distinct final-file samples, including start, middle and end of all 117 shots, both sides of 116 cuts, the revised shots and defect timestamps. The small cut sheets were used for continuity; 360 px midpoints and 480 px revised samples for framing; the four named timestamps were also inspected at 800 px. No full real-time playback or independent review claimed. |
| Scene lengths | PASS | All 117 frame intervals match v03 exactly and run 120–180 frames (4–6 seconds). |
| Former graphics | PASS | Zero extra layers in the exact edit, frozen command and delivery contract. At 07:04 and 08:23–08:34, date/statistics appear in the English speech caption band only. At 09:12 and 10:02 the report's heading and date read as part of the document; at 09:32 and 10:07 the Russian lettering belongs to the brick surface. English subtitle placement does not obstruct those clues. |
| Caption grouping | PASS | All 432 groups and associated timing, audio, transcript and word map are identical to v03. Existing full semantic review `Research/SUBTITLE_REVIEW_v02.md` applies to that identical input. |
| Caption placement and word highlight | UNVERIFIED | Caption band, legibility and yellow highlight visible in inspected samples. Full cue-by-cue visual placement and colour state coverage were not performed. |
| Audio stream identity | PASS | AAC packet payload and timing hashes both equal v03 throughout. AAC payload `SHA256=a5c143177e5daf0379ede95adb16063bdba4ed76312b810f309154090e7b6e39`, timing `7e0ff98f66b265df33ac5271bd393b6ab9952f50404305d5277f4a228f1c702a`. Prior signal measurement applies to identical payload. |
| Audible synchronization and subjective listening | UNVERIFIED | Available audio interface did not provide audible playback to this reviewer. Local ASR on 4 diagnostic regions matched 150 words; in three clips median word onset differed from provider alignment by roughly 0.40 s. This suggests possible lag in inherited highlighting and is not an audible timing verdict. ASR and packet evidence are separate. |
| Separate SRT | UNVERIFIED | Existing English SRT remains alongside the episode. Spoken recording and cue basis did not change; no new dedicated SRT audit or YouTube check in this visual revision. |

Key evidence: `exact-user-timestamps.jpg`, `removed-editorial-layers.jpg`, `scenes-01.jpg` through `scenes-05.jpg`, `revised-*.jpg`, `cuts-*.jpg`, `asr-spot-timing.json`, `technical.json`. The first, slower software extraction was stopped; the successful hardware decode/extraction has its own log. The v03 acceptance is superseded by `../CHANGES_REQUESTED_v03.md`; this v04 has no release authorization. No YouTube action.

The required browser consultation could not open in Chrome (timeout before prompt submission). The changes apply the user's exact decision to render scene text within images and keep the existing narration and timing.
