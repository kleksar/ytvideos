# Paper Detour one-prompt flow — episode 033 lessons

**Revalidation:** the latest section, “Updated-owner revalidation — 2026-11-02”, supersedes both the original implementation backlog and the earlier remaining H.264 recommendation. Export and scoped workspace cleanup are now documented. Do not implement them again or turn the proposed validation runs into mandatory production gates.

- Date, task and stage: 2026-11-02; workflow analysis after the Paper Detour 033 Time Stop private reupload; exploratory recommendation, not an approved change to channel rules.
- Coordinator / Google Chrome / URL: coordinator personally used the YT Видео project chat, https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae81252-f6d0-83ed-b7d3-05855f14fbeb
- Exact visible label immediately before the request: `Extra High`.
- Inputs: 033 `CURRENT_CONTEXT.md`, current README, offline QA receipt, reupload receipt, and this task's verified conversation context.
- Initial narrow prompt: asked for 8–12 transferable orchestration rules, observed failures with preventative gates, and 3–5 validation runs; explicitly limited conclusions to 033 and distinguished facts from hypotheses. It covered story/hook/storyboard, visual continuity and angle variety, semantic accents, localized audio repair, Palmier project/timeline identity, H.264 vs ProRes, grain removal and parallax, offline-only video QA, private reupload, and incomplete subjective/independent review.
- Response visibility: the initial request showed `Ответ готов` but no substantive text in the chat. One short retry was made in the still visibly marked `Extra High` mode. The retry returned a readable answer; the initial empty/status-only response is not treated as evidence.
- Retry prompt: `Ответ готов, но его содержательного текста не видно. Повтори коротко: 5 главных переносимых правил для Paper Detour one-prompt flow и 3 следующих тестовых прогона с pass-критериями. Только результат, без пояснения процесса.`

## Readable consultation result

The visible answer recommends five orchestration rules:

1. Complete story, opening/ending hook and accepted storyboard before production assets.
2. Treat a style reference as a visual continuity anchor, not a command to repeat compositions; define independent scene angles before batch generation.
3. Make on-screen phrases contribute a distinct visual meaning and align each cue to spoken triggers.
4. Repair audio defects locally, then regress the full audio track.
5. Keep Palmier project, source timeline, working timeline, export profile and upload as distinct, explicit identities; verify the selected H.264 file and YouTube privacy state.

The answer proposes gates for: shot diversity; story approval before storyboard/assets; semantic contribution of each accent; localized audio repair plus full-track regression; project/timeline identity; export profile before rendering; render lifecycle/dependency checks before cleanup; an upload manifest distinguishing current/superseded/uploaded versions; offline-only video QA; and separate human listening and independent review.

It proposes three validation runs:

1. **Story → hook → storyboard → visuals.** Input: one production prompt and an accepted S01 reference. Pass: story/hooks accepted before storyboard, all scenes independently composed, no near-identical neighboring angles, continuity preserved, no assets generated before storyboard acceptance.
2. **Narration → audio → accents.** Input: accepted storyboard, narration/TTS and phrase PNGs. Pass: narration unchanged, each cue has a distinct purpose and spoken trigger, no accidental verbatim duplication, defects repaired, and the whole track is listened to and independently reviewed.
3. **Palmier → H.264 → offline QA → YouTube.** Input: approved assets/audio/captions plus explicit project/timeline IDs. Pass: correct target; agreed H.264 export; full decode and evidenced frame/audio checks; exact file hash/version; upload ID/privacy read-back; old upload classified correctly; cleanup only after checking dependencies and preserving the new deliverable.

The consultant cautions that 033 cannot be called fully independently reviewed because subjective listening and independent QA were not completed. Upload success alone does not prove all QA checks.

## Coordinator review / limits

- Confirmed in 033: the user first accepted S01 as a style reference, then requested the remaining images be redone with varied angles while preserving hero/street continuity; they asked to discuss the story before storyboard and then strengthen the opening/ending loop; they specified that screen text should complement narration; a sound fault was reported near 0:45; Palmier project/timeline identity caused confusion; the user compared ProRes and H.264 and chose H.264; later they requested grain removal, motion/parallax and reupload; the final v02 was uploaded Private while the older private H.264 was retained; video-player playback is not required for QA.
- Qualification: the consultation table labels duplicated narration as an observed failure. The available record confirms the user set a complement-not-repeat rule, but it does not establish that every earlier accent draft duplicated narration. Keep this as a preventive gate, not a proven frequency claim.
- Qualification: mandatory human listening and independent QA are recommendations to evaluate against the canonical QA contract; this consultation does not itself make them new global channel rules.
- No skill or channel rule was changed by this consultation. Candidate owners to update only after review: `ytv-paper-production` for orchestration/gates; `ytv-scene-images` for angle-diversity handoff; `ytv-paper-captions` for meaning/trigger; `ytv-audio-delivery` and `ytv-video-qa` for repair/regression and offline QA; `ytv-palmier-edit`/`ytv-image-motion` for target identity/motion; `ytv-youtube-release` plus global `youtube-upload` for external state.
- Next dependent work: define the one-prompt contract and acceptance gates, then run the three validations above. Cross-episode lessons require corroboration in other Paper Detour episodes; this analysis intentionally does not generalize beyond 033.

