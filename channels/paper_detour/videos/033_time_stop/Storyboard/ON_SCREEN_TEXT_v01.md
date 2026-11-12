# Paper Detour 033 — экранные акценты v01

**Статус:** точные восемь фраз и решение оставить шесть сцен без текста приняты пользователем 2026-11-02: «Да: narration v02 + акценты v01, один TTS-запрос в ElevenLabs». Ориентир — принятый narration [v02](../Source/Script/NARRATION_EN_v02.txt), SHA-256 `af69eb8db211c132960531cf1a299ceda20d341a0483175b887e6c401214caba`.

**Тайминг:** пользователь принял фразы до озвучки; alignment для единственной записи v02 получен. Фактические словесные trigger/end и 30fps кадры записаны в [cue sheet](ON_SCREEN_TEXT_CUES_v01.json). Alignment совпадает с 667 символами текста; субъективное прослушивание, motion sync и playback остаются UNVERIFIED.

Принцип этого прохода: акцент добавляет рамку, следствие, образ или короткий вывод. Не переписываем каждую реплику поверх диктора. Пустые места оставлены намеренно, когда кадр или голос уже несут мысль.

| Сцена | Принятая реплика диктора (EN v02) | Принятый акцент | Показать → убрать (предварительный словесный ориентир; точные кадры в cue sheet) | Что добавляет / почему без текста |
|---|---|---|---|---|
| S01 | “Time stops. A raindrop hangs inches from your face. You have five seconds. What do you do?” | — | — | Макро капли и вопрос диктора уже создают хук. Надпись отвлекла бы от зазора между носом и каплей и повторила вопрос. |
| S02 | “At first, it sounds like the perfect power.” | — | — | Кадр показывает соблазн и масштаб. Не дублировать оценку диктора. |
| S03 | “Everything around you freezes—even light.” | — | — | Оставить раскрытие зрительским: текст заранее объяснил бы следующий кадр с темнотой. |
| S04 | “No light reaches your eyes. The world goes black.” | **NO LIGHT. NO IMAGE.** | Появление: “No light reaches your eyes” → убрать после “goes black”. | Сжимает причинную связь зрения в ясный визуальный вывод, не повторяя фразу диктора дословно. |
| S05 | “No sound reaches you, either. Sound needs vibrations moving through air.” | **NO MOTION. NO SIGNAL.** | Появление: “Sound needs” → убрать после “through air”. | Бумажная волна обрывается; акцент даёт короткую связку «нет движения — сигнал не доходит». |
| S06 | “But the air has frozen too.” | — | — | Нужна короткая пауза на новой угрозе. Следствие прозвучит и развернётся в следующих сценах. |
| S07 | “You can’t push through it.” | **AIR BECOMES A WALL** | Появление: “push through” → убрать после “it”. | Метафора переводит невидимое препятствие в читаемый образ; её поддерживают неподвижные частицы у обуви. |
| S08 | “You can’t draw it into your lungs.” | **THE TRAP IS ALL AROUND YOU** | Появление: “draw it into your lungs” → убрать после “lungs”. | Расширяет частную проблему дыхания до ловушки, окружающей героя; не дублирует формулировку о лёгких. |
| S09 | “You can’t even move the drop in front of your face.” | **OUT OF REACH** | Появление: “move the drop” → убрать после “in front of your face”. | Короткий вывод о недоступности капли; возвращает внимание к исходному предмету без повтора “can’t move”. |
| S10 | “Like an insect caught in amber, you’re stuck.” | — | — | Сама бумажная янтарная миниатюра показывает сравнение. Дополнительная надпись станет вторым объяснением той же метафоры. |
| S11 | “Five seconds of darkness, silence, and no way out.” | **FIVE SECONDS YOU CAN’T USE** | Появление: “Five seconds” → убрать после “no way out”. | Переводит три ограничения в цену хука: эти секунды нельзя потратить на действие. |
| S12 | “Then time starts again. The drop falls.” | — | — | Падение капли — визуальный ответ и смена состояния; не закрывать предметный возврат текстом. |
| S13 | “So, what did you do with your five seconds? Nothing.” | **NOTHING TO SHOW FOR IT** | Появление: после spoken “Nothing” → конец этой мысли. | Даёт короткое комическое послевкусие к ответу, не повторяя одно слово титром. |
| S14 | “You just became five seconds older.” | **FIVE SECONDS. ZERO PAYOFF.** | Появление: “five seconds older” → конец фразы. | Финальный авторский вывод: вместо суперсилы — нулевая польза. Держать после того, как диктор произнесёт punchline, не выдавать заранее. |

## Статус подготовки и проверки PNG

1. Alignment проверен на полное точное совпадение 667 символов с narration v02; trigger/end, кадры и anchors записаны в cue sheet.
2. Восемь PNG изготовлены по принятому тексту и typography references; exact wording, alpha, единая оптическая высота 90 px и восемь статических композитов на реальных сценах просмотрены автором.
3. Локальный review-preview v05 собран с прямыми cuts, непрерывной voice v02, текстовыми акцентами и film grain: [MP4](../Edit/Previews/Paper_Detour_033_time_stop_EN_mix_preview_v05.mp4). В v05 удалена ошибочно добавленная тишина после “Nothing.”; повторный TTS не выполнялся.
4. Произношение, темп и паузы, точный sync при полном просмотре на 1× и independent review ещё не проверены.
Утверждение текста не заменяет фактическую проверку произношения, alignment и playback. Отдельное разрешение пользователя на один TTS-запрос в ElevenLabs зафиксировано в текущей сессии 2026-11-02; оно не разрешает музыку/SFX или повторные запросы.
