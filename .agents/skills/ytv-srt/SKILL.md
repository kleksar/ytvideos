---
name: ytv-srt
description: Create, revise or validate separate SRT subtitle files against the actual spoken transcript, media and edit timing; distinguish applicability, text coverage, machine checks and playback sync. Does not create accent PNGs or chapter timestamps.
---

# SRT subtitle sidecars

Use current project instructions and the target channel profile. For Paper Detour read the [Paper profile](references/paper-detour.md). Another channel supplies its own language, subtitle policy, transcript scope and readability preferences; the core does not impose Paper typography, a language or subtitles on every Short.

## Scope before creation

Determine whether a sidecar is required by the request/profile (`REQUIRED`) or not part of the agreed package (`NOT_REQUESTED`, with reason). Missing required inputs are `BLOCKED` readiness, not proof a subtitle is unnecessary. An explicitly requested source-time draft may still be prepared and labeled as such. Keep separate SRT, burned-in subtitles and description chapters distinct. Creating a skill or subtitle file does not authorize burn-in, new audio/ASR service uploads or external subtitle publication.

Read the exact current transcript, audio identity/duration, alignment/timed words and their source identity, selected edit version and final-media identity. Reuse a valid existing subtitle. A filename, script estimate or old SRT from the same episode does not establish current synchronization. When there are multiple voices, translated text or non-speech cues, follow the agreed scope; do not present narration-only subtitles as a complete accessibility transcript.

## Prepare text and real timing

Use the transcript of what is actually retained in the final edit, preserving spelling, punctuation, order and all spoken content in scope. If the recording differs from the accepted script, reconcile the transcript without silently rewriting either recording or approved story. Use existing alignment adapters; the [helper contract](references/helper-contract.md) accepts provider-neutral timed cues and does not implement another ASR/character aligner.

Segment on meaningful clauses, syntax and real pauses. Avoid separating names, quantities/units and tightly connected phrases. Preserve the exact text when wrapping lines. Review short orphan cues, long pauses and reading density; use channel/language-specific configurable warnings rather than a universal YouTube rule. Automatic grouping is a draft until these decisions are checked.

Conform source times to the actual edit before calling them final times. For a retained source interval with constant speed `r`, `final_time = final_start + (source_time - source_in) / r`; apply each interval separately, once. A continuous unretimed track still needs confirmed start offset and file identity. Cuts, gaps, rearrangements and repeated clips require corresponding retained transcript and cue order. Split at edit boundaries; a cut inside a spoken word or ambiguous mapping requires resolution, not guessing. Do not spread text across removed speech or carry old artificial pauses forward. Record the map and its evidence with the edit version. Without verified mapping the result is a source-time draft, even if it fits the video duration.

For the shared renderer, serialize a final-time word map as an object with `audio_sha256` of the exact final mix, `transcript_sha256` of the UTF-8 transcript after trimming outer whitespace, and `words` (`text,start,end`). Keep source identity and conform evidence when deriving this from an earlier recording. The hash binding records identity, not audible verification. The renderer applies no additional speed or offset.

Provider punctuation/whitespace timings can exceed the media duration. Inspect which characters/words overrun and check the actual media; never silently clamp, compress or globally shift all cues to hide a mismatch. Ending the last cue on the actual final word rather than a provider's trailing punctuation timing must be documented. Millisecond rounding is deterministic; it must not produce zero-length or overlapping cues.

### Validate alignment against the retained recording

Before importing a full subtitle track or doing an expensive render, verify the timing source against the exact retained recording. Matching transcript text, an audio hash, equal durations and zero stream start times do not prove that word boundaries match speech. TTS-provided character alignment is a draft until this check; a second ASR/forced-alignment result is also an estimate, not audible acceptance.

Compare several identifiable spoken word onsets in the beginning, middle and end, plus each edit/speed change and any reported problem. Record the words, source/edit times, intended subtitle frames and observed differences with the audio/hash/edit identity. Use listening with waveform/frame evidence where available; if listening is unavailable, disclose that limitation rather than mark audible sync PASS. This early sample diagnoses the mapping and does not replace the channel's final-track coverage.

