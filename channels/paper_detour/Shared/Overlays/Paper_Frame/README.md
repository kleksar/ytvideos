# Paper Frame — approved v03

The approved thin animated frame applies to future Paper Detour films (16:9) and Shorts (9:16). It uses a 0.67 × 0.67 = 0.4489 normal-width factor along the straight sides, with smoothly blended corners, preserving the three original layers and the 16, 8 and 16/3 second movement periods. It is a separate straight-alpha overlay, not part of a generated scene. The user approved the second thinner preview on 2026-11-05.

## Masters and reproduction

- Long: `masters/paper-border-16x9-16s-v03.mov`, 2560×1440.
- Short: `masters/paper-border-9x16-16s-v03.mov`, 1440×2560.
- Both masters are verified 16-second, 30 fps, 480-frame ProRes 4444 loops with transparent centres. Exact checks and hashes: [validation](source/VALIDATION.md). Masters are local and not tracked by Git. Keep v02 assets unchanged for existing jobs.
- Rebuild from the versioned [source kit](source/README.md); use new output paths and verify the exact output before use. Do not substitute the older v02 frame.

## Montage

Use the master matching the canvas and format; don't stretch one orientation into the other. In a new Paper montage add it as the final item in `overlays`, for example (replace the path by the exact verified local master):

```json
{"role":"paper_frame","path":"/absolute/path/paper-border-16x9-16s-v03.mov","start_frame":0,"end_frame":1234,"x":0,"y":0}
```

Set `end_frame` to the exclusive frame count of that edit. The renderer loops this role and composites it after subtitles. Check exact orientation, canvas, identity/hash, full coverage, straight alpha, motion, edge continuity, loop boundary and subtitle visibility in a short sample and final MP4. Existing frozen plans and active renders keep their inputs. A final MP4 is opaque; the alpha exists in the overlay master.
