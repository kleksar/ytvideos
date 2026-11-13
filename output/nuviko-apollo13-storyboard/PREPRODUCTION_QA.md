# Independent preproduction review

Reviewer `/root/runtime_resume`, 2026-11-13. Scope includes STORYBOARD.md, storyboard.json, prompts.json, REFERENCES.md, the 20 messages in CORRECT_CHAT_USER_REQUESTS.json and inspected pixels of sheets/filter-states.png, sheets/locations.png and sheets/host-poses.png. The traveler turnaround PNG was also inspected for comparison. This report does not accept final scene images, animation or audio.

Overall verdict is REVISE before the packet is treated as a fully specified Ingredients production package. The text breakdown is usable for continuing bounded preproduction.

## Verified coverage

All 14 scene narration strings match the exact script substrings at their recorded character offsets. Consecutive gaps contain whitespace only, and the trailing byte is a newline. Every spoken word is covered once, in order. The script SHA-256 is d720fc90d9b726c2f064c4f18da13feccfbb1fb0b0e2c5e9b41a7b340d099f02. All listed scene reference paths exist relative to this packet. Runtime approval and claim were outside this review.

The current packet names Ingredients and one reference image per scene, matching the later request at 17:01 rather than the earlier A→B proposal. Timing is explicitly deferred to measured narration. The user’s current scope is still images and storyboard. No video dispatch is warranted by an older Larry batch approval.

## Required corrections

1. Scene prompts remain a common style paragraph plus a short description and start/end sentence. The 17:06 user request asks for detailed, saved prompts that fix the visible elements before animation. Add the precise inventory, object count and state, spatial placement, actor/head/hand orientation, camera height and viewing direction, light direction, and permitted action for each scene. `required_views: scene_camera_view` does not specify a view. Bind each required view to an actual accepted sheet cell and file hash. The generic inventory lock is useful after a still is accepted, but does not replace that inventory.

2. The entity sheets do not yet cover the declared cast and spaces. There is no listed astronaut reference sheet covering the three crew members and their recurring side/back/hand views. The board itself says to fix faces and clothing before final generation. REF-CM and the exact warning-panel visual are expressly pending in REFERENCES.md. Obtain those references before generating or accepting those historical details. A museum round ring is already identified as a simplified model and can retain that limited role.

3. S014 must use the exact S001 still if the planned visual loop is retained. The actual host sheet instead assigns two different hand poses to S001 and S014. In the inspected sheet the left pose has two open hands at waist height, while the right pose raises one arm and drops the other. Choose the same pose/file for both loop frames and update the sheet-consumer map. The sheet retains the established illustrated treatment, brown/gray hair, ochre jacket and backpack, but its two poses cannot substantiate an identical seam.

4. The filter sheet’s entire top row has gray tape bands although its prompt calls these views bare and S007 explicitly says no bag or tape. The prompt log acknowledges this defect. Preserve that draft status and use a corrected bare state for S001/S002/S007/S008. The lower row depicts the bag/hose assembly, with a single hose visible in side and elevated views. The front lower view alone hides the connection and is insufficient as the sole assembly reference.

5. The location sheet already includes a taped assembly in the upper cabin panels. This would leak a post-build object into the earlier emergency/shelter sequence if reused unchanged. Its lower-right panel puts cardboard, bag and duct tape on a Mission Control console. The board requires a distinct ground test setup for S009. Split the consumers and use NASA S70-35395 for that laboratory scene. Keep the MCC console reference for the radio scene.

6. The board has broad prop-state continuity but lacks a per-shot map of exact appearance and removal. For S011→S012 explicitly identify whose hands remain visible, where the loose tape strip and cardboard move, which face remains open and where the hose exits. For S013 keep that route connected to a fixed cabin anchor. This addresses the user’s 18:14 concern about props appearing without a cause.

## Qualified observations

S006 and S013 have much longer speech spans than neighboring scenes. Their final lengths require the promised audio measurement; the current 14-plan count is provisional. S003 supplies a reaction at a panel rather than a visible tank accident, which is a defensible reconstruction choice if the narration carries the event. S013 currently relies on narration for the falling CO₂ value. A fabricated numeric display would not improve its factual support.

The animation briefs include room tone, prohibit invented dialogue and reserve music for a continuous edit-stage score. This is a coherent draft sound plan. A final Ingredients prompt still needs scene-specific visible actions and sound cues based on the actual accepted still. The stated calm final expression and first/middle/last clip checks preserve the requested QA goals.

## Evidence boundary

No final scene set or full collage was available in this review. Only the three named sheet images were visually inspected. Their hashes below identify the exact versions reviewed. Later replacements need a new observation.

- STORYBOARD.md — `f075e6c9c088852f60b5f95da4b18bf65ef8bd32a07db21ff92d0f95076556b2`

- storyboard.json — `97560aca33cba5d1cbf05ee4ad8bae03d1ae82bc51e3540e5e5bba7623fd2419`

- prompts.json — `3ff30e4c7494a5e0f27a91353525d61ac2172a6d9c1081fefd3473708cbcfd0e`

- CORRECT_CHAT_USER_REQUESTS.json — `427b496873f155ff506be0a74cfa266aecb7f537ca1bdfddca0f91a3711ed49a`

- sheets/filter-states.png — `4475531182778ff015e096df494a9f789407b295512e27baaeac84fe30f25d9d`

- sheets/locations.png — `263528d44d5f50a80043de614ff3e247483eedda540e84ffaa4cb8ac67a85fc9`

- sheets/host-poses.png — `83eb6e433502847f739f2f226718380f1c56dc16cd36d7188522e767f84f0734`

## Исправления после первого прохода

Добавлены отдельные подробные постановочные задания для 14 сцен. Проверены S001/S002, их hashes сохранены в detailed-scene-specs.json. S014 использует exact S001. Ведущий представляет экспонат левой рукой, кольцо лежит горизонтально. Новые historical scene images и исправленные reference sheets требуют отдельной приёмки.
