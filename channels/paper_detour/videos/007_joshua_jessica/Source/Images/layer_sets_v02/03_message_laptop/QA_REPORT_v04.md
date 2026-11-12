# Plan 04 — message on laptop — v04 candidate review

**Status: NOT READY. No importable layers.** This is the current candidate for `03_message_laptop_master_v03.png`; it does not pass the independent source-registration review.

## Candidate files

- BG: [`03_message_laptop_BG_v03_whole_table_shared_with_04.png`](03_message_laptop_BG_v03_whole_table_shared_with_04.png)
- MG: [`03_message_laptop_MG_v04_original_left_edge_NOT_READY.png`](03_message_laptop_MG_v04_original_left_edge_NOT_READY.png)
- FG: [`03_message_laptop_FG_v02_book_reused_NOT_READY.png`](03_message_laptop_FG_v02_book_reused_NOT_READY.png)
- Canonical/t0: [`03_message_laptop_canonical_t0_BG0_MGminus8_FG0_v04_NOT_READY.png`](03_message_laptop_canonical_t0_BG0_MGminus8_FG0_v04_NOT_READY.png)
- t4: [`03_message_laptop_t4_BGplus4_MG0_FGplus11_v04_NOT_READY.png`](03_message_laptop_t4_BGplus4_MG0_FGplus11_v04_NOT_READY.png)

All candidates are full-canvas 941×1672 PNGs. BG is opaque RGB; MG and FG are RGBA. Positions are t0 BG 0/MG −8/FG 0 px and t4 BG +4/MG 0/FG +11 px. The strong-alpha MG bounds are x=0…931, y=564…1271; the book FG is inherited from a frame-edge crop and is not a motion-safe matte.

## Independent findings

The reviewer found t0 registration and the static contacts plausible, but the t4 MG shift moves the left-cropped hand/sleeve/table edge to about x=8, producing a hard internal cut. The layers also fail source registration: screen/hand/card edges double, with reported MAE 25.61 overall and 37.49 on the screen. Warm orange fringe remains over the room. These failures block import despite endpoint dimensions and simple recomposition.

The BG was derived from the whole-table clean plate shared with plan 05. The MG is the ImageGen cutout from `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-10079d4c-4e9a-45fd-b23a-0593b3c8f75b.png`; the book FG is reused from the earlier draft. All are diagnostic only. No source master was overwritten.
