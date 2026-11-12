"""Replace the audio on an existing cut with the film-only master."""
import json
import shutil
import sys
from pathlib import Path

from render_package import EPISODE, FPS, RATE, clip, freeze, mix, MASTERS_AUDIO_FILTER

def remux(plan_path, previous):
    spec = json.loads(plan_path.read_text())
    assert spec['film_only']
    old = EPISODE/'Deliverables'/previous
    out = EPISODE/'Deliverables'/spec['slug']
    work = EPISODE/'Work'/spec['slug']
    out.mkdir(exist_ok=True)
    work.mkdir(exist_ok=True)
    shots, runs, groups, _, frames = freeze(spec)
    picture = old/(previous+'.mp4')
    old_video = clip.probe(picture)['streams'][0]
    assert int(old_video['nb_frames']) == frames
    raw = mix(spec, runs, groups, frames, work)
    target = out/(spec['slug']+'.mp4')
    clip.run([*clip.FFMPEG, '-n', '-i', picture, '-f', 'f32le', '-ar', RATE, '-ac', '2',
              '-i', raw, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
              '-af', MASTERS_AUDIO_FILTER, '-metadata:s:a:0', 'language=eng',
              '-video_track_timescale', '24000', '-movflags', '+faststart+write_colr', target])
    raw.unlink()
    shutil.copyfile(old/(previous+'.en.srt'), target.with_suffix('.en.srt'))
    (work/'timeline.json').write_text(json.dumps(dict(shots=shots, runs=runs, groups=groups, frames=frames,
                                                  picture_source=str(picture)),ensure_ascii=False,indent=2)+'\n')
    print(target)

if __name__ == '__main__':
    remux(Path(sys.argv[1]), sys.argv[2])
