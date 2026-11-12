# Paper Detour 037 — depth preparation v03

**Date:** 2026-11-02  
**Status:** complete for all 73 images in storyboard v03. This records depth-map availability and file integrity only; it does not accept parallax quality or a rendered camera path.

## Inputs

- Exact scene map: [`storyboard_v03.md`](../../Storyboard/storyboard_v03.md), S01–S73.
- Exact PNG input list: [`depth_sources_v03.json`](depth_sources_v03.json), 73 entries.
- Config: [`prepare_depth_v03.json`](prepare_depth_v03.json); contains episode directory and source manifest only. No project or timeline IDs were set.
- Command: `python3 automation/image_motion/run.py prepare-depth --config /Users/diplomat/ytvideos/channels/paper_detour/videos/037_cost_of_living/Edit/ImageMotion/prepare_depth_v03.json`.
- Renderer: `DepthAnythingV2-small`, DepthFlow 1.0.1; helper version 1.0.0.

## Result

- All 73 entries reported `depth-ready` on the final cache-verification pass. The 73 image hashes resolve to 73 distinct cache keys.
- Every cache file exists under `/Users/diplomat/ytvideos/Shared/Image_Motion/Cache/depth/`, loads as an NPY array without pickle, has shape 518×924, dtype float32, and contains finite values.
- Exact scene-to-source hashes, depth cache keys, depth hashes, byte sizes and array ranges are in [`depth_manifest_v03.json`](depth_manifest_v03.json). The captured per-scene output is [`depth_prepare_receipt_v03.jsonl`](depth_prepare_receipt_v03.jsonl); the renderer log is [`renderer.log`](renderer.log).
- SHA-256: config `404aff2dc1b6605339e45ec8c711e4ffa430c7b292eb555aa6741b6406a994ba`; source manifest `9e3b8633da72fcfef4eddc3fc620814744c0fe22bd0f08ee6cb882e03e6594fb`; receipt `bb989911bcfa90b2f05b4a7d2930d0f97d350fa6120312f3a180f423e2e19b81`; depth manifest `2c0af34ec328611461eb13b0a9b81cdc6030e479b84d8e7c3572e1b5725e06ae`; renderer log `10074074338c5604b0f422e95bb172a09f49585d5a0b86bbb0b4c226099c6348`.

A fresh read-only lifecycle audit and non-executable plan were written before preparation: `Edit/MediaLifecycle/audit-motion-predepth-v01/` and `plan-motion-predepth-v01/`. Audit scope was `BOUNDED_NOT_EXHAUSTIVE`, with zero coverage errors; available packages and inaccessible/external consumer limitations remain as recorded in that report. No media was imported, moved or deleted. A separate read-only query of the live Palmier project list returned no project named or path-matched to episode 037; there is no baseline still timeline or explicit project/timeline ID to target yet.

## Not verified

The numeric depth arrays were checked for existence, loadability and finite values, not visually judged for object-level segmentation. No depth preview, camera motion or parallax clip was rendered. Edge exposure, depth ordering, overlap distortion and the final camera path remain UNVERIFIED until an actual still-image Palmier timeline, explicit project/timeline IDs, scene durations and per-scene motion plan are available and the image-motion render is inspected.
