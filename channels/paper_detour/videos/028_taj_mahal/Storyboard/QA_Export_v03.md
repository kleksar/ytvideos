# Export QA — Paper Detour 028 English v03

Date: 2026-11-02. Current local technical delivery, exported from the repaired Palmier timeline. No publication performed.

## Source and saved edit

- Project `25A8FF9A`; timeline `8565580B`, `028 Rough Cut EN v02 Grain`.
- Before repair snapshot `2372786F`; completed snapshot `CF126579`.
- Top-down stack: V3 paper accents `D5DF93A0` → V2 film grain `7C1E42B1` → V1 Main `DD050875` → A1 Dialogue `F5723FD2`.
- Grain clip `29CFE306`, media `BD49321B`, frames [0,1066), normal blend, opacity 1, no edge fades, auto-fit centered to canvas (normalized width/height 1). Alpha ×0.4 is baked once in the full-length overlay. Existing seven cue clips, eight scene clips and dialogue clip, including keyframes, were compared before/after and are identical.
- Read-only project.json verification confirmed the grain media, clip and track persisted on disk. No project files were edited manually. Original v01 timeline was preserved.
- Export job `B012B7F1-E6D5-43A1-9BC4-3B279D0891AA` completed at 100%. Palmier picture retained in `Edit/Previews/028_en_v03_palmier_grain_under_text_20261102.mp4`.
- Full MCP tools/list contains 58 tools. Earlier missing-command conclusion was caused by truncated display output, not missing edit capabilities. Capture and parse full responses before assessing capability.

## Current file and verification

- Delivery: `../Deliverables/028_taj_mahal_en_short_1080x1920_30fps_v03_grain_voice192_20261102.mp4`
- Size: 47,531,470 bytes. SHA-256 `11944d356b07ca8dbaf73e2d3502bbd6a5db240e6cf8262d74ec8f38af73bbf3`.
- H.264 High, 1080×1920, yuv420p, 30 fps, 1066 decoded frames, 35.533333 s, measured 10,499,892 b/s.
- AAC-LC mono 44,100 Hz, measured 192,112 b/s, 35.527007 s. Authorized accepted MP3 re-encode via aac_at CBR 192k; no new voice/music/SFX.
- All 1066 H.264 packet hashes match Palmier export after the authorized audio mux. Full-file ffmpeg decode with -xerror passed.
- Audio EBU R128: −24.1 LUFS integrated, 1.9 LU LRA, −4.8 dBFS true peak.
- Composited MCP frame 30 confirms cue → grain → scene order. Nine exported frame samples at 0,30,130,300,560,780,880,1025,1065 were visually inspected in `QA_Grain_v03_contact.png`: scenes and text remain legible, frame coverage reaches the end.
- Compared decoded grayscale 270×480 samples against grainless v01 at 30,31,233,234,235,467,468,469,701,702,703,935,936,937,1064,1065. Mean absolute residual 1.117–2.183 /255; adjacent residual changes 0.268–0.599 /255 show changing grain, including every internal seam and the final frames. This is a technical sampled check, not a perceptual playback judgment. Raw metrics in `QA_Grain_v03_metrics.json`.

## Review limits and history

- v03 was not fully reviewed at 1× with sound; subjective pronunciation, sync and seam visibility during continuous playback remain unconfirmed. No independent AV reviewer was used. Do not claim a complete perceptual acceptance.
- The previous flattened v02 delivery was removed after v03 passed the above checks and after checking it was not referenced as imported source in this project. Its historical QA remains in `QA_Export_v02.md`; source overlays and previews were preserved.
- No SRT, upload, publication or YouTube mutation occurred. Packaging draft remains unchanged. Next step: full final playback review, then a separately authorized YouTube release.
