"""Prepare reusable long-form word-highlight states from edit-conformed words.

The caller supplies validated words and hard segment boundaries. Groups use the
shared Paper/Nuviko semantic segmenter and drawing primitive; timing is at the
actual output frame rate, not the renderer's 30 fps production assumption.
"""
import importlib.util
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'automation/ffmpeg_montage'))
from montage import draw_caption_state

spec = importlib.util.spec_from_file_location('shared_semantic_grouping', ROOT/'.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py')
grouping = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grouping)

def prepare(segments, output, *, fps, width, height, font_path, font_index, font_size):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(font_path, font_size, index=font_index)
    style = {'background': None, 'text': '#F9EED6', 'highlight': '#FF302A', 'outline': '#18243A'}
    band = round(height * .19); baseline = round(band * .64); safe = width * .84
    result=[]; last_end=-1
    for si,segment in enumerate(segments):
        words=segment['words']
        for w in words:
            if not (isinstance(w['text'],str) and w['text'] and math.isfinite(w['start']) and math.isfinite(w['end']) and 0 <= w['start'] < w['end'] <= segment['end']):
                raise ValueError(f'Invalid word: {w}')
            if w['start'] < last_end-0.005: raise ValueError(f'Unordered/overlapping word: {w}')
            last_end=w['end']
        # Do not join disconnected speech, even if the punctuation is incomplete.
        chunks=[]; start=0
        for i in range(1,len(words)):
            if words[i]['start']-words[i-1]['end'] > 1.0:
                chunks.append(words[start:i]); start=i
        chunks.append(words[start:])
        for chunk in chunks:
            groups=grouping.group_words(chunk,font,safe-12,max_words=3,combine_sentences=False)
            for g in groups:
                texts=[w['text'] for w in g]
                start_frame=math.ceil(g[0]['start']*fps-1e-7)
                end_frame=min(math.ceil(g[-1]['end']*fps-1e-7)+2, math.floor(segment['end']*fps))
                states=[]
                for wi,word in enumerate(g):
                    frame=math.ceil(word['start']*fps-1e-7)
                    im=draw_caption_state(texts,wi,size=(width,band),center_x=width/2,baseline=baseline,font=font,profile=style,pad_x=0,stroke=2)
                    bounds=im.getbbox()
                    if bounds and (bounds[0] < (width-safe)/2 or bounds[2] > (width+safe)/2): raise ValueError('Caption exceeds safe width')
                    path=output/f's{si:02}-g{len(result):03}-w{wi:02}.png'; im.save(path)
                    states.append({'frame':frame,'path':str(path),'text':word['text']})
                result.append({'start_frame':start_frame,'end_frame':end_frame,'words':g,'states':states})
    # A small tail aids readability, but must never cover the next group's
    # first highlighted word when consecutive lines touch.
    for current, following in zip(result, result[1:]):
        current['end_frame'] = min(current['end_frame'], following['start_frame'])
    record={'fps':fps,'canvas':[width,height],'font':font_path,'font_index':font_index,'font_size':font_size,'style':style,'band_height':band,'baseline':baseline,'safe_width':safe,'algorithm':grouping.VERSION,'groups':result,'boundary_warnings':grouping.boundary_warnings([g['words'] for g in result])}
    (output/'caption-map.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    return record