Inspect complete word intervals around pauses, not just whether a proposed onset falls inside silence: a word can begin over the preceding spoken word and span a pause. Compare the exact transcript and recording with an independently derived alignment and speech/quiet evidence; flag disagreements, words spanning quiet, unmatched tokens and uncertain speech onsets. Do not move every cue to the nearest silence boundary or treat an amplitude threshold as proof of which word starts there. `scripts/reconcile_pauses.py` can produce a provisional diagnostic from provider and Whisper word maps, but retains provider timings; its flags and either model's output require verification and do not constitute forced alignment or audible acceptance. When useful, forced alignment of the exact transcript against the retained recording supplies another estimate; reconcile differences rather than assuming that agreement or a model score proves correctness. Save the recording and map identities and retain open checks.

For English or another language supported by WhisperX, `uv run --no-project --python 3.11 --with whisperx python .agents/skills/ytv-srt/scripts/forced_alignment.py --audio RECORDING --text TRANSCRIPT --language en --output NEW_MAP.json --raw-output NEW_RAW.json` creates a hash-bound draft against the full recording. The first run may download the language model. The helper rejects missing word times, mismatched tokenization and unordered timings; it does not perform the audible or edit-conform checks above. It accepts only distinct new output paths and never changes the recording. Long recordings may need an explicitly designed segmentation workflow before use.

A consistent difference can justify one documented offset; a growing difference requires checking speed/conform and timebase; irregular differences require local word corrections or renewed alignment against the exact recording. Reconcile names, numbers, split/joined words and missing/repeated speech before importing another machine result. Do not transplant an offset from a previous episode or use one global shift to hide drift. Preserve the recording unless audio changes were separately requested.

Follow the channel's export-review policy: Paper/Nuviko perform preparation and short implementation samples before full rendering, then hand the MP4 to the user immediately. Repeat affected speech-to-frame checks on exported media when an audit is requested; do not claim an unperformed post-render check. Check phrase entries, word changes, pauses and the ending, not only phrase midpoints. Verify audio preservation and subtitle sync separately; known unresolved lag is a defect even when decode, hashes and frame intervals pass. Save a reusable accepted timing map with its recording and edit identity; invalidate only affected timings after source/edit changes.

## Serialize and check

Run [srt_tool.py](scripts/srt_tool.py) by the [helper contract](references/helper-contract.md). It renders UTF-8 SRT from prepared cues or validates an existing SRT, checks every block, full literal text coverage (whitespace/NFC normalization only), ordering, overlap and measured duration bounds. Configurable readability limits produce diagnostics without rewriting the text. Fix the cause and repeat the affected checks; do not trim spoken content to pass a threshold.

Check actual player rendering and play the final media with this exact subtitle on 1×: first/last words, cue starts/ends, pauses, fast sections, all edit/speed changes and line breaks. Cover the whole subtitle track before claiming full playback QA. Machine validation cannot hear speech, establish naturalness, verify translation or prove conform. Self-review is not independent review.

## Deliver or resume

Save the requested current SRT beside its final media under the existing delivery contract; source-time or validation-only samples belong in work/research folders. Record language, exact transcript/audio/alignment/cue/map/final-media hashes, edit version, applicability and open dependencies in the existing episode state or linked receipt. Keep structural checks, text coverage, timing-map evidence, readability and actual playback statuses separate. The helper always leaves mapping/playback `UNVERIFIED`; a reviewer adds observed evidence separately, never changes that machine report into a fictional playback.

Changes to source audio/text invalidate corresponding alignment/coverage/segmentation; cuts, speed, offset, placement or retained speech change the conform; a replacement export requires confirming identity and repeating affected rendering/playback checks. Preserve valid unaffected work. New upload versions need their own subtitle association. Hand the exact verified file/hash and intended language/track scope to the release owner only for an authorized external action; local readiness is not saved YouTube state.
