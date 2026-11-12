# Paper Detour 037 — thumbnail v03 provenance and visual check

## Scope and decision state

- Three alternative cover-text/image pairs are prepared for user review. They are not an accepted final cover.
- Shared linked working title: `Wages Rose. Did Life Get Easier?` from [title decision v01](../Metadata/TITLE_DECISION_v01.md).
- Film/narration basis: [narration v01](../../Source/Script/narration_en_v01.md) (Paper transfer v01).
- English lettering; one complete cinematic handmade paper/card composition per cover, consistent with Paper Detour thumbnail standards.

## Provenance

- Generation method: built-in ImageGen editing mode.
- The v02 compositions were used as edit targets: `Concepts/Options_v02/037_thumb_v02_A_hand_off.png`, `037_thumb_v02_B_counting.png`, and `037_thumb_v02_C_empty_purse.png`.
- The actual style references were inspected: `channels/paper_detour/Shared/References/Paper/paper004_user_38.png` for Paper materials and `channels/paper_detour/videos/030_clothing_history/Packaging/Thumbnails/Concepts/a_tools_where_clothes_v02.png` for the approved cinematic cover hierarchy and lettering.
- Each edit was constrained to replace the existing `333 DAYS' PAY` wording while preserving the composition, hands/worker, props, basket, lighting, colors, crop and paper materials.
- Master outputs were copied without additional raster edits into `Concepts/Options_v03/`.

## Exact cover text and edit prompts

### A — `A YEAR. / 333 WAGES?`

Edit target: `Concepts/Options_v02/037_thumb_v02_A_hand_off.png`.

```text
Use case: text-localization
Asset type: long-form YouTube thumbnail for Paper Detour
Primary request: Replace only the existing lettering with the exact new two-line hook shown below.
Input image: the supplied image is the edit target, not merely a style reference.
Style/medium: preserve the existing cinematic handmade paper/card diorama and match the channel's approved cut-paper lettering: large warm cream uppercase letters, broad rounded irregular shapes, subtle paper texture, dimensional paper edges, soft contact shadow.
Text (verbatim, two lines): "A YEAR." / "333 WAGES?"
Composition/framing: Keep the words in the same upper-right dark negative space; preserve generous margins and phone-size legibility.
Constraints: preserve every part of the scene exactly: worker's arms and hands, coin handoff, bread-and-fuel basket, terrain, lighting, color, camera, texture, crop and all props. Remove every trace of the old words "333 DAYS' PAY". Change only the cover text and its line layout. Render the exact punctuation and spelling above. No other text, no labels, no watermark.
```

### B — `BIGGER PAY. / BIGGER BILL.`

Edit target: `Concepts/Options_v02/037_thumb_v02_B_counting.png`.

```text
Use case: text-localization
Asset type: long-form YouTube thumbnail for Paper Detour
Primary request: Replace only the existing lettering with the exact new two-line hook.
Input image: the supplied image is the edit target, not merely a style reference.
Style/medium: preserve the existing cinematic handmade paper/card diorama and match the channel's approved cut-paper lettering: large warm cream uppercase letters, broad rounded irregular shapes, subtle paper texture, dimensional paper edges, soft contact shadow.
Text (verbatim, two lines): "BIGGER PAY." / "BIGGER BILL."
Composition/framing: Keep the words in the same upper-right dark negative space. Make both lines similarly large, with generous margins and phone-size legibility.
Constraints: preserve every part of the scene exactly: counting worker, coins, coin trail, annual-needs basket, table, terrain, lighting, color, camera, texture, crop and all props. Remove every trace of the old words "333 DAYS' PAY". Change only the cover text and its line layout. Render the exact spelling and punctuation above. No other text, no labels, no watermark.
```

### C — `WAGES UP. / BUDGET TIGHTER?`

Edit target: `Concepts/Options_v02/037_thumb_v02_C_empty_purse.png`.

```text
Use case: text-localization
Asset type: long-form YouTube thumbnail for Paper Detour
Primary request: Replace only the existing lettering with this exact new two-line hook.
Input image: the supplied image is the edit target, not merely a style reference.
Style/medium: preserve the existing cinematic handmade paper/card diorama and match the channel's approved cut-paper lettering: large warm cream uppercase letters, broad rounded irregular shapes, subtle paper texture, dimensional paper edges, soft contact shadow.
Text (verbatim, two lines): "WAGES UP." / "BUDGET TIGHTER?"
Composition/framing: Keep the words in the same upper-left dark negative space. Both lines should be comparably large. Keep every glyph and its shadow inside a clear 8 percent margin from the image edges; preserve phone-size legibility.
Constraints: preserve every part of the scene exactly: empty purse, falling coin, coin path, annual-needs basket, table, terrain, lighting, color, camera, texture, crop and all props. Remove every trace of the old words "333 DAYS' PAY". Change only the cover text and its line layout. Render the exact spelling and punctuation above. No other text, no labels, no watermark.
```

## Master assets

All three masters are 1672×941 PNG.

| Option | File | SHA-256 |
|---|---|---|
| A | [`037_thumb_v03_A_year_333_wages.png`](Concepts/Options_v03/037_thumb_v03_A_year_333_wages.png) | `696e6785af477e5f3a86b99e979ac3dd9af84c650cac979c6f9fd2832386afe0` |
| B | [`037_thumb_v03_B_bigger_pay_bigger_bill.png`](Concepts/Options_v03/037_thumb_v03_B_bigger_pay_bigger_bill.png) | `b8898eb1c88bc436791f995a6f90a74cfa414128546c3b8475406e4939151d3d` |
| C | [`037_thumb_v03_C_wages_up_budget_tighter.png`](Concepts/Options_v03/037_thumb_v03_C_wages_up_budget_tighter.png) | `bda23e2aa8b397ff0f77782ab257072dd65229145fff243b60b49d10053e6434` |

## Visual verification

- Inspected all three exact PNG masters at native size and all three 320×180 previews generated with `.agents/skills/ytv-youtube-thumbnails/scripts/thumbnail_previews.py`.
- At 320×180, each exact phrase is readable, the main interaction and needs basket remain recognizable, and no essential element sits under the lower-right timer overlay. Text spelling and punctuation match the prompts.
- These are local preview observations, not proof of how YouTube renders an uploaded cover. The episode is not uploaded, and no Studio/card rendering has been checked.
- User selection and final title/cover pairing remain pending. No upload JPEG has been produced and no external YouTube state has changed.