## Current-documentation revalidation — 2026-11-02

User request: reread current rules/skills and revise recommendations to avoid duplicate or unnecessary work. Scope is Paper Detour workflow documentation, not a new production run.

Read root/bootstrap/registry/documentation map/catalog, Paper rules, production and its story-development/runbook/stages, storyboard, images/profile, captions/cue workflow/renderer, audio/export settings, video QA/profile/helper contract, lifecycle, motion and edit/release entrypoints. A local-target check of 28 relevant Markdown files found zero missing link targets. This is documentation evidence, not a new end-to-end runtime validation.

### Confirmed coverage

- Production already orchestrates one prompt through the requested local delivery; G stages are results/dependencies, not mandatory user approvals. Internal acceptance is allowed within scope; explicit user checkpoints persist.
- Story development already defines promise, causal beats, opening/ending pair, complete narration and factual/editorial passes. Storyboard owns angles and strictly 4–6-second scenes.
- Images already handles continuity, exact references, early motion-envelope framing, selective repair and resume. A first style sample is conditional on the user request; no extra mandatory multi-image approval pack is needed.
- Captions already supplies semantic-complement rules, cue/alignment checks and a universal PNG/preflight helper. Its actual-listening requirement for final caption acceptance remains applicable.
- Audio already requires explicit scope, reuse and targeted repair. Final-file QA belongs to video QA, which provides offline checks and a technical helper. Subjective and independent review are honest separate statuses; no new independent-review mandate follows from this audit.
- Lifecycle already supplies audit/plan and is called before heavy render and after QA/upload. It does not delete media. No new registry, cleanup helper or repeated scan for metadata-only changes is needed.
- Motion already reuses depth/video caches, resumes existing targets and checks source/target identity; release already handles authorized private upload and read-back.
- The old Paper thumbnail/title/description entrypoints are compatibility adapters to portable owners, not absent features requiring replacement skills.

### Remaining recommendation

The user's previously accepted H.264 preference is recorded in episode history. The inspected canonical export documents mention H.264 stream preservation and a QA example, but do not explicitly state a Paper-wide H.264 MP4 default with ProRes limited to a specific need/request. Recommend one scoped wording change at the existing export owner, with Paper/channel routing as appropriate; no new skill or media render is needed. No skill was changed in this audit.

The 033 artifacts can remain style/continuity/provenance references. Its 14 scenes across 50.067 seconds cannot all satisfy the newer minimum four-second scene policy. Current QA explicitly flags older nonconforming work while retaining past acceptance and forbidding silent re-editing; do not recreate 033 solely to validate the new workflow.

Prefer observing the next actually requested production run through the existing owners, recording concrete failures and repairing only their owner. The earlier three/four artificial validation runs are not a prerequisite or a backlog to execute automatically.

### Required personal consultation

Google Chrome, same project chat URL above. Visible mode immediately before sending: `Extra High`. Narrow task: revise the previous recommendations against the verified current coverage, identify what to drop and the minimal remaining work. The prompt supplied the actual production/no-extra-approvals, 4–6 s/storyboard, early motion-safe images, caption helper, QA/lifecycle, cache/resume and private-release contracts, and the missing explicit H.264 channel default.

The visible completed response returned seven points: drop production redesign; drop additional visual gates; drop duplicate caption workflow; retain the existing QA ownership/status contract; drop a new media registry/lifecycle procedure; retain current release/resume; recommend only an explicit H.264 default at the existing export owner. Coordinator qualification: documentation establishes that the workflow is specified and wired through owners, not that a fresh unattended end-to-end run has been demonstrated. Existing captions listening gates are not waived by the QA profile's separate subjective-listening status.

## Updated-owner revalidation — 2026-11-02

User requested another reread after documentation/skill updates. This section supersedes the earlier remaining recommendation and the earlier blanket statement that lifecycle cannot delete media. Scope: current Paper Detour documentation and routing; no production, migration, media cleanup, render or upload was performed.

