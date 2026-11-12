# Description revision v02 — hashtag update

- Channel/video: Nuviko History / `5v6exl0iQJE`; title unchanged.
- Source: `Source/Shorts/05_labour/retained_transcript_v01.txt`, accepted transcript, SHA-256 `63cb6f381de7f000f47647a629387ac541d14e85f7c8539ba35e859d90d3b270`.
- Baseline: fresh YouTube Data API `videos.list` read on 2026-11-03; full before text in `DESCRIPTION_BASELINE_EN_v02.txt`. It matched the prior description except the hash is preserved there exactly.
- Decision: `revise` — existing set covered event, era, broad labour history, named 1351 statute and Shorts format, but omitted the England setting, labour shortage, wage-control policy and distinct 1349 ordinance.
- Resulting block: `#BlackDeath #MedievalHistory #MedievalEngland #LabourHistory #LabourShortage #WageControls #OrdinanceOfLabourers #StatuteOfLabourers #Shorts` (9 tags).
- Source state: `accepted_material_checked`. The body paragraph and full-film CTA/link were unchanged. Separate YouTube Tags, title, category, language, audio language and privacy were preserved.
- Assembly: `validated`. `DESCRIPTION_EN_v02.txt` passed the description validator with the before body paragraph and CTA/link protected exactly. Diff: only the final hashtag line changed.
- External: `applied_verified`. The YouTube API initially returned a stale description immediately after the write; the next read returned the exact new description. A fresh expanded YouTube watch-page description showed the full block and the first three displayed hashtags: `#BlackDeath #MedievalHistory #MedievalEngland`. No second write was sent.
- Receipt: `DESCRIPTION_CHANGE_RECEIPT_v02.json`; complete selection rationale and usage observations: `HASHTAGS_v02.md`; Extra High consult record: `EXTRA_HIGH_HASHTAGS_v02.md`.
