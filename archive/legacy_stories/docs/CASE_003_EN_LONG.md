# CASE_003 — English Long, story 002: Pompeii

Updated: 28 October 2026. The timeline, storyboard, verification and delivery sections below describe an **earlier edit and export**, retained as historical notes. They are not the current edit. For the current canonical 1.05× timeline and export, see [AGENTS.md](../../../AGENTS.md) and [the export log](../../../channels/nuviko_history/videos/002_pompeii/Edit/002_canonical_export_105.md).

## Timeline and voice

- Palmier timeline `002_en_long`, ID `7D4B5711`, canvas 1920×1080 at 30 fps.
- Voice track `Voice`, track ID `14C4C2F6`; original clip `228EBE71` remains on A1 at `[0, 27185)` and references canonical media `CEC13D41`.
- Timeline duration is 906.167 s (15:06.17). The source audio is 906.188 s, so its file tail is about 21 ms longer than the existing frame-exact timeline placement. The narration transcript ends at about 905.84 s; the voice clip and placement were not changed during the visual edit.
- Canonical voice source: `videos/002_pompeii/Source/Voice/ElevenLabs_At_first,_lightweight_white_stones_began_.mp3`; library folder `Stories/002/Source/Voice`.

## Storyboard and edit

- All 30 original stills were copied without overwriting into `videos/002_pompeii/Source/Storyboard/`, byte-compared to the desktop originals, and imported through Palmier into `Stories/002/Source/Storyboard/`. Desktop originals remain untouched.
- The V1 montage uses all 30 images in 86 contiguous placements from frame 0 through frame 27185. The per-shot map and reproducible generator are `videos/002_pompeii/Edit/pompeii_montage_map.csv` and `videos/002_pompeii/Edit/build_pompeii_montage_map.py`.
- Timing follows the supplied narration transcript and montage plan, with short visual changes at phrase/story beats; maximum still hold is about 15 seconds. The opening alternates detail and people rather than running through the repeated guide-left images. The closing returns to everyday objects.
- Geographic assignments keep the Misenum observation and Pliny the Younger, Herculaneum's earlier overnight flows, Pliny the Elder's Stabiae episode, and Pompeii's later flow visually distinct. The Stabiae coast is not used as a Pompeii rescue scene; the Herculaneum illustration is confined to that passage.
- Each still has a subtle, smooth, alternating crop move (horizontal/vertical drift or small centered push) with no graphic titles or added music. Opening picture fade-in is 12 frames; closing fade-out 18 frames. Between-shot transitions are ordinary cuts; the available native operation exposes fades, not a true overlapping dissolve. The user allowed ordinary cuts.

## Verification and delivery

- Palmier was re-read after editing: V1 has 86 image clips covering `[0, 27185)` with no gaps or overlaps; all 86 have animated crop keyframes and 1.04× normalized width/height overscan. A1 still has the original voice clip at its original frame range. Other timelines retain their prior durations: `1_en` 104.100 s and `1_ru` 82.967 s.
- All 30 source images remain in `videos/002_pompeii/Source/Storyboard/`, byte-compared to the desktop originals, and are imported in Palmier under `Stories/002/Source/Storyboard/`. All 30 appear in the edit. The reproducible mapping is `videos/002_pompeii/Edit/pompeii_montage_map.csv`; the generator is `videos/002_pompeii/Edit/build_pompeii_montage_map.py`.
- Export completed to `/Users/diplomat/Desktop/pompei_story/002_en_long_Pompeii.mp4` (H.264, 1920×1080, 30 fps, AAC mono 44.1 kHz; video duration 906.167 s, container/audio duration 906.178 s). Full-file FFmpeg decode completed without errors. A full-file black-frame scan at 0.12 s threshold reported no black intervals. Ten exported anchor frames were inspected, including the Misenum/fleet, Herculaneum, Pompeii flow, Stabiae, excavation, and ending sections; the corrected overscan removes the previously observed narrow black edge, and faces/key details remain in frame. Two samples from the opening crop move show the animation in the final export. Audio-level checks at the beginning and end show non-silent signal, but are not a substitute for listening.
- **Audible playback was not verified.** The native Palmier window was unavailable to computer control and no audio-preview operation exists in the current project tools. A playback-capability report was sent to the Palmier team. Do not claim the voice was audibly reviewed or seams were confirmed by ear.
- The opening picture fade is 12 frames and the ending fade is 18 frames. Mid-shot changes are clean cuts; true overlapping dissolves are not exposed by the available edit tools. No new music or text was added.

## YouTube release and subtitles

Current local audio-quality revision: `videos/002_pompeii/Deliverables/002_en_long_Pompeii_105_audio192.mp4`, with separate `002_en_long_Pompeii_105_audio192.en.srt`. The former local canonical MP4 was removed after validation. See root `AGENTS.md` and `Edit/002_audio192_delivery.md`.

**YouTube API observation on 28 October 2026:** the audio192 export was uploaded to NuvikoHistory as [15reLbhKUNQ](https://www.youtube.com/watch?v=15reLbhKUNQ). Processing is `succeeded`, visibility is `public`, and the separate English caption track is `serving`. The private “History Documentaries” playlist (`PLXeReXm1udrM`) returned entries for both this ID and the previous `IyuRb-5HtuM` upon re-reading. A `videos.list` request did not return the previous video; the reason is unknown, so its deletion is not established. Full listening checks of the audio, subtitle synchronization and chapter timestamps remain outstanding.

**Earlier release history:** the previous `002_en_long_Pompeii_105_canonical.mp4` was uploaded as `IyuRb-5HtuM`; its processing had been recorded as `succeeded` and its visibility as `unlisted`, with a separate English caption track `serving`. The earlier upload `xy2w7uTm7_M` and mistakenly uploaded dynamic v14 `XL5Kf34QIxE` were deleted.
