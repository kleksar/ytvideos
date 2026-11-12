"""Render the five-shot 31 s reconstruction preview from its local source package."""
import json
import math
import random
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

EP = Path(__file__).resolve().parents[1]
W, H, FPS = 720, 1280, 24
INK = '#102032'
CREAM = '#fff6df'
DARK = '#11233b'
SCENES = [
    (0, 108, '2007', 'Dramatic Chipmunk', 'PHOTO RE-CREATION', '#3465d8', '#dceaff', '#c1ddff'),
    (108, 252, '2016', 'Bottle Flip', 'STOCK RE-CREATION', '#dc5045', '#ffeed9', '#ffc5a8'),
    (252, 420, '2018', 'Gru’s Plan', 'ILLUSTRATED RE-CREATION', '#8037a9', '#fff0f9', '#ecc5ff'),
    (420, 564, '2019', 'Baby Yoda Sips Soup', 'ILLUSTRATED RE-CREATION', '#216052', '#e9fff2', '#aaf0cc'),
    (564, 744, '2022', 'Corn Kid', 'ILLUSTRATED RE-CREATION', '#a34316', '#fff5cb', '#ffe174'),
]
CARD = (42, 256, 644, 965)
FONT_DIR = Path('/System/Library/Fonts/Supplemental')
HEAD = 'Arial Black.ttf'
BOLD = 'Arial Bold.ttf'
CONDENSED = 'DIN Alternate Bold.ttf'
CUES = json.loads((EP / 'Edit/cues-v02.json').read_text())
RGB = (W, H)


@lru_cache
def font(size, family=BOLD):
    return ImageFont.truetype(str(FONT_DIR / family), size)


def text(d, xy, value, size, fill=INK, anchor='la', family=BOLD):
    d.text(xy, value, font=font(size, family), fill=fill, anchor=anchor)


def fit(d, xy, value, size, limit, fill=INK, family=HEAD, anchor='la'):
    while d.textlength(value, font=font(size, family)) > limit:
        size -= 1
    text(d, xy, value, size, fill, anchor, family)


def rr(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius, fill, outline, width)


def ellipse(d, box, fill, outline=None, width=1):
    d.ellipse(box, fill, outline, width)


