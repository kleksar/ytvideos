"""Record working state without treating unheard mix or pending approval as passed."""
from build_review_edit import setup, read, ref, sha, ROOT
from pathlib import Path
import json, subprocess as sp, sys

for name in sys.argv[1:]:
 ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
 state=ep/'FLOW_STATE.json'
 expected=sha(state); o=read(state)
 e='codex://threads/01a1c0ae-3f13-70b1-a027-9b22d6512cd6 — пользователь, 9 ноября 2026: «продолжай. все разрешаю. жду готовые мп4 на утверждение».'
 o['scope']='Производство утверждаемого локального MP4 EN в наборе четырёх роликов; внешние действия не входят в поручение.'
 o['input_evidence']=e
 o['decisions']['story_accepted']=dict(accepted=True,target='EN review-v01, '+str(transcript)+' SHA-256 '+sha(transcript),evidence=e+' Разрешено продолжить производство без промежуточного утверждения.')
 done_render=(w/'qa-v01/REPORT.md').is_file() and out.is_file()
 length=frames/30
 state_map={s['id']:s for s in o['stages']}
 mapping={
  'develop_story':([ep/'EPISODE.md'],'Полный сюжет и источники в EPISODE.md'),
  'script':([transcript],'Точный производственный EN текст, озвучен полностью'),
  'storyboard':([w/'shot-map-v01.json'],'Реальные интервалы кадров, сцены, prompt/reference и движение'),
  'audio':([media,speed,word],'Выход и тайминги готовы, субъективное прослушивание UNVERIFIED'),
  'images':([w/'shot-map-v01.json'],'Выбранные уникальные кадры, положение субтитров и цели движения проверяются по композитам'),
  'subtitles':([d/'subtitle-preflight-v01.md',d/'subtitle-review-v01.json',out.with_suffix('.srt')],'Полная карта слов, экранные группы, preflight и отдельный SRT'),
  'render':([out,w/'qa-v01/REPORT.md',out.with_suffix('.mp4.delivery.json')],'Точный экспорт и QA; одобрение пользователем ожидается'),
 }
 for key,(paths,method) in mapping.items():
  stage=state_map.get(key)
  if stage is None: continue
  paths=[p for p in paths if p.is_file()]
  stage['artifacts']=[dict(**ref(p),version='EN review-v01') for p in paths]
  if paths:
   stage['skill_runs']=[dict(skill=k,status='APPLIED',evidence=method+' — '+str(paths[0])) for k in stage['skills']]
   if key in ('develop_story','script','storyboard'): stage['status']='DONE'
  if key=='audio':
   stage['checks']=[dict(name='mix_listening',status='UNVERIFIED')]
  if key=='render' and done_render:
   stage['checks']=[dict(name='technical_review',status='PASS',evidence=str(w/'qa-v01/REPORT.md'),reviewer='Codex',method='Полное декодирование, потоковые параметры и выборка финальных кадров',coverage='Весь файл и каждый план')]
 o['next_step']=('Получить пользовательское решение по точному MP4; упаковка и загрузка требуют отдельного поручения.' if done_render
                 else 'Дождаться экспорта, проверить точный MP4 и передать на пользовательское утверждение.')
 work=w/'flow-candidate-v01.json'
 work.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
 sp.run([sys.executable,ROOT/'.agent/scripts/episode_flow.py','update',state,work,'--expected-sha256',expected],check=True)
 text=f'# {o["episode"]} · текущий контекст\n\nEN {fmt}, {length:.3f} с. {e}\n\n[Сюжет и источники](EPISODE.md) · [План сцен](Work/shot-map-v01.json) · [Микс](Assets/Audio/HANDOFF.md).\n\n'
 if done_render:
  text+=f'[MP4 на утверждение](Deliverables/{out.name}), SHA-256 `{sha(out)}`. [Проверка точного файла](Work/qa-v01/REPORT.md). Одобрение не получено, YouTube не менялся.\n'
 else:
  text+='Текст озвучен, полный микс собран. Монтаж подготовлен; экспорт и/или финальная проверка ещё идут.\n'
 if name=='us': text+='\nРусский v14 сохранён. Оценка точной EN версии в Extra High и независимый итоговый фактчек UNVERIFIED; выполнена документированная авторская проверка.\n'
 (ep/'CURRENT_CONTEXT.md').write_text(text)
