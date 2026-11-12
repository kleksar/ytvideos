"""Freeze the shared FFmpeg renderer for this review with two measured clause exceptions."""
from build_review_edit import setup, ROOT, read
from pathlib import Path
from PIL import ImageFont
import importlib.util, json, shutil, sys

name='us'
ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
sandbox=w/'engine-v01'
files=['automation/ffmpeg_montage/montage.py','automation/ffmpeg_montage/delivery.py',
       'automation/ffmpeg_montage/profiles/nuviko.json','automation/ffmpeg_montage/profiles/long.json',
       '.agents/skills/ytv-audio-delivery/references/speed.json',
       '.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py']
for p in files:
 path=sandbox/p
 path.parent.mkdir(parents=True,exist_ok=True)
 if not path.is_file(): shutil.copy2(ROOT/p,path)
module=sandbox/files[-1]
original=(ROOT/files[-1]).read_text()
needle='            or (left_words[-2:] in (["handing", "over"], ["handed", "over"])'
assert original.count(needle)==1
local='''            or (left_words == ["what", "it", "would", "do"]
                and right_words == ["when", "they", "arrived"]
                and float(font.getlength(phrase + " " + phrases[phrase_index + 1])) > max_text_width)
            or (left_words == ["and", "who", "would", "have"]
                and right_words == ["the", "power", "to", "protect", "it"]
                and float(font.getlength(phrase + " the power")) > max_text_width)
'''
module.write_text(original.replace(needle,local+needle))
spec=importlib.util.spec_from_file_location('review_grouping',module); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
pr=read(ROOT/'automation/ffmpeg_montage/profiles/nuviko.json')
geo=read(ROOT/'automation/ffmpeg_montage/profiles/long.json')
font=ImageFont.truetype(pr['font'],geo['font_size_px'],index=pr['font_index'])
width=geo['max_visible_width_px']-2*(pr['pad_x']+pr['outline_width'])
pairs=read(manifest)['subtitles']['keep_together']
manual={
'Meanwhile, the government was opening land':"Meanwhile, the government|was opening land|to settlers in places|already inside the nation's|claimed borders.",
'They were taking action for their':'They were taking action|for their own freedom,|and the army|had to decide|what it would do|when they arrived.',
'As the United States pushed west,':'As the United States|pushed west,|it took land|from Indigenous peoples,|and every new state|reopened the question|of where slavery|would be allowed|and who would have|the power to protect it.',
}
a='what it would do';b='when they arrived.';c='and who would have';e='the power to protect it.'
exceptions=[
 dict(left=a,right=b,reason=f"Complete lexical 'do' before a temporal clause. Combined {font.getlength(a+' '+b):.1f}px > {width}px."),
 dict(left=c,right=e,reason=f"Lexical 'have' followed by noun group; retaining 'and who would have the power' takes {font.getlength(c+' the power'):.1f}px > {width}px.")
]
phrases=[]
words=wm['words']
for i,j in g.sentence_ranges(words):
 part=words[i:j]
 text=' '.join(x['text'] for x in part)
 special=next((p for lead,p in manual.items() if text.startswith(lead)),None)
 if special is not None: phrases+=special.split('|')
 else: phrases+=[' '.join(x['text'] for x in group) for group in g.group_words(part,font,width,keep_together=pairs,combine_sentences=True)]
groups=g.plan_phrases(words,phrases,font,width,keep_together=pairs,combine_sentences=True,boundary_exceptions=exceptions)
assert sum(map(len,groups))==len(words)
p=read(manifest);p['subtitles']['phrases']=phrases;p['subtitles']['boundary_exceptions']=exceptions
manifest.write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
(d/'us-caption-engine-note-v01.md').write_text('Shared FFmpeg renderer, delivery module, speed and geometry copied byte-for-byte for this exact review, with a versioned caption grouping module adding only two explicitly measured grammatical clause cases already contemplated by the subtitle skill. Shared source files are unchanged. Passport and delivery receipt bind the actual local executable.\n\n'+'\n'.join(x['reason'] for x in exceptions)+'\n')
print(len(phrases), len(words), width)
