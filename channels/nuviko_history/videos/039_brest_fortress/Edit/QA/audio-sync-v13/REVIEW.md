# V13 sound revision

Film `Work/rebuild-early-20261106/previews/full_review_v13.mp4`, SHA-256 `09f75673550c4322a1fb5a2d9d7b248e64095765dc4dfa136ebdb245c7913ad5`. New mix `Source/Audio/recovered_20261106/rebuild_full_mix_draft_v03.wav`, SHA-256 `c8da5d0bad8a8bb60837e30a681c7b60bbdfc26c0b65375b8ec5724d6f526563`. Source is v12 mix with additional delayed, faded artillery gain 0.13 at 55.0 s and water gain 1.22 at 239.6 s, same files and envelopes as v02. The pre-existing effects are retained; approximate resulting gains are 0.19 and 1.26. Original soundtrack, timings and outro retained.

Five-second mono 8 kHz RMS difference against original recovered soundtrack: 55–60 s -25.2 dB relative to soundtrack, 240–245 s -30.5 dB; previous version -35.2 and -60.4 dB. This numerical difference cannot establish subjective audibility, balance or speech intelligibility. V13 MP4 integrated loudness -18.8 LUFS, true peak -0.7 dBTP; see `loudness.txt`.

Video stream copied, not re-encoded: FFmpeg compressed stream SHA-256 for V12 and V13 both `18388cd24b182142d0fc0c9ba67f3640932715278a85ad70a45beed94d5ff8c6`. Subtitles and image content therefore unchanged; checks against prior map and sampled frames remain applicable. Original source and narration mapping are unchanged; audio mix differs only at intended effects. Audible mix, pronunciation and speech-to-caption timing remain UNVERIFIED; no claim of listening is made.

Decoded output audio versus v03 mix, in 622 matching 1 s blocks: minimum Pearson correlation 0.999900, median 0.999982; details `signal_correlations.json`. This verifies signal correspondence, not hearing.

Mix change scope check, both WAVs decoded to 8 kHz stereo: same 4,978,934 samples per channel, matching timeline. Only seconds 55–59 and 239–247 have sample differences above 1e-6; outside these intervals maximum absolute difference is 1.2e-7. Thus narration placement and original soundtrack timing remain unchanged in the mix; the caption timing map does not need a new global shift. This comparison does not establish that the original word map is aurally accurate. Full details `mix_change_scope.json`.

End-screen on exact V13 visually sampled at 612.4, 617.3 and 622.2 s, evidence `end_screen_sheet.jpg`; open area persists and scene remains visible. Native YouTube elements are not configured. V13 English sidecar review draft `Work/rebuild-early-20261106/previews/full_review_v13_en_draft.srt`: all 192 cues / 1,555 words match caption map text and first/last-word times within 2 ms (`srt_map_check.json`); soundtrack time mapping remains unchanged through the V13 mix scope check. Source alignment, semantic segmentation and subjective playback remain UNVERIFIED; this is a draft, not an accepted accessibility track.

V13 full video and audio decode completed with `ffmpeg -v error -xerror -i ... -map 0:v:0 -map 0:a:0 -f null -` exit code 0. Container reports 2560×1440, 30 fps, 18,671 frames, 622.366667 s, AAC stereo 44.1 kHz.
