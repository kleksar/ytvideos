# Paper Detour scene-image profile

Read [bootstrap](../../../../.agent/CHANNEL_BOOTSTRAP.md), root and [Paper AGENTS](../../../../channels/paper_detour/AGENTS.md). Before media search/reuse/generation consult the agreed asset library and dedupe manifest when supplied with the episode bundle; they are not part of the source-only clone. The coordinator personally follows [Extra High](../../ytv-chatgpt-extra-high/SKILL.md) for missing creative decisions. These project dependencies do not constrain unrelated channels using the core.

## Visual contract and reference choice

The [channel contract](../../../../channels/paper_detour/AGENTS.md#изображения-и-монтаж) requires a complete static opaque full-frame handmade paper/card diorama source per shot. Apply the core's composition/framing procedure and the channel's authorized motion boundary. Use actual accepted files from the [scene-reference catalog](../../../../channels/paper_detour/brand/SCENE_IMAGE_REFERENCES.md): original Paper004 user frame «38.08», plus accepted 033 S01. For a continuing episode also use its specific accepted anchor and current visual bible. New reuse takes the catalog's shared source; preserve imported paths.

Compare handmade paper/card fibers, cut/layered edges, folds, volume and physical light/shadows. A photographic human substituted for a paper character, flat vector or smooth digital render does not pass as the paper style. This does not forbid a photograph, painting, document or other real-world image carried by a physical object inside the diorama, as specified below. Match real files, not a verbal approximation. A particular hero, street, palette or glasslike droplet remains episode-specific. Promote an accepted image into the channel catalog only when the user's instruction covers that promotion; record provenance and scope.

### Real-world images inside the paper world

When an actual person's appearance, artwork, document or object matters to the story, it may remain recognizable as an image on a physical carrier inside the complete paper/card composition: a print, page, framed picture, display panel or stone-like layered paper slab. Preserve the carrier's thickness, edges, support, perspective, contact shadows and common lighting. Choose the carrier for the story, rather than putting every source on the same decorative rock. The image is part of the scene's material world, with a clear boundary from surrounding paper characters and environment.

Use the actual authorized source when identity or documentary detail matters; record provenance, rights and any alteration. A generated likeness or recreated painting does not become an authentic photo, original artwork or archival evidence because it looks realistic. Do not replace a needed historical source with an invented image while implying authenticity. The user's accepted [030 film reference](../../../../channels/paper_detour/brand/FILM_REFERENCE_030.md) demonstrates visual integration, not a blanket provenance certification.

## Canvas and text

Before scene work load the actual output geometry from the [Paper delivery profile](../../ytv-video-export/references/paper-detour.md); it owns default canvas/FPS for Shorts and long films. An explicit accepted aspect overrides the default. Record actual native source size, then fit proportionally without distortion; a smaller generated source does not become native delivery resolution through scaling. Design the camera/zoom crop envelope for the target canvas before generation. The complete PNG is opaque and full-bleed, with no empty bars or transparent fields. Verify the visible image reaches all four edges; matching pixel dimensions alone does not prove full-bleed framing. If needed, use proportional fill with minimal crop or repair the composition; do not stretch the image or add an artificial background to conceal bars.

### Generation quality and requested resolution

For every scene generation/edit request the maximum available image quality, native resolution and fine detail, preserving the accepted composition and handmade paper style. Specify 4K UHD as the generation target for the accepted orientation:

| Scene format | Requested generation target |
|---|---|
| Landscape, 16:9 | 3840×2160 px |
| Portrait, 9:16 | 2160×3840 px |

For another explicitly accepted aspect, request the highest available native resolution at that aspect; do not force it into one of these canvases. Emphasize visible paper fibers, layered cut edges, folds, physical light and shadows, and clear meaningful details such as faces, hands and action objects. A resolution label alone does not establish visual quality. Preserve intentional focus/depth and avoid adding sharpening or effects merely to suggest detail.

Reusable prompt wording, followed by the specific scene and its constraints:

> Maximum available image quality, native resolution and fine detail. Target 4K UHD: [3840×2160, landscape 16:9 / 2160×3840, portrait 9:16 — select the accepted format]. Preserve the accepted handmade paper/card diorama style, visible fibers, layered cut edges, folds, physical lighting and clear focal details.

The [core procedure](../SKILL.md#produce-only-the-needed-change) records requested targets, actual controls and native dimensions separately. A smaller returned PNG is not native 4K and does not by itself justify repeated generation; inspect its suitability for the actual delivery crop/zoom. Use the applicable image-generation skill for tool/mode choice. This quality target does not authorize a different API path or change the film's export resolution/FPS; those remain with the [export owner](../../ytv-video-export/SKILL.md).

### Scene text and storage

For both Shorts and long films, consume the storyboard's [text-area plan](../../ytv-paper-storyboard/SKILL.md#безопасные-области-текста) before generation and preserve only the crop/camera envelope and other explicit constraints it assigns. Subtitle geometry belongs to the separate subtitle layer; it does not reserve a lower portion of the source still or limit where scene subjects may appear. Compose the complete image naturally across the full frame; do not infer an empty lower band, move objects away from the bottom, or reduce detail based on a universal percentage. A written prompt does not prove compliance. If an actual later subtitle composite creates a specific conflict, route that exact frame for correction and inspect the relevant composite.

[Subtitles](../../ytv-paper-subtitles/SKILL.md#общая-геометрия-и-защита-композиции) owns narration-line geometry. Compose the scene from its accepted story action and objects; narration is carried by the subtitle layer. A replacement or changed framing invalidates affected subtitle-fit checks until rechecked.

If a scene becomes a Shorts cover, invoke [thumbnails](../../ytv-youtube-thumbnails/SKILL.md) with its [Paper safe-area procedure](../../ytv-youtube-thumbnails/references/paper-detour.md#shorts-cover-format-and-safe-area). Check master, specified crop and actual target surface separately. An observed card size is not a platform specification. Text below the card is a title field handled by [titles](../../ytv-youtube-video-titles/SKILL.md), not by repainting the scene.

Save scene versions in the episode's `Source/Images/`, with prompts/references and existing generation journal. A looping return uses the identical opening file when specified by the accepted storyboard. Do not move imported source paths. [Storyboard](../../ytv-paper-storyboard/SKILL.md) owns compositions/sequence; [production flow](../../ytv-video-production/SKILL.md) owns FFmpeg montage.

## Paper-specific acceptance

Apply the [core's actual-file checks](../SKILL.md#review-the-exact-files) to every final PNG before import, comparing it with the exact approved reference. Inspect paper material/edges, volume and physical lighting both in the full source and its framed phone-size reduction. Photographic humans replacing paper characters, flat vector art or smooth digital renders fail this profile even when the pixel dimensions match the request; an image on a physical carrier follows the integration contract above.

For water or another semitransparent overlap, trace every person/animal and crossing object from visible into obscured sections: torso, pelvis, limbs, scale, pose and support remain connected. If background is visible through water, the body must occlude it; tint, refraction and turbidity can lower contrast but cannot erase the figure. Check proportions above/below the surface and one coherent perspective/optical treatment for body, surroundings and background. Do not excuse an undersized submerged body with selective refraction. Distinguish real occlusion by an object/frame edge from generative disappearance. Inspect full source and final framing, not just a contact sheet. If split-level geometry cannot be made coherent, rebuild the complete frame with camera above opaque water that consistently hides body and background while retaining accepted meaning; a substantive story change returns to storyboard.

Record actual `ACCEPTED/REJECTED` decisions, their authors, inspected details, exact reference and limitations. A passed scene set does not accept future subtitle timing, final export, audio or publication. The [Paper entry](../../ytv-paper-images/SKILL.md) routes to this core/profile without a second procedure.
