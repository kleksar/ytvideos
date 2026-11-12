# V04 — empty-frame corrections

User rejected empty images at 09:46 and 09:55. V03 SHA-256 `09b0d086533f34b1ae17278af41955bc3d78e24d90f79ffe9a74ba83588b86fe` is rejected and moved to Trash; see `reject_v03_empty_frames_receipt.json`. V04 is being assembled with the retained narration, mix, subtitles, scene timings and ending, and retains the accepted-in-conversation 09:13 correction.

- 19.05 at 584–588.733 s: replace empty portrait frame with a symbolic uniform/helmet display labelled AUTHOR UNKNOWN, `revision04_author2.png` SHA-256 `90155a3578abd448ba9845db81b03e9616f4af3610a0e84e449bdb2dd7b2c916`.
- 19.05a at 588.733–594 s: replace empty interior with conceptual question display (HOW LONG? / WOUNDED? / ALONE?), `revision04_questions.png` SHA-256 `7ea0b66b4ec607df6916eb36fa06f76562e862bc79f74afe1defe2df21903bec`.
- 19.05b at 594–599.933 s: replace blank plaster with an explicitly marked inscription reconstruction, `revision04_words2.png` SHA-256 `dac5f5dcb993c0fda11ce20f25cd590a260b13991a34652ef16f990bf7aa4ddc`.
- Related audit replaces other empty presentation frames 17.02 and 17.04a–17.04c with meaningful report/defender imagery. These displays are interpretive and do not represent genuine artefacts. Full montage plan and command: `replace_empty_render_v04/`.

V04 has not yet been accepted by user. The inherited limitations remain: full audible listening and speech/subtitle sync are unverified; clickable YouTube end-screen elements are not configured. This revised targeted FFmpeg assembly does not have a new shared-renderer delivery receipt. Exact-file review follows after encoding.

## Exact V04 recheck

`previews/full_review_v04.mp4` SHA-256 `01ffd8a3ad8f1d2bc9d5082c21471ab0d75fc97064c7d7fdd0e766c6dc1f9439`; ffprobe reports H.264 2560×1440, 30 fps, 18671 frames, duration 622.366667 s, AAC stereo 44100 Hz. Exact-file frames at 465/487/493/499/553/586/591/595/601/617 s were viewed; changed content, retained 09:13 correction, text/subtitle layout and end-screen sampling confirmed. Ten three-second audio signal comparisons to the retained WAV, including changed scenes 585/595 s, show zero-offset Pearson correlation at least 0.99948 (`scratch/full_review_v04_audio_correspondence.json`). This does not replace listening. Full decode result follows; no subjective audio or sync PASS claimed.

Full exact-file video and audio decode with FFmpeg `-v error -xerror` completed with exit code 0.
