# v10 — Single Grain Track

Project `8BE390BC`; timeline `3859ADEC`, **031 Rough Cut v10 Single Grain Track**. Source: actual user-modified v09 `29C64CD5`, preserved by snapshot before duplication; exact source snapshot and mutations in `../../Edit/SINGLE_GRAIN_RECEIPT_v10.json`. Post-edit snapshot `43A5A095`.

User requested a single independently switchable grain track and reported disabling/removing grain made the image disappear. At readback v09 had already changed to one full-frame original270×480copy on an unnamed track. Main16scenes,Accents11cues and Voice remained intact. Historical disappearance cause cannot be established from current state. Do not claim a proven Palmier bug or user misclick.

Prepared reusable8-second540×960ProRes4444alpha file by combining the previous four270×480regions with the same0/60/120/180frame offsets. No new audio or alpha multiplier. Applied full-frame at25%normal blend. Nine contiguous clips (8×240frames plus219frames) on **one Grain track** cover[0,2139). Track order: Accents,Grain,Main,Voice. Main/Voice/Accents compared to the actual source state: unchanged apart from new IDs. Original sources retained.

Acceptance check: temporarily hid only Grain by stabletrackId; actual Palmier capture650 retained scene and OFF NIGERIA and lost only grain. Restored Grain in finally and captured with grain visible. Actual target composites reviewed0,239,240,650,2138: first/last image present, no obvious central grain discontinuity or black seam in sampled stills. These are author still checks, not full1×playback or all-seams/export/independent AVQA. No final export or audio generation.

Single-track source/settings now canonical in `channels/paper_detour/Shared/Overlays/Film_Grain/README.md`; Palmier skill references updated. Saved project JSON read-only parsing confirms v10 and grain-track ID persisted. Final UI selection unverified because CUA screenshot was unavailable and AX returned a stale File menu; edit itself verified by API and saved JSON.
