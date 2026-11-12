import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
repo = root.parents[1]
edit = root / 'Edit'
footage = root / 'Source/Footage'
pilot = repo / 'Work/satisfying-runaway-pilot/Source'
stock = repo / 'Work/nuviko-videos-short-batch-20261110/new-footage'

plans = {
    'paparazzi': ('Paparazzi', 'paparazzi-rilds.aac', 40.53, 525, [126, 264, 403], [
        (footage/'nps-mowich-rainstorm.webm', 7, ''), (pilot/'36974946.mp4', 3, ''),
        (pilot/'32509235.mp4', 3, ''), (pilot/'34535413.mp4', 1, '')]),
    'mthu': ('Its-Like-Im-Not-Even-Here', 'mthu-rilds.mp3', 22.63, 477, [116, 240, 360], [
        (footage/'usda-bumblebee.webm', 11.7, 'crop=1920:1040:0:120,'), (pilot/'33353416.mp4', 2, ''),
        (footage/'okanagan-mule-deer.webm', 8, ''), (stock/'5061380.mp4', 2, '')]),
    'bloodstream': ('Bloodstream', 'bloodstream-rilds.aac', 25.56, 431, [111, 218, 327], [
        (pilot/'33771384.mp4', 1, ''), (pilot/'35867202.mp4', 2, ''),
        (pilot/'36221445.mp4', 2, ''), (pilot/'8859850.mp4', 2, '')]),
}
for key, data in json.loads((edit/'dynamic-review-plans.json').read_text()).items() if (edit/'dynamic-review-plans.json').exists() else []:
    plans[key] = (data['title'], data['music'], data['offset'], data['frames'], data['preferred'],
                  [(repo/path, trim, '') for path, trim in data['clips']])
name = sys.argv[1]
title, music, offset, frames, preferred, clips = plans[name]
dynamic = name in ('super-funk', 'bow-bow-bow')
revision = sys.argv[2] if len(sys.argv)>2 else 'v01'
prefix = f'{name}-review' if revision=='v01' else f'{name}-review-{revision}'
source = root/'Source'/music
output = root/'Deliverables'/f'{title}-review-{revision}.mp4'
if output.exists():
    raise SystemExit(f'Output already exists: {output}')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(argv):
    subprocess.run([str(x) for x in argv], check=True, cwd=repo)

duration = frames/30
excerpt = edit/f'{prefix}-excerpt.wav'
beats = edit/f'{prefix}-beats.json'
if not excerpt.exists():
    run(['ffmpeg','-nostdin','-n','-v','error','-ss',offset,'-i',source,'-t',duration,'-c:a','pcm_s16le',excerpt])
if not beats.exists():
    run(['python3','automation/music_beats.py',excerpt,'--fps',30,'--output',beats])
attacks = json.loads(beats.read_text())['candidates']
centres = [min((a['frame'] for a in attacks if abs(a['frame']-ideal)<=12), key=lambda f:abs(f-ideal), default=ideal) for ideal in preferred]

analysis_path = edit/('vocals.json' if name=='super-funk' else f'{name}-analysis.json')
analysis = json.loads(analysis_path.read_text())
words = []
for segment in analysis['segments']:
    if name=='bow-bow-bow' and 8.7<segment['start']<9.0:
        continue  # Garbled pre-roll from the previous phrase.
    if name=='super-funk' and not 4.5<segment['start']<4.7:
        continue  # Only the first clearly identified phrase is ready for the review.
    seq = segment['words']
    idx = 0
    while idx < len(seq):
        word = seq[idx]
        token = word['word'].strip(' 🎵,!? .')
        start,end = word['start'],word['end']
        if name=='super-funk' and token=='Tomades':
            token=''
        if name=='super-funk' and token=='putarria':
            token='putaria'
        if name=='bloodstream' and token=='To' and start==end==32.82:
            start=32.74  # Draft estimate in the gap before “pick”.
        if dynamic and end<=start:
            start=max(offset,start-0.067)  # Draft timing for a short, clipped syllable.
        if name=='paparazzi' and token=='Papa':
            token='PaPa'
        if name=='paparazzi' and token=='Red' and idx+1<len(seq) and seq[idx+1]['word'].strip(' ,.!?')=='Sea':
            token='Paparazzi'
            idx+=1
            end=seq[idx]['end']
        if token and end>offset and start<offset+duration:
            words.append({'text':token,'start_seconds':start,'end_seconds':end})
        idx+=1
