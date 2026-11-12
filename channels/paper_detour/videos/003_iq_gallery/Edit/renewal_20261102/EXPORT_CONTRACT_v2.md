# IQ Gallery renewal — export contract

- 1080 × 1920, 30 fps, 1800 frames / 60 s, Rec. 709, H.264.
- Thirteen original portrait scenes, except the replacement wider Kasparov shot, straight cuts; existing name/IQ titles offset down 173 px, 4-frame fades. Gentle whole-image motion/depth with G08 grain where viable.
- Preserve existing 60-second music AAC at original 44.1 kHz stereo without re-encoding or added sounds. Final file receives the complete original audio stream by packet copy: Palmier reports its source as 1799 timeline frames. This is an intentional exception to 48 kHz delivery convention to preserve the original mix exactly. No narration exists in the source.
- No YouTube update or publication in this task. Existing title/description and their IQ-estimate caveat remain unchanged.

## Frozen native export mapping

Project 2675DD26; timeline 9D6684B4; source timeline read `motion_timeline_v2.json`; motion run `../ImageMotion/4c38474c25edbe867ca4/run.json`. Palmier H.264 Match Timeline; raw output `../../Work/renewal_20261102/palmier_raw_v2.mp4`, then stream-copy video and complete source audio into `../../Deliverables/003_iq_gallery_renewal_20261102_v2.mp4`. Pixel format yuv420p, progressive, limited range, bt709 primaries/transfer/matrix; square pixels. Bitrate, GOP, profile and codec internals AUTO_ENGINE_MANAGED. H.264 quality and limits measured during QA. Source music `../../Source/Audio/iq_gallery_music_mix_20261101.m4a`, AAC stereo 44100 Hz, start zero, duration 60 s; no gain, fade, remix, speed or added sound. READY_TO_RENDER after timeline/settings and scoped lifecycle audit; quality decision: generated Kasparov 941x1672 is softly upscaled for 1080x1920, inspected pilot.

Revision v2: fixed scene 9 head crop with framing-safe, centered 1.06 scale and gentle horizontal movement; other clips cached unchanged. Previous export not delivered.
