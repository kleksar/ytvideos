# Generation log — Paper Detour 035 paper dioramas v01

## Inputs and setup

- **Tool:** built-in `image_gen` via Codex; nine separate full-image generation calls. No CLI/API fallback.
- **Prompt record:** [`VISUAL_BIBLE_AND_PROMPTS_v01.md`](../../Production/VISUAL_BIBLE_AND_PROMPTS_v01.md). The shared block was combined with the corresponding scene prompt. Later generations for S01, S03, S07 and S09 tightened the scene block after review; those final prompt differences are recorded there.
- **Extra High consultation:** Google Chrome, visible label `Очень высокий`; [Visual Bible + 9 Production Prompts](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae7d859-b140-83eb-947e-f50dfab66cf5).
- **Style references on every call:** `channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png` and `channels/paper_detour/videos/033_time_stop/Source/Images/paper_v01/S01_v01.png`. Use was limited to paper craft, depth and light.
- **Additional per-scene references:** S06 used S05 for camera/framing/light only; S07 used S03 for early-form body organization only; S08 used S01 for broad animal treatment and left-right order only; S09 used S02 for generalized early anatomy only.
- **Accepted image size:** all nine files are RGB PNG, 941×1672 px (portrait ratio 0.5628, approximately 9:16), with no resizing or stretching. The loop repeats the exact S01 file.

## Per-frame status

| Frame | Source image_gen result | Workspace file | Status / inspection |
|---|---|---|---|
| S01 | `exec-42ec6075-5229-440d-8ad7-a4a0ffcb8209.png` | `S01_v01.png` | **ACCEPTED.** Two distinct forms read left/right, no habitat/set dressing, paper depth and attachment visible. This is the opening master and is reused unchanged. |
| S02 | `exec-9e7cd5a0-6271-4634-b9a1-ea1409b482f4.png` | `S02_v01.png` | **ACCEPTED.** Full early-form body, several similar connected limb pairs, neutral stage. |
| S03 | `exec-d942a819-5c73-4065-9e7c-ce1eebd18308.png` | `S03_v01.png` | **ACCEPTED.** The front pair stands out in framing without a modern club or strongly spined spear. |
| S04 | `exec-e2e799f2-7245-45b0-a57c-a0b012c3ff17.png` | `S04_v01.png` | **ACCEPTED.** Two separate modern outcomes on one stage; no connecting line or direct ancestry claim. |
| S05 | `exec-e2fdc5a7-ee20-4813-8600-2bdefd9be86a.png` | `S05_v01.png` | **ACCEPTED.** Spearer appendage remains connected; spines and layered paper detail are visible; no prey/action. |
| S06 | `exec-45456e33-fb04-4955-9a70-cf82ca0719c2.png` | `S06_v01.png` | **ACCEPTED.** Matching macro view; thickened terminal club remains part of connected appendage; no strike/action. |
| S07 | `exec-5a20bd15-559f-4d85-a88a-3c824f4e318e.png` | `S07_v01.png` | **ACCEPTED.** Early form with front pair emphasized by light and composition; no completed weapon. |
| S08 | `exec-3cc5e74c-60a4-4b5b-8df3-ac90ade704ad.png` | `S08_v01.png` | **ACCEPTED.** Returns to spearer-left/smasher-right; both limbs stay connected; contrast is clear. |
| S09 | `exec-14a4aa64-852c-4d88-a2e6-039acfc68eb2.png` | `S09_v01.png` | **ACCEPTED.** One simple limb remains attached to the visible body; no spines or club; composition cuts into S01. |

## Rejected iterations

| Frame | Source image_gen result | Decision |
|---|---|---|
| S01 first draft | `exec-57abdf4e-35cc-4c10-80f6-b55351c645f2.png` | **REJECTED.** It introduced coral/reef set dressing not in the storyboard. Replaced by S01 above with a minimal neutral stage. |
| S03 first draft | `exec-f0b515f2-a897-4072-ab29-45710706ccfa.png` | **REJECTED.** The front pair became oversized, spined claws, suggesting already completed spear specialization. Replaced by a more moderate early form. |
| S07 first draft | `exec-6c78d094-780c-46ba-83d7-f18f16b1d651.png` | **REJECTED.** The front pair again read as a finished spiny spear. Replaced with a form highlighted by framing/light with plain tapered ends. |
| S09 first draft | `exec-075edf75-b18c-4f28-aa88-9e0d266f10aa.png` | **REJECTED.** Terminal edge was too visibly spined and weapon-like. |
| S09 second draft | `exec-018c93ce-166c-42bb-8f4e-c705db54785b.png` | **REJECTED.** The limb still read too much like a claw. Replaced by the simpler smooth terminal plate in S09 above. |

## Visual QA

- Opened every actual workspace PNG at full frame beside approved Paper Detour 033 S01. Compared scene material and light with the two channel references; inspected the large appendage, terminal club and S09 joint/attachment details at closer view.
- **ACCEPTED:** all nine actual files are complete, opaque RGB paper dioramas with visible layered material, edge light and contact shadows. No in-image text, watermark, article, fossil, researcher, proof diagram, prey or action was found. Frame content matches the nine storyboard beats and the left/right reading in S01/S04/S08.
- This is coordinator visual acceptance against the channel standard; no independent reviewer was assigned. It does not verify scientific anatomy beyond the reviewed story constraints, timing, animation/edit quality or the final loop in a rendered video.
- S01 must be reused as the exact same PNG after S09. Image frame acceptance does not yet authorize import to Palmier or verify an edited/exported seam.
