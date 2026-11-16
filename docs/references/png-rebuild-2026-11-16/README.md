# PNG rebuild evidence, 2026-11-16

Historical, film-specific recipe and measured QA, not a new generic production default or permission to publish. Current requirements remain in [delivery](../../standards/delivery.md). Source dependencies and music/SFX rights remain in the [preservation audit](../two-film-preservation-audit.md).

## Inputs and build

The full visual rebuild used **232 original PNG scenes**: 110 Mind Reading and 122 Everyone Wants You. The corrected Mind scene 081 overrides its baseline. All 232 input PNGs decoded successfully. Timings, motion plan/storyboard and original scene texts were retained; no new narration or image generation was performed.

Each scene was rendered into a lossless H.264 CRF 0 MKV intermediate. The final composition was encoded once to H.264 CRF 16, yuv420p, 1920×1080 at 30 fps, faststart. Mind used preset `slow`; Everyone used `fast`. Old final MP4s supplied **audio only**, not visuals. Approved AAC was stream-copied, avoiding another audio encode; English SRTs were unchanged. Never use a chat preview or preview-of-preview as a master input.

Both supplied Flow inputs remain **1280×720, 24 fps, 119 frames / 4.958333 s**. Lanczos upscale and fps conversion do not make them native 1080p. Mind is a new take; Everyone is byte-identical to the previous intro. Their source hashes are in the preservation audit. Narration timing remains in the copied audio; no extra silent five-second lead-in was inserted.

## Exact composition and timestamp recovery

Mind: 150 intro frames followed by the original scene timeline from frame 60. Everyone: 171 intro frames, original timeline from frame 81, plus the 31-frame Alone hold at original frame 437. The first Everyone trial lost 31 frames because cloned hold frames had duplicate timestamps. It failed frame-count QA and was not delivered or uploaded. The successful correction resets timestamps **after** padding:

```text
trim=start_frame=81:end_frame=437,tpad=stop_mode=clone:stop=31,setpts=N/(30*TB)
```

That section must contain 387 frames / 12.9 s. The corrected final contains 6198 frames, not 6167. This is a visual timestamp fix, not another edit to the approved Alone audio pause. The final command is preserved in [everyone-command.json](everyone-command.json).

[build.py](build.py) is an archival reproduction script, not a hardened recovery runner. Its existing-file shortcut does not validate completeness. Before reusing any segment after interruption, validate decoded frame count against `audio/timings.json`; quarantine/rebuild incomplete segments rather than trusting file existence. Do not run it from this repository reference directory: materialize verified source bundles in an artifact workspace, place the script under `upload-ready-rebuild/`, and preserve its expected sibling input layout. `${ARTIFACT_ROOT}` in saved command/probe records replaces the original machine-local prefix and must be resolved locally. The repository contains no media or complete source bundle.

## Exact results and scope of QA

| Master | Frames / duration | Bytes | SHA-256 |
|---|---|---|---|
| MIND_READING_UPLOAD_READY_1080p30.mp4 | 6252 / 208.4 s | 89958636 | `0fc85aa624ad4c14f238cf0475f8d61611fd4d714d4f9055fa6a04b342cce58a` |
| EVERYONE_WANTS_YOU_UPLOAD_READY_1080p30.mp4 | 6198 / 206.6 s | 131213857 | `efa13225e5284bb276ea28b7e3719bc08b15ef25f4531f3af30979e445599a06` |

[QA.json](QA.json) stores stream probes and exact AAC elementary-stream hashes. Both files fully decoded without errors; AAC payload matched Mind V2 / Everyone V9 respectively. Audio is AAC-LC, 48 kHz stereo. Contact-sheet review covered intro joins, corrected Mind 081 and Everyone Alone hold. These checks are not a listening test or proof of native 1080p intro detail. [BUILD_MANIFEST.json](BUILD_MANIFEST.json) and [SOURCE_RECEIPTS.json](SOURCE_RECEIPTS.json) record parameters and provenance of the small archived evidence files. The machine-path redaction means repository evidence bytes differ from original local evidence, as recorded in receipts.

Upload is a separate step. At this checkpoint Chrome UI upload was blocked before metadata/progress/video ID; the two attempted Mind uploads were canceled, and Everyone was not uploaded. No new publication URL or successful metadata/subtitle/thumbnail application was verified. Intended visibility is **Private**, not Unlisted. Do not infer deletion of historical videos from Studio errors. Final render completion is not upload completion.
