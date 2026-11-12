#!/bin/sh
set -eu
kind=$1
case "$kind" in
 cable) p=channels/paper_detour/research/2026-11-09-atlantic-cable; n=Atlantic-Cable-Paper-Detour-en-v01; engine=automation/ffmpeg_montage/montage.py;;
 us) p=channels/nuviko_history/research/us-history; n=US-History-Nuviko-en-v01; engine="$p/Work/engine-v01/automation/ffmpeg_montage/montage.py";;
esac
base=.agent/research/2026-11-09-four-video-slate
PYTHONDONTWRITEBYTECODE=1 python3 "$base/check_review_subtitles.py" accept "$kind"
python3 - "$p" <<'PY'
from pathlib import Path
import json,sys
e=Path(sys.argv[1]).resolve(); m=e/'Edit/montage-v01.json'
p=json.loads(m.read_text()); p['subtitles']['review']=str(e/'Edit/subtitle-review-v01.json'); m.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
PY
python3 "$base/build_review_edit.py" finish "$kind" > "$p/Work/srt-build-v01.log"
python3 - "$p" <<'PY'
from pathlib import Path
import json,sys
p=Path(sys.argv[1])/'Edit/export-contract-v01.json'; v=json.loads(p.read_text());v['encoding']['requested_arguments']['encoder']='h264_videotoolbox';p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
PY
python3 "$engine" "$p/Edit/montage-v01.json" --encoder h264_videotoolbox --output "$p/Deliverables/$n.mp4" --work-dir "$p/Work/settings-v01" --export-contract "$p/Edit/export-contract-v01.json" --check-settings
