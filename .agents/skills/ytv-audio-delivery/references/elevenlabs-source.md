# ElevenLabs source format

Read for voice acquisition/format selection, separately from the final mix contract. Evidence checked 2026-11-02: [research receipt](../../../../channels/paper_detour/research/2026-11-02-export-settings/followup_fhd_stereo/REPORT.md).

## Current project route

[`automation/elevenlabs/tts.py`](../../../../automation/elevenlabs/tts.py) explicitly requests **`mp3_44100_128`** from `/v1/text-to-speech/{voice_id}/with-timestamps`. It decodes JSON `audio_base64` into MP3 and saves character alignment separately. Its format constant, MP3 signature check and fixed `.mp3` destinations mean PCM/WAV are **not implemented in this helper**; there is no `--output-format` argument. Merely changing the constant or extension is unsafe. Preserve other channels' behaviour when separately implementing a format change.

Actual retained Lawrence voice of Paper031 measured **MP3, 44 100 Hz, 128 000 bit/s, 1 channel (mono)**, matching the generation receipt/hash. This is evidence for that request route/file, not a guarantee that every ElevenLabs feature returns mono or that every future file has the same metadata. Inspect each actual new source. A mono voice-only export is acceptable under the [Paper delivery profile](delivery-checks.md#paper-detour-youtube-delivery); preserve stereo when the accepted mix contains stereo material.

## Service capabilities versus local support

The official [timestamped TTS endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps) defaults to `mp3_44100_128`; available formats depend on the endpoint/model/account. The [format guide](https://elevenlabs.io/docs/help-center/troubleshooting/what-audio-formats-do-you-support) documents MP3, WAV/PCM and other delivery options; the [TTS guide](https://elevenlabs.io/docs/overview/capabilities/text-to-speech) describes 16-bit S16LE PCM and effect-dependent stereo. Reverb/pan can produce stereo; do not infer channels from the provider name or file extension. Keep dry narration unless an effect is requested.

For a future new voice source, prefer a **genuine provider PCM/WAV response** at a supported 44.1/48 kHz when account/model/route and the consuming adapter support it; otherwise use the actually supported high-quality source and record it. Account-specific PCM/WAV access and a lossless request through this project's helper are **UNVERIFIED / not implemented**, respectively. Do not spend a test generation to resolve that in a documentation-only task. Raw `pcm_*` is headerless S16LE, not a WAV container; a future adapter must handle rate/channels/header and timing correctly, without lossy encoding.

Retain usable accepted MP3 sources. Converting MP3 to WAV/48 kHz does not recover removed information, and changing final AAC bitrate cannot improve the original synthesis. Do not regenerate accepted narration merely to change its extension. New voice/audio still requires its actual authorization. Source format, processing rate and final AAC delivery are separate recorded fields.
