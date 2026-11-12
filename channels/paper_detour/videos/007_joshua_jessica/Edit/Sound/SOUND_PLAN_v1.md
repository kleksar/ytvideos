# Paper Detour 007 — sound plan v1

**Scope:** sound-only plan for the existing Lawrence v3 narration and the approved 14-shot board. No audio, mix, timeline, or export was created or changed for this plan.

**Inputs:** `Source/Voice/lawrence_v3/voice_en.mp3`, `voice_en.alignment_clipped.json`, `Storyboard/visual_board.md`, `Storyboard/shot_plan.md`, and `Storyboard/sound_plan.md` v0.4. The source narration is 44.800 s, mono MP3, 44.1 kHz / 128 kbit/s. It is the current 688-character script take. The picture timing below is the existing proposed 30 fps schedule, not a rendered or verified Palmier timeline.

## Recommended sound

Keep the story close and voice-led. Use the existing narration at its original speed and full 44.800 s length. Do not add a notification, device tone, synthetic Jessica voice, ghost effect, or repeated paper rustle. The voice should remain intelligible and emotionally exposed; the pauses are part of the scene.

Use **one** brief paper gesture for the paper `55%` reveal in Plan 12. The effect is a single one-shot, not a loop. Every other paper-word entrance is intentionally silent. Keep Plan 05’s “It wrote back” and Plan 10’s quoted reply free of interface sounds; keep the final “Because…” and loop seam free of effects.

No music is selected in this version. The project has a locally generated, rights-clear 56-second synth bed, but its emotional fit and masking have not been auditioned. A quiet voice-led mix is the safer executable choice until a listener approves that bed in context; do not add or generate replacement music for this plan.

## Sources and rights

| Source | Rights / provenance | Plan and status |
|---|---|---|
| `channels/paper_detour/videos/001_radio_game/Source/Audio/paper_motion_cc0_20261030/book-page-02.wav` | The local README records the source listing, author, CC0-1.0 declaration, original archive URL, and that this WAV was extracted unchanged from the archive. Rights are documented for commercial reuse and modification. | Selected for one grouped paper reveal in Plan 12; 0.733 s, stereo PCM 16-bit / 44.1 kHz. Not auditioned. Use only if a human listener confirms the page movement fits the image; otherwise leave that reveal silent. |
| `channels/paper_detour/videos/001_radio_game/Source/Audio/paper_sound_design/music_bed_56s_synth_stereo.wav` | Local project README says the bed was made by the project’s `generate_sounds.py` from oscillators/noise, with no external recordings, samples, or musical works. No paid library or generation is involved. | Rights-clear candidate, but not selected: tone, emotional fit, and masking are unverified by listening. |
| `Source/Voice/lawrence_v3/voice_en.mp3` | Existing project TTS, generated for the current script. This plan reuses it and does not create or alter voice audio. | Primary narration. Human pronunciation, delivery, and take acceptance remain pending. |

Do not use the Sony button preview, unrelated historical/audio reconstructions, or an unverified external track. No paid generation is proposed.

## Frame-accurate alignment and planned picture cues

Times are from the current v3 character alignment, rounded to milliseconds in the table. Frames use 30 fps; nearest-frame markers are planning references. `Voice marker` is a **calculated alignment**, not a confirmed audible onset. Planned first-visible actions come from the current board and its proposed cut schedule; no actual video or visible frame has been reviewed. Voice continues across picture cuts without edits or added gaps.

