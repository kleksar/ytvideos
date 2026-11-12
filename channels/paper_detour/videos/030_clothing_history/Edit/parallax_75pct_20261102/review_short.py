import base64,importlib.util,io,json
from PIL import Image,ImageDraw
from pathlib import Path
R=Path(__file__).resolve().parent;P='B1BA2D18';T=(R/'short_timeline_id.txt').read_text().strip(); s=importlib.util.spec_from_file_location('p','/Users/diplomat/ytvideos/automation/palmier/inspect_connection.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);c=m.PalmierConnection();c.connect();t=c.read_tool('get_timeline',{'projectId':P,'timelineId':T}); clips=next(x for x in t['tracks'] if x['name']=='Scenes')['clips']
for first in range(0,len(clips),5):
 subset=clips[first:first+5]; canvas=Image.new('RGB',(1536,308*len(subset)),'black');draw=ImageDraw.Draw(canvas)
 for row,clip in enumerate(subset):
  begin,end=clip['frames'];res=c.request('tools/call',{'name':'inspect_timeline','arguments':{'projectId':P,'timelineId':T,'startFrame':begin,'endFrame':end,'maxFrames':3}})
  ims=[v for v in res.get('content',[]) if v.get('type')=='image'];assert len(ims)==3
  draw.text((4,row*308+2),f'Scene {first+row+1:02} frames {begin}-{end}',fill='white')
  for j,im in enumerate(ims): canvas.paste(Image.open(io.BytesIO(base64.b64decode(im['data']))).convert('RGB'),(j*512,row*308+20))
 out=R/f'short_review_{first+1:02}_{first+len(subset):02}.jpg';canvas.save(out,quality=88);print(str(out),flush=True)
res=c.request('tools/call',{'name':'manage_project','arguments':{'action':'show','id':P}});print('SHOW',json.dumps(res,ensure_ascii=False),flush=True)
