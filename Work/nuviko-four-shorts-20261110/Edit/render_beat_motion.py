"""Render the corrected accent, camera motion and soft-title pass."""
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
edit = root / 'Edit'
name = sys.argv[1]
variant = 'hold' if '--hold' in sys.argv[2:] else 'sync' if '--sync' in sys.argv[2:] else 'unique' if '--unique' in sys.argv[2:] else 'dynamic'
dynamic = any(flag in sys.argv[2:] for flag in ('--dynamic','--unique','--sync','--hold'))
if dynamic:
    spec = json.loads((edit / f'{name}-{variant}-input.json').read_text())
    timeline = json.loads((edit / f'{name}-{variant}-timeline.json').read_text())
    rhythm = {
        **spec, 'reference': spec['media'], 'reference_sha256': spec['media_sha256'],
        'accents': timeline['accents'], 'method': 'Constrained cadence planner on measured attacks.',
    }
else:
    rhythm = json.loads((edit / 'beat-motion-accents.json').read_text())[name]
old_revision, revision = rhythm['old_revision'], rhythm['new_revision']
plan = json.loads((edit / f'{name}-review-{old_revision}-contract.json').read_text())
clips = timeline['clips'] if dynamic else plan['clips']
centres = [accent['frame'] for accent in rhythm['accents']]
frames = plan['frames']
fps = 30
lead, tail = (1, 2) if dynamic else (2, 4)
prefix = f'{name}-review-{revision}'
previous = Path(rhythm['reference'])
output = root / 'Deliverables' / f"{plan['title']}-review-{revision}.mp4"
partial = root / 'Work' / f'{prefix}.encoding.mp4'
mask = Path(rhythm.get('caption_mask', plan['mask']))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

assert not output.exists() and not partial.exists()
assert sha(previous) == rhythm['reference_sha256']
assert sha(mask) == rhythm.get('caption_mask_sha256', plan['mask_sha256'])
assert len(clips) == len(centres) + 1
assert min(b-a for a,b in zip([0, *centres], [*centres, frames])) > lead + tail

filters, motion = [], []
boundaries = [0, *centres, frames]
for i, (clip, first, last) in enumerate(zip(clips, boundaries, boundaries[1:])):
    actual = sha(clip['path'])
    assert clip.get('sha256', actual) == actual
    clip['sha256'] = actual
    count = last - first + lead * (i > 0) + tail * (i < len(clips)-1)
    length = count / fps
    horizontal = '(iw-ow)*0.60' if 'deer' in clip['path'] else '(iw-ow)/2'
    first_scale, last_scale = (0.95, 1.05) if i % 2 == 0 else (1.05, 0.95)
    u = f'min(on/{count-1},1)'
    easing = f'(0.7*{u}+0.3*{u}*{u}*(3-2*{u}))'
    # The full overscan image represents 95% of the base framing.
    zoom = f'({first_scale}+({last_scale-first_scale:.5f})*{easing})/0.95'
    filters.append(
        f"[{i}:v]trim=duration={length+0.10:.6f},setpts=PTS-STARTPTS,"
        f"{clip.get('pre_crop','')}fps=30,scale=1440:2560:force_original_aspect_ratio=increase:flags=bicubic,"
        f"crop=1440:2560:x='{horizontal}':y='(ih-oh)/2',tpad=stop_mode=clone:stop_duration=0.2,"
        f"format=yuv420p,zoompan=z='{zoom}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,"
        f"trim=end_frame={count},setsar=1,settb=1/30[v{i}]"
    )
    motion.append({'first_frame': first-lead*(i>0), 'frames': count,
                   'relative_scale': [first_scale,last_scale], 'formula':zoom})

current = 'v0'
# By the attack the incoming plan has 70% opacity. The exit eases into full opacity.
weight = 'if(gte(P,2/3),0.70*(1-P)*3,0.70+0.30*sin((1-P-1/3)*3*PI/4))'
for i, centre in enumerate(centres, 1):
    filters.append(
        f"[{current}][v{i}]xfade=transition=custom:expr='A*(1-({weight}))+B*({weight})':"
        f"duration={(lead+tail)/fps:.6f}:offset={(centre-lead)/fps:.8f}[x{i}]"
    )
    current = f'x{i}'

commands, windows = [], []
for centre in centres:
    windows.append(f'between(t,{(centre-lead-0.1)/fps:.8f},{(centre+tail+0.1)/fps:.8f})')
    for delta in range(-lead, tail+1):
        when = (centre+delta-0.5)/fps
        amount = 0.5+0.5*math.cos(math.pi*delta/(lead if delta<0 else tail))
        commands.append(f'{when:.8f} gblur@transition sigma {max(0.01,9*amount):.6f}')
        commands.append(f'{when:.8f} eq@transition brightness {0.068*amount:.6f}')
        commands.append(f'{when:.8f} eq@transition contrast {1-0.15*amount:.6f}')
window = '+'.join(windows)
# Soften the alpha, not the footage. The tone curve preserves inverted colors without clipping their endpoints.
contrast = "127.5+107*(127.5-val)/127.5"
filters.extend([
    f"[{current}]eq=contrast=1.25:saturation=1.5,sendcmd=c='{' ; '.join(commands)}',"
    f"gblur@transition=sigma=0.01:steps=1:enable='{window}',"
    f"eq@transition=contrast=1:brightness=0:enable='{window}',split[base][area]",
    f"[area]crop=896:384:(iw-ow)/2:(ih-oh)/2,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=gbrp,lutrgb=r='{contrast}':g='{contrast}':b='{contrast}'[inversion]",
    '[inversion]scale=out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p[invyuv]',
    f'[{len(clips)}:v]format=gbrp,extractplanes=g,gblur=sigma=1.65:steps=2,lut=y=val*0.94[alpha]',
    '[invyuv][alpha]alphamerge[layer]',
    '[base][layer]overlay=x=(W-w)/2:y=(H-h)/2:format=yuv420:repeatlast=0[video]',
])
graph = edit / f'{prefix}.ffgraph'
graph.write_text(';\n'.join(filters)+'\n')
argv = ['ffmpeg','-nostdin','-n','-v','error','-filter_complex_threads','2']
for clip, movement in zip(clips, motion):
    argv.extend(['-threads','1','-ss',str(clip['source_in']),
                 '-t',str(movement['frames']/fps+.20),'-i',clip['path']])
argv.extend(['-threads','1','-i',str(mask),'-i',str(previous),'-filter_complex_script',str(graph),
             '-map','[video]','-map',f'{len(clips)+1}:a:0','-frames:v',str(frames),'-r','30',
             '-fps_mode','cfr','-c:v','libx264','-threads','3','-preset','superfast','-crf','18',
             '-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
             '-c:a','copy','-bsf:v',
             'h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0',
             '-movflags','+faststart+write_colr',str(partial)])
plan.pop('colour_metadata_mux_argv',None)
plan.update({'mask':str(mask),'mask_sha256':sha(mask),'clips':clips,'output':str(output),'previous_review':str(previous),'previous_sha256':sha(previous),
             'transition_centres':centres,'transition_seconds':(lead+tail)/fps,
             'transition_lead_frames':lead,'transition_tail_frames':tail,'incoming_opacity_on_accent':0.70,
             'transition_graph_sha256':sha(graph),'accents':rhythm['accents'],'rhythm_method':rhythm['method'],
             'motion':motion,'caption_alpha_sigma':1.65,'caption_opacity':0.94,'argv':argv,
             'audio':'AAC stream copy from preceding checked review'})
(edit/f'{prefix}-contract.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
subprocess.run(argv, check=True)
os.replace(partial, output)
print(output, flush=True)
