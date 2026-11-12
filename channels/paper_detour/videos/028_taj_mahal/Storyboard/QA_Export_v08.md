# Final picture QA v08 - 2026-11-02

Current delivery: ../Deliverables/028_taj_mahal_en_short_1080x1920_30fps_v08_film_grain20_voice192_20261102.mp4
87562981bytes, SHA256 25de3654fa3d7b48f4551022caff7de354c151e0607eb251c09cd293998433c2.
H264 High1080x1920 yuv420p30fps,1066frames35.533333s,19512645bps. AAC-LC mono44100Hz192112bps35.527007s from the already authorized accepted MP3 re-encode.

Saved project25A8FF9A,timeline8565580B,snapshot6A0338CF. Shared15min grainmaster media2200F995 on clip29CFE306[0,1066),normalopacity0.20. Source masteralpha3x and grain-size preparation in shared Film_Grain README. Existing scenes/cues/dialogue and keyframes unchanged. User rejected45% sample as too strong and requested slightly weaker than25%;20% implements that request. Explicit final acceptance of20% has not yet occurred.

Palmier H264 job5511D56A-AC91-4428-BB85-711C2927E239 and ProRes job64637678-C343-4E44-AD60-4C9A3D6E927A completed. Final picture encoded from the ProRes picture master via libx264 medium CRF16 tunegrain, with accepted MP3 encoded to AAC192. This high-quality encode is deliberate; final picture was not stream-copied from stock H264. Source picture retained in Edit/Previews/028_en_v08_grain_prores_mezzanine_20261102.mov.

Full-file ffmpeg -xerror decode passed,1066frames counted. Actual ProRes and actual final MP4 cropped frame1s inspected; six final scene/cue/end frames inspected in QA_Grain_v08_contact.png. Grain remains across image while cue typography stays above it. At270x480 decoded grayscale, adjacent first pair mean absolute difference2.204/255; internal seam pairs239/240,479/480,719/720,959/960 deltas1.177,1.451,1.229,1.290/255. These are sampled technical checks, not a full1x perceptual seam review.

v04 was rejected and technically faulty alpha max1/255; v05 CRT stripes rejected. v06 export canceled after too-strong feedback; v07 completed but user requested lower strength. Old v04 delivery removed only after v08 technical checks and project media-reference check; historical working files and QA retained. Shared CRT masters are separate rejected-for028 effects, not film grain.

Full subjective1x playback with sound remains unverified. No independent reviewer; no upload/publication or new audio content.
