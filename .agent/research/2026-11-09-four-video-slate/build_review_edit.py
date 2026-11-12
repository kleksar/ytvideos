"""Assemble a versioned edit, subtitle handoff and export passport for the slate."""
import json, math, subprocess as sp, sys, hashlib, datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PAPER=ROOT/'channels/paper_detour'
NUVIKO=ROOT/'channels/nuviko_history'
ENGINE=ROOT/'automation/ffmpeg_montage/montage.py'
DATA={
 'neptune':(PAPER/'research/2026-11-09-neptune','paper','short','Neptune-Paper-Detour-en-v01'),
 'cable':(PAPER/'research/2026-11-09-atlantic-cable','paper','long','Atlantic-Cable-Paper-Detour-en-v01'),
 'us':(NUVIKO/'research/us-history','nuviko','long','US-History-Nuviko-en-v01')
}
SUBJECTS=[
 ('expected and observed Uranus','Move toward the visible difference in the two positions'),
 ('small unseen planet tugging on Uranus','Open from the large planet toward the possible cause'),
 ('Le Verrier’s orbital calculation','Read across the orbit intersections at desk height'),
 ('prediction letter at Berlin','Move gently toward the destination stamp'),
 ('observer and chart at the telescope','Reveal the two separate positions within the dome'),
 ('unmatched star in the real sky','Close in on the one dot and corresponding gap'),
 ('offset and Neptune label','End by revealing both registrations and the physical name tab'),
]
KEEP={
 'neptune':['Urbain Le Verrier','Johann Galle','Heinrich d’Arrest','a star','By the next night'],
 'cable':['Cyrus Field','Wildman Whitehouse','William Thomson','Great Eastern','Heart\'s Content','six hundred miles','ocean floor'],
 'us':['New Orleans','Mississippi River','Saint-Domingue','Trail of Tears','Dred and Harriet Scott','Supreme Court','South Carolina','Fort Sumter','Fort Monroe','Ulysses S. Grant','Robert E. Lee','Puerto Rico','Thirteenth Amendment'],
}

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()

def ref(p):return dict(path=str(p),sha256=sha(p))

def read(p):return json.loads(p.read_text())

def dump(p,v):
 with p.open('x') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def pairs(seq):
 return [a+' '+b for phrase in seq for a,b in zip(phrase.split(),phrase.split()[1:])]

def setup(name):
 ep,ch,fmt,filename=DATA[name]
 d,w,a,q=[ep/p for p in ['Edit','Work','Assets/Audio','Deliverables']]
 for p in [d,w,q]:p.mkdir(parents=True,exist_ok=True)
 canvas=[1440,2560] if fmt=='short' else [2560,1440]
 word=w/'word-times-final-v01.json'; wm=read(word)
 transcript=ep/'Source/Script/narration_en_v01.txt'
 frames=wm['video_frames']; speech=wm['speech_frames']
 media=a/'full-mix-v01.wav'; speed=a/'HANDOFF.md'
 out=q/(filename+'.mp4'); manifest=d/'montage-v01.json'
 return ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest

def create(name):
 ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
 if name=='neptune':
  b=[0,140,279,410,543,677,833,frames]
 else:
  b=[round(30*t) for t in read(w/'proposed-shot-boundaries-v01.json')]
  b[-1]=speech; b.append(frames)
 prompts=read(w/'scene-prompt-manifest-v01.json')
 styles=[('none','in'),('left_to_right','out'),('right_to_left','none'),('none','in'),('right_to_left','out'),('none','in'),('left_to_right','out')] if name=='neptune' else [('none','in'),('left_to_right','out'),('right_to_left','none'),('none','in'),('right_to_left','out'),('left_to_right','none')]
 scenes=[]
 table=[]
 for i,(l,r) in enumerate(zip(b,b[1:])):
  is_end=fmt=='long' and i==len(b)-2
  assert (120<=r-l<=180) or (is_end and r-l==300),(name,i,l,r)
  direction,zoom=styles[i%len(styles)] if not is_end else ('none','none')
  prompt=prompts[i]['prompt']
  cue=' '.join(x['text'] for x in wm['words'] if l<=x['start']*30<r)
  subject,why=(SUBJECTS[i] if name=='neptune' else (prompt.split('. ')[0], 'Keep central action clear while moving the complete still'))
  t=0 if direction=='none' else (.008 if direction=='left_to_right' else -.008)
  zs={'in':(1.018,1.048),'out':(1.048,1.020),'none':(1.033,1.033)}
  z0,z1=(1,1) if is_end else zs[zoom]
  img=ep/f'Source/Images/v01/S{i+1:03d}.png'
  assert img.is_file(),img
  scene=dict(start_frame=l,end_frame=r,image=str(img),direction=direction,zoom=zoom,
    camera=dict(focus=[.5,.46],subject=subject,reason=why,start=dict(center=[.5+t,.5],scale=z0),end=dict(center=[.5-t,.5],scale=z1)))
  if is_end:scene['role']='end_screen'
  scenes.append(scene)
  table.append(dict(scene=f'S{i+1:03d}',start_frame=l,end_frame=r,narration_cue=cue,image=ref(img),purpose=subject,camera=scene['camera'],**prompts[i]))
 overlays=[]
 if ch=='paper':
  overlay=PAPER/'Shared/Overlays/Paper_Frame/masters'/f'paper-border-{"9x16" if fmt=="short" else "16x9"}-16s-v03.mov'
  assert overlay.is_file()
  overlays=[dict(role='paper_frame',path=str(overlay),start_frame=0,end_frame=frames,x=0,y=0)]
 dump(w/'shot-map-v01.json',table)
 dump(manifest,dict(channel=ch,format=fmt,fps=30,canvas=canvas,source_transfer='srgb',audio=str(media),
      audio_contract=dict(final_audio_sha256=sha(media),applied_speed=1.1,speed_evidence=str(speed)),
      scenes=scenes,subtitles=dict(mode='words',words=str(word),transcript=str(transcript),keep_together=pairs(KEEP[name]),
      end_frame=speech),overlays=overlays))
 (d/'pre-render-media-v01.md').write_text(f'# Pre-render media: {filename}\n\nFirst full review. No prior output to supersede. Protect Source/Images/v01, exact script/provider recordings, conformed mix and word map, shared soundtrack and Paper Frame when applicable. Unique Work/sub-prep-v01, Work/settings-v01 and Work/render-v01. Target {out}. Do not delete current MP4 or release dependencies.\n')

