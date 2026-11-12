# TWL_E001 · exact local review v01

**File:** [TWL_E001_review_v01.mp4](../../Deliverables/TWL_E001_review_v01.mp4)  
**SHA-256:** `9244a1806cebb5e3c6cfb93b3fe2f0b7f6f0567b892355c0cd2901a13e6ddd32`  
**State:** technical and sampled picture checks passed; awaiting owner review. No YouTube changes.

| Check | Finding and evidence |
|---|---|
| Experiment | 3 tests passed. R1 A 58 / B 48; R2 A 74 / B 88. For model states, completion at a sampled instant removes that shopper from the visible queue. [Events](../../experiment/events.json) |
| Image gate | Original K00/K01/K02 show 0/0 → 2/0 → 2/5 in one recognizable store. K00 edits changed framing slightly; the chosen K00 is a static composite of two matching empty lane halves. Checked identities, baskets, cart handles, queue order and visible counts in all event states. [Early sheet](early-image-gate.jpg), [exact lineage](../image_manifest_v01.json) |
| Format and integrity | 40.967 s, 1080×1920, 1229 progressive CFR frames at 30 fps, H.264 High/yuv420p limited BT.709, AAC LC stereo 24 kHz, MP4 with moov before mdat. Complete decode of video and audio without reported errors. [Probe](ffprobe_v01.json), [frame timestamps and atoms](packet-checks_v01.json) |
| Visual edit | Checked 39 first/mid/last frames covering all 13 intervals at 270×480, including both sides of each cut, both winner holds and the matched ending/opening composition. Confirmed overlays show A/B in the correct order, no black borders, both queues visible, and no observed caption overlap with the artwork or result values. [Frame map](inspected_frame_map_v01.json) · [sheet 1](scenes_v01_1.jpg) · [sheet 2](scenes_v01_2.jpg) · [sheet 3](scenes_v01_3.jpg) · [sheet 4](scenes_v01_4.jpg). Real Shorts UI and full continuous handset playback unverified. |
| Speech and cue timing | Offline Whisper on exact MP4 recovered all narration and numeric values, with normal digit and punctuation normalization. WhisperX forced alignment matched 100/100 words; mean absolute start difference from synthesis timing 0.081 s, maximum 0.168 s. Sampled picture confirms visual holds. Automated comparisons estimate timing; they do not verify sound subjectively. [ASR](asr_v01.json), [alignment](forced_alignment_v01.json) |
| Separate English SRT | 16 cues. Structure, literal full transcript, non-overlap, measured duration bounds and local readability limits passed. [SRT](../../Deliverables/TWL_E001_review_v01.en.srt) · [machine report](srt_v01.json). |
| Audio signal | Integrated −19.4 LUFS, true peak −2.7 dBFS, LRA 2.7 LU. English speech, original music and original effects present in the retained mix. [Mix sources and rights](../../Source/Audio/v01/mix-evidence.md). |
| Listening and loop | Sentence wrap was synthesized as one phrase and split at the hook; beginning and end show the same composition. Actual listening and subjective seamlessness are UNVERIFIED because the available model does not support audio input. Independent review has not been performed. |

Render: approximately 46 seconds from run initialization to written MP4 on this machine. All TTS and encoding ran locally; no paid API was called. Subscription cost and hands-on time were not separately metered.
