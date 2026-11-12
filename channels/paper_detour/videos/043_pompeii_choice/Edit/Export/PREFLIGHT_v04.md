# Export preflight v04 — caption display correction

This is a single targeted correction to v03: keep `Others stayed` in one group and `inside.` in the next. The prior v03 render displayed `Others` for only three frames; that exact preview is recorded as rejected in `Edit/SubtitleReview/decision_v03.json`. The lifecycle cleaner refused to delete it because its live Palmier dependency scan returned connection refused; the file remains in v04’s completed run pending a successful bounded cleanup. No external release changed.

Current accepted timeline: `Edit/plan_v06.json`; the only timeline difference from v05 is the `Others stayed / inside.` split. It keeps the spoken phrase intact, meets the 3-word cap, and the actual caption cue is 0.80 s before the next group begins. Its paired `inside.` cue begins at 24.40 s.

Preflight repeats the accepted Paper Short profile: Chalkboard SE Bold index 2 at 104 px; 1440×2560 at 30 fps; 1024 px max visible width; 978 px text allowance after padding and outline. The reviewed 81-token plan has 39 groups, no group over 3 words, and maximum measured line width 971.86 px. The forced `that / might collapse?` split remains because the intact 3-word phrase measures 1020.70 px.

Voice MP3, speed 1.10×, source images and camera/timeline content are unchanged; video playback speed remains 1.0×. Provider word timing map is unchanged. WhisperX exact-token diagnostic remains `REVIEW_REQUIRED` with 25 local disagreements; audible subtitle sync is unverified, and this is disclosed with the review MP4.

Output: `Work/paper043-prod-v05/previews/043_pompeii_choice_EN_review_v04.mp4`, absent at contract preparation. H.264 MP4, 1440×2560, 30 fps CFR, Rec.709 limited range, mono AAC-LC 192 kbit/s at 44.1 kHz. Use one FFmpeg worker.
