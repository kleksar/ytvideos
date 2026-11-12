import sys,json,pathlib,base64
from PIL import Image
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';src=root/'channels/paper_detour/videos/003_iq_gallery/Source/Graphics';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session_60s_active.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];assert '/root/film_editor' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text(); ids=json.loads((out/'built_60s_ids.json').read_text())
def call(name,args):
 assert '/root/film_editor' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text()
 r=c.request('tools/call',{'name':name,'arguments':args});
 if r.get('isError'):raise RuntimeError(r)
 text=[v['text'] for v in r.get('content',[]) if v.get('type')=='text'];obj=json.loads(text[0]) if len(text)==1 else {'texts':text}
 if name=='inspect_timeline':
  for j,v in enumerate(r['content']):
   if v['type']=='image':(out/f'reveal_fix_f{args["startFrame"]}_{j}.png').write_bytes(base64.b64decode(v['data']))
 with (out/'receipt_60s.jsonl').open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session_60s_active.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2));return obj
state=call('get_timeline',{});assert state['id']=='19F2B39F' and state['totalFrames']==1800
clips={v['id']:v for tr in state['tracks'] for v in tr['clips']};scores=['119','123','125','133','139','148','150','150','152','154','155','160','228']
for i in range(13):
 for j in range(4):
  cid=ids[f'glyph_{i}_{j}'];glyph='IQ' if j==0 else scores[i][j-1];p=src/'iq_letters_generated.png' if glyph=='IQ' else src/('digit_'+glyph+('_reference.png' if glyph in '01' else '_generated.png'));im=Image.open(p).convert('RGBA');bbox=im.getchannel('A').point(lambda v:255 if v>=64 else 0).getbbox();h=.13 if glyph=='IQ' else .105
  hidden=round(.755-h*bbox[1]/im.height,6);rows=clips[cid]['keyframes']['position'];rows=[[r[0],r[1],hidden if abs(r[2]-.72)<.001 else r[2], 'smooth'] for r in rows];call('set_keyframes',{'clipId':cid,'property':'position','keyframes':rows});off=21 if i else 0;call('set_keyframes',{'clipId':cid,'property':'opacity','keyframes':[[0,0,'hold'],[off+15,0,'linear'],[off+22,1,'linear']]})
print('fixed all 52 glyphs',flush=True)
starts=[0,139,278,417,556,695,834,972,1110,1248,1386,1524,1662]
for n in starts:
 for f in [n,n+14,n+15,n+18,n+22,n+30,n+43]:call('inspect_timeline',{'startFrame':f})
print('inspected',flush=True)
