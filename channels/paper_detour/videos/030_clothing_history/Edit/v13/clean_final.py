"""Remove only unreferenced episode derivatives after delivery verification."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'Edit/v13'
qa = json.loads((HERE / 'QA/REPORT.json').read_text())
assert qa['full_video_audio_decode'] == 'PASS'
assert qa['visual_sample_review'] == 'AUTHOR_PASS'
refs = set()
def walk(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == 'absolutePath' and isinstance(v, str):
                refs.add(str(Path(v).resolve()))
            else:
                walk(v)
    elif isinstance(node, list):
        for v in node: walk(v)
manifests = list(Path('/Users/diplomat/Documents/Palmier Pro').glob('*.palmier/media.json'))
assert manifests
for p in manifests: walk(json.loads(p.read_text()))
candidates = {HERE / 'Palmier_export.mp4'}
candidates.update((HERE / 'QA/BeforeHeadroom').glob('*.mp4'))
for folder in [ROOT / 'Edit/ImageMotion', HERE / 'FramingProbe', HERE / 'FramingPreflight']:
    for job in folder.rglob('*.job.json'):
        digest = job.name.removesuffix('.job.json')
        candidates.add(Path('/Users/diplomat/ytvideos/Shared/Image_Motion/Cache/video') / (digest + '.mp4'))
    candidates.update(folder.rglob('*.raw.mp4'))
removed = []
kept = []
for path in sorted(candidates):
    if not path.is_file(): continue
    if str(path.resolve()) in refs:
        kept.append(str(path)); continue
    removed.append({'path': str(path), 'bytes': path.stat().st_size,
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    path.unlink()
old = ROOT / 'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v06.srt'
new = ROOT / 'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v13.srt'
archive = ROOT / 'Edit/v05/Accepted_delivery_v05.srt'
if old.is_file():
    assert old.read_bytes() == new.read_bytes() == archive.read_bytes()
    removed.append({'path': str(old), 'bytes': old.stat().st_size,
                    'sha256': hashlib.sha256(old.read_bytes()).hexdigest()})
    old.unlink()
report = {'date': '2026-11-02', 'scope': '030 helper/probe derivatives and duplicate native export only',
          'dependency_manifests_checked': [str(p) for p in manifests],
          'removed': removed, 'kept_imported_videos': kept,
          'bytes_removed': sum(r['bytes'] for r in removed),
          'preserved': 'All original PNG/audio/mix/project files; all library-referenced derivatives; depth cache; logs and QA images'}
(HERE / 'FINAL_RENDER_CLEANUP.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'removed': len(removed), 'bytes': report['bytes_removed'], 'kept_imported': len(kept)}))
