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
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    (evidence/'ffprobe.json').write_text(json.dumps(probe,indent=2))
    assert len(probe['streams'])==1
    s=probe['streams'][0]
    for k,val in {'width':W,'height':H,'codec_name':'h264','profile':'High','pix_fmt':'yuv420p',
                  'color_space':'bt709','color_primaries':'bt709','color_transfer':'bt709','color_range':'tv',
                  'sample_aspect_ratio':'1:1','field_order':'progressive','nb_frames':'1500','r_frame_rate':'30/1'}.items():
        assert s[k]==val,(k,s.get(k),val)
    timeline=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_packets',
        '-show_entries','packet=pts_time,dts_time,flags','-of','json',str(video)]))['packets']
    timeline.sort(key=lambda f:float(f['pts_time']))
    ts=np.asarray([float(f['pts_time']) for f in timeline]);assert len(ts)==1500
    assert abs(ts[0])<.000002 and np.max(np.abs(np.diff(ts)-1/30))<.000002
    keys=[i for i,f in enumerate(timeline) if 'K' in f['flags']]
    assert max(np.diff(keys))<=15
    # Parse top-level MP4 atoms without retaining extracted elementary streams.
    atoms=[]
    with video.open('rb') as f:
        while (head:=f.read(8)):
            size=int.from_bytes(head[:4],'big');kind=head[4:].decode('ascii');start=f.tell()-8
            if size==1: size=int.from_bytes(f.read(8),'big')
            atoms.append({'type':kind,'offset':start,'size':size});f.seek(start+size)
    assert next(x['offset'] for x in atoms if x['type']=='moov')<next(x['offset'] for x in atoms if x['type']=='mdat')
    indices=sorted({150*i+j for i in range(10) for j in (0,29,30,60,90,120,149)})
    expr='+'.join(f'eq(n\\,{i})' for i in indices)
    cmd=['ffmpeg','-v','error','-xerror','-i',str(video),'-filter_complex',
         f'[0:v]split=2[all][sample];[sample]select={expr}[pick]',
         '-map','[all]','-fps_mode','passthrough','-f','framemd5','pipe:2',
         '-map','[pick]','-fps_mode','passthrough','-pix_fmt','yuv420p','-f','rawvideo','pipe:1']
    decoded=subprocess.run(cmd,capture_output=True);assert decoded.returncode==0,decoded.stderr[-1000:]
    trace=decoded.stderr.decode();(evidence/'full_decode_framemd5.txt').write_text(trace)
    lines=[x for x in trace.splitlines() if x and not x.startswith('#')]
    assert len(lines)==1500 and all(len(x.split(','))==6 for x in lines)
    hashes=[x.split(',')[-1].strip() for x in lines]
    for p in range(10): assert len(set(hashes[p*150+30:p*150+150]))==120,'Duplicate motion frames'
    frames=decoded.stdout; frame_bytes=N*3//2;assert len(frames)==frame_bytes*len(indices)
    actual={i:frames[k*frame_bytes:(k+1)*frame_bytes] for k,i in enumerate(indices)}
    strips=Image.new('RGB',(1280,960)); crops=Image.new('RGB',(1280,704)); cards=Image.new('RGB',(1280,1800))
    metrics=[]
    for group in range(2):
        sheet=Image.new('RGB',(1920,1800))
        for row in range(5):
            p=group*5+row
            for col,offset in enumerate((30,90,149)):
                idx=150*p+offset
                im=rgb(actual[idx]);im.thumbnail((640,360));sheet.paste(im,(640*col,360*row))
        sheet.save(evidence/f'frames_{group*5+1:02d}_{group*5+5:02d}.jpg',quality=94)
    base=np.frombuffer((ROOT/'Work/matrix10-v02-motion/scratch/clean_middle.yuv').read_bytes(),np.uint8,count=N).reshape(H,W)
    for p in range(10):
        idx=150*p+90; im=rgb(actual[idx]);im.crop((0,1248,2560,1440)).resize((1280,96)).save(evidence/f'label_{p+1:02d}.png')
        strips.paste(im.crop((0,1248,2560,1440)).resize((1280,96)),(0,p*96))
        tile=im.crop((1390,650,2030,1002));ImageDraw.Draw(tile).text((10,10),f'{p+1:02d}',fill='white',stroke_width=2,stroke_fill='black')
        # Save every native-pixel patch, plus compact overview from all ten.
        tile.save(evidence/f'grain_patch_{p+1:02d}.png')
        small=tile.resize((256,352));crops.paste(small,(p%5*256,p//5*352))
        card=rgb(actual[150*p]);card.thumbnail((640,360));cards.paste(card,(p%2*640,p//2*360))
        expected=np.frombuffer((ROOT/f'Work/matrix10-v02-motion/scratch/expected_{p+1:02d}.yuv').read_bytes(),np.uint8,count=N).reshape(H,W)
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
    for group in range(2):
        sheet=Image.new('RGB',(1280,1800))
        for row in range(5):
            p=group*5+row
            for col,off in enumerate((60,120)):
                im=rgb(actual[150*p+off]);im.thumbnail((640,360));sheet.paste(im,(640*col,360*row))
        sheet.save(evidence/f'quarters_{group+1}.jpg',quality=94)
    ends=Image.new('RGB',(1280,1800))
    for p in range(10):
        im=rgb(actual[150*p+29]);im.thumbnail((640,360));ends.paste(im,(p%2*640,p//2*360))
    ends.save(evidence/'cards_end_all.jpg',quality=94)

    report={'file':str(video),'sha256':identity,'contract':str(HERE/'EXPORT_CONTRACT_v02.json'),
            'contract_sha256':hashlib.sha256((HERE/'EXPORT_CONTRACT_v02.json').read_bytes()).hexdigest(),
            'stream_metadata':'PASS','full_decode':'PASS;all1500decodedframes counted and hashed in one pass',
            'cfr':'PASS;1500packetPTS at1/30s plus1500decodedframes','frame_count':1500,'duration':50,
            'moving_frame_uniqueness':'PASS;all120actualdecodedframes distinct in each of10imageholds',
            'fast_start':'PASS','top_level_atoms':atoms,'keyframe_indices':keys,'audio':'N_A: no stream, silent test',
            'motion':'PENDING_FINAL_FRAME_REVIEW; identical120frame commonclip','srt':'N_A: silent technical preview','extracted_indices':indices,
            'inspected_indices':[],'frame_sampling':'PENDING_ACTUAL_INSPECTION','grain_metrics':metrics,
            'preencode_grain':'See render receipt; held fields/same seed/common mask; UV untouched above label',
            'independent_review':'NOT_PERFORMED; author self-review','user_acceptance':'PENDING',
            'youtube_visual':'PENDING','verdict':'TECHNICAL_CHECKS_PASS_FRAME_REVIEW_PENDING'}
    (evidence/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'file':str(video),'sha256':identity,'count':1500,'sample_count':len(indices),'projection_range':[min(x['noise_projection_coefficient'] for x in metrics),max(x['noise_projection_coefficient'] for x in metrics)]}))


if __name__=='__main__': main()
