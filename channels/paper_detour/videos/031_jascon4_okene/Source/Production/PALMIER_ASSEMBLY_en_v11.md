# v11 — Cue timing audit and actual composition QA

Project `8BE390BC`; timeline `1BD3395C`, **031 Rough Cut v11 Cue Sync QA**; duplicated v10 `3859ADEC`. Snapshot `D61DD23A`. Existing16images,Englishvoice,scene camera movement,oneGraintrack and all11PNGartworks unchanged. Source version preserved; source snapshot, mutations and readback in `../../Edit/CUE_SYNC_QA_RECEIPT_v11.json` / `../../Edit/PALMIER_STATE_en_v11.json`.

Two measured corrections against the actual retained recording alignment:

- GRAB HIM:[236,259)→[237,260). First nonzero alpha at238=7.933s,after spoken “grab”7.920s.
- ONLY SURVIVOR:[1860,1906)→[1852,1898). First nonzero alpha1853=61.767s,after spoken “only”61.760s. Corrects an8-frame late start. Clip-relative motion/opacity curves, artwork and geometry preserved; cue now spans S14→S15.

Updated full interval table: `PAPER_CUE_SHEET_en_v05.md`. All first nonzero-alpha times within0–2frames after semantic trigger, with scene-cut/date-user-anchor rounding explicitly retained. This checks alignment-derived timing, not heard emphasis or spoken intelligibility.

Preflight: original actualPNG/geometry,3scene×cuepairs(S02/GRAB,S14/ONLY,S15/ONLY),fullentry/hold/exit envelopes,phonecontact and full-sizeS14 reviewed. Top labels overlap secondary pipes/gauges but no face,diverhelmet or hand action. `../../Edit/v11_sync_preflight/`.

Actual Palmier QA:27captured target-timeline composites,covering16scene midpoints and11cueholds. Contact viewed; changedGRABf241andONLYf1856also opened full-size. No blank sampled scene,missing title or obvious key-object collision. Evidence `../../Edit/v11_full_composite_qa/CONTACT.jpg` and `captures.json`. Actual full PNGs remain inside the project; source paths in captures.json avoid redundant full-size copies.

Structural checks: Main and Grain cover all2139frames contiguously; all11cueclips do not overlap; oneVoiceclip at0–2139; all other Main/Voice/Grain clip fields unchanged against v10 ignoring regeneratedIDs. Common source grain8-second cycle retained; prior first seam239→240 and first/last checks remain evidence from v10 but do not establish every current seam in playback.

Audio source technically fully decoded to null(no audio file rendered),MP3mono44.1kHz128kb/s71.28s. EBU R128:I−24.4LUFS,LRA2.1LU,truepeak−3.8dBTP. No clipping in this source measurement. No gain/speed/filter change. Log and measured parameters `../../Edit/v11_full_composite_qa/QA_REPORT.json` and `voice_ebur128.log`.

Saved project.json read-only parsing confirms v11 persisted. Actual UI observed v10 selected earlier in this pass; final UI navigation left untouched when it became occupied by another project's Save dialog(time_stop_visual_v01 copy.mov). Do not claim v11 selected. Full1×visual/audio playback,listening,pronunciation,all-seam review,finalMP4 and independent review remain UNVERIFIED.

User directly chose one MP4 instead of ProRes; the shared grain README already defines one H.264 MP4 as review/delivery encode. No separate ProRes master rendered. Export job `D5D641F6-C68E-4E1B-AC51-3C552E097AAB` completed to `../../Deliverables/031_jascon4_okene_en_short_1080x1920_30fps_v11_fine_grain25.mp4`. Actual export metadata, digest, decode result and audio-profile caveat: `../../Edit/MP4_DELIVERY_RECEIPT_v11.json`. Twelve rendered MP4 samples reviewed; grain visible, contact sheet `../../Edit/v11_full_composite_qa/MP4_CONTACT.jpg`.

Audio caveat: AAC-LC target192kb/s encoded from unchanged original voice MP3; measured average~172kb/s. The video stream is packet-identical to the Palmier H.264 export. Full decode and EBU R128 analysis passed; perceptual listening and full1×playback remain UNVERIFIED. Classify as REVIEW MP4 pending full audiovisual playback QA. No upload/publication.
