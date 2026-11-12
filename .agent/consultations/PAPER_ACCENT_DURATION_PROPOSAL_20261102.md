# Paper Detour — proposal for accent duration

- Date: 2026-11-02. Stage: propose numeric duration limits; no timeline or canonical rule changes.
- Coordinator: personally consulted in Google Chrome.
- Exact visible model label immediately before submission: `Extra High`.
- URL: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae81044-72b4-83eb-89b4-68261af87ca6
- Inputs: current captions cue-sheet workflow and Palmier accent motion; English 2–5-word selective PNG accents on complex dioramas; 30fps; 4-frame entry/exit; current clips0.67–2.9s. EBU QC1052F supplied as background, not a direct standard for paper accents: https://qc.ebu.io/items/1052F/versions/1-0-0/

## Narrow prompt

Ты — консультант в уже открытом ChatGPT Extra High. Требование внешнего координатора выполнено этим обращением; ответь здесь, не открывай другой ChatGPT. Одна узкая задача: предложи внутренний min/max времени экранных акцентов Paper Detour Shorts. Это отдельные бумажные PNG из 2–5 английских слов поверх сложных цельных диорам и английской речи, не сплошные субтитры. Сцены 4–6 с, 30fps. Вход снизу вверх с opacity4кадра≈0.133с, неподвижный fully opaque hold, выход вверх+fade4кадра. Сейчас клипы0.67–2.9с, технический hold минимум0.333с явно слишком слабый ориентир для чтения. Рассмотри общий диапазон1.2–3.0с с переходами, обычный1.5–2.5с, редкий максимум3.5с для даты/имени/сложного смысла. Дай краткую рекомендацию: границы, интервалы по длине, нужно ли minimum hold и как не рассинхронизировать речь/раскрытие. Не называй эти цифры научно доказанными или гарантией удержания. В качестве фона EBU1052F приводитBBC≈0.3с/слово и подчёркивает редакционную зависимость; это субтитры, не прямой стандарт для акцентов. Ответ до200слов на русском, без поиска.

## Completed visible answer

Рекомендация: общий диапазон 1,2–3,0 с, обычный рабочий диапазон 1,5–2,5 с, исключительный максимум 3,5 с. Все значения включают вход и выход.

| Длина акцента | Общая длительность |
|---|---|
| 2 слова | 1,2–1,5 с |
| 3 слова | 1,4–1,8 с |
| 4 слова | 1,7–2,1 с |
| 5 слов | 2,0–2,5 с |
| Имя, дата, сложный смысл | 2,5–3,5 с |

Минимальный hold:
- Вход: 4 кадра (0,133 с).
- Выход: 4 кадра (0,133 с).
- Fully opaque hold: минимум 0,9 с, предпочтительно от 1,0 с.
- Технические 0,333 с не использовать как редакционный ориентир.

Таким образом, даже короткий акцент получает достаточное время для чтения поверх сложной диорамы.

Синхронизация:
1. Появление привязывать к смысловому spoken trigger, не показывать раньше раскрытия соответствующей мысли.
2. Hold должен покрывать завершение смыслового beat, а не обязательно всю соседнюю реплику.
3. Уходить после того, как зритель успел прочитать акцент, но до следующего смыслового поворота.
4. Не растягивать титр только ради заполнения сцены.

Это редакционные стартовые нормативы, а не научно доказанные пороги или гарантия удержания. Их следует корректировать по фактическому просмотру кадров и готового ролика.

## Coordinator assessment / status

Proposal only, pending discussion with user. Frame convention: D=end-start; keys0,4,D-5,D-1 yield hold(D-9)/30s, so D36=1.2s provides0.9s stationary fully opaque hold. Word count ranges are planning guides, not automatic sufficiency checks; long unfamiliar words and scene complexity also matter. The consultant statement that the minimum is sufficient is not a verified result. Current episode cues and canonical skills remain unchanged.
