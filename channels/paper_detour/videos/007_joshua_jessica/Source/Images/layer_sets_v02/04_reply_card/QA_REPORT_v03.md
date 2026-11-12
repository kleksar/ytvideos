# Plan 05 — reply card — v03 candidate review

**Status: NOT READY. No importable layers.** The candidate is based on the selected `04_reply_card_master_v01.png` but includes a newly fitted screen card and revised MG movement.

## Candidate files

- BG: [`04_reply_card_BG_v03_whole_table_shared_with_03.png`](04_reply_card_BG_v03_whole_table_shared_with_03.png)
- MG: [`04_reply_card_MG_v03_shared_geometry_with_03_NOT_READY.png`](04_reply_card_MG_v03_shared_geometry_with_03_NOT_READY.png)
- FG: [`04_reply_card_FG_v02_book_reused_NOT_READY.png`](04_reply_card_FG_v02_book_reused_NOT_READY.png)
- Fitted blank reply card: [`04_reply_card_screen_card_v02_fitted_NOT_READY.png`](04_reply_card_screen_card_v02_fitted_NOT_READY.png)
- Canonical/t0: [`04_reply_card_canonical_t0_BG0_MGminus8_FG0_v03_NOT_READY.png`](04_reply_card_canonical_t0_BG0_MGminus8_FG0_v03_NOT_READY.png)
- t4: [`04_reply_card_t4_BGplus4_MG0_FGplus11_v03_NOT_READY.png`](04_reply_card_t4_BGplus4_MG0_FGplus11_v03_NOT_READY.png)

Each layer and endpoint is 941×1672. BG is opaque RGB; MG/FG are RGBA; endpoint stills are RGB. Positions are t0 BG 0/MG −8/FG 0 px and t4 BG +4/MG 0/FG +11 px. The fitted screen card is composited into the MG and moves with the laptop.

## Independent QA and blocker

Independent review found that t0 and t4 recompose exactly from the supplied layers, all three planes move by the planned +4/+8/+11 px, and the blank card, hand, laptop, loose cards and foreground book appear grounded in the stills. These are static endpoint checks; animation playback was not reviewed.

The set remains **NOT READY** because t0 is visibly recropped relative to `04_reply_card_master_v01.png`; a 50/50 overlay doubles the laptop contours, and the MG shows a strong orange fringe against cyan. The book FG is reused from the earlier crop. The fitted card is blank and contains no UI; its good placement does not correct the full-scene registration or matte defects. No original master was overwritten.
