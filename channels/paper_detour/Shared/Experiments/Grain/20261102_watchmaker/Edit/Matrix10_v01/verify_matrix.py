"""Offline scoped QA, reading actual final frames. No subjective acceptance."""
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
W,H,N=2560,1440,2560*1440


def rgb(frame):
    a=np.frombuffer(frame,np.uint8)
    y=(a[:N].reshape(H,W).astype(np.float32)-16)/219
    u=(a[N:N+N//4].reshape(H//2,W//2).repeat(2,0).repeat(2,1).astype(np.float32)-128)/224
    v=(a[N+N//4:].reshape(H//2,W//2).repeat(2,0).repeat(2,1).astype(np.float32)-128)/224
    return Image.fromarray(np.clip(np.stack([y+1.5748*v,y-.187324*u-.468124*v,y+1.8556*u],axis=-1)*255,0,255).astype(np.uint8))


def main():
    rr=json.loads((HERE/'render_receipt.json').read_text())
    video=Path(rr['file']); evidence=HERE/'QA';evidence.mkdir(exist_ok=False)
    identity=hashlib.sha256(video.read_bytes()).hexdigest();assert identity==rr['sha256']
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
    (evidence/'ffprobe.json').write_text(json.dumps(probe,indent=2))
    assert len(probe['streams'])==1
    s=probe['streams'][0]
    for k,val in {'width':W,'height':H,'codec_name':'h264','profile':'High','pix_fmt':'yuv420p',
                  'color_space':'bt709','color_primaries':'bt709','color_transfer':'bt709','color_range':'tv',
                  'sample_aspect_ratio':'1:1','field_order':'progressive','nb_read_frames':'1280','r_frame_rate':'30/1'}.items():
        assert s[k]==val,(k,s.get(k),val)
    timeline=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames',
        '-show_entries','frame=best_effort_timestamp_time,key_frame,pict_type','-of','json',str(video)]))['frames']
    ts=np.asarray([float(f['best_effort_timestamp_time']) for f in timeline]);assert len(ts)==1280
    assert abs(ts[0])<.000002 and np.max(np.abs(np.diff(ts)-1/30))<.000002
    keys=[i for i,f in enumerate(timeline) if f['key_frame']]
    assert max(np.diff(keys))<=15
    decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-map','0:v:0','-f','null','-'],capture_output=True,text=True)
    (evidence/'full_decode.log').write_text(decoded.stderr);assert decoded.returncode==0 and not decoded.stderr
    # Parse top-level MP4 atoms without retaining extracted elementary streams.
    atoms=[]
    with video.open('rb') as f:
        while (head:=f.read(8)):
            size=int.from_bytes(head[:4],'big');kind=head[4:].decode('ascii');start=f.tell()-8
            if size==1: size=int.from_bytes(f.read(8),'big')
            atoms.append({'type':kind,'offset':start,'size':size});f.seek(start+size)
    assert next(x['offset'] for x in atoms if x['type']=='moov')<next(x['offset'] for x in atoms if x['type']=='mdat')
    indices=sorted({128*i+j for i in range(10) for j in (0,7,8,68,127)})
    expr='+'.join(f'eq(n\\,{i})' for i in indices)
    cmd=['ffmpeg','-v','error','-i',str(video),'-vf',f'select={expr}','-fps_mode','passthrough','-pix_fmt','yuv420p','-f','rawvideo','pipe:1']
    frames=subprocess.check_output(cmd); frame_bytes=N*3//2;assert len(frames)==frame_bytes*len(indices)
    actual={i:frames[k*frame_bytes:(k+1)*frame_bytes] for k,i in enumerate(indices)}
    strips=Image.new('RGB',(1280,960)); crops=Image.new('RGB',(1280,704)); cards=Image.new('RGB',(1280,1800))
    metrics=[]
    for group in range(2):
        sheet=Image.new('RGB',(1920,1800))
        for row in range(5):
            p=group*5+row
            for col,offset in enumerate((8,68,127)):
                idx=128*p+offset
                im=rgb(actual[idx]);im.thumbnail((640,360));sheet.paste(im,(640*col,360*row))
        sheet.save(evidence/f'frames_{group*5+1:02d}_{group*5+5:02d}.jpg',quality=94)
    base=np.frombuffer((ROOT/'Work/matrix10-v01/scratch/base_1440.yuv').read_bytes(),np.uint8,count=N).reshape(H,W)
    for p in range(10):
        idx=128*p+68; im=rgb(actual[idx]);im.crop((0,1248,2560,1440)).resize((1280,96)).save(evidence/f'label_{p+1:02d}.png')
        strips.paste(im.crop((0,1248,2560,1440)).resize((1280,96)),(0,p*96))
        tile=im.crop((1390,650,2030,1002));ImageDraw.Draw(tile).text((10,10),f'{p+1:02d}',fill='white',stroke_width=2,stroke_fill='black')
        # Save every native-pixel patch, plus compact overview from all ten.
        tile.save(evidence/f'grain_patch_{p+1:02d}.png')
        small=tile.resize((256,352));crops.paste(small,(p%5*256,p//5*352))
        card=rgb(actual[128*p]);card.thumbnail((640,360));cards.paste(card,(p%2*640,p//2*360))
        expected=np.frombuffer((ROOT/f'Work/matrix10-v01/scratch/expected_{p+1:02d}.yuv').read_bytes(),np.uint8,count=N).reshape(H,W)
        a=np.frombuffer(actual[idx],np.uint8,count=N).reshape(H,W)
        roi=(slice(100,1150),slice(100,2450))
        desired=(expected[roi].astype(np.float32)-base[roi]).ravel()
        encoded=(a[roi].astype(np.float32)-base[roi]).ravel()
        beta=float(np.dot(desired,encoded)/np.dot(desired,desired))
        metrics.append({'preset':p+1,'middle_frame':idx,'noise_projection_coefficient':beta,
                        'encoded_difference_rms':float(np.sqrt(np.mean(encoded**2))),
                        'note':'Projection relative to clean source, not a perceptual grain survival percentage'})
        assert beta>.3,(p+1,beta)
    strips.save(evidence/'labels_all.png');crops.save(evidence/'patches_overview.jpg',quality=95);cards.save(evidence/'cards_all.jpg',quality=94)
    report={'file':str(video),'sha256':identity,'contract':str(HERE/'EXPORT_CONTRACT_v01.json'),
            'contract_sha256':hashlib.sha256((HERE/'EXPORT_CONTRACT_v01.json').read_bytes()).hexdigest(),
            'stream_metadata':'PASS','full_decode':'PASS','cfr':'PASS;1280PTS at1/30s','frame_count':1280,'duration':1280/30,
            'fast_start':'PASS','top_level_atoms':atoms,'keyframe_indices':keys,'audio':'N_A: no stream, silent test',
            'motion':'N_A: same static source','srt':'N_A: silent technical preview','extracted_indices':indices,
            'inspected_indices':[],'frame_sampling':'PENDING_ACTUAL_INSPECTION','grain_metrics':metrics,
            'preencode_grain':'See render receipt; held fields/same seed/common mask; UV untouched above label',
            'independent_review':'NOT_PERFORMED; author self-review','user_acceptance':'PENDING',
            'youtube_visual':'PENDING','verdict':'TECHNICAL_CHECKS_PASS_FRAME_REVIEW_PENDING'}
    (evidence/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'file':str(video),'sha256':identity,'count':1280,'sample_count':len(indices),'projection_range':[min(x['noise_projection_coefficient'] for x in metrics),max(x['noise_projection_coefficient'] for x in metrics)]}))


if __name__=='__main__': main()
