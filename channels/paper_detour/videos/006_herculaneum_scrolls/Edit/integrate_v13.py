#!/usr/bin/env python3
"""Produce the v1.3 working score without changing the archived Pro response."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'Script'
source = SCRIPT / 'GPT_PRO_PRODUCTION_v1_2.json'
director_path = SCRIPT / 'DIRECTOR_CORRECTIONS_v1_3.md'
vo_path = SCRIPT / 'VO_EN_v1_3.txt'
json_out = SCRIPT / 'PRODUCTION_v1_3.json'
md_out = SCRIPT / 'PRODUCTION_PACKAGE_v1_3.md'
log_out = SCRIPT / 'INTEGRATION_v1_3.md'
for output in (json_out, md_out, log_out):
    if output.exists() and '--rewrite-owned' not in sys.argv:
        raise FileExistsError(output)

d = json.loads(source.read_text(encoding='utf-8'))
old_music = d['global_direction_markdown'].split('## 3. Непрерывная звуковая партитура', 1)[1].split('## 4. Полный английский текст озвучки', 1)[0].strip()
old_music = re.sub(r'\*\*Расчёт хронометража:\*\*[^\n]+', '**Хронометраж:** см. текущие расчётные времена v1.3; точная длительность определится после получения разрешённой озвучки.', old_music)
rights_note = d['rights_and_delivery_markdown'].split('## 8. Проверка прав и решение для основного монтажа', 1)[1].split('## 10. Реестр утверждений', 1)[0].strip()
rights_note = rights_note.replace('| Source Sans 3 | S30: SIL Open Font License 1.1 | Использовать для бумажного набора; лицензию сохранить при передаче файлов шрифта |', '| Source Sans 3 | S30: SIL Open Font License 1.1 | Не является эталоном фирменных акцентов. Если используется отдельно для служебного паспорта, проверить условия и сохранить лицензию при передаче |')
rights_note = rights_note.replace('Проверены опубликованные условия и подписи.', 'Ниже сохранены предварительные сведения Pro об опубликованных условиях и подписях; каждый фактический файл и способ использования проверяются отдельно до импорта.')
director = director_path.read_text(encoding='utf-8')
vo = vo_path.read_text(encoding='utf-8')
cards = {c['id']: c for c in d['cards']}
beats = {b['id']: b for c in d['cards'] for b in c['beats']}
assert len(cards) == 53 and len(beats) == 230
old_sentence = 'Camillo Paderni cut rolls lengthwise, copied the writing that became visible, and scraped away material to continue.'
new_sentence = 'Camillo Paderni cut rolls lengthwise. The exposed writing was copied, and material was scraped away to reveal the next layer.'
original_vo = (SCRIPT / 'GPT_PRO_VO_EN_v1_2.txt').read_text(encoding='utf-8')
assert original_vo.count(old_sentence) == 1
assert original_vo.replace(old_sentence, new_sentence) == vo
beats['P07.B02']['quote'] = new_sentence
cards['P07']['vo'] = cards['P07']['vo'].replace(old_sentence, new_sentence)
np = {p['id']: p for p in d['narration']['paragraphs']}
np['P07']['vo'] = np['P07']['vo'].replace(old_sentence, new_sentence)
np['P07']['sentences'] = [s for b in cards['P07']['beats'] for s in re.split(r'(?<=[.!?])\s+', b['quote'])]

table = director.split('## 6. Карта конкретных замен', 1)[1].split('\nДополнительно для P07.B02', 1)[0]
changed = []
for line in table.splitlines():
    if not re.match(r'^\| P\d\d\.B\d\d \|', line):
        continue
    fields = [x.strip() for x in line.strip().strip('|').split('|')]
    assert len(fields) == 6, fields
    bid, frame, camera, action, accent, exit_ = fields
    beat = beats[bid]
    changed.append(bid)
    for key, value in [('frame', frame), ('camera', camera), ('action', action)]:
        if value != '—':
            beat[key] = value
    if accent != '—':
        if accent.startswith('Изменить только `mask`:'):
            beat['accent']['mask'] = accent.split(':', 1)[1].strip()
        elif accent == 'NONE / NONE / NONE / NONE':
            beat['accent'] = {k: 'NONE' for k in ('words', 'anchor', 'mask', 'placement', 'exit')}
        else:
            values = [x.strip().strip('`') for x in accent.strip('`').split(' / ')]
            assert len(values) == 4, (bid, accent, values)
            for key, value in zip(('words', 'anchor', 'mask', 'placement'), values):
                beat['accent'][key] = value
    if exit_ != '—':
        beat['accent']['exit'] = exit_
assert len(changed) == 39 and len(set(changed)) == 39, len(changed)

# Card-level continuity, matching the corrected beats and their independent props.
cards['P07']['layers']['background'] = 'Тёмная стенка с маркировками GENERAL METHOD • RECONSTRUCTION и SCHEMATIC MARKS. Карточка CAMILLO PADERNI относится только к этапу разрезания; последующее копирование и снятие слоя показаны без приписывания исполнителя.'
cards['P07']['occlusion'] = 'Пластина режет отдельный условный рулон; лист и лоток стоят раздельно. Сменой нейтральных рук или фокуса не приписывать копирование и соскабливание Падерни. Модель не является PHerc. 1667.'
cards['P07']['accuracy'] = 'Падерни приписано только разрезание. Копирование и снятие материала показаны без указания конкретного исполнителя; общий метод не привязан к 1667. Реконструкция условная, штрихи не являются греческим текстом.'
beats['P07.B03']['accent']['exit'] = 'Буквы прячутся за нижний край листа. Затем отдельная широкая непрозрачная плоскость проходит перед объективом и полностью закрывает кадр.'
cards['P07']['transition_out'] = 'Отдельная широкая непрозрачная плоскость полностью закрывает кадр; под ней склейка на вертикальную стойку механизма Piaggio. Карточка Paderni исчезает вместе с предыдущей сценой.'
cards['P01']['transition_out'] = 'Непрозрачная круглая заслонка полностью перекрывает кадр. Под перекрытием открыть более широкий ракурс модели 1667 в шкафу SET-D; бирка и опора остаются идентичными.'
cards['P12']['transition_out'] = 'Отдельная крупная непрозрачная рамка полностью перекрывает экран с запасом; после полного покрытия открыть отдельный широкий учебный томограф SET-E. При невозможности использовать мотивированную явную склейку с выдержкой нового плана ≥3 с.'
cards['P21']['transition_out'] = 'Удержать контрольные окна и пустую графу VERIFIED в начале P22.B01 до читаемого ухода NOT A VERDICT; затем боковая стенка полностью перекрывает кадр и открывает рабочие места конкурса.'
cards['P29']['transition_out'] = 'Конверт на собственной опоре полностью перекрывает экран до смены ракурса и пространства; после перекрытия открыть отдельную схему проверки P30.'
cards['P41']['transition_out'] = 'Один непрерывный отъезд открывает два раздельных постамента с паспортами Paris 4 и PHerc. 1667 в общей системе координат. Обе модели и их подписи сохраняются в P42; морфинг запрещён.'
cards['P44']['transition_out'] = 'Непрозрачная передняя рамка полностью покрывает экран до смены ракурса; затем открыть отдельный стол условной карты читаемости P45. Новая схема не претендует на точные координаты прежней.'
cards['P48']['transition_out'] = 'Сцена P48 продолжается в начале P49.B01 до читаемого ухода FURTHER SCRUTINY. Только затем передний бортик полностью перекрывает кадр и открывает стеллаж P49; переход выполняется один раз.'
cards['P53']['transition_out'] = 'После последнего слова сохранить финальный предмет в течение двухсекундной смысловой выдержки. Закрытие занимает 0,5 с, количество кадров пересчитать по фактическому FPS. Зерно продолжается; затем четыре титровые карточки общей длительностью 20 с.'
extras = {
 'P01': ('Отдельная круглая непрозрачная заслонка должна закрыть весь экран до смены сцены; её видимая и скрытая геометрия подготовлены с запасом.', 'REV13_P01_SHUTTER'),
 'P02': ('Две независимые ячейки и подвижная левая рама на направляющей; перекладина движется вместе с рамой и закрывает привязанный к ней текст. Ядро и бирка остаются на отдельной правой опоре.', 'REV13_P02_FRAME'),
 'P07': ('Отдельная широкая непрозрачная плоскость закрывает весь экран после ухода A COPY SURVIVES; она не является листом, повёрнутым ребром.', 'REV13_P07_TRANSITION'),
 'P12': ('Крупная отдельная непрозрачная рамка полностью покрывает экран с запасом, прежде чем открывается томограф P13.', 'REV13_P12_SCREEN_MASK'),
 'P14': ('Наружная непрозрачная кромка рамки на отдельном переднем слое скрывает TRACE THE SURFACE; начальное и конечное положение текста и кромки связаны.', 'REV13_P14_MASK'),
 'P21': ('Пустая графа VERIFIED и её непрозрачная стойка с маской для NOT A VERDICT отдельно от контрольных окон; кадр удерживается до начала P22.', 'REV13_P21_VERIFIED'),
 'P24': ('Единая рейка и отдельные карточки OBSERVATION, SCANNED и SEGMENTED; стойка OBSERVATION перекрывает SHARED CLUE. Текст привязан к этой движущейся карточке.', 'REV13_P24_RAIL'),
 'P34': ('Отдельная регистрационная рамка и её вертикальная стойка перекрывают NO SUBSTITUTE; поля AUTHOR и TITLE не заполняются.', 'REV13_P34_FRAME'),
 'P44': ('Физическое ядро на отдельном ложементе и цифровая схема на отдельной опоре видны одновременно; внешняя рейка является маской A BOUNDARY.', 'REV13_P44_SEPARATE'),
 'P51': ('Между окнами отдельная непрозрачная центральная кулиса; она скрывает NAMES UNCERTAIN, не прикрывая ни бирки, ни предметы. Каждое окно и каждая из двух боковых кулис на отдельных опорах.', 'REV13_P51_CURTAIN'),
 'P52': ('Та же модель 1667, что в P53: повреждения, ориентация, опора и бирка сохраняются; цифровая поверхность остаётся отдельной.', 'REV13_P52_CONTINUITY'),
 'P53': ('Та же модель и те же повреждения, что в P52; зерно движется даже во время смысловой неподвижности.', 'REV13_P53_CONTINUITY'),
}
for cid, (description, asset_id) in extras.items():
    c = cards[cid]
    c['occlusion'] += ' Дополнение v1.3: ' + description
    c['assets'].append(asset_id + ' — ' + description)
    d['assets'].append({'id': asset_id, 'descriptions': [description], 'paragraphs': [cid], 'rights_status': 'PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.'})
cards['P51']['layers']['middle'] = cards['P51']['layers']['middle'].replace('Между окнами пустой промежуток.', 'Между окнами пространственный промежуток с отдельной кулисой для NAMES UNCERTAIN.')
cards['P51']['occlusion'] = cards['P51']['occlusion'].replace('зазор между окнами остаётся пустым', 'центральная кулиса находится в зазоре между окнами')
cards['P44']['layers']['middle'] += ' Физическое ядро и цифровая схема размещены раздельно и одновременно.'
cards['P44']['layers']['background'] = 'Нейтральное кремовое пустое поле без второй модели. Подписи DIGITAL MODEL и APPROXIMATE EXTENT — NOT A RESTORATION постоянны.'
cards['P50']['camera_constraint'] = 'Один непрерывный мастер с пятью закреплёнными станциями и фоном с запасом; 42 см исходного макета не являются координатами Palmier. Координаты задать и проверить в отдельной беззвучной пробе.'

# Remove duplicated old v1.2 prose, which otherwise contradicts the working cards.
d.pop('global_direction_markdown', None)
d.pop('rights_and_delivery_markdown', None)
d['version'] = '1.3-working-reviewed-vo'
d['narration']['version'] = '1.3'
d['timing_provisional'] = True
d['timing_note'] = 'Механическая оценка 140 слов/мин и паузы из v1.2; до записи голоса время не является синхронизацией. Удержания и переносы сцен требуют ручной проверки.'
d['working_direction'] = {
 'typography': 'Фирменные акценты строить по реальным бумажным PNG выпуска 001 и channels/paper_detour/brand/TYPOGRAPHY_STANDARD.md; существующие глифы переиспользовать, недостающие изготовить и визуально сверить. Подтверждённого полного цифрового шрифта нет. Source Sans 3 не является основой акцентов; для предметных служебных паспортов допустимо отдельное оформление с проверкой лицензии.',
 'format': '16:9; конкретный размер и FPS определить по отдельному активному и видимому проекту 006. 3840×2160/24 и 1920×1080/30 — предложения, а не подтверждённые параметры.',
 'minimum_shot': 'Каждый новый основной план ≥3 с, кроме прямо согласованных пользователем исключений. Бит не равен склейке; непрерывные планы из v1.3 помечены в картах. Проверить всю длительность после получения разрешённой речи.',
 'layers': 'Совместимые FG/MG/BG, независимое движение, контактные тени, достроенный фон, настоящие маски и непрерывное движущееся мягкое зерно включая титры. Общий зум не заменяет параллакс.',
 'text_timing': 'Акцент синхронизировать с произнесённым маркером, дать осмысленное полное открытие и читаемую остановку. Чаще один крупный акцент; два окна P51 допускают краткое перекрытие при проверенной читаемости.',
 'sound': 'До прямого разрешения пользователя не генерировать и не рендерить новый звук, в том числе озвучку, музыку, эффекты и пробы. Запланированные SFX — указания, не готовая звуковая дорожка.',
 'continuity': 'Paris 4 и PHerc. 1667 — отдельные модели и подписи. При замене сцен под маской сначала добиться полного покрытия. P50 — один мастер с пятью станциями и фоном с запасом; P52/P53 — одна модель 1667.',
 'production_gates': 'До финальных активов проверить беззвучные пробы P02, P12→P13, P41→P42, P50 и деформации P13/P35–P39; проверить альфу, контакты, края, свет, параллакс и чтение в движении. После аудио пересчитать и прослушать весь фильм.',
 'provenance': 'Архивный исходный ответ Pro: GPT_PRO_PACKAGE_v1_2.md и GPT_PRO_PRODUCTION_v1_2.json. Адресные исправления: DIRECTOR_CORRECTIONS_v1_3.md. Сценарий: VO_EN_v1_3.txt и независимый INDEPENDENT_FACT_CHECK.md.',
}
d['music_direction_markdown'] = old_music
d['rights_and_uncertainty_note_markdown'] = rights_note

# Revise claim and font source: license evidence is not a visual brand reference.
for claim in d['claims']:
    if claim['id'] == 'C05':
        claim['claim'] = 'Paderni разрезал рулоны продольно; раскрытое письмо копировалось, а материал снимался для доступа к следующему слою.'
        claim['boundary'] = 'Источники не устанавливают, что Падерни лично выполнял каждое копирование и соскабливание; не доказано применение к 1667. Реконструкция условная.'
    if claim['id'] == 'C50':
        claim['claim'] = 'Лицензия Source Sans допускает использование по SIL OFL 1.1; эта гарнитура не подтверждена как фирменная типографика Paper Detour. Met 53.514.8 отмечен Public Domain.'
for s in d['sources']:
    if s['id'] == 'S30':
        s['supports'] = 'Условия лицензии, если Source Sans будет отдельно выбран для служебного музейного паспорта; не является эталоном бумажных акцентов.'

# Recompute estimated timings for all words, not the physical performance.
def fmt(seconds):
    m = int(seconds // 60)
    return f'{m:02d}:{seconds - 60*m:04.1f}'
def wc(s):
    return len(s.split())
rate = 60.0 / 140.0
elapsed = 0.0
for card in d['cards']:
    card['t0'] = round(elapsed, 3)
    for b in card['beats']:
        b['t0'] = round(elapsed, 3)
        b['word_count'] = wc(b['quote'])
        elapsed += b['word_count'] * rate
        b['t1'] = round(elapsed, 3)
        b['tc'] = f"{fmt(b['t0'])}–{fmt(b['t1'])}"
        ac = b['accent']
        if ac.get('words') != 'NONE':
            pos = b['quote'].lower().find(ac['anchor'].lower())
            if pos < 0:
                raise ValueError(f"Missing anchor {b['id']}: {ac['anchor']}")
            est = b['t0'] + wc(b['quote'][:pos]) * rate
            ac['estimated_entry_seconds'] = round(est, 3)
            ac['estimated_entry_tc'] = fmt(est)
        else:
            ac.pop('estimated_entry_seconds', None)
            ac.pop('estimated_entry_tc', None)
    elapsed += float(card['pause_after'])
    card['t1'] = round(elapsed, 3)
    card['tc'] = f"{fmt(card['t0'])}–{fmt(card['t1'])}"
    para = np[card['id']]
    para['t0'], para['t1'], para['tc'], para['word_count'] = card['t0'], card['t1'], card['tc'], wc(card['vo'])
for credit in d['end_credits']:
    credit['t0'] = round(elapsed, 3)
    elapsed += 5.0
    credit['t1'] = round(elapsed, 3)
    credit['tc'] = f"{fmt(credit['t0'])}–{fmt(credit['t1'])}"
d['narration']['total_words'] = wc(vo)
d['narration']['estimated_seconds'] = d['cards'][-1]['t1']

d['accent_register'] = [dict(beat=b['id'], paragraph=c['id'], **copy.deepcopy(b['accent'])) for c in d['cards'] for b in c['beats'] if b['accent'].get('words') != 'NONE']
d['sfx_register'] = [dict(beat=b['id'], tc=b['tc'], cue=b['sound']) for c in d['cards'] for b in c['beats'] if b['sound'] != 'NONE']
norm = lambda x: re.sub(r'\s+', ' ', x).strip()
assert norm(' '.join(x['vo'] for x in d['narration']['paragraphs'])) == norm(vo)
for c in d['cards']:
    assert norm(' '.join(b['quote'] for b in c['beats'])) == norm(c['vo']) == norm(np[c['id']]['vo']), c['id']
assert len(d['accent_register']) == 109, len(d['accent_register'])
assert len(d['sfx_register']) == 19, len(d['sfx_register'])
assert 'STILL OPEN' not in [x['words'] for x in d['accent_register']]
for word in ['NO SUBSTITUTE', 'TRACE THE SURFACE', 'NOT A VERDICT', 'NAMES UNCERTAIN']:
    assert word in [x['words'] for x in d['accent_register']]
source_ids = {x['id'] for x in d['sources']}
assert all(s in source_ids for c in d['cards'] for s in c['sources']), 'card source check'
assert all(s in source_ids for c in d['claims'] for s in c['sources']), 'claim source check'
d['qa'] = {
 'paragraphs': len(d['cards']), 'semantic_beats': sum(len(c['beats']) for c in d['cards']),
 'paper_accents': len(d['accent_register']), 'sfx_cues': len(d['sfx_register']),
 'word_count': wc(vo), 'wpm': 140, 'vo_seconds_estimate': d['cards'][-1]['t1'],
 'credits_seconds': 20, 'master_seconds_estimate': round(elapsed, 3),
 'source_count': len(d['sources']), 'claim_count': len(d['claims']), 'planned_asset_ids': len(d['assets']),
 'checks': ['Весь VO совпадает с 53 карточками и 230 цитатами; якоря акцентов встречаются в соответствующих репликах.', 'Исправления режиссёра раздела 6 применены к полям; реестры акцентов и SFX собраны из карточек.', 'Оценочные времена пересчитаны математически по 140 словам в минуту.'],
 'unverified': ['Полный аудит всех реальных границ планов и считываемости в монтаже', 'Фактическое время и произношение без озвучки', 'Существование и композит всех графических активов, прослушивание звука и проверка прав каждого заимствования', 'Техническая возможность и параметры проекта Palmier 006', 'Независимая проверка интеграции v1.3', 'Дополнительные активы v1.3 перечислены как составные требования к планам, не как полная покадровая нарезка отдельных файлов'],
}

out = []
out += ['# Paper Detour 006 — сценарно-постановочный пакет v1.3', '',
 '**Статус:** рабочая версия, в неё внесены указанные исправления независимого фактчека, визуального и операторского аудитов. Независимый обзор самой интеграции и техническая проверка композита ещё необходимы. Озвучка, новый звук и монтаж не созданы.', '',
 '**Тайминги:** расчётные при 140 словах в минуту и исходных паузах; их нельзя воспринимать как фактическую синхронизацию. Все границы планов и удержания требуют пересмотра по реальному исполнению. Аудио можно генерировать только по прямому разрешению пользователя.', '',
 '[Проверенный чистый текст](VO_EN_v1_3.txt) · [Режиссёрские исправления](DIRECTOR_CORRECTIONS_v1_3.md) · [Исходный пакет Pro v1.2](GPT_PRO_PACKAGE_v1_2.md) · [Независимый фактчек](../Research/INDEPENDENT_FACT_CHECK.md)', '', '## Общие правила']
for k,v in d['working_direction'].items(): out += [f'- **{k}:** {v}']
out += ['', '## Музыкальная драматургия M1–M6', '', 'Это план; любые новые звуки, включая пробы, требуют прямого разрешения пользователя.', '', d['music_direction_markdown'], '', '## Полный английский текст озвучки', '', vo.strip(), '', '## Сквозная партитура — 53 абзаца / 230 речевых битов', '']
for c in d['cards']:
    out += [f"### {c['id']} · оценочно {c['tc']} · {c['set']}", '', f"**Реплика:** {c['vo']}", '', f"**Цель и тип:** {c['intent']} ({c['status']}).", '',
      f"**Передний план:** {c['layers']['foreground']}", '', f"**Средний план:** {c['layers']['middle']}", '', f"**Задний план:** {c['layers']['background']}", '',
      f"**Перекрытия и опоры:** {c['occlusion']}", '']
    for b in c['beats']:
        ac = b['accent']
        out += [f"#### {b['id']} · оценочно {b['tc']}", '', f"> {b['quote']}", '', f"**Кадр:** {b['frame']}", '', f"**Камера:** {b['camera']}", '', f"**Действие:** {b['action']}", '']
        if ac.get('words') == 'NONE': out += ['**Бумажный акцент:** отдельного нового нет.', '']
        else: out += [f"**Акцент:** {ac['words']} · речевой маркер «{ac['anchor']}» · расчётное начало {ac['estimated_entry_tc']}. Маска: {ac['mask']} Место: {ac['placement']} Уход: {ac['exit']}", '']
        out += [f"**Звуковой замысел:** {b['sound']} (нового звука пока нет).", '']
    out += [f"**Переход:** {c['transition_out']}", '', f"**Музыкальный замысел:** {c['music']}", '', f"**Активы:** {'; '.join(c['assets'])}.", '', f"**Граница достоверности:** {c['accuracy']}", '', f"**Источники:** {', '.join(c['sources'])}.", '']
    if c.get('camera_constraint'): out += [f"**Камера — ограничение:** {c['camera_constraint']}", '']
out += ['## Заключительные титры', '']
for x in d['end_credits']: out += [f"- {x['id']} · оценочно {x['tc']}: {x['text'].replace(chr(10), ' / ')} — {x['action']}"]
out += ['', '## Реестр запланированных активов', '', 'Это производственное задание; файлы не считаются созданными.', '']
for x in d['assets']:
    out += [f"- **{x['id']}** ({', '.join(x['paragraphs'])}): {'; '.join(x['descriptions'])} — {x['rights_status']}"]
out += ['', '## Реестр акцентов', '']
for x in d['accent_register']: out += [f"- {x['beat']}: **{x['words']}**, маркер «{x['anchor']}», маска: {x['mask']} Уход: {x['exit']}"]
out += ['', '## Реестр запланированных звуковых жестов', '', 'Эти позиции являются замыслом и не подтверждают создание звука.', '']
for x in d['sfx_register']: out += [f"- {x['beat']} · оценочно {x['tc']}: {x['cue']}"]
out += ['', '## Права и пределы исследования — исходные сведения Pro для дополнительной проверки', '', d['rights_and_uncertainty_note_markdown'], '', '## Утверждения и ограничения', '']
for x in d['claims']: out += [f"- **{x['id']} ({x['paragraphs']}):** {x['claim']} Граница: {x['boundary']} Источники: {', '.join(x['sources'])}."]
out += ['', '## Источники', '']
for x in d['sources']: out += [f"- **{x['id']}** [{x['title']}]({x['url']}) — {x['supports']} Ограничения: {x['limits']}"]
out += ['', '## Что ещё не проверено', '']
for x in d['qa']['unverified']: out += [f'- {x}.']
out += ['', 'Права исходных материалов проверять по конкретному файлу и способу использования. Ограничение CC BY-NC у отдельных данных Vesuvius Challenge не считать разрешением на коммерческий монтаж. Подробнее: [исходное исследование](../../../research/2026-10-31-next-long-film/HERCULANEUM_SOURCE_RESEARCH.md).', '']
md = '\n'.join(out)
json_out.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
md_out.write_text(md, encoding='utf-8')
log = f'''# Интеграция v1.3\n\nИсходники Pro v1.2 сохранены. VO: `VO_EN_v1_3.txt`, SHA-256 `{hashlib.sha256(vo.encode()).hexdigest()}`. Сформированы `PRODUCTION_v1_3.json` и `PRODUCTION_PACKAGE_v1_3.md`.\n\n- Применена таблица раздела 6 режиссёрского листа: {len(changed)} записей по битам.\n- Добавлены карточные уточнения опор, масок, переходов и составные задания на недостающие активы; скорректированы C05/C50 и S30.\n- Из рабочего JSON удалены старые дублирующие текстовые копии, которые конфликтовали с новой версией; архивные источники остаются без изменений. Рабочая Markdown-партитура собрана из исправленных карточек и реестров.\n- Автопроверка: 53 абзаца, 230 битов, {len(d['accent_register'])} акцентов, {len(d['sfx_register'])} звуковых указаний; все цитаты покрывают текст, якоря акцентов присутствуют в репликах, JSON разбирается. Тайминги пересчитаны по 140 словам в минуту, но это оценка, а не проверка синхронизации.\n- Режиссёрские исправления и составные задания на дополнительные активы внесены, но раздельные координаты/файлы и вся монтажная реализуемость не подтверждены. Для новых дополнительных компонентов необходима детализация художником. Весь фильм не просмотрен, звук не создавался, права на отдельные будущие заимствования не подтверждены.\n- Потребуется независимая проверка интеграции и повторный проход по всем основным планам и читаемости после получения разрешённой озвучки.\n'''
log_out.write_text(log, encoding='utf-8')
print(json.dumps({'changed_beats': len(changed), 'paragraphs': len(d['cards']), 'beats': len(beats), 'accents': len(d['accent_register']), 'sfx': len(d['sfx_register']), 'words': wc(vo), 'vo_seconds_estimate': d['cards'][-1]['t1'], 'output': [str(json_out), str(md_out), str(log_out)]}, ensure_ascii=False))
