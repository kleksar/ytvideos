import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
edit = root / 'Edit'
repo = root.parents[1]
plans = {
    'mthu': ('mthu-review', 'v02', 'v03'),
    'super-funk': ('super-funk-review', 'v01', 'v02'),
    'bloodstream': ('bloodstream-review', 'v01', 'v02'),
    'bow-bow-bow': ('bow-bow-bow-review-v03', 'v03', 'v04'),
    'paparazzi': ('paparazzi-review', 'v02', 'v03'),
}
name = sys.argv[1]
base, old_revision, revision = plans[name]
plan = json.loads((edit / f'{base}-contract.json').read_text())
clips = plan['clips']
centres = plan['transition_centres']
frames = plan['frames']
if name == 'mthu':
    centres = [54, 115, 176, 237, 298, 359, 420]
    candidates = json.loads((edit/'mthu-review-beats.json').read_text())['candidates']
    assert set(centres) <= {candidate['frame'] for candidate in candidates}
    stock = repo/'Work/nuviko-videos-short-batch-20261110/new-footage'
    clips = clips + [
        {'path': str(stock/f'{number}.mp4'), 'source_in': 2, 'pre_crop': ''}
        for number in [33871227, 32120722, 28891505, 26346980]
    ]

fps = 30
half_window = 6
assert len(clips) == len(centres) + 1
assert min(b-a for a,b in zip([0,*centres],[*centres,frames])) > 2*half_window
prefix = f'{name}-review-{revision}'
previous = root/'Deliverables'/f"{plan['title']}-review-{old_revision}.mp4"
output = root/'Deliverables'/f"{plan['title']}-review-{revision}.mp4"
mask = edit/f'{base}-mask.mov'
if output.exists():
    print(f'Existing render, leaving it in place: {output.name}')
    raise SystemExit(0)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

for clip in clips:
    actual = sha(clip['path'])
    assert not clip.get('sha256') or actual == clip['sha256']
    clip['sha256'] = actual
filters = []
boundaries = [0,*centres,frames]
for i, (clip, first, last) in enumerate(zip(clips,boundaries,boundaries[1:])):
    length = (last-first+half_window*(i>0)+half_window*(i<len(clips)-1))/fps
    horizontal = '(iw-ow)*0.60' if 'deer' in clip['path'] else '(iw-ow)/2'
    filters.append(
        f"[{i}:v]trim=start={clip['source_in']}:duration={length+0.10:.6f},setpts=PTS-STARTPTS,"
        f"{clip.get('pre_crop','')}fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=bicubic,"
        f"crop=1080:1920:x='{horizontal}':y='(ih-oh)/2',tpad=stop_mode=clone:stop_duration=0.2,"
        f"trim=duration={length:.6f},setsar=1,settb=AVTB,format=yuv420p[v{i}]"
    )
current = 'v0'
for i, centre in enumerate(centres, 1):
    filters.append(f'[{current}][v{i}]xfade=transition=fade:duration=0.4:offset={(centre-half_window)/fps:.6f}[x{i}]')
    current = f'x{i}'
# One envelope controls both effects. Fade is at 50% where the effects peak.
pulse = '+'.join(f'(0.5+0.5*cos(PI*min(abs(n-{centre})/6,1)))' for centre in centres)
windows = '+'.join(f'between(t,{(centre-half_window)/fps:.6f},{(centre+half_window)/fps:.6f})' for centre in centres)
commands = []
for centre in centres:
    for delta in range(-half_window, half_window+1):
        # Commands fall between frames to avoid rounding at rational timestamps.
        when = (centre+delta-0.5)/fps
        amount = 0.5+0.5*math.cos(math.pi*delta/half_window)
        commands.append(f'{when:.8f} gblur@transition sigma {max(0.01,11*amount):.6f}')
contrast = "clip(127.5+1.30*(127.5-val),0,255)"
filters += [
    f"[{current}]eq=contrast=1.25:saturation=1.5,sendcmd=c='{' ; '.join(commands)}',"
    f"gblur@transition=sigma=0.01:enable='{windows}',"
    f"eq=contrast='1-0.22*({pulse})':brightness='0.0923*({pulse})':eval=frame:enable='{windows}',"
    'format=yuv444p,split[base][area]',
    f"[area]crop=896:384:(iw-ow)/2:(ih-oh)/2,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=gbrp,lutrgb=r='{contrast}':g='{contrast}':b='{contrast}'[inversion]",
    '[inversion]scale=out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv444p[invyuv]',
    f'[{len(clips)}:v]format=gbrp,extractplanes=g[alpha]',
    '[invyuv][alpha]alphamerge[layer]',
    '[base][layer]overlay=x=(W-w)/2:y=(H-h)/2:format=yuv420:repeatlast=0[video]',
]
graph = edit/f'{prefix}.ffgraph'
graph.write_text(';\n'.join(filters)+'\n')
argv = ['ffmpeg','-nostdin','-n','-v','error','-filter_complex_threads','2']
for clip in clips:
    argv += ['-i',clip['path']]
argv += ['-i',str(mask),'-i',str(previous),'-filter_complex_script',str(graph),'-map','[video]',
         '-map',f'{len(clips)+1}:a:0','-frames:v',str(frames),'-r','30','-fps_mode','cfr',
         '-c:v','libx264','-threads','3','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','copy',
         '-movflags','+faststart',str(output)]
plan.update({'previous_review': str(previous), 'previous_sha256': sha(previous), 'mask': str(mask),
             'mask_sha256': sha(mask), 'transition_centres': centres, 'transition_seconds': 0.4,
             'transition_types': ['fade'], 'transition_effects': ['fade-in', 'gaussian blur', 'luma lift'],
             'transition_graph_sha256': sha(graph), 'clips': clips, 'argv': argv,
             'audio': 'AAC stream copy from preceding checked review'})
(edit/f'{prefix}-contract.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
subprocess.run(argv, check=True)
