# CASE_002 — English language version 1_en

Date: 28 October 2026. This version was made inside the same Palmier project as episode 1's Russian cut. The pre-existing Russian timeline was retained; a named release copy `1_ru` was created, and the English version is on separate timeline `1_en`.

## Approved text, voice, and alignment

- User-provided English script: `reference/en/voice_en_original.txt`.
- Added ElevenLabs voice, registered media `A2A5174E`, duration 104.124 s. Timeline clip `29C33DF3` runs from frame 0 to 3123 at native speed.
- Palmier word timings/transcription: `reference/en/voice_en_word_timestamps.json` (350 tokens, BCP-47 result en-ZA). The approved script contains 350 tokens. Timings were aligned one-to-one; ASR did not replace wording, contractions, or spelling. The narration includes a small ASR/text spelling discrepancy such as `he'd` vs. `he`; approved text remains the caption source.
- Sentence punctuation is not displayed. Internal apostrophes (English contractions and possessives) and the orthographic hyphen in `EX-GIRLFRIEND'S` are retained because deleting them changes spelling/meaning.

## Timeline state

| Layer | Track | Media/clip | Range |
| --- | --- | --- | --- |
| Word-highlight captions | V2, `B25EA2A2` | `11831846` / `BABBE184` | [0, 3123) |
| Rendered inserts | V1, `FA6C18A4` | 23 consecutive clips | [0, 3123) |
| English voice | A1, `0AEC5067` | `A2A5174E` / `29C33DF3` | [0, 3123) |

Canvas: 1080×1920, 30 fps, 3123 frames (104.100 s). The MP3 is 104.124 s; the timeline rounds to frame units. The final caption ends with the last spoken word at 103.740 s, not at the end of the MP3.

The first 18 insert clips are the unchanged Russian montage. Five more clips from the existing numbered rendered-insert library extend the picture under the longer English voice: assets `6`, `8`, `19`, `28`, `5` in that order, with the last shot trimmed to 82 frames. These are craft/food/art close-ups in the established non-literal, process-led insert style. B-roll and captions meet the voice end with no timeline gap; insert audio is disabled, so the new voice is not doubled.

## Caption plan and style

- `reference/en/CAPTION_PLAN_1_EN_v4.txt`: preserved prior 106-cue plan for version history.
- `reference/en/CAPTION_PLAN_1_EN.txt`: current manually reviewed plan, 147 cues / 350 words. No cue exceeds three words.
- `reference/en/voice_word_captions_1_en_v5.srt`: word-timed captions; all 350 words appear once and in approved order; cue starts are contiguous; every cue is at least 260 ms.
- `reference/en/render_captions_1_en_v5.py`: deterministic renderer and validation rules.
- `reference/en/caption_sizes_1_en_v5.tsv`: confirms one fixed 92 px base size for every cue; the longest measured active-state line is 1007.7 px.
- `reference/en/voice_word_highlight_overlay_1_en_v5_prores4444.mov`: final transparent overlay imported into Palmier.

Measured caption style: Helvetica Neue Condensed Black; fixed 92 px base size on every word and every cue; 1.5 px letter tracking; 32.5 px word gap; centered at y = 0.40H. White inactive words stay fixed. Only the spoken word is warm yellow (#FFD54F) and smoothly scales up by 5%; 5 px dark outline. Every cue is one line and contains at most three words. The single fixed size replaces per-line font shrinking; the slightly larger 92 px setting maintains legibility while fitting all cues inside a 1020 px active-state width cap.

## Verification and limits

Palmier timeline state was re-read after replacing the caption layer. Composite frames were inspected at the opening and corrected mid-story grouping; fixed-size white words remained even, only the active word was highlighted and smoothly enlarged, and the caption remains a single row at y = 0.40H. The last sampled end frame has no caption after narration. The transparent overlay fully decodes at 1080×1920, 30 fps, 3123 frames. The revised export is recorded below.

## Delivery

On 28 October 2026, revised `1_en` was exported through Palmier as H.264 at Match Timeline resolution to `/Users/diplomat/Desktop/story_1_en_2026-10-28_caption-v2.mp4`; the file was later moved to `/Users/diplomat/ytvideos/channels/nuviko_stories/videos/001_brother_ex_best_friend/Deliverables/story_1_en_2026-10-28_caption-v2.mp4`. Export job `187636B7-3BF8-4C37-A893-83268BD4656D` completed. The file reports 1080×1920, 30 fps, H.264 video, AAC audio, 104.100 s, and 137,523,709 bytes. Full video decode completed without errors; a rendered frame at 44.2 s confirms the three-word maximum, uniform base size, and single active-word highlight. Full real-time playback/listen-through was not performed.

The earlier desktop export `/Users/diplomat/Desktop/story_1_en_2026-10-28_final.mp4` was deleted on 28 October 2026 after verification of the revised export to save space.

No full real-time audio listening or complete audio/video playback was performed, so this note does not claim subjective sync or intelligibility was listened through. The MP4 file was decoded and sampled as described above.

## YouTube check — 29 October 2026

Read-only API verification found [IwNYgAneRqA](https://www.youtube.com/watch?v=IwNYgAneRqA), “My Brother Proposed to His Ex’s Best Friend. Then I Saw the Texts.”, on Nuviko Videos `UC4nNJWr_PDL3QCZ76KGHF1g`. The video is `public`, processing is `succeeded`, its audio language is English, and it appears in Stories `PLXYIl-8efRUE`. Its English automatic caption track is `serving`; no separate manual track was returned. No duplicate upload was made. The historical MP4 path noted above was absent from `Deliverables/` when checked; its removal or relocation was not investigated.
