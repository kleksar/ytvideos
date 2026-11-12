import json, pathlib, math, importlib.util
from PIL import Image, ImageDraw, ImageFont
ROOT=pathlib.Path('/Users/diplomat/ytvideos')
EP=ROOT/'channels/nuviko_history/videos/009_black_death'
SHORT=EP/'Source/Shorts/05_labour'
EDIT=EP/'Edit/Short/black_death_labour_remake_v03'
RUN=EP/'Work/black-death-labour-short-caption-remake-v03'
PREFLIGHT=RUN/'subtitle_preflight'
PREFLIGHT.mkdir(parents=True,exist_ok=True)
raw=json.loads((RUN/'alignment_v03.json').read_text())
words=[{'text':('Nuviko' if x['text'].casefold()=='nuvico' else x['text']),'start':float(x['start']),'end':float(x['end']),'score':x.get('score')} for x in raw['words']]
phrases=['After the Black Death,','a worker\'s bargaining power','could change,','because so many workers had died.','Across England,','fields and workshops','still needed labour,','but the supply of people had fallen.','Some survivors could seek','better wages or another employer.','Landowners faced higher costs.','The government tried','to hold wages down.','An ordinance in 1349','and the Statute of Labourers','in 1351 sought to control pay','and compel work','under set conditions.','Those laws did not simply','restore the old order,','and change was uneven.','Survival did not mean freedom','from poverty or dependence,','but the catastrophe forced','a struggle over who decided','the value of work.','Watch the full story','on Nuviko History.']
profile=json.loads((ROOT/'automation/ffmpeg_montage/profiles/nuviko.json').read_text())
shortgeom=json.loads((ROOT/'automation/ffmpeg_montage/profiles/short.json').read_text())
font_size=53; pad_x=18; pad_y=14; canvas=(1440,2560); center_x=720; center_y=round(canvas[1]*shortgeom['center_y_ratio'])
font=ImageFont.truetype(profile['font'],font_size,index=profile['font_index'])
safe_text_width=shortgeom['max_visible_width_px']-2*pad_x
spec=importlib.util.spec_from_file_location('semantic_grouping',ROOT/'.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py')
grouping=importlib.util.module_from_spec(spec); spec.loader.exec_module(grouping)
groups=grouping.plan_phrases(words,phrases,font,safe_text_width)
widths=[float(font.getlength(' '.join(w['text'] for w in group))) for group in groups]
if max(widths)>safe_text_width: raise SystemExit('a phrase exceeds one-line width')
ascent,descent=font.getmetrics(); band_h=ascent+descent+2*pad_y+4; top=round(center_y-band_h/2); baseline=pad_y+ascent+2
states=PREFLIGHT/'caption_states'; states.mkdir(exist_ok=True)
def draw_state(gi,active):
 group=groups[gi]; line=' '.join(w['text'] for w in group); line_w=font.getlength(line); box_w=math.ceil(line_w+2*pad_x); x=round(center_x-box_w/2)
 im=Image.new('RGBA',(canvas[0],band_h),(0,0,0,0)); draw=ImageDraw.Draw(im)
 draw.rectangle((x,0,x+box_w-1,band_h-1),fill=profile['background'])
 pen=center_x-line_w/2
 for j,w in enumerate(group):
  draw.text((round(pen),baseline),w['text'],font=font,anchor='ls',fill=profile['highlight'] if j==active else profile['text'])
  pen+=font.getlength(w['text'])+font.getlength(' ')
 path=states/f'g{gi:02d}_w{active if active is not None else "neutral"}.png'
 if not path.exists(): im.save(path,compress_level=1)
 return path,box_w
frames=1152; events=[(0,draw_state(0,None)[0])]; word_events=[]; group_rows=[]
for gi,(phrase,group,text_width) in enumerate(zip(phrases,groups,widths)):
 first_frame=0 if gi==0 else math.ceil(group[0]['start']*30-1e-7)
 for wi,w in enumerate(group):
  frame=math.ceil(w['start']*30-1e-7)
  if not 0<=frame<frames: raise SystemExit(f'word out of frame range: {w}')
  png,_=draw_state(gi,wi); events.append((frame,png))
  word_events.append({'text':w['text'],'start_seconds':w['start'],'end_seconds':w['end'],'first_highlight_frame':frame,'group':gi})
 group_rows.append({'text':phrase,'start_frame':first_frame,'end_frame_exclusive':None,'word_count':len(group),'measured_text_width_px':round(text_width,2),'measured_panel_width_px':math.ceil(text_width+2*pad_x),'start_seconds':first_frame/30,'spoken_word_last_end_seconds':group[-1]['end']})
for i,row in enumerate(group_rows): row['end_frame_exclusive']=group_rows[i+1]['start_frame'] if i+1<len(group_rows) else frames
if group_rows[0]['start_frame']!=0 or group_rows[-1]['end_frame_exclusive']!=frames or any(a['end_frame_exclusive']!=b['start_frame'] for a,b in zip(group_rows,group_rows[1:])): raise SystemExit('subtitle continuity failure')
counts={}
for f,png in events: counts[f]=counts.get(f,0)+1
ordered=sorted({f:p for f,p in events}.items())
ffcat=RUN/'captions_v03.ffconcat'; lines=['ffconcat version 1.0']
for i,(frame,png) in enumerate(ordered):
 end=ordered[i+1][0] if i+1<len(ordered) else frames
 if end>frame: lines+=['file '+"'"+str(png).replace("'","'\\''")+"'",'option framerate 30',f'duration {(end-frame)/30:.12f}']
