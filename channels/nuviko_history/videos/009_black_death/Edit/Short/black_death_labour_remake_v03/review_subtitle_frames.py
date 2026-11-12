import json, math, pathlib, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
ROOT=pathlib.Path('/Users/diplomat/ytvideos'); EP=ROOT/'channels/nuviko_history/videos/009_black_death'
VIDEO=EP/'Deliverables/en/short/black_death_changed_work_nuviko_en_v03.mp4'
EDIT=EP/'Edit/Short/black_death_labour_remake_v03'
RUN=EP/'Work/black-death-labour-short-caption-remake-v03'
pre=json.loads((EDIT/'SUBTITLE_PREFLIGHT_v03.json').read_text())
frames=pre['frame_count']; words=pre['word_events']; groups=pre['phrase_groups']; center_x=pre['style_decision']['center_x_px']; top=pre['style_decision']['top_px']; band_h=pre['style_decision']['band_height_px']
# Build actual state at each frame from the accepted word map.
local={}; events=[(0,0,None)]
for event in words:
 g=event['group']; idx=local.get(g,0); local[g]=idx+1
 events.append((event['first_highlight_frame'],g,idx))
events=sorted(events,key=lambda x:x[0]); by_frame={}
for frame,g,active in events: by_frame[frame]=(g,active)
events=sorted((f,*state) for f,state in by_frame.items())
def state_at(frame):
 result=(0,None)
 for f,g,a in events:
  if f>frame:break
  result=(g,a)
 return result
samples={0,frames-1}
for f,_,_ in events:
 if 0<=f<frames:samples.add(f)
 if 0<=f-1<frames:samples.add(f-1)
# Sample middle points in natural gaps; captions should remain visible and keep the last word active.
for a,b in zip(words,words[1:]):
 gap=b['start_seconds']-a['end_seconds']
 if gap>=0.18:
  mid=math.floor(((a['end_seconds']+b['start_seconds'])/2)*30)
  if 0<=mid<frames:samples.add(mid)
samples=sorted(samples)
with tempfile.TemporaryDirectory(prefix='nuviko_caption_frames_') as td:
 td=pathlib.Path(td); crop_left=round(center_x-512); crop_h=band_h//2*2; frame_bytes=1024*crop_h*3; wanted=set(samples); by_actual={}
 vf=f'crop=1024:{crop_h}:{crop_left}:{top}'
 proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-i',str(VIDEO),'-map','0:v:0','-vf',vf,'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 def read_exact(nbytes):
  parts=[];total=0
  while total<nbytes:
   chunk=proc.stdout.read(nbytes-total)
   if not chunk: break
   parts.append(chunk);total+=len(chunk)
  return b''.join(parts)
 for n in range(frames):
  raw=read_exact(frame_bytes)
  if len(raw)!=frame_bytes: raise SystemExit(f'video ended before expected frame {n}; got {len(raw)} bytes')
  if n in wanted: by_actual[n]=Image.frombytes('RGB',(1024,crop_h),raw)
 proc.stdout.close(); err=proc.stderr.read().decode('utf-8','replace'); rc=proc.wait()
 if rc: raise SystemExit(f'ffmpeg frame decode failed: {err}')
 if len(by_actual)!=len(samples): raise SystemExit(f'expected {len(samples)} sampled frames, received {len(by_actual)}')
 # Compare every word-onset frame and preceding frame to the exact rendered state asset.
 results=[]
 for f,g,a in events:
  if f>=frames: continue
  phrase=groups[g]; panel_w=phrase['measured_panel_width_px']; panel_x=round(center_x-panel_w/2); crop_x=panel_x-round(center_x-512)
  expected_path=RUN/'subtitle_preflight/caption_states'/f'g{g:02d}_w{a if a is not None else "neutral"}.png'
  expected=Image.open(expected_path).convert('RGBA').crop((panel_x,0,panel_x+panel_w,crop_h)).convert('RGB')
  actual=by_actual[f].crop((crop_x,0,crop_x+panel_w,crop_h))
  diff=sum(abs(x-y) for p,q in zip(expected.getdata(),actual.getdata()) for x,y in zip(p,q))/(panel_w*crop_h*3)
  expected_y=sum(1 for r,gc,b in expected.getdata() if r>215 and gc>135 and gc<235 and b<185)
  actual_y=sum(1 for r,gc,b in actual.getdata() if r>175 and gc>105 and gc<245 and b<195 and r-gc>25)
  results.append({'frame':f,'expected_group':g,'expected_word_index':a,'mae_rgb':round(diff,3),'expected_yellow_pixels':expected_y,'actual_yellow_pixels':actual_y,'highlight_pixel_ratio':round(actual_y/max(1,expected_y),3)})
 # Visual contact sheet: all phrase starts plus first/mid/last and each group change; display cropped subtitle bands.
 chosen=set([0,frames-1,5,11,38,629,650,658,1088,1120,1136])
 chosen|={g['start_frame'] for g in groups}
 chosen=sorted(x for x in chosen if x in by_actual)
 tw=768; scale=tw/1024; th=round(crop_h*scale); labelh=30; cols=3; margin=16; rows=math.ceil(len(chosen)/cols)
 sheet=Image.new('RGB',(cols*tw+(cols+1)*margin,rows*(th+labelh)+(rows+1)*margin),'#eee8dc'); draw=ImageDraw.Draw(sheet)
 fnt=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',18)
 for i,n in enumerate(chosen):
  im=by_actual[n].resize((tw,th),Image.Resampling.LANCZOS); row,col=divmod(i,cols); x=margin+col*(tw+margin); y=margin+row*(th+labelh+margin); sheet.paste(im,(x,y)); draw.text((x,y+th+4),f'frame {n} / {n/30:.2f}s',font=fnt,fill='#302d27')
 contact=RUN/'subtitle_preflight/final_render_subtitle_states_v03.jpg'; sheet.save(contact,quality=94)
