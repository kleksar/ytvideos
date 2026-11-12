# Export preflight v02

The first render attempt failed while encoding temporary scene clips with “No space left on device”; no final MP4 was created. Its exact temporary files, identities and source references are recorded in `Work/paper043-prod-v02/manifest.json` and `Edit/Export/RENDER_FAILURE_v01.json`. That completed run is retained for disposition.

The edit, voice and images are unchanged. The new render has a distinct work run (`paper043-prod-v03`) and output (`Work/paper043-prod-v03/previews/043_pompeii_choice_EN_review_v02.mp4`). Plan-only validation, subtitle contact sheet review, source hashes, 1440×2560/30 fps geometry, voice coverage, encoder availability and audio contract remain current. The earlier plan-only audit was refreshed for this output in `Edit/MediaLifecycle/audit-pre-render-v02/audit.json`. The output path was absent when the contract was prepared.

The disk reported 1.4 GiB available immediately before starting this retry. Use one FFmpeg scene worker to limit concurrent storage pressure. No YouTube upload or metadata mutation is included.
