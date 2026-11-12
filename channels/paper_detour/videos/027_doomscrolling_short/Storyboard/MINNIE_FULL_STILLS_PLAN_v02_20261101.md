# Minnie Freeman — full-still assembly plan v02

**Current story:** English script candidate v03 with the existing Lawrence voice recording. This version replaces the v01 image set with the approved Paper Detour paper-diorama look. The Palmier timeline keeps the same 35-second voice-sync cut points and uses the new v05 images.

**Format and visual method:** Paper Detour Short, 1080×1920 at 30 fps. One complete static 9:16 paper diorama per scene, direct cuts, and no BG/MG/FG, cutouts, masks, parallax, zoom, or animated body parts. The exact S01 media is reused at the end to close the voice's open phrase. No ordinary subtitles, new audio, music, or SFX are added.

**Style references:** the user-approved Paper Detour 004 still at `channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png` sets the material, miniature depth, light, and shadows. Earlier Minnie images are story-continuity references only. Current production stills are in `Source/Images/minnie_v05_paper_diorama/`; image prompts were prepared in the ChatGPT project conversation “Промпты для ImageGen” with the visible mode **Extra High**, then rendered with ImageGen.

## Scene order and cut points

Timeline frames use half-open `[start, end)` ranges at 30 fps. Cut points follow the existing voice alignment and place visual changes near the story's key nouns and actions.

| Scene | Frames | Approx. time | Still | Beat |
|---|---:|---:|---|---|
| S01 | 0–173 | 0.00–5.77 s | `Source/Images/minnie_v05_paper_diorama/S01_hook_blizzard.png` | Cold open: Minnie leads the pupils through the blizzard. Destination and rescue remain hidden. |
| S02 | 173–300 | 5.77–10.00 s | `Source/Images/minnie_v05_paper_diorama/S02_door_blown.png` | The entrance door has blown inward. Windows and roof remain intact. |
| S03 | 300–420 | 10.00–14.00 s | `Source/Images/minnie_v05_paper_diorama/S03_windows_broken.png` | Windows are broken; the roof is still attached. Minnie recognizes the danger. |
| S04 | 420–516 | 14.00–17.20 s | `Source/Images/minnie_v05_paper_diorama/S04_farmhouse_distance.png` | The farmhouse is visible only at a great distance through a broken school window; all pupils remain inside and untied. |
| S05 | 516–626 | 17.20–20.87 s | `Source/Images/minnie_v05_paper_diorama/S05_twine_memory.png` | Earlier classroom memory: a boy plays with the ball of twine as Minnie notices it. |
| S06 | 626–716 | 20.87–23.87 s | `Source/Images/minnie_v05_paper_diorama/S06_pupils_wait.png` | Minnie has connected the pupils; they wait inside under the intact roof. |
| S07 | 716–780 | 23.87–26.00 s | `Source/Images/minnie_v05_paper_diorama/S07_roof_gone.png` | The roof is gone; all pupils remain inside and waiting. No child is carried yet. |
| S08 | 780–870 | 26.00–29.00 s | `Source/Images/minnie_v05_paper_diorama/S08_blizzard_crossing.png` | The journey begins; Minnie carries the youngest, while twelve pupils walk toward the distant farmhouse. |
| S09 | 870–960 | 29.00–32.00 s | `Source/Images/minnie_v05_paper_diorama/S09_near_loss.png` | The same group presses on through a darker storm. Twelve walkers are arranged in two rows of six, plus the youngest carried by Minnie. |
| S10 | 960–1020 | 32.00–34.00 s | `Source/Images/minnie_v05_paper_diorama/S10_farmhouse_arrival.png` | All thirteen pupils reach the farmhouse and remain gathered outside the threshold. |
| S01 repeat | 1020–1050 | 34.00–35.00 s | **Same media as S01** | Exact S01 media returns as the final voice trails off on “connected by—”. |

S07's 64-frame hold and S10's 60-frame hold are short impact beats kept on the roof-loss and arrival turns. They are deliberate and have no gaps.

## Visual continuity and review

- The ten source images are complete, opaque, same-canvas 941×1672 PNGs. Each shows the whole scene; the montage does not separate or animate its contents.
- S04 is an illustrative spatial reconstruction of the distant house through a classroom window; the historical script does not establish that Minnie saw it from the school.
- S07 keeps the youngest child with the other pupils. Carrying begins in S08, matching the spoken sequence.
- The v05 contact sheet is `Source/Images/minnie_v05_paper_diorama/QA/CONTACT_SHEET_v01.jpg`. The render contact sheet is `Edit/Palmier/Automation/QA/PD027_Minnie_PaperDiorama_v02_render_contact.jpg`.
- S09 was inspected at full size: twelve walking pupils appear as two staggered rows of six, plus the youngest carried by Minnie. This is a coordinator visual count, not an independent review.
- The preview fully decodes and is 1080×1920 at 30 fps. Only representative frame samples were reviewed; a full 1× playback and human audio listening remain open.
- The preview is in `Edit/Previews`, not `Deliverables`. It has not been published.
