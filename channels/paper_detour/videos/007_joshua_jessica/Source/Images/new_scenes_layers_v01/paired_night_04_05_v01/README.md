# Paired night beats 04/05 — image set v01

**Status: PASS for independent static/t0/t4 still review.** Continuous motion has not been rendered or reviewed.

Canvas target: 941×1672 px. Compositing order: **BG → MG → FG**. The original ImageGen masters `masters/04_old_messages_master_v01.png` and `masters/05_reply_card_master_v01.png` are retained as visual/story references. Canonical masters are new layer-first composites at v02; they do not claim pixel equality with those v01 references.

| Plan | Canonical master | Layers | t0 → t4 positions | Actual check / status |
|---|---|---|---|---|
| 04 — old messages | `masters/04_old_messages_master_v02_layered.png` | `layers/04_old_messages_BG_v02.png`, `_MG_v02.png`, `_FG_v02.png` | BG `0→+4`; MG `−8→0`; FG `−20→−9` (net `+4/+8/+11`) | All layers are 941×1672; BG RGB opaque, MG/FG RGBA. Master is byte-identical to t0 preview. t4 uses a mirrored 4px BG left-edge extension. Contains three blank physical message cards; no text/UI. Actual t0/t4 and cyan matte inspected. Independent review passed recomposition, physical-card read, mirrored BG fill and contacts; continuous motion unverified. **PASS for tested stills** |
| 05 — reply card | `masters/05_reply_card_master_v02_layered.png` | `layers/05_reply_card_BG_v02.png`, `_MG_v02.png`, `_FG_v02.png` | BG `0→+4`; MG `−11→−3`; FG `0→+11` (net `+4/+8/+11`) | All layers are 941×1672; BG RGB opaque, MG/FG RGBA. Master is byte-identical to t0 preview. t4 uses a mirrored 4px BG left-edge extension. One blank physical card rests on the laptop screen plane; no UI/text. Actual t0/t4 and cyan matte inspected. Independent review passed recomposition, screen-perspective/contact read and no-UI treatment; continuous motion unverified. **PASS for tested stills** |

## Plan 04 — layer map

| Role | Exact file | Dimensions / alpha | t0 position | t4 position |
|---|---|---|---|---|
| Master | `masters/04_old_messages_master_v02_layered.png` | 941×1672 RGB | Canonical composite | — |
| BG | `layers/04_old_messages_BG_v02.png` | 941×1672 RGB opaque | x=0 | x=+4 |
| MG | `layers/04_old_messages_MG_v02.png` | 941×1672 RGBA | x=−8 | x=0 |
| FG | `layers/04_old_messages_FG_v02.png` | 941×1672 RGBA | x=−20 | x=−9 |

Source reference: `Source/Images/03_message_laptop_master_v03.png`. ImageGen created the medium over-shoulder v01 shot, with Joshua’s hand by the trackpad and three blank paper cards arranged toward the laptop. BG removes Joshua, chair, laptop and cards while retaining the room, tabletop and existing props. MG carries Joshua, hand, chair, laptop and its immediate desk-support patch as one group. FG contains the three separate blank message cards and their contact shadows. MG v01 was 941×1671; v02 adds one transparent bottom row without shifting visible pixels. The v02 t0 composite, `previews/04_old_messages_v02_t0_BG0_MGminus8_FGminus20.png`, is the canonical master. The 4s endpoint is `previews/04_old_messages_v02_t4_BGplus4_MG0_FGminus9.png`; its first 4px of BG are mirrored into the exposed left edge for that preview only. The cyan matte check is `previews/04_old_messages_v02_t0_matte_cyan.png`.

Plan 04 t0/t4 previews were visually checked over the actual BG. The hand remains by the trackpad; laptop base and desk support travel with the subject group; cards retain a table/input-surface relationship. Independent review passed alpha-edge scene read, endpoint safety, exact recomposition and hand/laptop/table/card contacts. The three cards move +7px relative to the BG tabletop across the t0/t4 stills. Still endpoints do not prove motion through intermediate frames.

## Plan 05 — layer map

| Role | Exact file | Dimensions / alpha | t0 position | t4 position |
|---|---|---|---|---|
| Master | `masters/05_reply_card_master_v02_layered.png` | 941×1672 RGB | Canonical composite | — |
| BG | `layers/05_reply_card_BG_v02.png` | 941×1672 RGB opaque | x=0 | x=+4 |
| MG | `layers/05_reply_card_MG_v02.png` | 941×1672 RGBA | x=−11 | x=−3 |
| FG | `layers/05_reply_card_FG_v02.png` | 941×1672 RGBA | x=0 | x=+11 |

Source references: plan 04 v01 for the same night-room/character palette and `Source/Images/04_reply_card_master_v01.png` for the physical-card metaphor. The v01 composition is a tighter, distinct screen close-up with the laptop, hand and same lamp/window context. BG removes Joshua, laptop and card while retaining the room, desk and existing props. MG carries the whole laptop/hand and its immediate table-support patch together. FG is one blank physical paper card with its soft contact shadow, aligned to the screen perspective; it is not a digital panel. FG v01/v02 were rejected diagnostics because they expanded the paper across the laptop; v03 was generated on a 981×1602 canvas. To create v04, ImageMagick mechanically cropped its alpha region `540×338+200+834`, resized it to `444×278`, and placed it at `+238+676` on a 941×1672 transparent canvas. No new semantic content was painted in this registration step. The t0 layer composite `previews/05_reply_card_v02_t0_BG0_MGminus11_FG0.png` is canonical; t4 is `previews/05_reply_card_v02_t4_BGplus4_MGminus3_FGplus11.png`, using mirrored 4px BG left fill for that preview only. Matte check: `previews/05_reply_card_v02_t0_matte_cyan.png`.

Plan 05 t0/t4 previews were visually checked over the actual BG. The single card remains inside the screen plane with visible paper edges/contact shadow and safe bezel margins. Independent review passed screen/card registration, laptop/table contact, matte-edge scene read, safe margins and no-UI treatment. The physical card moves +3px relative to the screen across t0/t4. Still endpoints do not prove continuous motion.

## Excluded diagnostics

- `layers/04_old_messages_MG_v01.png` is the ImageGen source for the registered v02 copy; `layers/04_old_messages_FG_v01.png` is the source for the v02 card group.
- Plan 05 FG v01/v02/v03 outputs are kept for provenance but are not importable: they cover too much of the laptop or have a non-target canvas. The exact reviewed import is `layers/05_reply_card_FG_v02.png` with the v02 canonical master; static/t0/t4 review passed.
- No voice, audio, video, timeline, or Palmier project was created or changed.
