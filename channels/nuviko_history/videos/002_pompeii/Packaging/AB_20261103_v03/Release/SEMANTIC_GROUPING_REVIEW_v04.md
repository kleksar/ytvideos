# Subtitle semantic grouping review — MP4 v04

- Exact MP4 SHA-256: `5212f7f04dcb607a642dd24e9e3895290c05ab1a30fc6b702efd209bf9c672ff`.
- Reviewed the full generated [group map](../../../Edit/FFmpeg/subtitles-20261103-v04/groups_review_v04.txt) against the accepted English narration and current Paper/Nuviko one-line grouping rules: 591 groups, 2,136 words, 14:16.37 runtime.
- Result: `PASS` for semantic grouping and continuity. Phrase chunks preserve the spoken sequence and form a readable progression; no unresolved isolated “who” or “we do not” break remained. The three phrase changes are tracked in [REVIEWED_PHRASE_CHANGES.json](../../../Edit/FFmpeg/subtitles-20261103-v04/REVIEWED_PHRASE_CHANGES.json). The strict serializer and [SUBTITLE_CHECKS_v04.json](../../../Edit/FFmpeg/subtitles-20261103-v04/SUBTITLE_CHECKS_v04.json) confirm 2,136 tokens in order and continuous subtitle-state coverage over all 25,691 frames.
- Reviewer: Codex, self-review. Method: complete textual read-through of the 591-group map plus the saved structural checks. This is not an independent review or audio-sync evidence.
