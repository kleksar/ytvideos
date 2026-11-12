#!/usr/bin/env python3
"""Prepare a measured one-line SRT grouping draft from the exact mix word map."""
import importlib.util, json, hashlib, sys
from pathlib import Path
from PIL import ImageFont

EP = Path(__file__).resolve().parents[3]
SKILL = Path('/Users/diplomat/ytvideos/.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py')
spec = importlib.util.spec_from_file_location('semantic_grouping', SKILL)
grouping = importlib.util.module_from_spec(spec); sys.modules[spec.name]=grouping; spec.loader.exec_module(grouping)
FONT = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
GEOM = EP.parents[3] / 'automation/ffmpeg_montage/profiles/long.json'
STYLE = EP.parents[3] / 'automation/ffmpeg_montage/profiles/nuviko.json'
WORK = EP / 'Work/production-20261105-v01/subtitles'
transcript_path = EP / 'Source/Voice/voice_en_text_v01.txt'
word_map_path = EP / 'Source/Audio/word_map_mix_v01.json'
transcript = transcript_path.read_text(encoding='utf-8').strip()
word_data = json.loads(word_map_path.read_text(encoding='utf-8'))
words = word_data['words']
if [w['text'] for w in words] != transcript.split():
    raise SystemExit('Timed word map does not preserve the literal transcript tokenization')
geometry=json.loads(GEOM.read_text()); style=json.loads(STYLE.read_text())
fs=geometry['font_size_px']
font=ImageFont.truetype(style['font'],fs,index=style['font_index'])
safe=geometry['max_visible_width_px']-2*style['pad_x']-2*style['outline_width']
# Use a non-binding word cap only so the helper can fall back to a measured
# weak boundary when a sentence has no syntax-safe partition; it is not a cue limit.
groups=grouping.group_words(words,font,safe,max_words=len(words),combine_sentences=True)
phrases=[' '.join(w['text'] for w in g) for g in groups]
if ' '.join(phrases) != ' '.join(transcript.split()):
    raise SystemExit('Grouping changed the literal transcript')
cues={'cues':[{'start_seconds':format(float(g[0]['start']),'.6f'),
               'end_seconds':format(float(g[-1]['end']),'.6f'),
               'text':' '.join(w['text'] for w in g)} for g in groups]}
(WORK/'cues_v01.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(WORK/'transcript_en_v01.txt').write_text(transcript+'\n',encoding='utf-8')
review={
 'status':'DRAFT_REVIEW_REQUIRED','grouping_algorithm':grouping.VERSION,'groups':len(groups),
 'words':len(words),'audio_sha256':word_data['audio_sha256'],'transcript_sha256':word_data['transcript_sha256'],
 'font':FONT,'font_size_px':fs,'max_text_width_px':safe,
 'boundary_warnings':grouping.boundary_warnings(groups),
 'cps_max':max(len(x)/(cues['cues'][i]['end_seconds'] and (float(cues['cues'][i]['end_seconds'])-float(cues['cues'][i]['start_seconds']))) for i,x in enumerate(phrases)),
 'semantic_review':'UNVERIFIED; automatic grouping is a draft and requires sequential editorial review',
 'audible_sync':'UNVERIFIED; word timings are provider-derived and were not listened against audio',
 'timebase':'source audio time (mix is continuous; edit conformance not yet performed)'
}
(WORK/'grouping_review_v01.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'groups':len(groups),'warnings':len(review['boundary_warnings']),'max_chars':max(map(len,phrases)), 'audio_sha256':word_data['audio_sha256'],'font_size_px':fs,'safe_width_px':safe},ensure_ascii=False,indent=2))
