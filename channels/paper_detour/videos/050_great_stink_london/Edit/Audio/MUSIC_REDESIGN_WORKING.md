# Music — Paper 050 redesign, working state

The user explicitly requested music during the visual rebuild. Preserve accepted narration, timing and speed, and create a separate full stereo mix only when the track and placement are selected. Existing voice: `Source/Voice/voice_en_v03_end_silence.wav` SHA-256 97e04a40368b7686ed28f16b97abb1d1b818aa97a187ff00cb4a4cb9c4f006db. Ten-second silent ending must be considered in the music plan.

Approved-catalog candidate for investigation, not final selection: Satiate - only percussion, Kevin MacLeod, ISRC USUAN1200057. Author's track details identify exact alternative and CC BY 4.0; explicit credit required in description, including title, artist, source and license, and changes. Source https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1200057 . Other catalogue options require separate verification. Avoid treating a candidate as selected or a machine mix as aurally accepted.

Pending: project-required personal ChatGPT consultation for creative music decision; retrieve verified exact track, select sections according to story, ensure license and attribution, construct stereo mix without changing voice timing, rebind word map to new mix, verify full mix and mono compatibility including listening, update render contract and QA. Subjective listening remains unverified; no new mix or track acquired yet.

## Trial v01

Creative consultation completed and recorded in `CONSULTATION_20261106.md`. Author's exact `No Piano Melody` alternative downloaded from https://www.scottbuckley.com.au/library/wp-content/uploads/2020/04/sb_signaltonoise_nomelody.mp3 (linked from https://www.scottbuckley.com.au/library/signal-to-noise/ ). SHA-256 `8e20b496b0614053565d4f43c80f469c84abd2aefb3ba01e29dfa813f49b9594`; MP3 44.1 kHz stereo, 354.353 s. Author requires CC BY 4.0 attribution in YouTube description; cite title, author, source, license URL and indicate cutting/mixing if used.

`mix_trial_v01.wav` SHA-256 `a2b9756cdaf6eb976459b5f40a6baa143c2414eb647c50e43052a7c2e7584335`: test only, voice unchanged at original placement; source music 0–110 s starts at film 105 s, linear volume 0.055, 4 s fade-in and 6 s fade-out, 44.1 kHz stereo PCM, 252.8 s. No other music. This is a rough technical experiment, not a selected track/placement or accepted mix. Tonal fit, intelligibility, stereo/mono playback, levels, peaks, voice preservation, edit timing, caption mapping, rights documentation and final export remain to be checked; playback UNVERIFIED. No automatic adoption into montage.

## Technical checks, 2026-11-06

FFmpeg ebur128 over full trial reports integrated -21.4 LUFS and true peak -2.8 dBTP. Both WAVs are 44.1 kHz, 16-bit PCM, 11,148,480 frames (252.8 s); original is mono and trial stereo. Direct sample comparison after duplicating the original mono to two channels found zero difference at 0–104 s and 216–252 s; at 105–215 s the difference is nonzero, consistent with the added music (difference RMS 155.028/32768, max 1160/32768). This does not assess intelligibility, subjective balance, music choice, mono compatibility or listening. Trial remains unaccepted.

## Trial v02

Technical-only alternate `Edit/Audio/mix_trial_v02.wav` SHA-256 `fe83beea1065bfe9f24aa025f08225b1367a160c35165f507303bbb577e6a629`: same voice and music placement as v01; music gain 0.14 instead of 0.055, fades unchanged. FFmpeg ebur128 full mix: -21.4 LUFS integrated, -2.7 dBTP true peak. v01's music alone over 0–110 s measured -44.4 LUFS; relative values do not establish audibility or intelligibility. Both trials remain unaccepted until the permitted checks; subjective listening UNVERIFIED.

If trial v02 is selected for a later review render, required description credit must travel with the exact edit: `Music: “Signal to Noise” (No Piano Melody) by Scott Buckley — https://www.scottbuckley.com.au/library/signal-to-noise/ — licensed under CC BY 4.0, https://creativecommons.org/licenses/by/4.0/. Edited for length and mixed with narration.` This is a credit draft; confirm applicability before release. No new publication is authorized by the rebuild request.

## Review candidate selection

Coordinator selects trial v02 for the requested user-review candidate based on the approved track catalog, the saved creative consultation, exact source/license, and technical measurements. This selection fixes the exact audio for a review render; it is not a claim that the sound or balance was heard or that the audio phase passed. The user will hear the candidate as part of normal MP4 review. Subjective listening and balance remain UNVERIFIED; correct if defects are identified. Preserve the required CC BY credit above for any later release.


## Next revision — continuous music coverage

Planning against review redesign v02 (252.8 s). Preserve exact narration, speech placement, and picture. Use separate edit tracks for narration, base bed, and thematic cue, then export one stereo mix. These are placement targets, not a rendered or auditioned mix.

| Edit interval | Music role |
|---|---|
| 00:00–01:45 | Base bed from the opening through the crisis. Select an approved instrumental recording and audition it with the opening narration. |
| 01:45–03:35 | Use the existing Signal to Noise (No Piano Melody) cue as the starting point for the thematic section. Let the base fade into its entrance. Retain the base under the beginning of the fade until the thematic cue can carry the background. |
| 03:35–04:02.8 | Return to the base as the thematic cue fades. Keep the base under the closing narration, through the final screen, and resolve at the end. |

The table shows the current cue anchors. Set exact overlap boundaries against the words and the two recordings after selecting the base. No deliberate music gap is specified at this stage. Verify coverage across the transitions and through the final screen, voice position and intelligibility, mono playback, levels, and final mix identity. Confirm attribution for every recording used. The existing v02 review file retains its original trial audio.