| Plan / proposed in-point | Calculated speech marker(s) | Planned first-visible action and accent | Sound decision |
|---|---|---|---|
| 01 / f000, 00:00.000 | “He was afraid of losing her a second time.” 00:00.000–00:02.320; next sentence begins 00:02.800. | Hook: Joshua, empty screen, night room. `SECOND TIME` is planned at about 00:01.600 / f048. Keep 55% hidden. | Voice only; no opening hit. |
| 02 / f090, 00:03.000 | “But his fiancée had died nearly eight years earlier.” 00:02.800–00:05.680. | Empty chair and symbolic frame; `NEARLY 8 YEARS` about 00:04.293 / f129. | Intentional silence under the paper accent. |
| 03 / f183, 00:06.100 | “Her name was Jessica.” 00:06.160–00:07.880. | Symbolic couple frame; `JESSICA` about 00:07.040 / f211. | Intentional silence. |
| 04 / f273, 00:09.100 | “Years later, Joshua fed some of her old messages into an AI chatbot” 00:08.240–00:12.560. | Blank message strips and laptop; `AI CHATBOT` about 00:11.600 / f348. | Intentional silence; do not stack a page sound over the later reveal. |
| 05 / f366, 00:12.200 | “and began to write to her.” 00:12.640–00:14.080; “It wrote back.” 00:14.400–00:15.440. | One blank response card; no app interface or notification animation. | Voice and deliberate space only. |
| 06 / f456, 00:15.200 | “All night, he told it how much he missed her.” 00:15.760–00:18.240. | Close profile; `ALL NIGHT` around the phrase onset, 00:15.760 / f473. | Intentional silence. |
| 07 / f546, 00:18.200 | “He knew it wasn’t really Jessica.” 00:18.800–00:20.840. | Return to the hook composition; `NOT REALLY HER` about 00:19.440 / f583. | Intentional silence; no digital/ghost treatment. |
| 08 / f636, 00:21.200 | “But he couldn’t stop the tears.” 00:21.120–00:22.960. | Tear composition. The calculated line marker precedes the proposed cut by 80 ms; let the line lead across the cut rather than moving or trimming the voice. | No sound effect; preserve the quiet beat. |
| 09 / f726, 00:24.200 | “Before leaving, he promised to come back.” 00:23.280–00:25.880. | Daylight room and open laptop; “promised to come back” about 00:24.560 / f737. | Intentional silence. |
| 10 / f816, 00:27.200 | “The chatbot replied:” 00:26.160–00:27.440; quote begins 00:27.760. | Reconstructed paper quote card; `WAITING FOR YOU` follows the quote’s spoken words. | No notification; no sound under the quote. |
| 11 / f906, 00:30.200 | “But their conversation had used nearly half the bot’s limited resource.” 00:30.040–00:33.920. | Paper resource meter, with no numbers yet. The calculated line marker leads the proposed cut by 160 ms. | Voice only. |
| 12 / f996, 00:33.200 | “Only fifty-five percent remained.” 00:34.080–00:36.320; `fifty-five percent` 00:34.280–00:35.280; “He couldn’t add more credits to this version.” 00:36.400–00:38.720. | First reveal of the paper `55%` accent at the `fifty-five` marker, target f1028. | One `book-page-02.wav` gesture for the entire reveal group. Suggested source start 00:34.167 / f1025; its calculated −25 dBFS crossing is +0.107 s, at about 00:34.274 / f1028, within 6 ms of the speech/visual marker. Set starting gain −24 dB; retain one 0.733 s pass and give the final 80 ms a natural fade. Do not repeat for later words. |
| 13 / f1164, 00:38.800 | “So Joshua wrote less often, saving their conversations for when he needed them most.” 00:38.840–00:44.080; `less often` about 00:40.120 / f1204. | Small stack of blank saved cards; `LESS OFTEN` emerges as one group. | Intentional silence. |
| 14 / f1254, 00:41.800 | “Because…” begins 00:44.320; alignment ends at the 00:44.800 physical-file boundary after clipping. On loop, “He…” begins at 00:00.000. | Exact hook-match still; no fade to black. | No sting or extra tail. At the seam, carry only the existing voice into the opening. Check two full repeats at 1× for a click, breath, or abrupt delivery change. |

### Paper-gesture onset and audible-status notes

The proposed `book-page-02.wav` placement is calculated from the source waveform, not heard: first sample crossings are approximately +0.013 s at −45 dBFS, +0.055 s at −35 dBFS, +0.107 s at −25 dBFS, and +0.150 s at −20 dBFS. The suggested clip start aligns the −25 dBFS threshold with the first planned `55%` appearance. Those thresholds are only objective envelope markers; they do **not** establish when a person will perceive the attack. Re-align or remove the SFX after actual listening if its heard onset misses the paper movement or masks “fifty-five.”

