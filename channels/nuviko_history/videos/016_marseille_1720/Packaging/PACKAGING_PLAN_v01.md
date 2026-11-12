# Marseille 1720 — packaging plan v01

Status: working draft only; do not upload from this file. Final wording, chapters, thumbnail, disclosure and links must be checked against the finished cut.

## Title-only experiment

Keep the same thumbnail and all video metadata constant while comparing these three titles in YouTube Studio. This isolates title as the tested variable. User authorized switching the QA-passed upload from Private to Unlisted (link-only) so the native test can run.

- A — control: **The Ship That Brought Plague to Marseille | 1720**
- B: **How the Plague Reached Marseille in 1720**
- C: **Marseille 1720: The Ship, the Quarantine, and the Plague**

These are candidates, not accepted final titles. Review against the actual final film and thumbnail before creating the test. Use native YouTube testing only if Studio offers the feature for this upload. The test can compare up to three variants and uses watch-time results; it may take up to two weeks. Do not promise a winner or infer it before Studio reports a result.

Eligibility note checked 3 November 2026: YouTube Help says tests cannot run on Private videos, while TeamYouTube's announcement describes eligible videos as public long-form. The Help page does not clearly say whether Unlisted is eligible. User authorized Unlisted after QA, not Public. After upload, inspect the actual Studio control while the video is Unlisted. If it is unavailable, leave the video Unlisted and report the limitation; do not switch it to Public without a new explicit instruction. Channel advanced-features access also needs to be active.

## Description structure

Draft opening: “In 1720, the Grand Saint-Antoine reached Marseille after a voyage through the eastern Mediterranean. What happened at the port’s quarantine station helped shape the city’s response to the plague.”

Then, after final cut review:

1. Concise summary limited to events actually narrated and depicted.
2. Chapters verified against final MP4 (not yet available).
3. Keep source list and fact-check records in internal Research materials; do not include public “Further reading” links by default.
4. Include only explicitly requested functional links and a small relevant hashtag set, following the global rule and Nuviko profile.

## Upload/release constraints

- First upload: Private through the project YouTube API adapter, after fresh channel/OAuth preflight.
- Disclose realistic synthetic historical scenes using YouTube's altered/synthetic-content control.
- Complete video/audio/caption QA and verify API read-back before any visibility change.
- Then change to Unlisted as explicitly approved and verify read-back. Create the native title-only experiment only if Studio confirms eligibility in that state.
- Do not publish publicly or schedule; no such authorization is present.
