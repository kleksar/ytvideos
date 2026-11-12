"""Mechanical minimum-change timing draft; does not invent new compositions."""
import array
import collections
import copy
import hashlib
import json
import pathlib
import re

episode=pathlib.Path(__file__).resolve().parents[2]
root=episode.parents[2]
old=json.loads((episode/'Storyboard/storyboard_v01.json').read_text())
alignment_path=root/'channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en.alignment.json'
align=json.loads(alignment_path.read_text())['alignment']
text=''.join(align['characters'])
starts=align['character_start_times_seconds']; ends=align['character_end_times_seconds']
words=[{'text':m.group(),'start':starts[m.start()]/1.05,'end':ends[m.end()-1]/1.05} for m in re.finditer(r'\S+',text)]
assert len(words)==1514

def schedule(begin,end,nominals):
    n=len(nominals)-1; length=end-begin
    previous=[float('inf')]*(length+1); previous[0]=0
    backs=[]
    gap_cost=[4.0]*(length+1)
    for w,nextw in zip(words,words[1:]):
        a=round(w['end']*30)-begin;b=round(nextw['start']*30)-begin
        for f in range(max(0,a-1),min(length,b+1)+1):gap_cost[f]=0
    for i in range(1,n+1):
        current=[float('inf')]*(length+1); back=array.array('i',[-1])*(length+1); queue=collections.deque()
        lo=max(i*120,length-(n-i)*180); hi=min(i*180,length-(n-i)*120)
        if i==n:lo=hi=length
        next_add=max(0,lo-180)
        for t in range(lo,hi+1):
            while next_add<=t-120:
                s=next_add;next_add+=1
                while queue and previous[queue[-1]]>=previous[s]:queue.pop()
                queue.append(s)
            while queue and queue[0]<t-180:queue.popleft()
            if queue:
                s=queue[0];current[t]=previous[s]+((begin+t-nominals[i])/30)**2+(0 if i==n else gap_cost[t]);back[t]=s
        previous=current;backs.append(back)
    if previous[length]==float('inf'):raise ValueError('No 4–6 second conform')
    cut=[length]
    for back in reversed(backs):cut.append(back[cut[-1]])
    return [begin+x for x in reversed(cut)]

scenes=old['scenes']
prefix=[0]+[x['out_frame_exclusive'] for x in scenes[:106]]
suffix=[14841]+[x['out_frame_exclusive'] for x in scenes[110:]]
prefix=schedule(0,14173,prefix)
church=schedule(14173,14841,[round(14173+i*668/5) for i in range(6)])
suffix=schedule(14841,17233,suffix)
result=[]

def add_row(id,a,b,source=None,church_index=None):
    spoken=[w for w in words if a<=round(w['start']*30)<b]
    row=copy.deepcopy(source) if source else {}
    row.update({'scene_id':id,'in_frame':a,'out_frame_exclusive':b,'fps':30,'in_seconds_estimated':a/30,'out_seconds_estimated':b/30,'duration_seconds_estimated':(b-a)/30,'timing_status':'MECHANICAL_CONFORM_DRAFT; character alignment /1.05; not listened; no final semantic-boundary acceptance','current_spoken_words':' '.join(w['text'] for w in spoken),'word_count':len(spoken),'cut':'direct','grain':'g08','composition_status':'EXISTING_COMPOSITION_UNCHANGED_PENDING_NEW_TIMING_REVIEW' if source else 'UNASSIGNED_PENDING_CONSULTATION_EXCEPTION','caption_status':'existing cue functions retained for later wording/timing pass; no new PNG selection'})
    if source:
        row['legacy_scene_id']=source['scene_id']
        row['approved_revision_tasks']=[]
        n=int(source['scene_id'])
        if n<=4 or n>=123:row['approved_revision_tasks'].append('Связать мотив порога/пустоты и нового основания по принятому brief; новые композиции ещё не разработаны.')
        if 69<=n<=75:row['approved_revision_tasks'].append('Последовательно объяснить две защиты; не смешивать числовые datum и не раскрывать вторую меру раньше голоса.')
        if 89<=n<=98:row['approved_revision_tasks'].append('Связать доставку песка, постепенное заполнение и завершение основания; сохранить человеческий масштаб.')
    else:
        row.update({'composition_type':'PLANNED documentary carrier / paper reconstruction sequence','image_path':None,'image_status':'PLANNED_NOT_GENERATED','paper_composition_prompt_en':None,'approved_revision_tasks':['Архивный снимок → бумажная реконструкция → деталь согласованного подъёма по принятому brief. Точная новая композиция не утверждена.'],'church_slot':church_index})
    result.append(row)

