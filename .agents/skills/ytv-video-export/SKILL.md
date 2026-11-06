---
name: ytv-video-export
description: Prepare a versioned pre-render technical contract, map it to the actual editor capabilities and deliver an authorized export to video QA. Use for render settings, export preparation or final video encoding with a channel profile.
---

# Video export

Read current project/channel instructions and the current saved edit. In ytvideos start with [bootstrap](../../../.agent/CHANNEL_BOOTSTRAP.md). Paper and Nuviko use the [shared delivery profile](references/delivery.md) and the active channel audio/voice settings; other channels provide their own contract. This skill owns the **pre-render technical contract**, not editing decisions or final acceptance.

## Prepare before rendering

1. Identify the exact saved project/timeline revision and dependency handoff: scene/cue timing, motion, complete accepted mix and output purpose/language. Read actual timeline settings through the editor. Do not infer the target from UI focus or an old output. Reuse episode state; no second registry.
2. Load the profile early, before creating the timeline, images or motion derivatives. Record exact width/height/aspect, rational FPS and output colour. FPS means frames per second; total frame count is the final edit's exclusive end frame, not another FPS setting. Derive duration as `frame_count / fps`, checking it against the saved edit. Count deliberate tails; do not round narration duration to invent a timeline length.
3. Assemble one versioned [export contract](references/export-contract.md) in the episode's existing `Edit/` handoff. Include video/container/quality settings and the [audio owner's](../ytv-audio-delivery/SKILL.md) exact complete-mix contract. Distinguish required delivery properties, quality preferences, requested controls and engine-managed values. Unsupported controls get an explicit status/reason, never invented arguments or a claimed setting.
4. Map the contract to FFmpeg: record the exact input manifests, scene/cue timing, filters, encoder, dimensions, FPS and output path. Changing canvas or FPS affects fit, motion and timing; update the plan before rendering. For Paper/Nuviko link the shared renderer subtitle contract and exact final-audio/speed evidence in this existing export handoff. Run subtitle preparation through that same renderer; carry actual review evidence via `subtitles.review`. The generated `VIDEO.mp4.delivery.json` is the machine binding for this export, not a second approval process.
5. Pass this exact passport to the shared renderer with `--export-contract`. Use `--check-settings` to compare the actual generated FFmpeg argv before encoding scenes. Resolve mismatches and unsupported required controls before the full render; preserve requested values instead of rewriting them to fit the implementation. Settings PASS is not encoded-output or AV QA. The [renderer contract](../../../automation/ffmpeg_montage/README.md#сверка-настроек-и-происхождение-рендера) owns machine checks and frozen provenance.
6. Confirm output path/purpose, no accidental overwrite, current inputs, no unresolved required field and no conflicting writer/export. Run the scoped [media lifecycle](../ytv-media-lifecycle/SKILL.md) pre-render audit. `READY_TO_RENDER` means a complete executable plan with disclosed automatic controls, not proof of the encoded result. An unresolved required target/input blocks the dependent render; engine-managed settings alone do not.

## Execute and hand off

The shared full-production scope authorizes the review export before user acceptance at stage 16. Execute other exports within their actual authorization and audio scope. Preparing this contract does not authorize new sound, timeline changes beyond the assignment or publication. Use explicit IDs and a new output path; record exact command/tool arguments, job ID, editor version when available, selected resolution/codec and completion warnings. A queued/started job is not a completed file. On uncertain mutation state inspect the job/file before retrying.

After successful encoding, hand the exact MP4 and frozen contract to [video QA](../ytv-video-qa/references/export-review.md) for internal verification before the user sees it for final approval. Scoped test exports and audits follow their stated scope.

A subsequent renderer update alone does not invalidate an accepted MP4. Compare its frozen passport, actual saved commands and file; changes to the accepted edit or sources still invalidate dependent results. Missing historical provenance calls for a scoped saved-command audit under the renderer contract, not an automatic rerender.

If output differs, preserve the original expectation and record the discrepancy. Required violations need correction or an explicit scoped revised contract, never changing expected values merely to match the file. Preferred quality differences need an evidenced suitability decision, not automatic re-encoding to reach a number. Route sound repair to audio delivery and edit repair to the FFmpeg montage plan. Use a higher-quality intermediate only when needed; re-encoding damaged AAC/H.264 cannot recover lost quality. Finish with exact file/hash/contract/edit/QA links and remaining limitations.
