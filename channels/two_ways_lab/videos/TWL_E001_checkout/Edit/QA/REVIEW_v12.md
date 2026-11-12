# TWL_E001 v12 - local review

MP4 SHA-256 `6d0be0205847b1f807bd33f321f2533e1a0d8cd174937cbcb60dd700ce691de7`. User acceptance pending.

- The user-provided exact narration was synthesized locally in the same Kokoro af_heart voice as v01; 90/90 transcript words aligned on the exact voice and independent offline Whisper ASR recognized the user text with normal punctuation and numeral normalization. Maximum adjacent aligned gap 0.241s. ASR and alignment do not prove naturalness or pronunciation. See asr_v11.json and forced_alignment_v11_raw.json.
- The initial and final narration were synthesized as one phrase and split at the opening, so the user's exact final line leads back to the opening. Subjective loop playback and listening are UNVERIFIED; no claim of a seamless audible loop.
- Narrative sequence: A2/B5, A2/B4, A2/B3 with payment, then A0/B1 with the protagonist behind the remaining shopper, return to initial choice. User's model result: 74s vs 88s, margin 14s, from ../../experiment/events.json.
- Only screen lettering other than speech subtitles is from generated image assets; hook provenance is retained v04, and payment/loss label originals and hashes are in ../image_manifest_v12.json. Their appearance, spelling, transparent edges and bounded motion were checked in sampled rendered frames. At 0:13 the only overlay is a speech subtitle, documented by v12_at_13.png. Nine phone-scale frame samples: v12_sheet.jpg; not every frame was checked.
- Full FFmpeg decode succeeded, ffprobe_v12.json records streams and duration. Physical phone playback and independent review remain UNVERIFIED.
