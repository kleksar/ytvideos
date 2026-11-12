# Paper 028 — camera motion consultation

- Date: 2026-11-01
- Visible model/mode label in ChatGPT composer: **Extra High**.
- Chat: [Camera Motion Prescription](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae7b413-0b38-83eb-aaed-704d986f3248)
- Scope: the already assembled 028 EN rough cut; whole-frame movement on complete still dioramas only.

## Initial prompt

> You are the consultant in this already open ChatGPT Extra High project chat. The coordinator requirement is satisfied here; do not open another ChatGPT. One narrow motion-design task: recommend a restrained whole-frame camera-move pattern for the existing 028 EN rough cut, now that the user explicitly asked to add movement to the still images. Specs: 1080×1920, 30 fps; eight complete still dioramas with direct cuts; durations in order: S01 4.20s (Ahmad answers), S02 4.50s (king's order), S03 4.50s (construction), S05 4.50s (finished Taj and praise), S06 4.20s (no comparable builder), S07 4.60s (Ahmad and assistants after the punishment), S10 5.00s (Ahmad remembered behind the monument), S11 4.03s (king's question). End-to-start loop is S11→S01. Keep each still as one intact image: no parallax, no separated layers, no character/object animation; direct cuts remain. Give a compact shot-by-shot motion prescription using only gentle whole-image zoom/pan, with a consistent ceiling and a loop-friendly S11 ending. Specify approximate normalized start/end scale and position for each, plus easing/holds. Do not rewrite narration or design text cues; no export advice.

## Follow-up prompt

> The visible reply only shows status labels, not the prescription. Please provide the actual concise eight-row motion table now. Use the exact shot order and durations from my prior message; whole-frame only, no parallax or layer motion; state normalized start/end scale and focal position, easing, and how S11 ends to match S01. Keep each move subtle enough to preserve full-frame diorama readability.

The first response was visibly clipped after the S02 row began. A second focused follow-up asked for the missing rows; no new task was combined with it.

## Complete adopted recommendation

Focal position is normalized source space, `(0.500,0.500)` is center, X grows right and Y down. Keep scales in 1.020–1.045 and focal drift within 0.005. Apply each move to the entire intact diorama. All moves use smooth ease-in-out without overshoot and 0.2s opening/closing holds.

| Shot | Duration | Start scale / focal | End scale / focal | Move |
|---|---:|---|---|---|
| S01 — Ahmad answers | 4.20s | 1.020 / (0.500, 0.500) | 1.040 / (0.504, 0.498) | Slow push-in |
| S02 — King’s order | 4.50s | 1.040 / (0.504, 0.498) | 1.022 / (0.500, 0.500) | Gentle pull-back |
| S03 — Construction | 4.50s | 1.022 / (0.500, 0.500) | 1.043 / (0.497, 0.503) | Slow push-in |
| S05 — Finished Taj and praise | 4.50s | 1.043 / (0.497, 0.503) | 1.022 / (0.502, 0.500) | Gentle pull-back |
| S06 — No comparable builder | 4.20s | 1.022 / (0.502, 0.500) | 1.040 / (0.498, 0.500) | Slow push-in |
| S07 — Ahmad and assistants after punishment | 4.60s | 1.040 / (0.498, 0.500) | 1.022 / (0.501, 0.503) | Gentle pull-back |
| S10 — Ahmad remembered behind monument | 5.00s | 1.022 / (0.501, 0.503) | 1.044 / (0.499, 0.497) | Very slow push-in |
| S11 — King’s question | 4.03s | 1.044 / (0.499, 0.497) | 1.020 / (0.500, 0.500) | Slow pull-back; settles to opening pose |

The ending pose equals the S01 opening pose exactly, so the S11→S01 loop can cut without a camera-position jump. Palmier keyframes use the prescribed scales and focal coordinates converted to normalized top-left position.
