# Offline helper

`scripts/inspect_video.py` requires Python 3, ffprobe and ffmpeg. It reads existing media, writes logs/JSON/native PNG frames into a **new** output directory, and never generates audio, mutates a timeline or uploads anything. No extra packages are needed. Run from the current workspace:

```sh
python3 .agents/skills/ytv-video-qa/scripts/inspect_video.py \
  --episode /absolute/episode --run-id qa-film-v02 --owner actual-owner \
  --media /absolute/episode/Deliverables/final.mp4 --plan /absolute/qa-plan.json \
  --output-dir /absolute/episode/Edit/QA/qa-film-v02
```

The plan binds expected frame count/FPS and optional SHA to real edit intervals. It is an asserted input, not proof that the edit/export is current. Use this shape with actual values:

```json
{
  "frame_count": 300,
  "fps": "30/1",
  "required_review_checks": ["stream_metadata", "full_decode", "frame_sampling"],
  "freshness": {"status": "UNVERIFIED", "evidence": "actual edit/export receipt"},
  "expected": {
    "video": {"width": 1080, "height": 1920, "codec_name": "h264"},
    "audio": {"required": true, "codec_name": "aac", "channels": 1, "sample_rate": 44100}
  },
  "scenes": [{"id": "S01", "start": 0, "end": 150}, {"id": "S02", "start": 150, "end": 300}],
  "cues": [{"id": "C01", "start": 20, "end": 100, "entry_end": 24, "exit_start": 95}],
  "extra_frames": [74, 149, 151]
}
```

Intervals are integer frames `[start,end)`; end is exclusive. Optional `scene_seconds:[min,max]` comes from the profile, not the portable core. Optional `sha256` prevents sampling the wrong file. Scenes, when supplied, must cover the whole frame range without gaps/overlaps. Subtitle intervals follow the accepted cue map. Additional motion extrema/risks belong in `extra_frames`, and out-of-range values are refused rather than clamped. The helper adds scene start/mid/last, both sides of cuts, cue boundaries/hold/mid/exit and file first/last. If no scene/cue plan is supplied it samples only file endpoints; that does not close scene/cue coverage.

Supported expected video fields are `width`, `height`, `codec_name`, `pix_fmt`, `color_space`; audio fields are `required`, `codec_name`, `channels`, `sample_rate`. The example's mono/44.1 kHz describes one voice-only case, not a universal expectation: omit an exact field when the contract accepts multiple layouts/rates or leaves it engine-managed, and inspect actual metadata and preservation of the accepted mix separately. Unknown expectation keys are refused rather than silently ignored. Cue phase fields must come from actual authored transitions; omit absent fades, including a final held punchline.

These illustrative values do not select a channel default. The [pre-render contract](../../ytv-video-export/references/export-contract.md#existing-qa-helper) owns all expected technical properties and lists fields that need additional explicit QA beyond this helper. Preserve its identity/path/hash in the reviewer receipt.

Output `report.json` separates technical status, profile-policy violations, reported freshness, extraction map and actual inspection (initially empty). Full decode includes all AV streams. Frame sampling and counts target one video stream; multiple video streams cannot pass its counted-frame contract. Signal measurements target first audio stream; other stream/mix correspondence needs explicit review. Raw logs retain silence candidates at −50 dBFS for ≥250 ms, an operational detector setting, not an acceptance threshold. No subjective or clipping/true-peak conclusion is inferred from these measurements.

The exit code is 0 for completed technical checks, 1 for technical failure and 2 for invalid input/output setup. A 0 exit may coexist with `verdict=FAIL` for stale media or profile violations. `verdict` never becomes full AV PASS automatically: extracted PNGs have not been inspected, mix/timing have not been verified and audio has not been heard. Keep a separate reviewer receipt keyed to the same SHA and frame map.

Frame selection uses a balanced FFmpeg expression so long-film plans do not exceed the expression parser's depth. Regression checks: `python3 -m unittest discover -s .agents/skills/ytv-video-qa/tests -v` (the large-selection test invokes real FFmpeg without audio).


Новый default — managed-режим из примера: указать полный применимый `required_review_checks` в plan, `--episode --run-id --owner`; helper эксклюзивно создаёт отдельный run и `Work/<run>/scratch/qa`, после синхронной проверки пакетно регистрирует frame map и завершает writer. Media должен находиться внутри episode; source/report/output paths не содержат symlinks. Managed-флаги передаются вместе и не совместимы с `--no-extract`/`--frames-dir`. Отчёт всегда остаётся техническим: extraction никогда не становится визуальным PASS. Поля recipe/version записываются в report для проверяемого восстановления выборки.

После реального review и сохранения профильного receipt одна команда [finalize-qa](../../ytv-media-lifecycle/references/qa-finalization.md) сохраняет нужные доказательства и очищает разрешённые PNG. Старые вызовы без managed-флагов, с `--frames-dir` или единым output продолжают работать для совместимости, но не получают автоматического batch accounting. Перемещение или очистка старого активного набора не следуют из нового default. Отдельный новый run не наследует приёмку предыдущего фильма.
