# YouTube chapters — v02

- Episode: Paper Detour 045, English long film.
- Exact media: `/Users/diplomat/ytvideos/channels/paper_detour/videos/045_edmund_fitzgerald_last_voyage/Work/frame_overlay_v03/previews/edmund_fitzgerald_full_film_en_frame_v03.mp4`
- SHA-256: `c372b380c94b857fd746284114bf8922fcfaf467e1ca75a0322f43ba2dd0d0e3`
- Duration: 225.466667 s (6764 frames at 30 fps).
- Version: v02 chapter timing proposal, checked against accepted v03 MP4 frames and English SRT v02.
- Method: sampled frame pairs before/at each scene chapter boundary; compared adjacent SRT cues to avoid starting within the preceding sentence. At 01:18 the damage report begins at 01:17.440; at 01:46 the radio-reply introduction begins at 01:46.480; at 02:42 the first investigation explanation begins at 02:42.480; at 03:28 the closing unanswered-gap sentence begins at 03:27.920. Other markers align to the listed frame/scene transitions and adjacent narration.
- Coverage: all 10 boundaries sampled; each resulting section is at least 10 seconds, including the final section (17.466 s).
- Formal validation: syntax and measured intervals checked with `validate_chapters.py --media` against this exact MP4.
- Status: machine-checked with sampled frame and SRT boundary evidence; not full real-time playback checked, not a live YouTube chapter display check. Whole-second times are approximate.
- Current YouTube help checked 2026-11-05: first marker 00:00, at least three ascending markers, each chapter at least 10 seconds. https://support.google.com/youtube/answer/9884579?hl=en