for i,s in enumerate(scenes[:106]):add_row('R'+s['scene_id'],prefix[i],prefix[i+1],s)
for i in range(5):add_row(f'CH{i+1:02}',church[i],church[i+1],church_index=i+1)
for i,s in enumerate(scenes[110:]):add_row('R'+s['scene_id'],suffix[i],suffix[i+1],s)
assert result[0]['in_frame']==0 and result[-1]['out_frame_exclusive']==17233
assert all(120<=r['out_frame_exclusive']-r['in_frame']<=180 for r in result)
assert all(a['out_frame_exclusive']==b['in_frame'] for a,b in zip(result,result[1:]))
assert sum(r['word_count'] for r in result)==1514
output={'episode':old['episode'],'channel':'Paper Detour','version':2,'status':'TIMING_CONFORM_DRAFT_NOT_COMPLETE_CREATIVE_STORYBOARD','authorization':'User approved revision plan and requested G08. New creative consultation returned no result; exception pending.','source_narration':old['source_narration'],'source_audio':old['source_audio'],'audio_speed_factor_already_applied':1.05,'timeline_frames':17233,'frame_rate':30,'scene_count':len(result),'grain':'g08','timing_method':'minimum squared boundary displacement from legacy; 120–180 frame hard constraints; preference for character-alignment word gaps; prefix/church/suffix boundaries fixed','new_images_created':0,'unassigned_church_slots':5,'scenes':result,'checks':{'duration_policy':'PASS_NUMERIC','full_word_coverage':1514,'semantic_reveal_and_heard_sync':'UNVERIFIED','new_composition_selection':'PENDING','consultation':'NO_SUBSTANTIVE_RESULT'}}
dest=episode/'Storyboard/storyboard_v02_timing_conform_draft.json'
dest.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
md=['# Галвестон — раскадровка v02: технический timing draft','','**Не законченная новая постановка.** Сетка всей озвучки приведена к4–6с, существующие композиции сохранены как входы для проверки. Пять церковных слотов зарезервированы, новые композиции/PNG не выбраны: Extra High не выдал результат, исключение у пользователя ожидается. Полная текущая сборка не изменена.','','Основа:1514слов;17233кадра;30fps;574.433с;129слотов. Озвучка1.05× уже применена, повторного ускорения нет. Зерно:G08 по новому поручению. Слова распределены по началу в character alignment /1.05; это не проверка на слух.','', '| ID | Кадры / секунды | Текст по alignment | Картинка / статус | Принятая задача доработки |','|---|---|---|---|---|']
for r in result:
    a=r['in_frame'];b=r['out_frame_exclusive'];asset=r.get('image_path') or 'PLANNED — новая композиция ожидается'
    md.append(f"|{r['scene_id']}|{a}–{b}; {a/30:.3f}–{b/30:.3f} ({(b-a)/30:.3f}с)|{r['current_spoken_words'].replace('|','/')}|{asset}|{' '.join(r.get('approved_revision_tasks',[])) or 'Сохранить композицию; проверить новую границу и порядок раскрытия.'}|")
(episode/'Storyboard/storyboard_v02_timing_conform_draft.md').write_text('\n'.join(md)+'\n')
print(json.dumps({'slots':len(result),'frames':17233,'words':1514,'duration_min':min((r['out_frame_exclusive']-r['in_frame'])/30 for r in result),'duration_max':max((r['out_frame_exclusive']-r['in_frame'])/30 for r in result),'church_boundaries':church,'output':str(dest)}))