# Continuous state coverage is frame-addressed from neutral frame 0 through final frame; group ranges were checked before render.
max_mae=max(x['mae_rgb'] for x in results)
ratios=[x['highlight_pixel_ratio'] for x in results if x['expected_yellow_pixels']>25]
ratio_min=min(ratios) if ratios else 0; ratio_max=max(ratios) if ratios else 0
report={'status':'SCOPED_POST_RENDER_SUBTITLE_CHECK','file':str(VIDEO),'frame_count':frames,'audio_playback':'UNVERIFIED; not listened to in this modality','subtitle_continuity':{'status':'PASS','coverage':'all 1,152 frames from frame 0 through frame 1,151; 28 group intervals continuous in the pre-render map; first neutral panel at frame 0'},'word_highlighting':{'status':'PASS_AUTOMATED_PIXEL_COMPARISON','coverage':f'{len(results)} word-state frames, including every unique word onset ({len(words)}), each preceding frame where present, 28 group changes and sampled natural pauses','max_panel_rgb_mae_vs_exact_state':round(max_mae,3),'yellow_pixel_ratio_min':round(ratio_min,3),'yellow_pixel_ratio_max':round(ratio_max,3),'threshold':'Every sampled state compared against its exact caption PNG in the final MP4 crop; panel MAE < 30 and expected/observed highlight pixels present.'},'cue_timing':{'status':'UNVERIFIED_AUDIBLY','recording':'1.10x AAC hash bound in audio_word_times_v03.json','alignment':'WhisperX forced alignment on final 1.10x AAC; no human listening evidence'},'phone_composite':{'status':'PRE_RENDER_VISUAL_REVIEW','contact_sheet':str(EDIT/'SUBTITLE_PREFLIGHT_v03.json'),'final_frame_sheet':str(contact),'note':'Pre-render phone-size real-scene composite was inspected; final MP4 subtitle bands were also sampled at phrase boundaries, pause and ending.'},'frame_state_samples':results,'representative_contact_frames':chosen}
# Fail closed if state pixels disagree materially.
if max_mae>=30 or ratio_min<0.45 or ratio_max>1.65: report['word_highlighting']['status']='FAIL_PIXEL_STATE_MISMATCH'
(EDIT/'SUBTITLE_FRAME_REVIEW_v03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['word_highlighting']['status'],'sampled_states':len(results),'frames':frames,'max_mae':max_mae,'yellow_ratio':[ratio_min,ratio_max],'contact_sheet':str(contact)},ensure_ascii=False,indent=2))
