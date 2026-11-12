# 028 — thumbnail generation log

## 2026-11-01 — `PRAISED. THEN PUNISHED.` (v01)

- Purpose: one English Shorts cover for the accepted Taj Mahal architect retelling. User confirmed cover-only scope; existing scene stills remain untouched.
- Status: local review candidate. Not entered in YouTube Studio or uploaded.
- Concept source: [Extra High thumbnail consultation](../../.agents/consultations/20261101-paper-taj-mahal-thumbnail-concept.md). The consultation returned an image rather than a written concept; its visible phrase and composition were treated as a direction, not as the finished local asset.
- Working title paired with cover: `The Architect Who Was Too Good at His Job` (consultant recommendation; not yet user-approved).
- Tool: built-in `image_gen.imagegen`; first generated the full 9:16 scene, then made a layout-only edit to lower and reduce the headline for the central crop.
- Master: [`taj_mahal_architect_thumbnail_v01_praised_then_punished_safe_20261101.png`](taj_mahal_architect_thumbnail_v01_praised_then_punished_safe_20261101.png), PNG, 941×1672, 9:16; SHA-256 `8f3258098e1c0ce64aeda39db0ec94fd1e5a4ee59d2fb661f30894d28b0b72c2`.
- Upload copy: [`taj_mahal_architect_thumbnail_v01_praised_then_punished_20261101_upload.jpg`](taj_mahal_architect_thumbnail_v01_praised_then_punished_20261101_upload.jpg), JPEG, 941×1672; SHA-256 `84899caa1b636e2a3b1b5bb13aab00f54370a695844d2abb6186531c13c22f4b`.
- Visual QA: full frame reviewed. The centered 2:3 crop is 941×1412 with a 130 px top offset; the complete two-line headline remains inside it. A 320×480 crop preview was checked at phone size; the phrase remains legible and the Taj Mahal, king, Ahmad, and empty sleeves still read clearly. This is a local preview check, not a YouTube Studio display check.
- Release checks still pending: user approval of title/cover pair and actual Shorts card preview in Studio when a video draft is available.

### Initial image generation prompt

```text
Create one finished 9:16 vertical YouTube Shorts cover for the handmade paper-diorama channel Paper Detour. This is a complete story thumbnail, not a film still. Build the entire scene as a handcrafted layered cardstock miniature: tactile fibrous paper, clean cut and folded edges, sculpted paper architecture, real miniature depth and dramatic soft shadows, cinematic handcrafted detail. Match the channel’s established cover language: high-contrast warm/cool lighting, rich midnight blue shadows and warm amber light, large chunky cream paper lettering with a dark dimensional paper shadow.

Composition: keep every important element inside the central 2:3 crop-safe area; leave a small clear margin at the top and bottom. At the top, place exactly this legible English headline, on two compact lines: “PRAISED.” / “THEN PUNISHED.” Use only these words; do not add any other text, letters, numbers, logos, or watermarks. Main story action below the headline: the luminous white Taj Mahal stands unmistakably in the center background, framed by Mughal arches. On the right, the emperor stands on a raised palace landing, solemnly presenting the finished monument with one open hand. In the foreground, Ahmad is the clear central subject, facing the viewer at a slight angle, shocked and devastated. His long robe sleeves hang visibly empty and limp with folded, hollow paper cuffs; his hands are not visible. Two smaller assistants stand just behind him with similarly empty hanging sleeves and lowered heads. The king is not holding a weapon and no violence is shown. The image should communicate the irony of praise followed by punishment in a single instantly readable composition.

Use purposeful warm gold light on the king and the monument, cool deep blue shade around Ahmad and his assistants. Keep faces expressive but stylized as crafted paper sculptures. Leave the headline legible at phone size and fully within the center crop. No blood, no wounds, no severed body parts, no visible hands on Ahmad or assistants, no additional people, no calligraphy, no split panels, no photorealistic skin, no glossy CGI.
```

### Safe-area edit prompt

```text
Make a layout-only correction to this existing Paper Detour thumbnail. Preserve the scene artwork, colors, characters, Taj Mahal, king, empty sleeves, framing, and wording exactly. Do not generate a new scene and do not alter any content except the heading layout. Move the exact two-line headline “PRAISED. / THEN PUNISHED.” down and slightly reduce its overall size so the entire top of the first letter begins just below 8% of the image height and the bottom of the last line ends before 22% of the image height. Keep the text crisp, centered, large enough to read on a phone, with its existing cream cut-paper fill and deep shadow. This places every letter within the central 2:3 safe crop of the 9:16 image, whose top edge is about 7.8% down from the image top. Keep the Taj Mahal dome clear below the text. No other changes.
```

## 2026-11-02 — pre-upload recheck

PNG/JPEG decode, JPEG hash/size and centered 2:3 crop at 320×480 rechecked. Complete title, faces, empty sleeves and monument remain legible in the local preview. Existing package retained after the narrow Extra High consistency review. Exact user title/cover approval and actual Shorts card remain unverified. See [current pre-upload report](../Metadata/PRE_UPLOAD_REVIEW_20261102.md).