def clamp(x):
    return max(0, min(1, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def star(d, x, y, size, color, points=4, angle=0):
    coords = []
    for i in range(points * 2):
        a = angle + math.pi * i / points
        r = size if i % 2 == 0 else size * .32
        coords.append((x + r * math.cos(a), y + r * math.sin(a)))
    d.polygon(coords, fill=color)


@lru_cache
def bg(index):
    _, _, year, name, mode, accent, light, mid = SCENES[index]
    im = Image.new('RGB', RGB, light)
    d = ImageDraw.Draw(im)
    for x in range(36, W, 22):
        for y in range(24, H, 22):
            d.point((x, y), fill=mid)
    d.rectangle((0, 0, W, 9), fill=accent)
    text(d, (43, 47), 'SCENES ON REPEAT', 20, INK, family=CONDENSED)
    text(d, (641, 48), 'MEME TIME MACHINE', 18, accent, 'ra', CONDENSED)
    for i in range(5):
        rr(d, (43 + i*121, 83, 150 + i*121, 90), 3, accent if i <= index else mid)
    rr(d, (43, 109, 115, 148), 8, INK)
    text(d, (79, 129), f'{index + 1:02}/05', 17, CREAM, 'mm', CONDENSED)
    rr(d, (125, 109, 204, 148), 8, accent)
    text(d, (164, 129), year, 23, 'white', 'mm', CONDENSED)
    fit(d, (42, 201), name, 65, 605, INK, HEAD, 'ls')
    text(d, (43, 222), mode, 17, accent, family=CONDENSED)
    rr(d, (49, 269, 651, 979), 35, mid)
    rr(d, CARD, 34, DARK)
    return im


def cookie(d, x, y, r, dark=False):
    fill = '#dfa458' if not dark else '#c68544'
    ellipse(d, (x-r, y-r+8, x+r, y+r+12), '#9f5a2b')
    ellipse(d, (x-r, y-r, x+r, y+r), fill, '#9f5a2b', 3)
    for dx, dy, size in [(-.43,-.24,.13), (.35,-.35,.10), (.34,.25,.16),(-.25,.36,.11),(.02,-.02,.10)]:
        xx, yy, rr_ = x + dx*r, y + dy*r, size*r
        ellipse(d, (xx-rr_, yy-rr_, xx+rr_, yy+rr_), '#64371f')


def clip_box(base, content, box=CARD, radius=33):
    x0, y0, x1, y1 = box
    mask = Image.new('L', (x1-x0, y1-y0))
    rr(ImageDraw.Draw(mask), (0, 0, mask.width-1, mask.height-1), radius, 255)
    base.paste(content, (x0, y0), mask)


PRAIRIE = Image.open(EP / 'Source/usgs-prairie-dog.jpg').convert('RGB')
PRAIRIE.thumbnail((1400, 1600))


def chipmunk(im, t):
    d = ImageDraw.Draw(im)
    if t < .82:
        rr(d, CARD, 34, '#1746a0')
        for i in range(13):
            d.arc((59+i*12, 300+i*14, 624-i*12, 911-i*15), 28, 348, '#3168cc', 2)
        ellipse(d, (101, 365, 598, 872), '#12367d')
        ellipse(d, (103, 345, 590, 833), '#e8f1ff')
        ellipse(d, (135, 379, 558, 801), '#fafdff', '#c0d3ff', 4)
        for x, y, s in [(342,556,11),(397,526,8),(279,608,6),(368,640,5),(415,625,4)]:
            d.polygon([(x-s,y),(x+s,y-s*.5),(x+s*.5,y+s),(x-s*.3,y+s*.8)], fill='#9b5c37')
        star(d, 504, 427, 46, '#ffd064', 4, .2)
        text(d, (346, 751), 'LAST COOKIE?', 34, '#244e98', 'mm', CONDENSED)
        return
    zoom = ease((t-.82)/.29)
    w, h = PRAIRIE.size
    cx = .46*w
    cy = (.52 - .138*zoom)*h
    cw = w*(.93 - .48*zoom)
    ch = cw*(CARD[3]-CARD[1])/(CARD[2]-CARD[0])
    region = (int(cx-cw/2), int(cy-ch/2), int(cx+cw/2), int(cy+ch/2))
    shot = PRAIRIE.crop(region).resize((602,709), Image.Resampling.BICUBIC)
    clip_box(im, shot)
    d = ImageDraw.Draw(im)
    if t < 1.27:
        for x, y, s in [(106,365,35),(574,425,28),(108,770,22)]:
            star(d, x, y, s, '#ffe066', 4)
    if t >= 1.38:
        rr(d, (69, 877, 618, 943), 15, '#102f69')
        text(d, (342, 910), 'THAT LOOK.', 37, 'white', 'mm', HEAD)


def bottle(im, source, t):
    d = ImageDraw.Draw(im)
    rr(d, CARD, 34, '#742d32')
    for x in range(71, 640, 19):
        d.line((x, 283, x, 935), fill='#963f42', width=1)
    image = Image.fromarray(source)
    x0, y0 = 158, 275
    video_box = (x0, y0, x0 + image.width, y0 + image.height)
    rr(d, (x0-6,y0-6,video_box[2]+6,video_box[3]+6), 25, '#101e34')
    clip_box(im, image, video_box, 19)
    d = ImageDraw.Draw(im)
    if t < 1.25:
        for k in range(4):
            star(d, 94, 452+82*k, 12, '#ffce9c', 4, .24)
    else:
        local = (t-1.25)
        if local < .50:
            for a in range(8):
                angle = a*math.tau/8
                radius = 70+local*110
                star(d, 312+radius*math.cos(angle), 834+radius*math.sin(angle), 17, '#ffe275', 4, angle)
        rr(d, (59, 876, 258, 933), 13, '#ffe16c')
        text(d, (157, 904), 'LANDED!', 28, INK, 'mm', HEAD)


def charts(im, t):
    d = ImageDraw.Draw(im)
    rr(d, CARD, 34, '#442368')
    for x in range(66, 640, 26):
        for y in range(286, 942, 26):
            ellipse(d, (x, y, x+2, y+2), '#79499b')
    phase = 0 if t < 2.65 else 1 if t < 4.15 else 2
    entry = [0, 2.65, 4.15][phase]
    bounce = 18*(1-ease((t-entry)/.28))
    x, y = 90, 362+bounce
    rr(d, (x+8, y+12, 609, y+510), 22, '#2e174a')
    rr(d, (x, y, 597, y+498), 20, '#fff8e8')
    d.rectangle((x+1, y+50, 596, y+54), '#d8c4a6')
    for dx in [35,75,114,153,192,231,270,309,348,387,426,465]:
        rr(d,(x+dx,y-15,x+dx+8,y+24),4,'#e0d5f2', '#231534',2)
    labels = ['THE PLAN', 'HIDE THE COOKIE', 'EAT THE EVIDENCE']
    fit(d, (344, y+108), labels[phase], 36, 452, '#4f286e', HEAD, 'mm')
    if phase == 0:
        ellipse(d,(190,y+164,472,y+446),'#ede2f5')
        ellipse(d,(232,y+206,430,y+404),'#e3b85f','#614276',5)
        for bx, by, br in [(265,259,13),(372,253,23),(334,347,23),(379,329,10)]:
            ellipse(d,(bx-br,y+by-br,bx+br,y+by+br),'#bf8944')
        d.polygon([(278,y+403),(242,y+447),(255,y+396),(230,y+388),(288,y+347),(298,y+384)],fill='#ed7957')
        star(d,484,y+166,24,'#9853bf')
    elif phase == 1:
        d.polygon([(198,y+310),(348,y+226),(495,y+310),(343,y+380)],fill='#e5a272')
        d.polygon([(198,y+310),(343,y+380),(343,y+448),(198,y+376)],fill='#be7758')
        d.polygon([(343,y+380),(495,y+310),(495,y+380),(343,y+448)],fill='#cb875b')
        cookie(d,349,y+274,55)
        d.line((343,y+398,343,y+424),fill='#ffe0a5',width=5)
    else:
        cookie(d,344,y+316,124)
        for bx, by, br in [(431,252,39),(456,288,37),(462,328,34)]:
            ellipse(d,(bx-br,y+by-br,bx+br,y+by+br),'#fff8e8')
        for bx, by in [(469,261),(498,276),(461,325),(506,319)]:
            ellipse(d,(bx-5,y+by-5,bx+5,y+by+5),'#b97543')
        star(d, 195, y+205, 34, '#ffbf42', 4)
        rr(d,(440,y+405,565,y+472),16,'#6e3a92')
        text(d,(502,y+440),'WAIT…',24,'white','mm',HEAD)
    text(d,(344,915),'MOVIE MEME  /  DESPICABLE ME',17,'#ead3ff','mm',CONDENSED)


def soup(im, t):
    d = ImageDraw.Draw(im)
    rr(d, CARD, 34, '#133e43')
    for i in range(7):
        x = 102 + 81*i
        d.line((x,334,x,782), fill='#1b5552', width=3)
        star(d,x,345+(i%3)*75,8+(i%3)*5,'#67a999',4,.2)
    ellipse(d,(142,382,541,781),'#256961')
    ellipse(d,(174,417,508,746),'#367e6c')
    d.ellipse((131,869,554,934), fill='#0c2930')
    rr(d,(175,703,516,934),110,'#347f8b', '#102d3e',5)
    rr(d,(259,742,435,900),50,'#8ecdbd', '#2d6673',4)
    rr(d,(161,578,209,704),22,'#bd8951','#173b48',5)
    rr(d,(478,578,529,704),22,'#bd8951','#173b48',5)
    d.line((345,506,337,455),fill='#082b3a',width=12)
    ellipse(d,(317,432,359,474),'#ffbd61','#173a46',4)
    rr(d,(187,501,502,748),107,'#66b7b5','#153842',6)
    rr(d,(209,535,480,708),71,'#b8e8d6','#267977',4)
    blink = abs(t-4.65)<.08
    for ex in [278,412]:
        if blink:
            d.line((ex-17,613,ex+17,613), fill='#153e46', width=6)
        else:
            ellipse(d,(ex-22,586,ex+22,640),'#153e46')
            ellipse(d,(ex-10,592,ex+2,604),'white')
    d.arc((323,636,365,659),0,180,fill='#205652',width=4)
    u = ease((t-1.85)/.72) - .55*ease((t-3.65)/.75)
    cy = 764-91*u
    rr(d,(383,cy+5,432,cy+81),18,'#f7b25b','#81523c',6)
    rr(d,(293,cy,406,cy+105),22,'#f7b25b','#81523c',6)
    ellipse(d,(294,cy-7,405,cy+24),'#a76546','#81523c',4)
    ellipse(d,(303,cy-2,397,cy+17),'#ad644a')
    for sx in (318,347,372):
        dx=math.sin(t*4+sx)*5
        d.arc((sx-9+dx,cy-53,sx+11+dx,cy-16),-45,135,'#e7f4cc',2)
    text(d,(344,924),'TV MEME  /  THE MANDALORIAN',17,'#baf7df','mm',CONDENSED)


@lru_cache
def confetti():
    rng=random.Random(184)
    return [(rng.randrange(62,622),rng.randrange(260,933),rng.choice(['#f4ab38','#f0825a','#80a448','#fff0a3'])) for _ in range(36)]


def corn(im, t):
    d = ImageDraw.Draw(im)
    rr(d, CARD, 34, '#793c2d')
    for x in range(70, 640, 25):
        for y in range(290, 937, 25):
            ellipse(d,(x,y,x+2,y+2),'#bf7555')
    ellipse(d,(109,354,584,878),'#a94e2b')
    ellipse(d,(151,394,542,834),'#ba622b')
    y = 526 + math.sin(t*3.9)*5
    if t < 5.3:
        d.polygon([(258,y+293),(180,y+169),(169,y+90),(265,y+154),(330,y+288)],fill='#486b40')
        d.polygon([(341,y+294),(424,y+160),(497,y+80),(478,y+211),(397,y+303)],fill='#6d924b')
        rr(d,(235,y-41,444,y+285),91,'#f3b03c','#663a29',5)
        for row in range(8):
            for col in range(5):
                rx=262+col*35
                ry=y+row*34
                if row in (0,7) and col in (0,4):
                    continue
                rr(d,(rx-12,ry-12,rx+13,ry+13),8,('#ffdf6c' if (row+col)%2 else '#ffca52'))
        for ex in (297,379):
            ellipse(d,(ex-11,y+71,ex+11,y+100),'#3d2c24')
            ellipse(d,(ex-5,y+73,ex+1,y+80),'white')
        ellipse(d,(317,y+104,358,y+138),'#743928')
        d.arc((324,y+104,351,y+126),0,180, fill='white', width=5)
        d.polygon([(560,836),(484,754),(495,733),(596,810)],fill='#273849')
        rr(d,(445,716,511,769),25,'#546375','#273849',4)
        if t > 3.1:
            for x, dy, s in [(192,50,25),(481,-34,23),(530,111,21)]:
                star(d,x,y+dy,s,'#ffec94',4,t*.6)
        text(d,(344,918),'FROM AN INTERVIEW TO A SONG',17,'#fff0b1','mm',CONDENSED)
    else:
        for i,(x,cy,c) in enumerate(confetti()):
            yy=287+(cy+int((t-5.3)*(45+i%7*8)))%610
            d.line((x,yy,x+7,yy+10),fill=c,width=4)
        rr(d,(220,477,477,687),49,'#f3b742','#4a2e25',6)
        for x0,x1 in [(164,268),(422,534)]:
            d.arc((x0,495,x1,651),15,343,fill='#ffde67',width=14)
        d.polygon([(317,666),(384,666),(386,759),(313,759)],fill='#e3a03b')
        rr(d,(247,745,455,803),16,'#ffc950','#73412b',5)
        star(d,349,568,64,'#fff5ae',5,-math.pi/2)
        text(d,(346,864),'CORN WINS',51,'#fff3b9','mm',HEAD)


def captions(im, frame):
    cue = next((c for c in CUES if c['start_frame'] <= frame < c['end_frame']), None)
    if not cue:
        return
    d = ImageDraw.Draw(im)
    for row, line in enumerate(cue['lines']):
        y = 1013 + row*50
        w = d.textlength(line, font=font(37, BOLD))
        rr(d,(343-w/2-19,y-23,343+w/2+19,y+24),12,INK)
        text(d,(343,y),line,37,CREAM,'mm')


def main():
    out = Path(sys.argv[1])
    width, height = 364, 688
    source = EP / 'Source/pexels-ron-lach-8360257-excerpt.mp4'
    payload = subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-vf',
        f'scale={width}:{height}','-frames:v','144','-pix_fmt','rgb24','-f','rawvideo','-'])
    stock = np.frombuffer(payload,dtype=np.uint8).reshape((-1,height,width,3))
    if len(stock) != 144:
        raise ValueError(f'Stock cut must have 144 frames, got {len(stock)}.')
    args = ['ffmpeg','-nostdin','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24',
            '-s','720x1280','-r','24','-i','pipe:0','-i',str(EP/'Edit/mix-v02.wav'),
            '-map','0:v:0','-map','1:a:0','-vf',
            'scale=1080:1920:flags=lanczos:out_color_matrix=bt709,setsar=1,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709',
            '-c:v','libx264','-preset','fast','-crf','18','-profile:v','high',
            '-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries',
            'bt709','-color_trc','bt709','-c:a','aac','-b:a','256k','-ar','48000','-ac','2',
            '-movflags','+faststart+write_colr',str(out)]
    (EP/'Edit/render-command-v02.json').write_text(json.dumps(args,indent=2)+'\n')
    funcs = [chipmunk, bottle, charts, soup, corn]
    process = subprocess.Popen(args,stdin=subprocess.PIPE)
    with process.stdin as pipe:
        for i,(start,end,*_) in enumerate(SCENES):
            for frame in range(start,end):
                im = bg(i).copy()
                t = (frame-start)/FPS
                if i == 1:
                    bottle(im,stock[frame-start],t)
                else:
                    funcs[i](im,t)
                captions(im,frame)
                pipe.write(im.tobytes())
    if process.wait():
        raise RuntimeError('FFmpeg export failed.')


if __name__ == '__main__':
    main()