lines+=['file '+"'"+str(ordered[-1][1]).replace("'","'\\''")+"'",'option framerate 30']; ffcat.write_text('\n'.join(lines)+'\n')
# Phone-size composition contact sheet samples each scene at its temporal midpoint.
names=['S01_labour_field_v01.png','S02_empty_workshop_v01.png','S03_employer_offer_v01.png','S04_worker_choice_v01.png','S05_owner_worker_negotiation_v01.png','S06_labour_council_v01.png','S07_worker_stopped_v01.png','S08_field_work_rules_v01.png','S09_traveler_cta_v01.png']
thumb_w,thumb_h=390,694; margin=18; label_h=32; cols=3; rows=3
sheet=Image.new('RGB',(cols*thumb_w+(cols+1)*margin,rows*(thumb_h+label_h)+(rows+1)*margin),'#E9E1D4')
sd=ImageDraw.Draw(sheet); label_font=ImageFont.truetype(profile['font'],20,index=profile['font_index'])
for si,(name,t) in enumerate(zip(names,[(128*i+64)/30 for i in range(9)])):
 eligible=[i for i,w in enumerate(words) if w['start']<=t]; wi=max(eligible) if eligible else 0
 gi=next(j for j,g in enumerate(groups) if wi in [k for k in range(len(words)) if words[k] in g]); group=groups[gi]; local=group.index(words[wi]); overlay_path,_=draw_state(gi,local)
 im=Image.open(SHORT/'Images'/name).convert('RGB').resize((thumb_w,thumb_h),Image.Resampling.LANCZOS).convert('RGBA')
 overlay=Image.open(overlay_path).convert('RGBA').resize((thumb_w,round(band_h*thumb_w/canvas[0])),Image.Resampling.LANCZOS)
 im.alpha_composite(overlay,(0,round(top*thumb_h/canvas[1])))
 row,col=divmod(si,cols); x=margin+col*(thumb_w+margin); y=margin+row*(thumb_h+label_h+margin)
 sheet.paste(im.convert('RGB'),(x,y)); sd.text((x,y+thumb_h+4),f'S{si+1:02d} · {t:.2f}s · {phrases[gi]}',font=label_font,fill='#302D27')
contact=PREFLIGHT/'caption_scene_phone_contact_v03.jpg'; sheet.save(contact,quality=92)
report={'status':'PRE_RENDER_CHECKED; AUDIBLE_SYNC_UNVERIFIED','reference':'Nuviko selected field-notes treatment; Georgia Bold, fixed center, #20252B panel, #F3E9D5 text, #FFD166 current word, no outline.','style_decision':{'font_path':profile['font'],'font_size_px':font_size,'center_x_px':center_x,'center_y_ratio':shortgeom['center_y_ratio'],'center_y_px':center_y,'pad_x_px':pad_x,'pad_y_px':pad_y,'band_height_px':band_h,'top_px':top,'safe_area_max_visible_width_px':shortgeom['max_visible_width_px'],'safe_text_width_px':safe_text_width,'reason':'Current 104px shared Shorts size cannot fit several exact complete narration phrases within 1024px width. Use one uniform Georgia Bold 53px size matching the accepted Nuviko S01 type size while retaining fixed single-line geometry and Nuviko colors.'},'canvas':list(canvas),'fps':30,'frame_count':frames,'audio_speed':1.10,'video_speed_filter':'NONE; image scenes retimed to new narration duration','word_count':len(words),'phrase_count':len(groups),'max_text_width_px':round(max(widths),2),'phone_contact_sheet':str(contact),'audible_sync':'UNVERIFIED; two machine forced-alignment drafts agree closely, but no human listening was possible.','word_map':str(SHORT/'audio_word_times_v03.json'),'phrase_groups':group_rows,'word_events':word_events,'same_frame_event_collisions':sum(v>1 for v in counts.values()),'one_line_fit':'PASS_GEOMETRY_ONLY','subtitle_continuity':'PASS: first group frame 0, contiguous groups, last group ends at frame_count','position':'fixed screen-space center x=720 and y-ratio 0.762'}
(EDIT/'SUBTITLE_PREFLIGHT_v03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
plan={'channel':'nuviko','format':'short','fps':30,'canvas':[1440,2560],'audio':str(EP/'Assets/Generated/short_20261103_v03/audio/black_death_labour_short_audio_1_10x.m4a'),'scenes':[],'subtitles':{'mode':'overlay','path':str(ffcat),'y':top}}
movements=[('left_to_right','in'),('right_to_left','out'),('none','in'),('left_to_right','out'),('right_to_left','in'),('left_to_right','none'),('right_to_left','out'),('left_to_right','in'),('none','out')]
for i,(name,(direction,zoom)) in enumerate(zip(names,movements)):
 start=i*128; end=(i+1)*128
 plan['scenes'].append({'id':f'S{i+1:02d}','image':str(SHORT/'Images'/name),'start_frame':start,'end_frame':end,'direction':direction,'zoom':zoom})
(EDIT/'montage_plan_v03.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'groups':len(groups),'words':len(words),'max_width':round(max(widths),2),'top':top,'band_height':band_h,'frames':frames,'duration':frames/30,'plan':str(EDIT/'montage_plan_v03.json'),'captions':str(ffcat),'contact':str(contact)},ensure_ascii=False,indent=2))
