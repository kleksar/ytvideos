# Plan 06 — “All night” — layer set v01

**Status: NOT READY — independent review confirms a corrupted left-edge strip at t4, including after the bounded BG patch.** The master composition was accepted by the director for continuing layer preparation; that approval is not a production pass. Endpoints are stills only; continuous animation has not been reviewed.

## Initial v02 layer-first candidate (superseded by failed BG v03 patch)

| Role | Exact file | Dimensions / mode | t0 placement | t4 placement |
|---|---|---|---|---|
| Canonical master | `masters/06_all_night_master_v02_layered.png` | 941×1672 RGB | equals t0 | — |
| BG | `layers/06_all_night_BG_v02_table.png` | 941×1672 RGB opaque | x=0, y=0 | x=+4, y=0 |
| MG | `layers/06_all_night_MG_v01.png` | 941×1672 RGBA | x=0, y=0 | x=+8, y=0 |
| FG | `layers/06_all_night_FG_v01.png` | 941×1672 RGBA | x=0, y=0 | x=+11, y=0 |

Order: **BG → MG → FG**. The positive plane deltas are +4/+8/+11 px left-to-right. BG t4 preview uses a mirrored 4 px left-edge fill. The canonical master is the actual BG+MG+FG t0 composite, not the source composition image. Exact stills: `previews/06_all_night_v02_t0_BG0_MG0_FG0.png` and `previews/06_all_night_v02_t4_BGplus4_MGplus8_FGplus11.png`.

## QA record

- All selected files are exactly 941×1672. BG is opaque RGB. MG and FG are RGBA.
- T0 composite is byte-identical to the canonical master. T0 preview and t4 preview both recompose byte-for-byte from the selected layers and listed offsets; RGB difference bounding boxes are empty.
- MG carries Joshua, both arms/hands, chair, laptop and the entire continuous tabletop/front edge as one moving group. Strong alpha bounds are x=0…940, y=391…1671; soft alpha reaches x=0…940, y=41…1671.
- FG is a small closed paper book with its contact shadow; registered strong alpha bounds are x=63…317, y=1266…1373, soft bounds x=50…329, y=1265…1383. It was made from the transparent ImageGen source by cropping the alpha-support bounds x=26…808/y=1112…1445, clearing only alpha values below 2, proportionally scaling the cutout to 280×119 and placing it at x=50/y=1265. The source crop had generated at a much larger scale; this mechanical registration is recorded and the raw file remains excluded.
- In the actual t0 composite Joshua remains recognizable, the laptop and hand-to-keyboard/table contacts look connected, the book is fully inside frame and rests on the tabletop with a contact shadow. No text or UI was generated. The visible typing hand does not clearly expose all five digits; no obvious extra digit is present. Do not animate the hand.
- **Blocker:** independent review confirmed an 8 px corrupted strip at x≈0–7 from about y≈1110 down through the table/lower edge in t4. The bounded BG-only v03 patch preserved t0 byte-for-byte but left red/green/dark blocks and dashed fragments at that edge. No more repair was attempted. The set remains **NOT READY** and must not be imported. The outermost book edge and laptop remain inside in the saved stills.
- **Reverse-registration test:** without changing any source layers, a second endpoint pair was composed from BG −4/MG −8/FG −11 at t0 to BG 0/MG 0/FG 0 at t4 (all y=0); the t4 still equals the existing canonical master byte-for-byte. Hand/laptop/table and book/table contacts read connected, and the laptop is inside frame. The exposed right BG edge at t0 shows a new orange vertical strip from the mirrored BG fill, so this test also remains **NOT READY** and was not sent for review. Exact stills: `previews/06_all_night_reverse_test_v01_t0_BGminus4_MGminus8_FGminus11.png` and `previews/06_all_night_reverse_test_v01_t4_BG0_MG0_FG0.png`.
- **Final registration-only test:** reused the same v02 BG/MG/FG, with t0 BG 0/MG −4/FG 0 and t4 BG +4/MG +4/FG +11, all y=0. Net motion is +4/+8/+11 px left-to-right. Exact endpoint previews are `previews/06_all_night_registration_test_v02_t0_BG0_MGminus4_FG0.png` and `previews/06_all_night_registration_test_v02_t4_BGplus4_MGplus4_FGplus11.png`; six enlarged edge/contact QA crops sit beside them. Both previews recompose exactly from the named layers and positions; t4 BG uses the same mirrored 4 px left fill. Full-frame and enlarged inspection found a distinct vertical tonal strip at the far-left BG/MG boundary in t4, across the wall-to-table edge. At t0, laptop/hand/table and book/table contacts remain connected; MG −4 advances the already frame-cropped left sweater by 4 px. This registration is **NOT READY** and was not sent for review. Per the bounded task, no further Plan06 registration or repair attempts should be made.
- Warm amber edge light appears on the alpha cutout over cyan; over the actual night room it reads mostly as scene lighting. Endpoint stills only; intermediate motion, contact through motion and playback are unverified.

## Provenance and excluded attempts

- Character/style reference: `../../05_joshua_profile_master_v03.png` (visual reference only; not overwritten).
- Initial generated composition: `masters/06_all_night_master_v01_composition.png`, ImageGen output `/Users/diplomat/.codex/generated_images/01a194de-e95f-7233-95be-7f11b3636ee3/exec-62f94282-e529-411f-89aa-c185eea4fa2c.png`, SHA-256 `60d1d440433c4c34b880c6267205d42796587cb9dbf7da5294c7af19cd28aefb`.
- BG v01 without table is retained but excluded: `layers/06_all_night_BG_v01.png`; its t4 revealed floor where the MG tabletop moved.
- v02 table BG ImageGen source: `/Users/diplomat/.codex/generated_images/01a194de-e95f-7233-95be-7f11b3636ee3/exec-a53360a1-f742-4f27-99b0-16175307e1bc.png`.
- Bounded BG-only test: `layers/06_all_night_BG_v03_table_continuation.png`. It patches only BG source columns x=0…3/y=1100…1671, extending the underlay beneath the t0 MG so the t0 composite remains byte-identical. Exact t0/t4 stills are `previews/06_all_night_v03_t0_BG0_MG0_FG0_BGv03.png` and `previews/06_all_night_v03_t4_BGplus4_MGplus8_FGplus11_BGv03.png`. Independent review confirmed the visible colored/fragmented strip remains at the far left in t4; this is the stopping defect. No further correction was attempted.
- MG transparent ImageGen source: `/Users/diplomat/.codex/generated_images/01a194de-e95f-7233-95be-7f11b3636ee3/exec-3968c8e9-e8c4-4452-895b-00455d1806bb.png`.
- FG raw transparent ImageGen source: `layers/06_all_night_FG_v01_raw.png`; excluded from import because it is oversized and misregistered.
- MG overscan experiment `layers/06_all_night_MG_v02_leftoverscan8.png` and its v03 master/endpoints are diagnostic only. Mirrored edge content created visible frame-edge strips; do not import.
- Initial v01 layered composite and endpoints using the no-table BG are diagnostics only: `masters/06_all_night_master_v01_layered.png`, `previews/06_all_night_v01_t0_BG0_MG0_FG0.png`, `previews/06_all_night_v01_t4_BGplus4_MGplus8_FGplus11.png`.
- No audio, video or Palmier project was created or changed.
