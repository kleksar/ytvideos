# Export QA — Paper Detour 028, English v02 grain

Date: 2026-11-02  
Historical receipt: superseded by `QA_Export_v03.md`; v02 delivery removed after verified replacement.

Status at v02: local MP4 render is technically verified and contains moving full-frame grain. The saved Palmier timeline has not yet been updated with that layer; see the limitation below.

## File

- Delivery: `../Deliverables/028_taj_mahal_en_short_1080x1920_30fps_v02_grain_voice192_20261102.mp4`
- Size: 138,421,176 bytes
- SHA-256: `1ff6a77af5e162f63e240e405f819fa6dabc934c804067a2c52967d375008944`
- Source picture: accepted v01 Palmier preview, preserving its scene order, camera motion and phrase accents.
- Accepted voice source: `../Source/Voice/lawrence_v01/voice_en.mp3`. The user authorized re-encoding this source to AAC-LC mono 192 kb/s and muxing it with the copied H.264 stream.

## Measured streams

- Container: MP4, 35.533333 s
- Video: H.264 High, 1080×1920, yuv420p, 30 fps, 1066 decoded frames, 35.533333 s, measured 30,962,929 b/s
- Audio: AAC-LC, mono, 44,100 Hz, 192,112 b/s, 35.527007 s
- The accepted H.264 stream was copied during the audio mux; packet hashes matched the pre-mux video candidate.
- Full-file FFmpeg decode completed with `-xerror` and no decode errors.
- EBU R128: −24.1 LUFS integrated, 1.9 LU LRA, −4.8 dBFS true peak.

## Grain pass

- Source: `../../001_radio_game/Shorts/02_decoder/Source/Graphics/director_trial_20261031/film_grain_vertical_8s_prores4444.mov` (540×960, ProRes 4444 with alpha, 30 fps, 240 frames).
- Prepared overlay: `../Edit/Overlays/028_film_grain_full_length_v01_540x960_30fps_40pct.mov` (ProRes 4444 with alpha, 540×960, 30 fps, 1066 frames, 35.533333 s).
- Construction: repeated source with six-frame / 0.2-second linear crossfades starting every 234 frames / 7.8 seconds; cropped only at the final frame count. Source alpha was multiplied by 0.4 once. No head or tail fade was applied.
- Seam samples: frames around 234, 468, 702 and 936 were checked. Mean adjacent alpha deltas at those seams were 5.64–6.08, comparable to ordinary neighboring source frames (about 6.05); no extra seam jump was detected in those samples. Grain changes across adjacent frames.
- Visual export inspection: nine scene/cut/end samples are in `QA_Grain_v02_contact.png`. The texture is present across the full picture and the final question remains legible in the sampled cue frame.

## Playback and limits

- The delivery MP4 was played in QuickTime Player from the first frame to the final frame. The elapsed position reached 35.534 seconds and the last-frame question was visible. QuickTime did not expose the selected speed value through its accessibility tree, so this run is recorded as full playback with speed unverified rather than a confirmed 1× review.
- The AAC stream decodes and its measurements are recorded above. Subjective loudness, pronunciation and sound quality were not independently confirmed by listening.
- Palmier became unresponsive after the 2.27 GB overlay was selected for import. Reopening the project in a separate Palmier window confirmed that `028 Rough Cut EN v02 Grain` has V2 cues, V1 scenes and A1 Dialogue; the overlay is in the media bin but is not on the timeline. Episode 031 remained open and untouched. To deliver this episode's requested grain effect, v02 was composited externally over the accepted v01 preview. That preview is already flattened, so the grain sits above its phrase accents. The sampled cue is still legible, but the output does not satisfy the preferred compositing order of scene → grain → text.
- A clean recovery snapshot, `028 v02 before grain layer 20261102`, is saved on the isolated v02 timeline. Place the overlay as V2 below cues moved to V3, verify the full span and seams, then export from Palmier to replace this output. The original v01 timeline remains unchanged.
- No new narration, music, SFX, mix, SRT, upload or publication was created. Subjective AV review by an independent reviewer was not performed. YouTube Shorts card fit remains unverified because no upload draft was created.
