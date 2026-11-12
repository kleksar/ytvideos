"""Read-only sampled QA of the explicit Palmier target; no export or mutation."""
import argparse,base64,importlib.util,json
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path('/Users/diplomat/ytvideos')
EP=ROOT/'channels/paper_detour/videos/032_galveston_1900'
W=EP/'Edit/Motion_v01'
parser=argparse.ArgumentParser();parser.add_argument('timeline');args=parser.parse_args()
spec=importlib.util.spec_from_file_location('motion',ROOT/'automation/image_motion/run.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=W/'Palmier_QA'/args.timeline;out.mkdir(parents=True,exist_ok=True)
c=m.Palmier(out)
state=c.call('get_timeline',{'projectId':'25533909','timelineId':args.timeline})
m.save(out/'timeline.json',state)
shots=json.loads((EP/'Edit/Review_v01/static_review_manifest_v01.json').read_text())['scenes']
cues=json.loads((W/'cue_motion_applied_v02.json').read_text())

def capture(frame):
    file=out/f'frame_{frame:05}.jpg'
    if file.exists():return file
    a={'projectId':'25533909','timelineId':args.timeline,'startFrame':frame}
    response=c.connection.request('tools/call',{'name':'inspect_timeline','arguments':a})
    if response.get('isError'):raise RuntimeError(response)
    images=[x for x in response['content'] if x.get('type')=='image']
    texts=[x for x in response['content'] if x.get('type')=='text']
    assert len(images)==1, 'Expected a composited frame'
    file.write_bytes(base64.b64decode(images[0]['data']))
    with (out/'inspection_metadata.jsonl').open('a') as f:
        f.write(json.dumps({'requested_frame':frame,'text':texts})+'\n')
    return file

scenes=[]
for i,s in enumerate(shots):
    a,z=s['start_frame'],s['end_frame_exclusive']
    frames=[round(a+(z-a-1)*t) for t in [0,.25,.5,.75,1]]
    for n in frames:capture(n)
    scenes.append({'id':s['id'],'frames':frames})
    m.save(out/'coverage.json',{'timeline':args.timeline,'scenes':scenes,'cues':[]})
    print(json.dumps({'inspected_scene':i+1}),flush=True)
for page in range(32):
    sheet=Image.new('RGB',(2560,4*312),'#202020');d=ImageDraw.Draw(sheet)
    for row,s in enumerate(scenes[page*4:page*4+4]):
        for col,n in enumerate(s['frames']):
            im=Image.open(capture(n)).convert('RGB').resize((512,288))
            x=col*512;y=row*312;sheet.paste(im,(x,y+24))
            d.text((x+4,y+5),f'{s["id"]} PALMIER f{n}',fill='white')
    sheet.save(out/f'scenes_{page+1:02}.jpg',quality=95)
cue_coverage=[]
for cue in cues:
    a,z=cue['start_frame'],cue['end_frame_exclusive'];N=z-a
    frames=sorted(set([a-1,a,a+2,a+4,a+N//4,a+N//2,a+3*N//4,z-5,z-3,z-1,z]))
    sheet=Image.new('RGB',(1536,((len(frames)+2)//3)*312),'#202020');d=ImageDraw.Draw(sheet)
    for j,n in enumerate(frames):
        im=Image.open(capture(n)).convert('RGB').resize((512,288));x=j%3*512;y=j//3*312
        sheet.paste(im,(x,y+24));d.text((x+4,y+5),f'{cue["id"]} PALMIER f{n}',fill='white')
    sheet.save(out/f'{cue["id"]}_path.jpg',quality=96)
    cue_coverage.append({'id':cue['id'],'frames':frames})
m.save(out/'coverage.json',{'timeline':args.timeline,'scenes':scenes,'cues':cue_coverage,
    'coverage':'Actual composited timeline: five samples per scene, all cut edges, eleven samples per cue. Sampling, not continuous playback; MP4 export QA not performed.'})
print(json.dumps({'status':'CAPTURE_COMPLETE','scenes':len(scenes),'cues':len(cue_coverage)}),flush=True)
