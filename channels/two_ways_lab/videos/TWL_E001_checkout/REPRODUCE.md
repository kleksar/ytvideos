# Historical v01 reproduction — REJECTED

This document records the rejected v01. Its scripted scene-lettering builder is not a permitted route for new work; use the current channel visual profile and EPISODE instead.

# Reproduce TWL_E001 v01

The retained image PNGs and mix WAV are local dependencies. Preserve them with [image hashes](Edit/image_manifest_v01.json) and [mix hashes](Source/Audio/v01/mix-evidence.md); a fresh clone does not contain the media. Re-generating a painting from its prompt does not reproduce the same bytes.

Run from the repository root. Python with Pillow, FFmpeg/ffprobe and the system Arial Bold font are required.

```sh
twl=channels/two_ways_lab/videos/TWL_E001_checkout
python3 -m unittest discover -s "$twl/experiment" -v
```

To rebuild the review from the frozen edit and retained mix, use a new output and run directory. Change `rebuild_01` in all paths for each subsequent run:

```sh
twl=channels/two_ways_lab/videos/TWL_E001_checkout
python3 - "$twl" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1]).resolve()
contract = json.loads((p / 'Edit/export_contract_v01.json').read_text())
contract['preflight']['output_path'] = str(p / 'Work/TWL_E001_rebuild_01.mp4')
with (p / 'Work/rebuild_01.contract.json').open('x') as f:
    json.dump(contract, f, indent=2)
PY
python3 automation/ffmpeg_montage/montage.py "$twl/Edit/timeline_v01.json" \
  --work-dir "$twl/Work/rebuild_01" --output "$twl/Work/TWL_E001_rebuild_01.mp4" \
  --export-contract "$twl/Work/rebuild_01.contract.json" --encoder libx264 --bitrate 10M --jobs 3
```

The exact delivered run also retained `Work/render_v01/render_command.json`, individual scene commands and renderer provenance. The command above rebuilds the edit; encoder/OS versions can affect encoded bytes.

For a new editorial revision, use a new version of the builders and assets. `Edit/build_audio.py` reads the English block in EPISODE and builds voice, original pluck music/SFX, mix and predicted word timings. It requires Python 3.12 with `kokoro==0.9.4`, `en_core_web_sm==3.8.0`, and the locally cached [Kokoro model revision](https://huggingface.co/hexgrad/Kokoro-82M/tree/f3ff3571791e39611d31c381e3a41a3af07b4987) with `af_heart`. For v01 the interpreter was `/private/tmp/twl-e001-tts/bin/python` with `HF_HOME=/private/tmp/twl-e001-hf`; these paths are temporary and are unnecessary when reusing the retained audio. `Edit/build_edit.py` reads the model events and exact speech timing, builds the overlay PNGs, and writes the FFmpeg plan and export contract. The builders require fresh version directories. For the separate SRT, use the [project SRT helper](../../../../.agents/skills/ytv-srt/SKILL.md) with [the exact cues](Edit/srt_cues_v01.json) and the retained transcript.

For the next episode: specify what is measured and what stays equal, calculate event states, then write the Short and choose its loop. Test the hardest pair of images on one consistent scene before making the rest. Use the same [channel profile](../../AGENTS.md), and verify the new video's own numbers, subtitle timing, cover and final file before offering it for review.
