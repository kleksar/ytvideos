# Paper cue selection — Extra High consultation — 031 Jascon-4

## Session and task

- Date: 2026-11-01.
- Coordinator consulted ChatGPT.com in Google Chrome inside project `YT Видео`.
- Exact visible model/reasoning label immediately before sending: **Extra High**.
- [Project chat](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae7adff-4824-83ed-9e5b-cf5570ed3700).
- User scope: paper accents in frame only. No full subtitles and no SRT/WebVTT sidecar.
- The complete narration and 16-scene order had already been provided earlier in the same chat. This request asked only for an audit of the proposed cue wording, suspense order, and story function.

## Exact request sent

> Ты — консультант в уже открытом ChatGPT Extra High. Требование внешнего координатора выполнено этим запросом; не открывай другой ChatGPT. Одна узкая редакционная задача: проверь список бумажных акцентов для Paper Detour 031 по дословности, suspense order и ясности функции. Пользователь выбрал только экранные бумажные акценты; постоянных субтитров и SRT нет. Убедись, что каждый показанный акцент — 2–5 подряд идущих слов из английского закадрового текста, не раскрывает следующий поворот раньше речи и действительно добавляет отдельный смысл. Подтверди список или предложи поправки, максимум 7 пунктов. Для каждого пункта укажи scene slug, точные слова акцента, trigger/end из речи и функцию. Без таймкодов, типографики, движения, новых изображений и правки сценария.
>
> Предложенные cues:
> 1) 02_hand_contact — GRAB HIM; trigger grab, end him; физический шок прикосновения.
> 2) 05_depth_section — TWELVE PEOPLE / ON BOARD; trigger twelve, end board; масштаб команды и ставки.
> 3) 07_search_continues — BROUGHT UP FOUR; trigger brought, end four; количество поднятых тел увеличивает тревогу.
> 4) 08_same_ship_missed_pass — STILL INSIDE; trigger still, end inside; Harrison остаётся в корпусе, его не заметили.
> 5) 10_air_pocket — AIR POCKET; trigger air (во втором упоминании), end hull; механизм выживания.
> 6) 11_depth_time — SIXTY HOURS; trigger sixty, end hours; длительность и глубина выживания.
> 7) 15_surface_survivor — ONLY SURVIVOR; trigger survivor, end died; развязка и контраст с погибшими.
>
> Сверяй с английским текстом и scene order, уже приведёнными выше в этом чате.

## Completed answer received

> Список из 7 акцентов можно сохранить. Последовательность раскрытия выдержана, каждый акцент выполняет отдельную функцию. Нужны три исправления: убрать разделитель в №2, исправить `end` в №5 и `trigger/end` в №7.
>
> 1. `02_hand_contact`  
> Cue: `GRAB HIM`  
> Trigger: `grab` → End: `him`  
> Функция: неожиданный физический контакт, первый поворот истории.  
> Статус: без изменений.
>
> 2. `05_depth_section`  
> Cue: `TWELVE PEOPLE ON BOARD`  
> Trigger: `twelve` → End: `board`  
> Функция: масштаб катастрофы и количество людей под угрозой.  
> Исправление: убрать `/`, сохранить четыре последовательных слова.
>
> 3. `07_search_continues`  
> Cue: `BROUGHT UP FOUR`  
> Trigger: `brought` → End: `four`  
> Функция: фиксирует результат поисков и усиливает ожидание трагической развязки.  
> Статус: без изменений.
>
> 4. `08_same_ship_missed_pass`  
> Cue: `STILL INSIDE`  
> Trigger: `still` → End: `inside`  
> Функция: подчёркивает, что Окене оставался в корпусе после первого прохода водолаза.  
> Статус: без изменений.
>
> 5. `10_air_pocket`  
> Cue: `AIR POCKET`  
> Trigger: `air` → End: `pocket`  
> Функция: выделяет физическое условие, позволившее выжить.  
> Исправление: end должен быть `pocket`, не `hull`. Используется повторное упоминание в сцене 10.
>
> 6. `11_depth_time`  
> Cue: `SIXTY HOURS`  
> Trigger: `sixty` → End: `hours`  
> Функция: подчёркивает исключительную продолжительность выживания.  
> Статус: без изменений.
>
> 7. `15_surface_survivor`  
> Cue: `ONLY SURVIVOR`  
> Trigger: `only` → End: `survivor`  
> Функция: окончательная развязка, контраст с судьбой остальных одиннадцати членов экипажа.  
> Исправление: прежние `survivor → died` захватывали слова за пределами акцента.
>
> Итог: 7/7 акцентов соответствуют требованию 2–5 последовательных слов из озвучки после исправления №2. Преждевременных раскрытий нет при условии появления каждого акцента не раньше соответствующего spoken trigger. Текст озвучки менять не требуется.

## Coordinator disposition

- All seven cues were retained. The slash was removed from the displayed wording; the accepted four words use a line break only.
- The end of A05 changed from `hull` to `pocket`; A07 timing changed from `survivor → died` to `only → survivor`.
- Alignment was used to calculate frame intervals; the assistant's editorial response is not acoustic sync verification or an independent factual source.
- The A07 trigger begins before the scene-14/15 cut. It starts on frame 1852 with zero opacity; its first visible frame is 1853, immediately after the aligned `only` onset. A preflight checked the cue on both adjacent scene images.
- On-ear sync, full 1× playback, and MP4 review remain **UNVERIFIED**.