def prepare(name):
 ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
 sp.run([sys.executable,ENGINE,manifest,'--output',out,'--work-dir',w/'sub-prep-v01','--prepare-subtitles'],check=True)

def finish(name):
 ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
 p=read(manifest); prep=w/'sub-prep-v01'; plan=prep/'plan.json'
 deps=[media,*[Path(s['image']) for s in p['scenes']],*[Path(x['path']) for x in p['overlays']],word,transcript,d/'subtitle-review-v01.json',speed,prep/'subtitle_contract.json',w/'shot-map-v01.json']
 profile=ROOT/'.agents/skills/ytv-video-export/references/delivery.md'
 width,height=canvas
 passport=dict(schema_version=1,status='READY_TO_RENDER',episode=filename,language='en',format=fmt,purpose='Internal review candidate',
 settings_profile=ref(profile),
 edit=dict(project_id=filename,timeline_id=str(manifest),saved_revision_evidence='edit-v01; exact versioned montage and plan',timeline_read_path=str(plan),timeline_read_sha256=sha(plan),dependencies=[ref(x) for x in deps]),
 timeline=dict(width=width,height=height,aspect_ratio='9:16' if fmt=='short' else '16:9',sample_aspect_ratio='1:1',fps='30/1',frame_count=frames,duration_seconds=frames/30,output_color_space='Rec.709 SDR'),
 required_delivery=dict(container='MP4',video=dict(codec_name='h264',pix_fmt='yuv420p',scan='progressive',cadence='constant 30/1 fps',color_primaries='bt709',color_transfer='bt709',color_space='bt709',color_range='tv'),
  audio_contract=dict(owner_handoff=str(speed)+'; subjective listening UNVERIFIED',accepted_complete_mix=ref(media),source_rate_channels=dict(sample_rate_hz=48000,channels=2,codec='pcm_s24le'),codec_name='aac',profile='LC',sample_rate=48000,channels=2,target_bit_rate='256k')),
 encoding=dict(engine='FFmpeg montage.py',version_evidence=sp.check_output(['ffmpeg','-version'],text=True).splitlines()[0],requested_arguments=dict(encoder='libx264',video_bitrate='20M',output_pix_fmt='yuv420p',fps='30/1',audio_codec='aac',audio_profile='aac_low',audio_bitrate='256k',audio_sample_rate=48000,audio_channels=2),quality_preferences=['Measured native scene images; renderer scales to 2K delivery'],capability_evidence='FFmpeg and --check-settings',engine_managed_fields=['VBR, H.264 profile/level and GOP']),
 preflight=dict(author='Codex',time=datetime.datetime.now(datetime.timezone.utc).isoformat(),authorization_references=['2026-11-09: продолжай. все разрешаю. жду готовые мп4 на утверждение'],fresh_settings_evidence=str(manifest),writer_and_export_state='New exclusive review output; no prior MP4',output_path=str(out),overwrite=False,media_lifecycle_receipt=str(d/'pre-render-media-v01.md'),unresolved_required_fields=[]),render_receipt=None,qa_receipt=None,settings_check_receipt=None,render_provenance=None)
 dump(d/'export-contract-v01.json',passport)
 groups=read(prep/'caption_groups.json')['groups']
 buckets=[]; current=[]
 for group in groups:
  if current and (group[-1]['end']-current[0]['start']>4.7 or len(' '.join(x['text'] for x in current+group))>75):
   buckets.append(current); current=[]
  current+=group
  if current[-1]['text'][-1] in '.!?' and len(current)>2: buckets.append(current);current=[]
 if current:buckets.append(current)
 cues=[dict(start_seconds=x[0]['start'],end_seconds=x[-1]['end'],text=' '.join(t['text'] for t in x)) for x in buckets]
 dump(w/'srt-cues-v01.json',{'cues':cues})
 sp.run([sys.executable,ROOT/'.agents/skills/ytv-srt/scripts/srt_tool.py','build','--cues',w/'srt-cues-v01.json','--text',transcript,'--duration',str(frames/30),'--timebase','final','--output',out.with_suffix('.srt'),'--report',w/'srt-qa-v01.json'],check=True)

if __name__=='__main__':
 globals()[sys.argv[1]](sys.argv[2])