### Verified current owners

- `ytv-video-export` now owns the pre-render technical contract. Its Paper profile explicitly sets MP4/H.264 AVC, Shorts 1080×1920, long films 2560×1440, 30/1 fps, progressive, 8-bit yuv420p SDR Rec.709. The ordinary native path is one Palmier H.264 export using Match Timeline after checking actual timeline settings. Profile selection precedes timeline/images/motion preparation. ProRes is a controlled, specifically authorized fallback/intermediate, not a mandatory master. The earlier H.264 recommendation is closed.
- A versioned export contract records the exact saved edit, settings and requested/required/preferred/engine-managed fields before rendering; QA uses that same contract. Palmier engine-managed encoder/audio controls must not be described as explicitly set. Exact fallback bitrate/CRF preferences are not blanket native-export pass thresholds. Actual properties still require verification.
- New Paper deliveries use AAC-LC, 48 kHz, Stereo 2.0, target 384 kbps. Centre mono narration on the stereo bus and preserve real stereo music/SFX; do not manufacture spatial effects. Existing ElevenLabs source helper remains `mp3_44100_128`; the new delivery profile does not authorize regenerating accepted narration or pretending PCM source support exists.
- New Paper scene-image generation requests maximum available quality with a 4K UHD target (2160×3840 portrait / 3840×2160 landscape). Requested target, available tool controls, measured native image dimensions and final video dimensions are separate facts. Smaller returned images do not automatically require regeneration when suitable for the accepted crop/motion.
- `ytv-media-lifecycle` now also owns workspace setup, run registration, promotion and scoped cleanup through `workspace.py`. `media_lifecycle.py` remains read-only audit/plan. New work separates selected sources, permanent generated assets, registered temporary runs, edit evidence and current deliveries. Existing imported dependencies are recorded without automatic relocation.
- Promotion verifies the QA receipt/file identity and updates `Deliverables/current.json`; promotion does not grant artistic acceptance or delete prior files. Cleanup defaults to dry-run and is limited to exact eligible registered temporary files in completed owned runs, after fresh dependency/pin/current/identity/evidence checks. It is not recursive source/project/cache cleanup. Failed or abandoned runs are not automatically disposable.
- Production now requires complete packaging state: exact title, description, selected cover, hashtag coverage and playlist plan; languages, API Tags, SRT, chapters and Related Video receive values or explicit applicability/request/verification statuses. Hashtag policy asks for relevant coverage on the first pass rather than an arbitrary three-tag limit; relevance, observed usage and demand evidence remain distinct.
- Existing accepted deliveries keep their previous acceptance/contract. None of these changes alone requires remaking 033, converting earlier accepted files, moving legacy media or running artificial validation episodes. Offline video QA remains applicable; no MP4 player was opened. Caption listening gates and separate subjective/independent statuses remain as specified by their owners.

### Check coverage and conclusion

Reread current root/bootstrap/registry/map/catalog, Paper rules and applicable owners/references, including the new export profile/contract/Palmier reference and updated lifecycle/workspace, audio, images, production and QA routing. A local Markdown target check covered 32 files across 11 relevant skill trees and found zero missing file targets; anchors and runtime behavior were not validated by that check.

No new skill, duplicate registry, mandatory extra approval pack, migration or render is justified by the earlier recommendations after this reread. Use the existing production entry point for the next actually requested episode, reuse accepted work and repair concrete execution failures at their canonical owner. Documentation coverage does not demonstrate a fresh unattended end-to-end production run.

### Required personal consultation

Coordinator personally used Google Chrome and the same project chat URL above. Exact visible mode immediately before both requests: `Extra High`. The narrow prompt supplied the verified new export, image, audio, lifecycle and owner-routing facts and asked which previous recommendations should be withdrawn. The first response displayed `Не удалось загрузить этот ответ.` One short retry asked for only three conclusions, without tools. The retry returned readable text:

1. Withdraw the recommendation to add an H.264 default; `ytv-video-export` already supplies it and limits ProRes to a controlled fallback.
2. Revise the earlier lifecycle recommendation: workspace registration/promotion/current pointer and scoped cleanup already exist; no new registry or cleanup workflow is needed.
3. Do not introduce further refactoring merely from this previous backlog; existing export/images/lifecycle/production/QA owners are connected.

Coordinator qualification: the consultant relied on the supplied local-document findings; this is not an independent repository audit or runtime validation. The conclusion is limited to withdrawing superseded proposals, not a claim that all possible production defects have been eliminated.
