# Layer sets v01 — QA manifest

**Overall status: NOT READY FOR MONTAGE.** All generated PNGs in this folder are drafts. No layer trio passed exact registration, edge cleanliness, and composite checks. Same dimensions and an alpha channel alone do not establish compatibility.

The intended Z order for every planned set is **BG → MG → FG**. Every plane must be a full-canvas 941×1672 PNG; BG is opaque RGB, MG and FG are transparent RGBA. All source masters remain untouched in `../`.

## QA results

| Set / source master | Draft planes and format | Composite / edge findings | Status |
|---|---|---|---|
| `01_opening` — `../01_room_laptop_master_v03.png` (v03) | Selected regrouping: `01_room_laptop_master_v03_BG_v02.png` — 941×1672 RGB; `01_room_laptop_master_v03_MG_v03.png` — 941×1672 RGBA; `01_room_laptop_master_v03_FG_v02.png` — 941×1672 RGBA. Alternate drafts: `01_room_laptop_master_v03_BG_v01.png` (941×1672 RGB); `01_room_laptop_master_v03_MG_v01.png` (941×1672 RGBA), `_MG_v02.png` (941×1671 RGBA), `_MG_v04.png` (941×1672 RGBA); `01_room_laptop_master_v03_FG_v01.png` (941×1672 RGBA). | Regrouped preview `01_room_laptop_master_v03_static_composite_preview_v02.png` avoids the earlier horizontal tabletop join, but the room/objects still differ materially from the source and red/yellow fringes remain around hair, arm and plant. The targeted matte cleanup in MG v04 still leaves colored fringe. Earlier preview v01 has a wooden wainscot absent from the master. Tested the selected RGBA planes over gray and cyan matte diagnostics; edge fringe is visible. Desk/plant touch frame edges, so margin-safe independent drift is not available. | **NOT READY** |
| `02_photo` — `../02_photo_master_v03.png` (v03) | `02_photo_master_v03_BG_v01.png` — 941×1672 RGB; `02_photo_master_v03_MG_v01.png` — 941×1672 RGBA; `02_photo_master_v03_FG_v01.png` — 941×1672 RGBA. | Static diagnostic `02_photo_master_v03_static_composite_preview_v01.png` duplicates the lamp and differs materially from the master; fringe is visible on gray/cyan matte diagnostics. | **NOT READY** |
| `03_message_laptop` — `../03_message_laptop_master_v03.png` (v03) | `03_message_laptop_master_v03_BG_v01.png` — 941×1672 RGB; `03_message_laptop_master_v03_MG_v01.png` — **941×1671 RGBA**; `03_message_laptop_master_v03_FG_v01.png` — 941×1672 RGBA. | Static composite and gray/cyan matte diagnostics show redraw differences and colored edge fringe. MG is one pixel short in height and cannot be used as a registered plane. | **NOT READY** |
| `04_reply_card` — `../04_reply_card_master_v01.png` (v01) | BG/MG/FG not generated. | No set attempted after ImageGen extractions failed exact registration and clean-edge checks on the first three masters. | **NOT READY — no assets** |
| `05_joshua_profile` — `../05_joshua_profile_master_v03.png` (v03) | BG/MG/FG not generated. | No set attempted after ImageGen extractions failed exact registration and clean-edge checks on the first three masters. | **NOT READY — no assets** |
| `06_daylight` — `../06_daylight_master_v2.png` (v2) | BG/MG/FG not generated. | No set attempted after ImageGen extractions failed exact registration and clean-edge checks on the first three masters. | **NOT READY — no assets** |
| `07_resource_meter` — `../07_resource_meter_master_v01.png` (v01) | BG/MG/FG not generated. | No set attempted after ImageGen extractions failed exact registration and clean-edge checks on the first three masters. | **NOT READY — no assets** |

## Provenance and checks

- Draft BG/MG/FG art was created with ImageGen edits referenced to the named reviewed master. Source masters were not modified.
- The static composites and solid-color matte diagnostics were made with FFmpeg solely for QA. Files containing `ALPHA_EDGE_CHECK_NOT_SCENE_PREVIEW` are matte diagnostics, not shot previews and not montage assets.
- Dimensions and channel layout were checked with `sips` and `file`. Draft alpha edges were inspected over the source background and over light gray and cyan. The three attempted sets failed visual registration or edge checks; no set passed.
- No movement render or drift test was performed because the layers failed static compositing checks. In particular, cropped objects in 01–03 do not have safe margins for independent movement.
- Generation method limitation: ImageGen altered some geometry/texture and left colored matte fringes; it did not produce exact pixel-registered cutouts. A different extraction workflow is needed before these planes can be used.

## SHA-256 of selected draft planes

| File | SHA-256 |
|---|---|
| `01_opening/01_room_laptop_master_v03_BG_v02.png` | `58aaccee758937437fab61cf0ff97cdd738e0d8bdbc4619aaee4726900846f51` |
| `01_opening/01_room_laptop_master_v03_MG_v03.png` | `dd8bc0e9246a2d4dcce9160965bf045d27583ff237c54571f246ada6f672bfc2` |
| `01_opening/01_room_laptop_master_v03_FG_v02.png` | `bb16946e17ff2b80f7d40c775cdf91560bccc1f7f185deaaec6182b42536a475` |
| `02_photo/02_photo_master_v03_BG_v01.png` | `2c97d8cb7424c55506d6b2a9e23371ca96d50dfbf9eac8747838820cd1804e82` |
| `02_photo/02_photo_master_v03_MG_v01.png` | `b9ac897995a41b40d8084a74282554ab6e33fa5a1623d97caf0062d1da219091` |
| `02_photo/02_photo_master_v03_FG_v01.png` | `dcf5e2b105004d6d215f1488415daa18c6f7927baacaf569e100f25afee70fb6` |
| `03_message_laptop/03_message_laptop_master_v03_BG_v01.png` | `fa65b7d9dcfa94f433a5e32356811c4f85a41f9523348543f187ea1c560f1c64` |
| `03_message_laptop/03_message_laptop_master_v03_MG_v01.png` | `29b6e5457572f33f30daf68c1b2ff8bfb23a33706b2eff3381f17c001a408048` |
| `03_message_laptop/03_message_laptop_master_v03_FG_v01.png` | `56acb8f400e38800b192d36a01ca0a7f1afd9c1ed5e9b44edfe59a56772da288` |
