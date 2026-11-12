# Full HD Shorts / stereo delivery follow-up — 2026-11-02

User changed geometry: Shorts1080×1920, horizontal films remain2560×1440;30FPS unchanged. This receipt supersedes the initial2K-for-both policy in the [previous research](../REPORT.md); that receipt remains historical evidence. Canonical current rules are the [export profile](../../../../.agents/skills/ytv-video-export/references/paper-detour.md) and [audio delivery](../../../../.agents/skills/ytv-audio-delivery/references/delivery-checks.md#paper-detour-youtube-delivery).

## ElevenLabs: observed route and file

- Graph-inspected `stories/automation/elevenlabs/tts.py`: `OUTPUT_FORMAT="mp3_44100_128"`; `synthesize` uses the timestamped endpoint with that explicit query, decodes `audio_base64`, checks MP3 signature and saves MP3/alignment. `arguments` has no output-format switch. No code changed and no API generation/test request sent.
- Read Paper031 current context and voice generation handoff before examining its source. Actual retained English Lawrence voice measured with ffprobe: MP3,44100Hz,1channel/mono,128000bit/s,71.28s. [Measured data and SHA](voice031_ffprobe.json). SHA matches the generation receipt: `3c628dbdb72b5960d8dcb9289eaf653c3163d2b3751c4af7eb4e8dd293312a5e`. This task did not listen to or revalidate pronunciation of the source.
- Paper035/036 generation logs also describe the same helper/format; these are corroborating historical receipts, not fresh measurements of those files.
- [Timestamped API documentation](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps) confirms defaultMP3 format and format/account dependence. [Format support](https://elevenlabs.io/docs/help-center/troubleshooting/what-audio-formats-do-you-support) and [TTS capabilities](https://elevenlabs.io/docs/overview/capabilities/text-to-speech) distinguish MP3, PCM/WAV and effect-dependent stereo. Current account's PCM entitlement and an actual lossless request remain unverified. The existing project adapter does not support PCM/WAV; no promise of a new source format was made.

## Decision and constraints

Coordinator's recommended new-delivery policy: central mono source narration on a Stereo2.0 program bus, retained music/SFX channel mapping, final AAC-LC48000Hz2channels384kbps target, including voice-only programs. Identical central speech in L/R is dual mono, not additional spatial information. No widening, double summing, automatic gain boost or new effects. Scope/acceptance of old media remains intact.

Consultation: [receipt](../../../../.agent/consultations/paper_fhd_stereo_20261102.md), [completed response](../../../../.agent/consultations/paper_fhd_stereo_20261102.txt). First attempt failed to load; one short retry returned a substantive answer. Exact visible model/mode verified before both: GPT-6 / Extra High,4из5. No exception required.

[YouTube encoding guide](https://support.google.com/youtube/answer/1722171?hl=en) supplies the platform references; ordinary [audio troubleshooting](https://support.google.com/youtube/answer/58134?hl=en) explicitly calls out phase/mono compatibility and permits other rates/bitrates. Our384kbps choice is a target, not a rejection threshold for every valid YouTube file. Same for channel layout: Stereo2.0 is a workflow recommendation, not a claim mono uploads are unsupported.

Native Palmier path stays H.264 / Match Timeline / automatic HighestQuality, with actual timeline1080×1920 or2560×1440 verified before export. Manual-rate-control fallback starting targets:12Mbps FullHD /20Mbps2K, or x264CRF18medium. These local choices are not hidden Palmier arguments or proven universal optima. Existing-schema/public-source evidence from the initial receipt remains applicable; no new live app schema/export characterization was performed here.

QA now explicitly checks channel mapping and mono compatibility from the audio owner's contract; metadata, signal findings and heard review stay separate. A mono fold-down need not be saved as a new audio artifact to analyse it. Correct48k resampling is not restoration of MP3 information. Optional future genuine PCM/WAV source acquisition requires adapter capability/account confirmation, not a renamed MP3 or unapproved test generation.

Updated skills/profile/QA example only; no sound, render, timeline, publication or application-preference mutation. Validation: [validation.json](validation.json). Actual render of the proposed new audio profile and listening remain **NOT_PERFORMED**.

## User acceptance — 2026-11-02

After receiving the final settings, the user replied: «Да, принимаем эти настройки». The proposed technical profile is now the accepted standard for new Paper Detour deliveries. This includes Full HD Shorts / 2K horizontal films at 30 FPS, MP4/H.264 SDR Rec.709, the native Match Timeline route with automatic HighestQuality and the documented manual-encoding fallback targets. Final audio is Stereo 2.0 / AAC-LC / 48 kHz / 384 kbps target for both voice-only and music-bearing programs, with mono narration centred and stereo music/SFX preserved. Canonical rules remain in the export and audio profiles linked above.

This entry records the later acceptance; the recommendation and consultation sections above retain their original provenance. Acceptance does not qualify an actual native export, approve an unheard mix, implement a PCM/WAV TTS adapter or authorize new sound, rendering or publication. No media or application state changed while recording it.

## Recheck after possible concurrent edits — 2026-11-02

At the user's request, mechanically compared the current canonical export/audio profiles, Palmier adapter, portable contract template, QA profile/example and production/image handoffs with the accepted settings. No drift found in the checked current rules; no settings restoration was necessary. The accepted standard remains effective for new Paper Detour deliveries. Image-generation 4K targets concern source images and do not override Full HD Shorts / 2K film delivery.

[Verification receipt](RECHECK_20261102.json): 19 documents with SHA-256, 18 consistency checks, 238 local link targets checked; export/audio/QA skill frontmatter validation passed. This verifies documentation and templates only, not a live project configuration or encoded output. No Palmier setting/timeline mutation, render, sound generation or upload was performed.
