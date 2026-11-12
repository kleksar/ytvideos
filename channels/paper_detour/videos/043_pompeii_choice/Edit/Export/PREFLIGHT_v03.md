# Export preflight v03 — subtitle correction

Scope: replace the review MP4 captions for Paper 043 using the exact 81-token caption map and a reviewed 39-group phrase plan. Narration MP3, voice speed 1.10×, source images, camera plan, frame rate and full-video speed are unchanged. No YouTube changes are included.

The accepted FFmpeg timeline is `Edit/plan_v05.json`; only the `subtitles.phrases` field differs from v04. The measured Paper Short profile is Chalkboard SE Bold index 2 at 104 px, 1440×2560, maximum visible width 1024 px, center x at 0.472222 and y at 0.762. After padding/outline the measured text width allowance is 978 px. Preflight resolved 81 tokens, 39 groups, maximum 3 words and maximum phrase width 971.86 px; all phrase overlays were generated successfully.

One forced syntax compromise is recorded in `Edit/subtitle_groups_v05.json`: `that / might collapse?`. `that might collapse?` is 1020.70 px at the fixed 104 px size, exceeding the 978 px text allowance. The separate marker is preferred over splitting the modal from its verb. The script now permits this relative-marker split only when the full antecedent-plus-relative clause exceeds the safe width. The parser also treats `inside` as a locative adverb after stay/remain/stand verbs. Both conditions remain subject to the normal strict width check.

The actual caption renderer generated 82 overlay states. Contact sheet: `Work/paper043-prod-v04/scratch/caption-preflight-v01/caption_preflight_contact.jpg`. The preview contact sheet uses the actual accepted scene images and profile overlays; it is a static layout check, not full motion review. The cue report remains `alignment_not_audibly_verified`; neither provider alignment nor this preflight establishes audible synchronization.

Output: `Work/paper043-prod-v04/previews/043_pompeii_choice_EN_review_v03.mp4`, new path, absent at contract preparation. Encode as H.264 MP4 1440×2560, 30 fps CFR, Rec.709 limited range, mono AAC-LC 192 kbit/s at 44.1 kHz; one FFmpeg worker. The complete MP3 duration (36.080 s) covers the 36.100 s, 1083-frame output per the established audio contract.

Alignment note: `Edit/word_times_v04.json` is retained; transcript and audio hashes match v05. WhisperX forced alignment was rerun with the exact 81-token caption transcript to avoid the prior em-dash tokenization split. `reconcile_pauses.py` returned `REVIEW_REQUIRED` with 25 local disagreement flags and no consistent global offset. Provider timings remain an automatic draft; their audible starts were not reviewed. The render will preserve the existing map and its flags for user review; subtitle sync is not certified. Diagnostics and their hashes are retained under `Work/paper043-prod-v04/scratch/alignment-reconcile-v01/`.

Fresh lifecycle audit: `Edit/MediaLifecycle/audit-pre-render-v03/audit.json`; coverage `BOUNDED_NOT_EXHAUSTIVE`, errors 0. Available disk reported 19 GiB before render.
