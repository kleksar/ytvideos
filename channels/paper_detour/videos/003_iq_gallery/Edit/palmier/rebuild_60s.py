import sys,json,pathlib,base64,time
from PIL import Image
root=pathlib.Path('/Users/diplomat/ytvideos'); out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier'; src=root/'channels/paper_detour/videos/003_iq_gallery/Source';lock=root/'channels/paper_detour/.rarovista-timeline-lock/owner.md'
sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
session=json.loads((out/'session_60s_active.json').read_text());c=PalmierConnection();c.headers=session['headers'];c.seq=session['seq'];refs=json.loads((out/'refs.json').read_text()); log=out/'receipt_60s.jsonl'
def call(name,args):
 assert lock.exists() and '/root/film_editor' in lock.read_text(),'lock lost'
 res=c.request('tools/call',{'name':name,'arguments':args});
 if res.get('isError'):raise RuntimeError((name,res))
 text=[a['text'] for a in res.get('content',[]) if a.get('type')=='text']
 try: obj=json.loads(text[0]) if len(text)==1 else {'texts':text}
 except ValueError:obj={'texts':text}
 if name=='inspect_timeline':
  for j,item in enumerate(res.get('content',[])):
   if item.get('type')=='image':(out/f'minute_f{args["startFrame"]}_{j}.png').write_bytes(base64.b64decode(item['data']))
 with log.open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session_60s_active.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2))
 return obj
def key(cid,prop,rows):call('set_keyframes',{'clipId':cid,'property':prop,'keyframes':rows})
def add(entries):return call('add_clips',{'entries':entries})['clips']
assert call('get_timeline',{})['id']=='19F2B39F'
# Import newly generated materials; assets are referenced in place, never moved.
new=['john_f_kennedy','kanye_west','rm','frank_lampard','sharon_stone','lee_byung_hun']
paths={}
for n in new:
 paths['person_'+n]=src/'Images/paper_v1'/(n+'.png');paths['name_'+n]=src/'Graphics/names'/('john_f_kennedy_v2.png' if n=='john_f_kennedy' else n+'.png')
paths['person_marilyn']=src/'Images/paper_v1/marilyn_photo_ref.png'
paths['iq']=src/'Graphics/iq_letters_generated.png'
for n in ['4','8']:paths['digit_'+n]=src/'Graphics'/('digit_'+n+'_generated.png')
assert all(p.is_file() for p in paths.values()),[str(p) for p in paths.values() if not p.is_file()]
for k,p in paths.items():
 refs[k]=call('import_media',{'source':{'path':str(p)},'name':'minute_'+k})['mediaRef']
(out/'refs_60s.json').write_text(json.dumps(refs,indent=2)+'\n'); print('IMPORTED',len(paths),flush=True)
# Remove only clips of the current IQ Gallery timeline, never media or other projects.
t=call('get_timeline',{});assert t['id']=='19F2B39F' and t['totalFrames']==912
clips=[x['id'] for tr in t['tracks'] for x in tr.get('clips',[])];assert len(clips)==49,len(clips)
call('remove_clips',{'clipIds':clips}); print('REMOVED OLD CLIPS',len(clips),flush=True)
# Foundation, pre-existing music with exact fades, no synthetic audio generation.
base=add([{'mediaRef':refs['background'],'startFrame':0,'endFrame':1800},{'mediaRef':refs['music'],'startFrame':0,'endFrame':1620}]); bg=base[0]['id'];music1=base[1]['id']
key(bg,'position',[[0,-.01,0,'smooth'],[1799,.01,0,'smooth']]);key(bg,'scale',[[0,1.02,1.0]])
call('set_clip_properties',{'clipIds':[music1],'volumeDb':15,'fadeInFrames':15,'fadeOutFrames':120,'fadeInInterpolation':'linear','fadeOutInterpolation':'linear'})
music2=add([{'mediaRef':refs['music'],'startFrame':1500,'endFrame':1800}])[0]['id'];call('set_clip_properties',{'clipIds':[music2],'volumeDb':15,'fadeInFrames':120,'fadeOutFrames':30,'fadeInInterpolation':'linear','fadeOutInterpolation':'linear'})
people=['john_f_kennedy','kasparov','feynman','kanye_west','logan_paul','rm','nolan_gould','frank_lampard','kate_beckinsale','sharon_stone','lee_byung_hun','tarantino','marilyn']; scores=['119','123','125','133','139','148','150','150','152','154','155','160','228']
starts=[];z=0
for i in range(13):starts.append(z);z+=139 if i<6 else 138
assert z==1800
spans=[(starts[i]-(21 if i else 0),starts[i+1] if i<12 else 1800) for i in range(13)]; ids={'music':[music1,music2],'background':bg}
def motion(cid,i,x,y):
 s,e=spans[i];d=e-s;rows=([[0,x,y,'smooth']] if i==0 else [[0,x+1,y,'smooth'],[20,x,y,'smooth']]);rows.append([d-21,x,y,'smooth']);rows.append([d-1,x-1 if i<12 else x,y,'smooth']);key(cid,'position',rows)
