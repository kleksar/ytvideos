# School plates — minnie v02

## Scope and source

This is a generated paper-diorama asset pack for Paper Detour 027. The visual target was the approved parallax reference `channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png`: tactile matte paper/cardboard, visible cut edges and contact shadows, warm amber interior against deep blue/teal storm light. The room is a generic invented set; it is not evidence about a specific historic school. Plates contain no people or lettering. Generated with the image-generation tool from that visual brief/reference; QA composites below were made locally from these new files only.

## Canvas

Most files are **941 × 1672 px**, RGB or RGBA, portrait 9:16-ish (941:1672; not 1080 × 1920). All state-specific BG/master pairs are kept at the same pixel dimensions. Roofless v01/v02 are **941 × 1671 px**; this one-pixel mismatch is a known registration limitation. Do not place them into a 941 × 1672 stack without a deliberate canvas correction. RGB plates are opaque full-frame fills; transparent masks use full-frame RGBA to preserve their intended registration. No movement-bound/underfill test has been done, so the BGs are known to be closed at their static frame only.

## Shot map and current status

| Shot | Sequence / master preview | BG plate | MG slot | Status |
|---|---|---|---|---|
| **S02** | intact room → door opens → windows break. `MS01_intact_classroom_master_v02.png` → `MS02_door-only_master_v01.png` → `MS03_windows-damaged_master_v01.png` | `MS01_BG_intact_room_v02.png` → `MS02_BG_door-only_v01.png` → `MS03_BG_windows-damaged_v01.png` | Reserved for the separately owned whole character/held-prop layer; not included here. | BGs are opaque state plates. Masters are previews. Door mask and window masks are **DRAFT / fail QA**, see below. Not montage-ready as a moving stack. |
| **S03** | damaged classroom, roof intact. `MS03_windows-damaged_master_v01.png` | `MS03_BG_windows-damaged_v01.png` | Reserved / external. | Static BG/master pair is available for review; no MG, no parallax underfill test. |
| **S05–S06** | twine origin → wait beat. Use the same damaged-room setup and change framing by a new master when the approved board requires it; current reference: `MS03_windows-damaged_master_v01.png`. | `MS03_BG_windows-damaged_v01.png` | MG must come from the separately owned character/twine layer. | Desk/twine FG is **DRAFT / fail edge QA**; cannot be called ready. |
| **S07** | same room as roof departs. `MS04_roofless_master_v02.png` is the later roof-off preview. | `MS04_BG_roofless_v02.png` | Reserved / external. | Roofless BG is opaque, but 941 × 1671. `MOV_roof_plane_DRAFT_v01.png` is not cleared for movement; overlay suggests approximate shape alignment only. |

### Master previews available

- `MS01_intact_classroom_master_v02.png` — intact roof, closed door, glazed windows, room/desk staging; empty MG slot.
- `MS02_door-only_master_v01.png` — door open while roof/windows hold; empty MG slot.
- `MS02_damaged_room_master_v01.png` — earlier damaged-room variant; retained as a source candidate, not the current door→window sequence.
- `MS03_windows-damaged_master_v01.png` — door/windows damaged, roof intact; empty MG slot.
- `MS04_roofless_master_v02.png` — later roof-off state, empty MG slot.

The master previews are composition references, not proof of three-layer registration. There is **no finished MG in this package** and no complete montage-ready BG/MG/FG setup. Parent/coordinator should merge only after receiving the separately assigned MG and clearing the outstanding FG masks.

## Layer inventory

### Opaque BGs (RGB, full-frame fill)

- `MS01_BG_intact_room_v02.png` — intact room; open door/window regions show matching cold exterior backing.
- `MS02_BG_door-only_v01.png` — door-open state, windows intact.
- `MS02_BG_damaged_room_v01.png` — earlier damaged-room state.
- `MS03_BG_windows-damaged_v01.png` — damaged door/windows, intact roof.
- `MS04_BG_roofless_v02.png` — roof-off exterior/storm fill, damaged door/windows; 941 × 1671.
- `MS01_BG_intact_room_v01.png`, `01_classroom_room_block_v02.png`, `MS04_BG_roofless_v01.png` — earlier drafts/source candidates; use v02 state BGs above where applicable.

### Transparent paper planes / FG (RGBA, full-frame)

- `MOV_door_leaf_registered_DRAFT_v02.png` — approximately registered door leaf; visible red/orange fringe is still a concern; no light/dark edge clearance. DRAFT.
- `MOV_door_leaf_unregistered_DRAFT_v01.png` — superseded rough cutout, not registered; reject for assembly.
- `MOV_window_panes_registered_DRAFT_v02.png` — panes overflow below the sill and cover parts of the mullions when overlaid on the intact BG; obvious edge/registration failure. DRAFT / reject for assembly.
- `MOV_window_panes_registered_DRAFT_v01.png` — earlier failed pane extraction; not for assembly.
- `MOV_roof_plane_DRAFT_v01.png` — approximate roof/crossbeam plane; static overlay leaves a small extraneous fragment/seam mismatch. DRAFT / reject for motion until corrected.
- `MS01_FG_desk_twine_v02.png` — transparent desk/twine; conspicuous red/white fringe on tabletop top edge and around twine, visible over both dark and light fields. DRAFT / reject as final FG.
- `MS01_FG_desk_twine_v01.png` — earlier fringe-bearing extraction; not for assembly.

### Static QA composites (not source layers)

- `QA_overlay_door_v02.png` — intact BG with registered-door DRAFT overlaid.
- `QA_overlay_windows_v02.png` — intact BG with registered-window DRAFT overlaid; visibly fails at sill/mullion alignment.
- `QA_overlay_roof_v01.png` — current roof mask over roofless v02 BG; approximate static fit, not cleared for motion.
- `QA_desk_dark_v02.png`, `QA_desk_light_v02.png` — alpha-edge check backgrounds for the desk FG; fringe persists on both.

## Checks performed

- Enumerated actual PNG dimensions and RGB/RGBA channels with ImageMagick `identify`.
- Composed the registered window, door and roof masks over their intended opaque BGs as static overlays. Window mask visibly overruns the sills/mullions; door shape is only approximate pending edge check; roof mask has a small seam/fragment issue. Preview paths are listed above.
- Composed desk/twine v02 over `#1A1E27` and `#E7E4DC`; red/white fringe persists. Tried an image-generation edit and a fresh transparent generation before retaining it only as DRAFT; neither cleared the fringe sufficiently.
- Verified BG plates are RGB opaque at the file level. I have not tested movement bounds, shifted underfill, actual MG alignment, or a rendered edit. Therefore none of the packages is represented as assembled or montage-ready.

## Known omissions / next work

1. Replace/repair desk-twine FG and clear alpha edges on dark and light backgrounds.
2. Re-register door and pane planes; ensure pane shapes sit inside the frames or use a coherent broken-glass/fragments plane matching the damaged-state BG.
3. Rebuild/clean the roof plane and verify it over the roof-off BG at 100%.
4. Normalize roofless layers to the shared exact canvas after choosing a correction that preserves scene registration.
5. Receive the separately owned MG; then test static overlay pairs, contact points, movement bounds, and BG underfill before marking any setup ready.