words.sort(key=lambda item:item['start_seconds'])
wordmap = edit/f'{prefix}-words.json'
wordmap.write_text(json.dumps({'words':words},ensure_ascii=False,indent=2)+'\n')
mask=edit/f'{prefix}-mask.mov'
mask_plan=edit/f'{prefix}-caption-plan.json'
run(['python3','automation/captions/music_lyrics.py',wordmap,'--font','/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf','--font-size',147,'--output',mask,'--plan',mask_plan,'--offset',offset,'--frames',frames,'--invert-masks','--max-words',1,'--tilt-every',6])

boundaries=[0,*centres,frames]
blend_half=4 if dynamic else 6
transition_duration=2*blend_half/30
transition_types=('smoothleft','radial','smoothup','circleopen','smoothright','fadefast') if dynamic else ('fade',)
filters=[]
for i,((path,trim,pre),start,end) in enumerate(zip(clips,boundaries,boundaries[1:])):
    length=(end-start+blend_half*(i>0)+blend_half*(i<len(clips)-1))/30
    side_crop='(iw-ow)*0.60' if 'deer' in path.name else '(iw-ow)/2'
    filters.append(f"[{i}:v]trim=start={trim}:duration={length+0.10:.6f},setpts=PTS-STARTPTS,{pre}fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=bicubic,crop=1080:1920:x='{side_crop}':y='(ih-oh)/2',tpad=stop_mode=clone:stop_duration=0.2,trim=duration={length:.6f},setsar=1,settb=AVTB,format=yuv420p[v{i}]")
previous='v0'
for i,centre in enumerate(centres,1):
    effect=transition_types[(i-1)%len(transition_types)]
    filters.append(f'[{previous}][v{i}]xfade=transition={effect}:duration={transition_duration:.6f}:offset={(centre-blend_half)/30:.6f}[x{i}]')
    previous=f'x{i}'
if dynamic:
    pulse='+'.join(f'pow(max(0,1-abs(n-{centre})/3),2)' for centre in centres)
    colour=f"eq=contrast=1.25:saturation=1.5:brightness='0.055*({pulse})':eval=frame"
else:
    colour='eq=contrast=1.25:saturation=1.5'
filters += [
    f'[{previous}]{colour},format=yuv444p,split[base][area]',
    '[area]crop=896:384:(iw-ow)/2:(ih-oh)/2,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=gbrp,lutrgb=r=negval:g=negval:b=negval,lutrgb=r=contrast:g=contrast:b=contrast[inversion]'.replace('lutrgb=r=contrast:g=contrast:b=contrast',"lutrgb=r='clip(127.5+1.30*(val-127.5),0,255)':g='clip(127.5+1.30*(val-127.5),0,255)':b='clip(127.5+1.30*(val-127.5),0,255)'") ,
    '[inversion]scale=out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv444p[invyuv]',
    f'[{len(clips)}:v]format=gbrp,extractplanes=g[alpha]',
    '[invyuv][alpha]alphamerge[layer]',
    '[base][layer]overlay=x=(W-w)/2:y=(H-h)/2:format=yuv420:repeatlast=0[video]',
    f'[{len(clips)+1}:a]volume={-5.5 if name=="super-funk" else -3 if dynamic else 0}dB,afade=t=in:d=0.07,afade=t=out:st={duration-0.19:.6f}:d=0.19[audio]',
]
graph=edit/f'{prefix}.ffgraph'
graph.write_text(';\n'.join(filters)+'\n')
argv=['ffmpeg','-nostdin','-n','-v','error','-filter_complex_threads',2]
for clip,_,_ in clips:
    argv+=['-i',clip]
argv += ['-i',mask,'-i',excerpt,'-filter_complex_script',graph,'-map','[video]','-map','[audio]','-t',duration,'-r',30,'-fps_mode','cfr','-c:v','libx264','-threads',3,'-preset','veryfast','-crf',19,'-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar',44100,'-ac',2,'-movflags','+faststart',output]
contract={'title':title,'source':str(source),'source_sha256':digest(source),'offset':offset,'frames':frames,'fps':30,'size':[1080,1920],'transition_centres':centres,'transition_seconds':transition_duration,'transition_types':transition_types,'clips':[{'path':str(p),'source_in':t,'sha256':digest(p),'pre_crop':crop} for p,t,crop in clips],'lyrics':'ASR draft with scoped manual corrections; listening pending','argv':[str(x) for x in argv]}
(edit/f'{prefix}-contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
run(argv)
