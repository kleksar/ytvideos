"""Register five verified full versions and preserve the approved excerpt record."""
from pathlib import Path
import json
import subprocess
import sys
from full_song_plan import NAMES, batch, edit, read, repo, sha, write

active=edit/'review-index.json'
fragment=edit/'FRAGMENTS.json'
old_index=edit/'review-index-before-full-songs.json'
old_fragment=edit/'FRAGMENTS-before-full-songs.json'
assert not old_index.exists() and not old_fragment.exists()
entries=[]
contracts={}
for name in NAMES:
    prefix=edit/f'{name}-full-song-v01'
    cp=prefix.with_name(prefix.name+'-contract.json')
    qp=prefix.with_name(prefix.name+'-qa.json')
    contract,qa=read(cp),read(qp)
    video=Path(qa['file'])
    assert qa['full_decode']==qa['constant_frame_cadence']=='PASS'
    assert qa['visual_inspection']=='PASS'
    assert qa['sha256']==sha(video)
    assert contract['output']==qa['file']
    entries.append(dict(title=contract['title'],file=str(video),qa=str(qp),sha256=qa['sha256'],
                        duration_seconds=qa['duration_seconds'],audio_duration_seconds=qa['audio_duration_seconds'],
                        edition='full-song-v01',status='READY_FOR_REVIEW'))
    contracts[str(cp)]=contract
candidate=edit/'full-song-review-index.json'
candidate_fragments=edit/'full-song-fragments.json'
write(candidate,entries)
subprocess.run([sys.executable,str(repo/'automation/music_fragments.py'),'--index',str(candidate),'--output',
                str(candidate_fragments)],check=True)
journal=read(candidate_fragments)
for record in journal['exports']:
    audio=record['audio']
    contract=contracts[record['edit_contract']]
    audio.update(source_out_exclusive_seconds=round(contract['samples']/contract['sample_rate'],9),
                 source_decoded_samples=[0,contract['samples']],source_sample_rate=contract['sample_rate'])
write(candidate_fragments,journal)
old_index.write_bytes(active.read_bytes())
old_fragment.write_bytes(fragment.read_bytes())
candidate.replace(active)
candidate_fragments.replace(fragment)
brief=batch/'SIX_SHORTS_BRIEF.md'
current=brief.read_text()
table=current[current.index('| Трек'):current.index('Точные таймкоды 76')].rstrip()
brief.write_text(f"""# Пять полных музыкальных монтажей — Nuviko Videos

Пользователь одобрил короткие версии и поручил собрать пять треков целиком. Текущие MP4, точные длительности, хеши и квитанции проверки перечислены в `Edit/review-index.json`. Все версии вертикальные, 1440×2560 и 30 кадров/с. Epic Inspiration снят с работы.

{table}

Полные версии включают 341 план и 265 новых футажей. Одобренные фрагменты сохранены внутри соответствующих треков. Смена планов привязана к музыкальным атакам, пословные титры закрывают паузы короче 500 мс по [канальному стандарту](../../.agent/SATISFYING_SHORTS.md). Карты слов, источники тайминга, FFmpeg контракты и результаты проверки сохранены под именами `Edit/*-full-song-v01-*.json`.

[Журнал фрагментов](Edit/FRAGMENTS.json) связывает каждый MP4 с полным аудио и каждым исходным планом. Повторы источников проверены по ID и SHA-256. Лицензии новых футажей записаны в `Source/Footage/full-song-stock/manifest.json`, источники треков — в `MUSIC_SOURCES.md`. Сведения об убранных файлах записаны в `Edit/cleanup-*-full-song-v01.json`.
""")
print('Registered',len(entries),'full-length MP4s',flush=True)
