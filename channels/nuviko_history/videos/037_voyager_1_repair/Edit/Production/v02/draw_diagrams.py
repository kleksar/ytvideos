"""Original editable explanatory graphics, not edits of generated scene images."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,math,html,base64,json,hashlib
EP=Path(__file__).resolve().parents[3]; OUT=EP/'Source/Images/v02'; OUT.mkdir(exist_ok=True)
W,H=2560,1440;FONT='/System/Library/Fonts/Supplemental/Georgia.ttf';BOLD='/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
CREAM='#f3e9d5';TEAL='#73cbd0';GOLD='#e6b567';MUTED='#8c9aab';DIM='#2c3d51';DAMAGE='#64565e';ORANGE='#d58a79'
MASTER=EP/'Source/Images/v01/voyager_master.png'
class Art:
 def __init__(self,title,kicker='VOYAGER 1'):
  yy,xx=np.mgrid[0:H,0:W];glow=np.exp(-(((xx-W*.55)/(W*.70))**2+((yy-H*.38)/(H*.65))**2)*2)
  a=np.zeros((H,W,3),dtype=np.uint8)
  for i,(lo,hi) in enumerate([(6,14),(14,35),(25,55)]):a[:,:,i]=lo+(hi-lo)*glow
  self.im=Image.fromarray(a,'RGB');self.d=ImageDraw.Draw(self.im)
  self.svg=['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="2560" height="1440" viewBox="0 0 2560 1440">','<defs><radialGradient id="bg" cx="55%" cy="38%" r="80%"><stop stop-color="#0e2337"/><stop offset="1" stop-color="#060e19"/></radialGradient></defs>','<rect width="2560" height="1440" fill="url(#bg)"/>']
  for y in range(240,1150,80):self.line([(200,y),(2360,y)],'#15263a',1)
  self.text((200,110),kicker,30,GOLD);self.text((2360,110),'Conceptual diagram',28,MUTED,'ra');self.text((200,210),title,66,CREAM)
 def text(self,pos,s,size=44,color=CREAM,anchor='la',bold=False):
  font=ImageFont.truetype(BOLD if bold else FONT,size);self.d.text(pos,s,font=font,fill=color,anchor=anchor)
  align={'la':'start','ma':'middle','ra':'end'}[anchor];x,y=pos;ascent=font.getmetrics()[0]
  self.svg.append(f'<text x="{x}" y="{y+ascent}" font-family="Georgia" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{align}" fill="{color}">{html.escape(s)}</text>')
 def rect(self,box,fill='#14293f',outline=TEAL,width=3,r=16):
  self.d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width);x,y,x2,y2=box
  self.svg.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" rx="{r}" fill="{fill}" stroke="{outline}" stroke-width="{width}"/>')
 def line(self,pts,color=TEAL,width=5,dashed=False):
  if dashed:
   for a,b in zip(pts,pts[1:]):
    length=math.dist(a,b);steps=max(1,int(length/22))
    for j in range(0,steps,2):
     t=j/steps;u=min((j+1)/steps,1);self.d.line([(a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])),(a[0]+u*(b[0]-a[0]),a[1]+u*(b[1]-a[1]))],fill=color,width=width)
  else:self.d.line(pts,fill=color,width=width,joint='curve')
  self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="22 22"' if dashed else '')+'/>')
 def arrow(self,pts,color=TEAL,width=6,dashed=False):
  self.line(pts,color,width,dashed);a,b=pts[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);l=27
  tri=[b,(b[0]-l*math.cos(ang-.5),b[1]-l*math.sin(ang-.5)),(b[0]-l*math.cos(ang+.5),b[1]-l*math.sin(ang+.5))];self.d.polygon(tri,fill=color);self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in tri)+f'" fill="{color}"/>')
 def circle(self,c,r,fill,outline=TEAL,width=4):
  x,y=c;self.d.ellipse((x-r,y-r,x+r,y+r),fill=fill,outline=outline,width=width);self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{outline}" stroke-width="{width}"/>')
 def ship(self,x=2130,y=650,w=500):
  im=Image.open(MASTER).convert('RGBA');h=round(im.height*w/im.width);im=im.resize((w,h),Image.Resampling.LANCZOS);box=(round(x-w/2),round(y-h/2));self.im.paste(im,box,im);encoded=base64.b64encode(MASTER.read_bytes()).decode();self.svg.append(f'<image x="{box[0]}" y="{box[1]}" width="{w}" height="{h}" xlink:href="data:image/png;base64,{encoded}"/>')
 def earth(self,x=420,y=650,r=100):
  self.circle((x,y),r,'#173d63','#85b9ce',4)
  points=[(x-r*.6,y-r*.2),(x-r*.15,y-r*.65),(x+r*.2,y-r*.5),(x+r*.1,y-r*.12),(x+r*.5,y+r*.05),(x+r*.2,y+r*.5),(x-r*.1,y+r*.25),(x-r*.2,y-r*.05)]
  self.d.polygon(points,fill='#5f948b');self.svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in points)+'" fill="#5f948b"/>')
 def save(self,sid):
  p=OUT/f'{sid}_diagram_v01.png';v=p.with_suffix('.svg');self.im.save(p);v.write_text('\n'.join(self.svg+['</svg>']));return {'id':sid,'image':str(p),'svg':str(v),'native_size':[W,H],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'original deterministic editable vector diagram; Pillow rasterization of same authored shapes; master spacecraft embedded as supporting production asset','depiction':'conceptual explanation, not actual memory/code/telemetry or hardware layout'}

def endpoints(a):
 a.earth();a.ship();a.text((420,850),'EARTH',39,CREAM,'ma');a.text((2130,850),'VOYAGER 1',39,CREAM,'ma')
def payload(a,x,y,ordered=True,color=TEAL,scale=1):
 for j in range(5):
  px=x+(j%3)*95*scale;py=y+(j//3)*62*scale
  if not ordered:py+=(j%3-1)*30*scale;px+=(j%2)*13*scale
  a.rect((px,py,px+66*scale,py+26*scale),color,color,1,5)
def memory(a,x=390,y=390,cell=70,gap=12,damaged=True):
 for i in range(100):
  row,col=divmod(i,20);bad=damaged and i in (34,35,36);xx=x+col*(cell+gap);yy=y+row*(cell+gap)
  a.rect((xx,yy,xx+cell,yy+cell),DAMAGE if bad else '#183b4b',ORANGE if bad else '#376979',2,8)
 if damaged:
  a.text((x,y+5*(cell+gap)+55),'Damaged region',37,ORANGE)
 return (x+14*(cell+gap)+cell*1.5,y+cell*1.5)
def program(a,mode):
 # Fixed conceptual damage marker persists in the same position across the workaround sequence.
 for j in range(3):a.rect((2055+j*67,380,2105+j*67,430),DAMAGE,ORANGE,2,6)
 a.text((2040,455),'Unavailable',30,ORANGE)
 slots=[(320,730,790,870),(1040,730,1420,870),(1670,730,2180,870)]
 for box in slots:a.rect(box,'#0f2435',MUTED,2)
 if mode=='proposed':
  a.rect((380,470,1830,565),'#244f5a',TEAL,3);a.text((1105,485),'Instructions to move',43,CREAM,'ma')
  a.arrow([(1105,600),(1105,680)],TEAL,4,True)
 else:
  cols=[TEAL,'#9dced3',GOLD]
  for i,(x,y,x2,y2) in enumerate(slots):
   a.rect((x+30,y+22,x2-30,y2-22),'#24434e',cols[i],4);a.text(((x+x2)/2,y+38),f'Part {i+1}',43,cols[i],'ma')
  if mode=='old':
   a.line([(550,725),(550,585),(1910,585)],MUTED,4,True);a.line([(1240,725),(1240,620),(1910,620)],MUTED,4,True)
   a.text((380,490),'References must follow the moved instructions',41,CREAM)
  elif mode!='split':
   a.arrow([(790,800),(1040,800)],TEAL);a.arrow([(1420,800),(1670,800)],TEAL)
   a.line([(550,730),(550,590),(1900,590),(1900,730)],TEAL,5)
   a.text((380,490),'One program · separate locations',43,CREAM)
 a.text((1280,990),'Illustrative memory spaces, not actual addresses',31,MUTED,'ma')

ids=[7,8,11,12,15,16,19,20,21,23,24,25,26,27,29,30,31,32,34,36,38,39,41,42,43];records=[]
for n in ids:
 sid=f'S{n:02d}'
 titles={7:'The command still gets through',8:'The signal arrives. The data is unreadable.',11:'Beyond the heliosphere',12:'The Sun shapes a vast region',15:'A command takes about 22½ hours',16:'The reply takes just as long',19:'One onboard computer',20:'Preparing data for transmission',21:'A diagnostic command',23:'The contents of memory',24:'Earlier records reveal a difference',25:'About 3% of memory was damaged',26:'The damaged region cannot be repaired',27:'Move the instructions into intact memory',29:'Split the program into smaller pieces',30:'Update the references',31:'Make the pieces work together',32:'Spacecraft status comes first',34:'Restore a view of the spacecraft’s condition',36:'Almost a day there. Almost a day back.',38:'Readable information after five months',39:'Spacecraft status reaches Earth',41:'Data from four operating instruments',42:'The damage is still there',43:'The program takes another route'}
 a=Art(titles[n])
 if n in (7,15,16,21,34,36,39,41):
  endpoints(a)
  if n==7:
   a.arrow([(620,650),(1820,650)]);a.text((1280,450),'COMMANDS',56,TEAL,'ma');a.text((1280,960),'Radio contact remains possible',39,MUTED,'ma')
  elif n in (15,16):
   if n==15:a.arrow([(620,650),(1820,650)],GOLD)
   else:a.arrow([(1840,650),(640,650)],TEAL)
   a.text((1280,410),'22½ hours',112,GOLD if n==15 else TEAL,'ma',True);a.text((1280,1000),'ONE WAY',35,MUTED,'ma')
  elif n==21:
   a.arrow([(620,650),(1820,650)],GOLD);a.rect((1010,560,1510,730),'#29303d',GOLD);a.text((1260,595),'DIAGNOSTIC',45,GOLD,'ma');a.text((1280,980),'MARCH 2024',42,CREAM,'ma')
  elif n==34:
   a.arrow([(1830,650),(640,650)],GOLD,5,True);a.text((1280,450),'Spacecraft status',62,GOLD,'ma');a.text((1280,1000),'THE TARGET · NOT YET THE RESULT',33,MUTED,'ma')
  elif n==36:
   a.arrow([(620,570),(1830,570)],GOLD);a.arrow([(1830,760),(640,760)],TEAL);a.text((1280,425),'OUTBOUND FIX',44,GOLD,'ma');a.text((1280,900),'RETURNING REPLY',44,TEAL,'ma');a.text((1280,1030),'Almost two days for one exchange',44,CREAM,'ma')
  elif n==39:
   a.arrow([(1840,650),(640,650)]);payload(a,1135,560,True);a.text((1280,430),'SPACECRAFT STATUS',55,TEAL,'ma');a.text((1280,1000),'20 APRIL 2024',44,CREAM,'ma')
  elif n==41:
   a.arrow([(1750,650),(640,650)]);a.text((1280,400),'JUNE 2024',70,GOLD,'ma')
   for j in range(4):
    a.circle((1520,510+j*100),25,'#337680',TEAL,3);a.line([(1490,510+j*100),(1380,650)],TEAL,3)
   a.text((1280,1020),'Four sources · one returning stream',43,CREAM,'ma')
 elif n==8:
  a.earth(420,740,100);a.ship(2160,650,480)
  for y,label in ((500,'Scientific measurements'),(790,'Spacecraft status')):
   a.text((1280,y-155),label,48,CREAM,'ma');a.arrow([(1870,y),(620,y)],MUTED,4);payload(a,1000,y-20,False,ORANGE,1.1)
  a.text((1280,1040),'Radio link present · messages unreadable',37,MUTED,'ma')
 elif n in (11,12):
  a.circle((780,670),100,'#b9823d',GOLD,5)
  for r in (230,360,490):
   points=[(780+math.cos(t)*r*1.4,670+math.sin(t)*r*.65) for t in np.linspace(0,2*math.pi,180)];a.line(points,'#3d6878',2,True)
  a.text((780,845),'SUN',35,GOLD,'ma');a.ship(2150,560,470)
  if n==11:
   a.text((1940,930),'2012',90,GOLD,'ma');a.text((1100,1080),'A conceptual boundary, not a solid shell',34,MUTED,'ma')
  else:
   for ang in (-.45,-.15,.15,.45):a.arrow([(950,670),(1510,670+600*ang)],TEAL,4)
   a.text((1510,930),'Solar wind + magnetic field',43,CREAM,'ma')
 elif n==19:
  a.ship(680,700,760);a.rect((1430,440,2150,830),'#122d41',TEAL,4);a.text((1790,555),'ONBOARD',54,CREAM,'ma');a.text((1790,640),'COMPUTER',54,TEAL,'ma');a.line([(1080,650),(1390,650)],MUTED,4,True);a.text((1280,1060),'A functional concept, not a view inside the spacecraft',31,MUTED,'ma')
 elif n==20:
  for y,label,col in [(400,'Scientific data',TEAL),(750,'Engineering data',GOLD)]:
   a.rect((260,y,850,y+160),'#10283b',col,3);a.text((555,y+45),label,46,col,'ma');a.arrow([(860,y+80),(1090,660)],col,4)
  a.rect((1100,510,1670,830),'#193847',TEAL,4);a.text((1385,580),'PREPARE',54,CREAM,'ma');a.text((1385,660),'MESSAGES',54,TEAL,'ma');a.arrow([(1680,670),(2200,670)]);a.text((1920,870),'To Earth',43,CREAM,'ma')
 elif n==23:
  memory(a,390,390,70,12,False);a.text((1280,1020),'A diagnostic response exposes the stored information',38,CREAM,'ma')
 elif n==24:
  memory(a,260,480,35,7,False);memory(a,1450,480,35,7,True);a.text((650,350),'Earlier records',48,CREAM,'ma');a.text((1840,350),'March 2024',48,GOLD,'ma');a.text((1280,1030),'Same information structure · a revealing difference',38,MUTED,'ma')
 elif n in (25,26,42):
  memory(a,390,400,70,12,True)
  if n==25:a.text((1280,1000),'≈3%',128,GOLD,'ma',True)
  elif n==26:a.text((1280,1010),'PHYSICAL REPAIR IS NOT POSSIBLE',40,ORANGE,'ma')
  else:a.text((1280,1010),'Still damaged. Still avoided.',55,GOLD,'ma')
 elif n in (27,29,30,31,43):
  program(a,'proposed' if n==27 else 'split' if n==29 else 'old' if n==30 else 'working')
 elif n==32:
  a.rect((280,450,1220,840),'#183947',TEAL,5);a.rect((1370,450,2310,840),'#101d2c',DIM,3);a.text((750,560),'SPACECRAFT',58,CREAM,'ma');a.text((750,655),'STATUS',70,TEAL,'ma');a.text((1840,550),'SCIENTIFIC',56,MUTED,'ma');a.text((1840,650),'MEASUREMENTS',50,MUTED,'ma');a.text((750,980),'FIRST PRIORITY',40,GOLD,'ma');a.text((1840,980),'NEXT',40,MUTED,'ma')
 elif n==38:
  a.rect((260,420,1190,980),'#122337',MUTED,3);a.rect((1370,420,2300,980),'#143444',TEAL,4);payload(a,550,625,False,ORANGE,1.5);payload(a,1650,625,True,TEAL,1.5);a.text((725,470),'Unreadable',52,MUTED,'ma');a.text((1835,470),'Readable status',52,TEAL,'ma');a.arrow([(1220,710),(1340,710)],GOLD,5)
 records.append(a.save(sid))
(EP/'Edit/Production/v02/diagrams_manifest_v01.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print(len(records),'original vector diagrams at',W,H)
