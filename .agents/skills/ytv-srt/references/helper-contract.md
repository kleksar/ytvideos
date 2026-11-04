# Offline helper and timing handoff

Use `python3 scripts/srt_tool.py --help` from this skill, or its resolved path. Python standard library only; no network, media rendering or account access. It supports plain-text SRT, not styling/translation, ASR, automatic sentence grouping or edit-conform inference.

Prepare UTF-8 `transcript.txt` and provider-neutral `cues.json`:

```json
{"cues": [
  {"start_seconds": "0.400", "end_seconds": "2.500", "text": "First complete phrase."},
  {"start_seconds": "3.100", "end_seconds": "5.000", "text": "Another phrase\nwith a deliberate line break."}
]}
```

Times may be finite numbers or decimal strings. They are seconds in the explicitly declared source/final timebase. No implicit clip speed, offset or pause is applied. Prepare conformed cues separately using the actual edit map. The helper cannot establish a map merely because `--timebase final` is supplied.

```bash
python3 scripts/srt_tool.py build --cues cues.json --text transcript.txt --duration 50.066667 --timebase source --output draft.srt --report draft-check.json
python3 scripts/srt_tool.py validate --srt draft.srt --text transcript.txt --duration 50.066667 --timebase source --report recheck.json
```

Use the measured duration of the declared timebase, not this example value. Optional warnings: `--max-lines`, `--max-line-chars`, `--max-cps`, `--min-duration`, `--max-duration`. Thresholds are selected by the profile/request; no threshold is enforced by default. CPS counts normalized Unicode code points including spaces, not glyph width, and is only a reading-density proxy. Semantic breaks and visual player layout still require review.

Build writes a new SRT only when structural/bounds and coverage checks pass, and round-trips the serialized file. All output paths must be new and their parents exist. Return code1 indicates failure; a diagnostic report may still be written for validly parsed failed cues. Schema/encoding errors can fail before a report, with an error on stderr. Readability `WARN` is visible even when the machine checks return0. Rounding is half-up to milliseconds; raw and rounded intervals are both checked. No clamping, reordering, auto-shortening or silent source overwrite.

Validation parses every complete block, verifies sequential cue numbers, timestamp syntax/ranges, nonempty text, positive intervals, overlap and duration bounds. It accepts UTF-8 BOM and CRLF. Coverage compares the complete SRT text with the expected retained transcript under NFC and whitespace normalization; punctuation/case changes, omitted/repeated/reordered content fail. This strict literal mode needs a reconciled final transcript; a translation or shortened accessibility version needs its own approved expected text and separate semantic review.

The machine JSON records input hashes, declared timebase/duration, output hash, per-cue measurements, errors and warnings. `timing_mapping` and `playback` stay `UNVERIFIED`; duration-fit is not synchronization evidence. Link another receipt containing actual audio/final-media identities, edit version, source-to-final map and its validation, segmentation provenance and playback coverage. This avoids a second conflicting current selection.