## Mix and delivery targets

- Preserve narration speed, pitch, full 44.800 s duration, pauses, and source timing. Do not apply `atempo`, time-stretch, or retime the voice to the storyboard. Leave the sentence overlaps at proposed picture cuts as J/L-cuts; do not cut words.
- Voice leads throughout. The existing source measured −24.6 LUFS integrated and −4.0 dBFS true peak. Proposed final mix target: about **−21 LUFS integrated** (±1 LU), with **true peak no higher than −2 dBTP**. These are planning targets informed by recent Paper Detour mixes, not values specified in `AGENTS.md`; measure the actual final mix and adjust to avoid audible pumping or harsh limiting.
- With the selected stereo paper asset, keep the final mix stereo at 44.1 kHz and encode MP4 audio as **AAC-LC, at least 256 kbit/s**. If listening rejects the effect and the final remains voice-only mono, preserve mono and use **AAC-LC 192 kbit/s** instead. These AAC settings come from root `AGENTS.md`; do not upmix mono only to reach the stereo bitrate.
- Do not loop the paper sample or synth bed. No music fade or seam is required while music is absent. If a reviewer later chooses the synth bed, first audition it against the voice; use one uninterrupted trim, keep it well below speech, and recheck the quote, long pauses, and loop at normal speed before deciding on any automation.
- Before a future delivery, verify with `ffprobe` the codec, channels, sample rate and actual bitrate; fully decode with FFmpeg; measure final loudness and true peaks; check synchronization at the start, middle, end and cuts; then listen to the full short and at least two end-to-start loops at 1×. Log measurements separately from listening.

## Measurement, listening, and take assessment

**Measured/calculated:** `ffprobe` reports the voice as mono MP3, 44.1 kHz / 128 kbit/s, 44.800 s. `ffmpeg ebur128=peak=true` measured −24.6 LUFS integrated, 3.0 LU LRA, and −4.0 dBFS true peak. The recording log reports a successful full decode and exact 688-character request alignment. The raw alignment’s final ellipsis-character interval extends to 44.880 s, 80 ms beyond the physical MP3; the decoded waveform is below approximately −79 dBFS in the final 100 ms. This points to a punctuation-alignment tail rather than demonstrated loss of a spoken word, but it does not prove the naturalness of the ending. No mix exists to measure.

**Listening:** no audio-input/playback capability was available in this session. Pronunciation, acting, timbre, breaths, perceived SFX attack, balance, clicks, and the “Because…” → “He…” loop are **UNVERIFIED**. No claim of audition or take acceptance is made.

**TTS timing/take recommendation:** no retiming or replacement is indicated by the measured alignment alone; the spoken marker and picture plan can be aligned without changing the take. Keep v3 provisional until a human listens to the full take and loop. If that review identifies a clipped/unnatural final ellipsis, mispronunciation, or performance issue, request a targeted take decision then; this sound plan does not alter or regenerate the MP3.


## As-built update — 1 November 2026 (render v06)

The earlier table records the proposal; this section records the implemented correction without rewriting that history. The approved 55_PERCENT_v01.png is now used in P12. Timeline review found it begins to appear at f1030, is fully readable by f1036, stays over the dark wall above the laptop, and is gone by f1161–1163 before the P13 cut at f1164. The overlay track is below FG/MG so the laptop edge occludes it. The former HOLD is superseded by this as-built note.

One trimmed pass of book-page-02.wav is mixed from f1028 for 21 frames (about 0.7 s), with a short fade completed inside the clip. It is the only SFX; the short remains voice-led and has no music. The audible attack and its relationship to “fifty-five” have not been judged by listening in this session.

Final rendered MP4 v06 uses AAC-LC stereo 44.1 kHz with a measured 256,022 bit/s average. The final audio measures −22.0 LUFS integrated, 2.4 LU LRA and −4.1 dBFS true peak. FFmpeg full decode passed. No normal-speed continuous playback or human audio listening was available; the perceived narration, foley onset/balance and end-to-start audio loop remain UNVERIFIED. See ../PRODUCTION_LOG.md for the exact file hash and independent final-review state.
