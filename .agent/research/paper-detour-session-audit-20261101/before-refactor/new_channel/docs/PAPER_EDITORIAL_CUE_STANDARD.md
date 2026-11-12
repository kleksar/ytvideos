# Paper Detour — editorial cues for text and emotion

**Approved:** 1 November 2026, following the user's direction and a focused ChatGPT.com review in project **YT Видео**, with the visible model setting **Extra High**. Review chat: [Стандарт визуального монтажа](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae76c9c-64f8-83ed-b223-60bf1c0176fb).

## Core rule

Every visual element appears when it becomes meaningful to the viewer. The image and on-screen text follow the narration's reveal order, emphasize the words that matter, and convey a character's attitude through visible evidence. Do not reveal a later point early or add an emotion, motive, or relationship the story does not support.

## Enumerations

- Show each spoken list item as it is named. Keep the on-screen order aligned with the voice; do not display the full list before later items are spoken.
- In one scene, reveal the items with sequential text accents; when the story benefits from a new composition, use a direct cut to another complete diorama. Do not divide a scene into moving layers to present the list.
- Keep each item readable at the pace of the narration. If the list is too dense to read in time, revise the visual plan or cue timing rather than showing future items early.

## Human speech and quotations

- When a person's spoken line is the scene's important clue, reversal, expression of attitude, or emotional beat, show the selected words verbatim at the moment they are spoken.
- Use the final recorded wording and timing. Do not paraphrase the quote, strengthen its emotion, or add words the person did not say.
- Keep emphasized dialogue and quotations selective. Do not turn ordinary dialogue or the whole narration into continuous subtitles.

## Emotion, attitude, and relationships

- Stage emotion through concrete, legible evidence: gaze, facial expression, posture, gesture, distance between people, eyelines, framing, camera angle, and supported paper details.
- Match the visual shift to the point in the narration: show a change in attitude when it occurs, not before. Make relationships readable through how people face, approach, avoid, or leave one another.
- Treat unconfirmed inner states as unknown. Do not present an inferred motive or feeling as fact; keep the image with observable behavior when the narration does not establish more.

## Typography and motion default for vertical Shorts

- Center the visible glyphs at `x = 0.50`; do not center the transparent PNG canvas. Use one approved visible cap height per line throughout the episode. Do not use the source PNG canvas dimensions or the old `0.055`/`0.11` ratios as a sizing default.
- Measure letter size from the cream face pixels, not the transparent PNG canvas or the orange shadow. For the approved Paper cream/orange title assets, the helper uses pixels with `alpha > 30`, `R > 160`, `G > 110`, `B > 70`, `G > 0.58R`, and `B > 0.50G` as the face mask. Measure the full alpha box separately; it includes the complete outline and shadow and sets the horizontal fit. Record authored line count per asset in the cue manifest. Per line, calculate `face_height_px = face_bbox_height / source_height × transform.height × canvas_height / line_count`; calculate the full rendered width from the alpha box. Set a shared target from `safe_width_px / max(full_alpha_width_px / face_height_px_per_line)` and round down to the nearest 10 px. The safe width must be approved for the episode; Short 008 uses 90% of its 1080 px canvas. Keep the same target for every cue. If an authored phrase cannot fit, revise its line layout or asset; never shrink one phrase automatically.
- Use [`normalize_paper_accent_cues.py`](../automation/normalize_paper_accent_cues.py) in dry-run mode before applying a batch. Supply the authored line-count manifest when the current assets are not already normalized. The tool snapshots the target timeline before editing, updates only accent transforms and positions, and verifies the final face height, optical center, and preserved opacity curves.
- **Short 008 calibration, 2026-11-01:** the alpha-box-only pass still left letter-face heights visibly inconsistent, so v06 was recalibrated from the cream face mask. At 90% safe width (972 px), N07 `DIDN’T WANT THIS / KIND OF RELATIONSHIP` is the limiting cue: maximum feasible face height 101.51 px; the selected shared target is 100 px. Its full alpha box renders 957.5 px wide (88.7% of canvas); the largest measured alpha-width/face-height ratio is 9.5755. All 57 active cue instances from 54 assets now use a 100 px face height per line; Palmier's 0.001 transform rounding yields at most 0.676 px height error. A03 `AGAIN` increased from 67.49 px to 100 px (1.48×). Three times its prior size would make the limiting title about 1,939 px wide, beyond the 972 px safe width. The final transform plan and visual checks are recorded in the episode's v06 note.
- Use three vertical levels for the title motion: enter from the lower level (`center_y = 0.20`, opacity `0`), rise to the reading anchor (`0.18`, opacity `1`), then leave from that anchor upward (`0.16`, opacity `0`). Hold the text at the same anchor and size while it is read. At 30 fps the standard relative keys are `0`, `4`, `D−5`, and `D−1`; a final cue held through the last frame may omit the exit when its cue sheet specifies that.
- Palmier's `position` keyframes describe the transformed PNG's top-left corner. Calculate those values from the cream face bounds so the visible letter-face center lands on the selected anchor; verify the full alpha outline and shadow at every motion level. Keep X fixed through the motion. Use another anchor only when the primary zone truly collides with a face or important clue, and preserve the same visible letter height.

## Paper and review constraints

- One scene remains one complete, static paper diorama with direct cuts. No scene parallax, moving layers, or animation of characters or their parts.
- Text accents should carry a story beat: question, contrast, clue, attribution, or answer. Prefer a compact phrase of about 2–5 meaningful words; omit isolated names, dates, or generic labels with no clear editorial job. Read the entire accent sequence alongside the narration to catch long unexplained gaps and unrelated title fragments.
- Text PNGs keep the episode's chosen safe-zone, consistent visible alignment, and approved entrance/hold/exit motion. Set one primary anchor and visible glyph height before importing; use only preflighted alternates. Keep words clear of faces, heads, animals, gestures, documents, and story clues; do not add chaotic position changes or shrink a single cue to rescue a collision.
- Time each accent to the final recording: begin on the first spoken trigger, become readable while the key phrase is being said, retain it through the final emphasized word, and begin the exit after that word. Record trigger/end words and exact frame/time from alignment. Re-time every cue after a change in script, recording, speed, or cut.
- Review every list item and selected quote against the final voice/alignment. Check each cue's appearance, readable hold, and disappearance in the actual composite at the spoken words and cut boundaries; confirm its entire path clears the composition. Then watch the assembled cut at 1× with sound and, as a clarity check, without sound. Alignment or isolated stills do not prove playback sync.

