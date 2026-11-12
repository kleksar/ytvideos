import json
import subprocess
from pathlib import Path

root = Path('/Users/diplomat/ytvideos')
work = root / 'Work/nuviko-videos-short-batch-20261110'
source = root / 'Work/satisfying-runaway-pilot/Source'
plans = [
 {'name':'running-away-hd-v02','track':'BADBADNOTGOOD and Samuel T Herring - Running Away Time','reference':'running-away-time-reference.mp3','reference_offset':0,'cuts':[0,59,116,173,231,288,345,403,450],'shots':['/Users/diplomat/ytvideos/Work/nuviko-videos-short-batch-20261110/pexels-30320376.mp4','34535413.mp4','/Users/diplomat/ytvideos/Work/nuviko-videos-short-batch-20261110/pexels-35188969.mp4','6316369.mp4','32509235.mp4','/Users/diplomat/ytvideos/Work/nuviko-videos-short-batch-20261110/pexels-36086839.mp4','33353416.mp4','8859850.mp4']},
 {'name':'bloodstream-hd-v02','track':'Alyssa Grace - bloodstream','reference':'bloodstream-reference.m4a','reference_offset':2.233333,'cuts':[0,39,110,165,201,253,327,379,462],'shots':['35867202.mp4','/Users/diplomat/ytvideos/Work/nuviko-videos-short-batch-20261110/pexels-35179742.mp4','34535413.mp4','/Users/diplomat/ytvideos/Work/nuviko-videos-short-batch-20261110/pexels-37362542.mp4','32509235.mp4','36974946.mp4','6316369.mp4','/Users/diplomat/ytvideos/Work/nuviko-videos-short-batch-20261110/pexels-35188969.mp4']},
]
for plan in plans:
    name = plan['name']
    output = work / f'{name}-draft-v01.mp4'
    assert not output.exists()
    filters = []
    for index, (start, end) in enumerate(zip(plan['cuts'], plan['cuts'][1:])):
        frames = end-start
        filters.append(f"[{index}:v]fps=30,trim=start=1:end={1+frames/30:.8f},setpts=PTS-STARTPTS,scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,zoompan=z='1+0.1*(1-cos(PI*on/{frames-1}))/2':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s=1080x1920:fps=30,setsar=1,setpts=PTS-STARTPTS[v{index}]")
    filters.append(''.join(f'[v{i}]' for i in range(len(plan['shots']))) + f"concat=n={len(plan['shots'])}:v=1:a=0,eq=contrast=1.25,unsharp=5:5:0.75:5:5:0,split[base][high]")
    filters.append("[high]lutyuv=y='max(0,val-190)*3':u=128:v=128,gblur=sigma=12[glow]")
    cuts = plan['cuts'][1:-1]
    glow = '+'.join(f'pow((1+cos(PI*min(abs(T*30-{n})/3.75,1)))/2,2)' for n in cuts)
    blur = '+'.join(f'((1+cos(PI*min(abs(T*30-{n})/7.5,1)))/2)' for n in cuts)
    filters.append(f"[base][glow]blend=c0_expr='min(235,A+B*0.8*({glow}))':c1_expr='A':c2_expr='A',split[clean][blur_source]")
    filters.append('[blur_source]gblur=sigma=6[blurred]')
    filters.append(f"[clean][blurred]blend=all_expr='A+(B-A)*0.55*({blur})',scale=1108:1936:flags=lanczos,crop=1080:1920:x='14+6*sin(n*4.3)*({blur.replace('T*30','n')})':y='8+4*cos(n*3.1)*({blur.replace('T*30','n')})',setsar=1[video]")
    graph = work / f'{name}-draft-v01.ffgraph'
    graph.write_text(';\n'.join(filters)+'\n')
    argv=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-filter_complex_threads','2']
    for shot in plan['shots']:
        argv += ['-i',str(source/shot)]
    argv += ['-filter_complex_script',str(graph),'-map','[video]','-an','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
    plan.update({'kind':'low-resolution visual timing draft, not publication','output':str(output),'fps':30,'reference_only':True,'native_audio_offset':'unverified','lyric_captions':'pending manual verification','argv':argv})
    (work/f'{name}-draft-v01.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    subprocess.run(argv,check=True)
