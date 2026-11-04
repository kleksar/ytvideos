---
name: ytv-scene-images
description: Create, revise, reuse or verify scene images from an accepted storyboard and channel visual profile; preserve continuity, exact selected files and review evidence. Covers scene assets; thumbnails and narration subtitles have separate owners.
---

# Scene images

Use the current project instructions, episode state and channel profile. For Paper Detour explicitly read the [Paper profile](references/paper-detour.md) before preparing prompts, generating, editing or reviewing scenes, both for a direct image request and a full-production handoff. References are not loaded automatically. For Nuviko read the [Nuviko visual profile](../../../channels/nuviko_history/brand/VISUAL_PROFILE.md). Both channels follow the [same production flow](../ytv-video-production/SKILL.md); other channels supply their own visual contract. The core does not prescribe a medium, aspect ratio, palette, scene count or approval of every image. Read the applicable image-generation skill for tool mechanics; do not copy its API procedure here.

## Establish the actual selection

Read the accepted storyboard revision, current scene selection and acceptance evidence before choosing files. Record the image's narrative job, depiction status (evidence/reconstruction/metaphor), composition, recurring identities, object state and relevant source constraints. Missing creative decisions return to the storyboard owner through the project's consultation procedure. A scene-image task does not rewrite narration or invent another event.

Before media search, reuse or generation, check the project's asset library and dedupe records where present. Reconcile actual paths and hashes, editorial suitability, provenance and rights separately. An identical file or public source is not permission or visual acceptance.

Resume at the first missing or invalid result. Preserve accepted images whose relevant dependencies still match. Do not select the highest filename version or treat review of the same scene ID as review of a different image. Do not migrate every historical manifest just to use this skill; the [handoff contract](references/scene-handoff.md) maps existing records without replacing them.

## Motion-safe composition

Before generating an image intended for permitted whole-image movement/zoom, obtain the planned camera envelope and protected faces, action objects and text from the storyboard. Compose for the whole path: source aspect, delivery fill crop, whole-image zoom/horizontal pan and overlay regions together. Choose a wider composition or reduce planned motion before generation when needed; do not reserve a universal percentage. Check the actual selected PNG against that envelope before import, including intermediate extrema. Start/middle/end samples alone do not establish containment throughout motion. A static image passing its own review does not establish motion safety. Changed framing or motion requires a targeted recheck and the actual composite is reviewed before the stage-16 MP4 handoff; export checks follow the shared QA profile.

At acceptance of each actual image, finalize and save its motion decision once: subject, focus point, direction/zoom, start/end center and scale, and narrative reason under the [motion owner](../ytv-image-motion/SKILL.md). Use the observed composition and spoken beat, considering the adjacent scene. This handoff is reused directly during montage; do not reselect movement by scene number.

## Produce only the needed change

Fix identity/material/location invariants in the episode's visual bible, anchored to actual accepted reference files. Pass the appropriate files as image references in every related generation/edit, identifying their roles. A style reference defines appearance; the current storyboard defines whether an object has moved, disappeared or changed. Never reset an event to match the reference. Compare with the original accepted anchor and current state instead of accumulating drift from the latest generation.

Separate identity/style from pose and composition whenever the reference contains a character. Do not assume a reference image's stance, gaze, arm/hand positions, gesture, prop grip or framing are identity invariants. Before generation, state each visible hand's intended action and relation to the body/props; make the action differ from the reference when the story calls for it. If the hands have no story purpose, frame or occlude them naturally, or omit the character. Do not rely on a generic “vary the pose” instruction or a negative prompt alone: specify a concrete replacement action for this shot. Inspect both hands against that brief in the full image and reject an inherited/repeated pose when it conflicts.

Execute the accepted composition and profile, preserving unaffected content. Include the profile's requested quality, aspect and resolution in every generation/edit brief. Set corresponding tool controls explicitly when available; otherwise express the targets in the prompt without claiming a control was applied. Keep the requested generation target, measured native source dimensions and intended video delivery geometry separate; a prompt is not proof of the returned size. The delivery geometry comes from the accepted brief/export contract and its owner.

Save an immutable new version, exact prompt, requested and actually applied controls, available generation/source provenance, actual reference paths/hashes and measured native dimensions. Unknown parameters stay unknown. Keep imported assets at their existing paths; do not overwrite or move them. A repeated shot may reuse the exact opening file if the storyboard requires it.

If the user requested only a first style sample, make and check that sample, show it with the actual reference and record the user's decision before the rest of the series. This is conditional on that request. For an authorized full series, continue through remaining scenes and internal checks without inventing per-image approval gates. A draft is not a newly approved channel reference.

## Review the exact files

Open every selected image individually, full-frame, against the actual applicable reference; magnify consequential details. Check the readable action/state, identity, number of people, era, clothing/prop continuity, faces, fingers, jewelry, head/body proportions, perspective, supported plants/objects, contact and natural shadows. Inspect connected bodies/objects across transparent surfaces and occlusions; a hidden limb and a generatively missing limb differ. Apply the profile's material and defect criteria.

Visible story-relevant books, pages, notebooks, cards, newspapers and screens must contain relevant content. Check lettering, historical symbols and quotes against required content and sources; identify reconstructions in production records rather than present them as originals. Empty relevant pages, unsupported objects and broken anatomy block import until repaired.

Measure decodeability, native size, format and alpha. Record fit to the delivery frame: proportional scaling, crop and any padding. Inspect the actual crop at target viewing size; do not stretch to force a ratio or call an upscale native detail. If an image doubles as a cover, invoke the thumbnail owner for that separate use.

Reject a blocking defect, describe it concretely, repair the affected version and recheck the whole replacement plus relevant neighboring continuity. Contact sheets help compare a sequence but do not replace full individual inspection. Record which details, reductions and composites were viewed; uninspected details stay unverified. Technical checks and SHA do not prove style, rights, caption fit or final-film QA.

## Hand off and resume

Return the exact selection with versions/hashes, dependencies, acceptance author/evidence, rejection reasons, checks performed and limitations using the [handoff contract](references/scene-handoff.md). Internal acceptance, user approval and independent review are separate evidence; preserve their actual scope. Self-review is not independent review.

Only currently accepted assets are ready for import, except a clearly labeled draft explicitly requested for review. A partial set remains partial. Changed relevant storyboard content, reference requirements, source bytes or framing requires targeted recheck; unchanged dependencies keep their evidence. Editing an unused future prompt alone does not invalidate an accepted PNG. A replacement invalidates dependent crop/caption-fit/edit/export checks until rechecked, not unrelated narration or the entire series.

Storyboard controls scene meaning/sequence; subtitles owns the narration line and cue fit; editor owns import, permitted motion, timing and export; final QA owns the actual film. Pass framing and text areas as constraints, not proof that later composites work. This skill grants no new audio, publication, timeline mutation or delegation authority.
