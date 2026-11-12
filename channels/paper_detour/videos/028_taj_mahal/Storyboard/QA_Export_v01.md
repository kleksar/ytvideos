# Export QA — Paper Detour 028, English v01

Date: 2026-11-01  
Status: review export verified technically; final delivery remains open due to audio encoding.

## File and project

- Review MP4: `../Edit/Previews/028_taj_mahal_en_short_1080x1920_30fps_voice_v01_palmier_audio64_review_20261101.mp4`
- Source Palmier project: `Paper Detour 028 Taj Mahal Montage Draft 20261101.palmier` (`25A8FF9A`)
- Source timeline: `028 Rough Cut EN v01` (`5F604C92`), snapshot `520475F5`
- SHA-256: `9ea4c67aa992df470c64649acef4283b7333d88c9b69e0a5cfb71720fcd4362e`

## Measured export

- Container: MP4, 44,428,621 bytes
- Video: H.264 High, 1080×1920, 30 fps, Rec. 709 / yuv420p, 1066 frames, 35.533333 s, approximately 9.93 Mb/s
- Audio: AAC-LC, mono, 44,100 Hz, approximately 63.8 kb/s, 35.533333 s
- Full `ffmpeg` decode completed with exit code 0 and no decode errors.
- `ebur128`: −24.2 LUFS integrated, 1.9 LU LRA, −4.8 dBFS true peak.

## Playback and visual checks

- The MP4 was opened in QuickTime Player and played at 1× through the final frame. The final king-question cue remained visible at the end.
- The audio stream is present and fully decodes. Subjective loudness, pronunciation and sound quality were not independently confirmed from the UI capture.
- Seventeen actual exported frames were extracted at indices `0, 27, 63, 107, 193, 293, 328, 463, 574, 593, 726, 784, 870, 883, 1005, 1038, 1065`. They cover every scene, selected word accents, the two cue/cut crossings, and both ends of the loop. Contact sheets are in `QA_Export_v01/contact_01.jpg` through `contact_05.jpg`.
- The sampled export frames preserve the full diorama composition; the visible phrase accents are legible in the sampled scenes, and the final question survives through the last frame. This is sampled frame inspection, not a claim of frame-by-frame visual inspection.
- The full playback ran, but no separate continuous playback recording was made.

## Open item

The channel delivery setting for mono dialogue is AAC-LC at 192 kb/s. Palmier exposed no audio bitrate control and exported approximately 63.8 kb/s. The accepted source voice is `Source/Voice/lawrence_v01/voice_en.mp3`, mono MP3 at 128 kb/s. Do not raise the bitrate on the already compressed AAC export. To meet the delivery setting, rebuild the audio stream from the accepted source and mux it with the verified H.264 video stream copied without re-encoding. That would re-render audio and has not been authorized as a separate action. The current MP4 is therefore kept under `Edit/Previews/`, not `Deliverables/`.

No new voice, music, SFX, mix, SRT, upload or YouTube mutation was made. Shorts phrase accents are already embedded as the accepted selective text layer; no duplicate subtitle track was added.