for parity in (0,1):
 indexes=[i for i in range(13) if i%2==parity];entries=[{'mediaRef':refs['person_'+people[i]],'startFrame':spans[i][0],'endFrame':spans[i][1]} for i in indexes]
 for i,clip in zip(indexes,add(entries)):
  cid=clip['id'];ids['person_'+str(i)]=cid;key(cid,'scale',[[0,.74,.625]]);motion(cid,i,.13,.15)
print('PEOPLE DONE',flush=True)
# Glyphs are positioned using visible alpha, not image-box spacing.
def alpha_info(path):
 im=Image.open(path).convert('RGBA'); a=im.getchannel('A').point(lambda v:255 if v>=64 else 0);box=a.getbbox();return im.width,im.height,box
info={'IQ':alpha_info(paths['iq'])}
for n in '0123456789':
 p=src/'Graphics'/('digit_'+n+('_reference.png' if n in '01' else '_generated.png'));info[n]=alpha_info(p)
raw_w={'IQ':.31, **{str(n):.21 for n in range(10)}};raw_h={'IQ':.13, **{str(n):.105 for n in range(10)}}
def glyph_xs(score):
 seq=['IQ']+list(score); visible=[raw_w[g]*(info[g][2][2]-info[g][2][0])/info[g][0] for g in seq]; spaces=[24/1080,8/1080,8/1080]; start=(1-sum(visible)-sum(spaces))/2;outx=[]
 for j,g in enumerate(seq):
  outx.append(start-raw_w[g]*info[g][2][0]/info[g][0]);start+=visible[j]+(spaces[j] if j<len(spaces) else 0)
 return outx
for j in range(4):
 for parity in (0,1):
  indexes=[i for i in range(13) if i%2==parity];entries=[{'mediaRef':refs['iq'] if j==0 else refs['digit_'+scores[i][j-1]],'startFrame':spans[i][0],'endFrame':spans[i][1]} for i in indexes]
  for i,clip in zip(indexes,add(entries)):
   cid=clip['id'];ids[f'glyph_{i}_{j}']=cid;glyph='IQ' if j==0 else scores[i][j-1];x=glyph_xs(scores[i])[j];s,e=spans[i];d=e-s; offset=21 if i else 0
   key(cid,'scale',[[0,raw_w[glyph],raw_h[glyph]]]);rows=([[0,x,.72,'hold']] if i==0 else [[0,x+1,.72,'smooth'],[20,x,.72,'smooth']]);rows += [[offset+15,x,.72,'smooth'],[offset+43,x,.50,'smooth'],[d-21,x,.50,'smooth'],[d-1,x-1 if i<12 else x,.50,'smooth']];key(cid,'position',rows)
print('GLYPHS DONE',flush=True)
fg=add([{'mediaRef':refs['foreground'],'startFrame':0,'endFrame':1800}])[0]['id'];ids['foreground']=fg;key(fg,'scale',[[0,1.12,.355]]);key(fg,'position',[[0,-.06,.50,'smooth'],[1799,-.08,.50,'smooth']])
for parity in (0,1):
 indexes=[i for i in range(13) if i%2==parity];entries=[{'mediaRef':refs['name_'+people[i]],'startFrame':spans[i][0],'endFrame':spans[i][1]} for i in indexes]
 for i,clip in zip(indexes,add(entries)):
  cid=clip['id'];ids['name_'+str(i)]=cid;key(cid,'scale',[[0,.70,.134]]);motion(cid,i,.15,.645)
g=add([{'mediaRef':refs['grain'],'startFrame':s,'endFrame':min(s+240,1800),'includeAudio':False} for s in range(0,1800,240)]);ids['grain']=[a['id'] for a in g];call('set_clip_properties',{'clipIds':ids['grain'],'opacity':.4})
t=call('get_timeline',{});(out/'built_60s_state.json').write_text(json.dumps(t,ensure_ascii=False,indent=2));(out/'built_60s_ids.json').write_text(json.dumps(ids,indent=2));print('BUILT',t['totalFrames'],len(t['tracks']),sum(len(a['clips']) for a in t['tracks']),flush=True)
for i in range(13):call('inspect_timeline',{'startFrame':starts[i]+75})
for f in [0,118,138,139,140,276,277,278,1799]:call('inspect_timeline',{'startFrame':f})
print('DONE',flush=True)
