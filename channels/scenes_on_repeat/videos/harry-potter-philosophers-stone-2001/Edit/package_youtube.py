import hashlib
import io
import json
import subprocess
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
from render_package import EPISODE, ROOT, clip

channel='UCqct_dth0WSCwiDZx1WMfgg'
playlist='PLfB5SSM7Xx98'
pack=EPISODE/'Packaging'
record=dict(channel='scenes_on_repeat',channel_id=channel,revision='hp-package-v01',
            requested_visibility='private',clips=[])
data=[
    ('trailer-v03', "They Told Him Magic Wasn't Real #Fantasy",
     "A boy told that magic does not exist finds a place at Hogwarts, then learns that this new world has dangers of its own. A mini-trailer edited from Harry Potter and the Philosopher's Stone (2001).",
     'Constance', '#HarryPotter #Hogwarts #FantasyMovies #MovieTrailers',
     ['Harry Potter and the Philosopher’s Stone 2001','Harry Potter and the Sorcerer’s Stone','Hogwarts arrival','Diagon Alley','fantasy movie trailer'],
     3.38,'MAGIC IS REAL','trailer'),
    ('leviosa-v02','He Said the Spell Wrong #MovieScenes',
     "Ron tries to make a feather fly. Hermione corrects his pronunciation and shows what the spell can do. From Harry Potter and the Philosopher's Stone (2001).",
     'Sneaky Adventure','#HarryPotter #WingardiumLeviosa #HermioneGranger #MovieScenes',
     ['Harry Potter and the Philosopher’s Stone 2001','Wingardium Leviosa scene','Hermione feather scene','Ron Weasley','Leviosa not Leviosar'],
     24.88,'THE FEATHER FLIES','lead'),
    ('wand-v02','The Wand Makes Its Choice #Fantasy',
     "Harry's first try sends boxes flying at Ollivanders. Another wand gives him a very different answer. From Harry Potter and the Philosopher's Stone (2001).",
     'Constance','#HarryPotter #Ollivanders #WizardingWorld #MovieScenes',
     ['Harry Potter and the Philosopher’s Stone 2001','the wand chooses the wizard','Harry Potter first wand','Ollivanders wand shop','wand choosing scene'],
     21.6,'HARRY’S FIRST WAND','reserve'),
]
def save(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
for slug,title,story,music,hashtags,tags,time,words,role in data:
    mp4=EPISODE/'Deliverables'/slug/(slug+'.mp4')
    srt=mp4.with_suffix('.en.srt')
    cover=pack/(slug+'.cover.jpg')
    metadata=dict(title=title,description=f'{story}\n\nMusic: “{music}” by Kevin MacLeod (incompetech.com). Excerpt edited and mixed. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\n\n{hashtags}',
                  category_id='1',language='en-US',audio_language='en-US',made_for_kids=False,
                  contains_synthetic_media=False,tags=tags)
    save(pack/(slug+'.metadata.json'),metadata)
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(time),'-i',str(mp4),'-frames:v','1','-threads','1',
                                 '-c:v','mjpeg','-q:v','2','-f','image2pipe','-'])
    frame=Image.open(io.BytesIO(raw)).convert('RGB').crop((0,640,1080,1280))
    backdrop=ImageOps.fit(frame,(180,320)).filter(ImageFilter.GaussianBlur(20))
    image=ImageEnhance.Brightness(backdrop.resize((1080,1920))).enhance(.45)
    image.paste(frame,(0,640))
    draw=ImageDraw.Draw(image)
    font=clip.get_font(82,'bold')
    draw.rounded_rectangle((74,354,1006,528),radius=22,fill='#151616',outline='#F8B242',width=4)
    draw.text((540,440),words,font=font,anchor='mm',fill='#F9EED6',stroke_width=2,stroke_fill='#151616')
    image.save(cover,quality=94)
    duration=json.loads((EPISODE/'Work'/slug/'timeline.json').read_text())['frames']/24
    entry=dict(id=slug,mp4=str(mp4.relative_to(ROOT)),srt=str(srt.relative_to(ROOT)),
               mp4_sha256=hashlib.sha256(mp4.read_bytes()).hexdigest(),srt_sha256=hashlib.sha256(srt.read_bytes()).hexdigest(),
               qa=str((EPISODE/'Work'/slug/'qa-receipt.json').relative_to(ROOT)),duration_seconds=duration,
               metadata=metadata,thumbnail_candidate=str(cover.relative_to(ROOT)),release_role=role)
    if role=='trailer': entry['playlist_id']=playlist
    record['clips'].append(entry)
save(EPISODE/'RELEASE.json',record)
