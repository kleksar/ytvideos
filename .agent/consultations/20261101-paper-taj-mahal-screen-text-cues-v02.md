# Paper Taj Mahal screen-text cues v02

- **Task:** a separate seven-cue wording pass for accepted narration RU v07 and storyboard RU v01.
- **Visible model label immediately before submission:** `Extra High`.
- **Conversation:** https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae788be-7ef0-83ed-9921-889914af93ef
- **Project rules consulted:** [Paper Editorial Cue Standard](../../new_channel/docs/PAPER_EDITORIAL_CUE_STANDARD.md), [Typography Standard](../../new_channel/brand/TYPOGRAPHY_STANDARD.md), and [ytv-paper-storyboard skill](../../.agents/skills/ytv-paper-storyboard/SKILL.md).
- **Result:** seven provisional accents, four meaningful silent scenes, correct reveal order, no claimed timing or collision pass. Integrated into [STORYBOARD_RU_v01.md](../../new_channel/videos/028_taj_mahal/Storyboard/STORYBOARD_RU_v01.md). No images, PNGs, or audio generated.

## Prompt submitted

> Ты — консультант в проекте YT Видео. Это отдельная узкая редакционная задача после сохранённой композиционной раскадровки: подбери партитуру коротких текстовых акцентов к финальному тексту и 11 сценам. Не переписывай озвучку и кадры, не создавай PNG/изображения и не назначай монтажные позиции.
>
> Принятая озвучка RU v07:
> «Конечно. У меня хорошо получается.
> Именно за этот ответ король приказал отрубить Ахмаду руки.
> До этого Ахмад по приказу короля руководил строительством Тадж-Махала. Стройка длилась двадцать два года; он продумывал каждую мелочь.
> Когда здание было готово, король похвалил Ахмада за великолепную работу. Но не хотел, чтобы кто-то построил что-то подобное.
> В тот же день рук лишились и Ахмад, и его помощники.
> Король сделал так, чтобы взяться за следующую работу было нечем.
> Так что в следующий раз, когда захочется слишком хорошо выполнить свою работу, вспомните Ахмада.
> Король спросил:
> — Ахмад, ты будешь дальше работать архитектором?»
>
> Порядок кадров: S01 — ответ Ахмада через плечо короля; S02 — приказ короля; S03 — общий план стройки; S04 — Ахмад проверяет мелкую деталь модели, за ним леса и недостроенный купол; S05 — завершённый Тадж-Махал и похвала; S06 — король в тёмном проёме смотрит на здание, Ахмад далеко; S07 — Ахмад и помощники с пустыми рукавами, неграфическая символическая сцена; S08 — Ахмад у стола с инструментами, которыми больше не может пользоваться; S09 — крупный план тщательно собранной бумажной модели; S10 — маленькая фигура Ахмада с пустыми рукавами перед огромным зданием; S11 — обратный план, король задаёт вопрос Ахмаду. Петля S11→S01: тот же дворец, ось, взгляды и позиции; вопрос сразу получает ответ.
>
> Стандарт проекта: акцент — короткая смысловая фраза, обычно 2–5 содержательных слов, а не полный повтор диктора и не постоянные субтитры. Реплики-повороты можно выводить дословно. Каждый текст появляется только когда произнесён смысловой trigger, держится до конца выделяемой фразы и не раскрывает последующее раньше времени. Бумажные глифы сверять по реальным PNG-эталонам проекта; название шрифта неизвестно, его не выдумывать.
>
> Учти стандарт входа и выхода именно для текстового слоя поверх статичных диорам: видимый центр текста x=0.50; одна постоянная безопасная позиция чтения, высота видимых букв около 0.055 высоты кадра на строку. Короткий вертикальный вход: центр y=0.20, opacity 0 → y=0.18, opacity 1; удержание неподвижно на anchor; чистый выход вверх: y=0.16, opacity 0. При 30 fps относительные ключи проекта: 0, 4, D−5, D−1. Буквы не движутся по отдельности, не пересекают предметы, в hold не скачут. Сам кадр/персонажи остаются статичными, смены сцен — прямые склейки.
>
> Предложи ровно 7 действительно нужных акцентов на протяжении выпуска и таблицу: ID сцены | точная надпись (2–5 слов) | дословный spoken trigger | последнее слово/граница смысла для удержания | смысловая работа фразы | как и где она читается с учётом сцены | потенциальное столкновение, которое надо проверить на реальной картинке. Обязательно сохрани вопрос и ответ как два разных конца петли, не превращай их в повторяющиеся заголовки. Пропуски между cue объясни: они должны быть осмысленными тихими интервалами, не дырой в рассказе. После таблицы прочитай весь ряд надписей подряд и коротко проверь, не спойлерит ли он и не повторяет ли диктора целиком.
>
> Таймкоды, номер кадра появления/исчезновения, статус синхронизации и pass по collision сейчас не выдумывай: фактической записи, word-alignment и готовых кадров/PNG ещё нет. Для каждого cue укажи, что точное время и collision-check остаются ожидаемыми. Это предварительная партитура фраз, которую потом нужно выровнять по записанной озвучке и проверить на реальных композициях.

## Result returned

The consultant specified these seven provisional accents and noted that collision checks and alignment are pending actual scenes, PNGs, a recording, and word alignment:

| Scene | Text | Spoken trigger → hold through | Placement / collision to verify |
|---|---|---|---|
| S01 | `Конечно. У меня хорошо получается.` | `«Конечно.»` → `«получается.»` | Two lines above Ahmad, upper centre; check arch and his head. |
| S02 | `Цена одного ответа` | `«Именно за этот ответ»` → `«руки.»` | Upper centre over the space between king and Ahmad; check the king's raised hand and architectural detail. |
| S04 | `22 года точности` | `«двадцать два года»` → `«мелочь.»` | Upper centre above the work area; check the dome and scaffolding. |
| S06 | `Никакого повторения` | `«чтобы кто-то построил»` → `«подобное.»` | Upper centre inside the dark arch; check contrast and arch contour. |
| S08 | `Работа вне досягаемости` | `«взяться за следующую работу»` → `«нечем.»` | Upper centre above Ahmad and table; check tools and empty sleeves. |
| S10 | `За зданием — человек` | `«слишком хорошо выполнить свою работу»` → `«Ахмада.»` | Upper centre against the building; do not cover the Taj Mahal dome. |
| S11 | `Ты будешь дальше работать архитектором?` | `«ты будешь»` → `«архитектором?»` | Two lines above king; check arches, raised hand, and headroom. Remove before S11→S01. |

Silent frames: S03 establishes the construction scale; S05 lets the architecture and praise gesture carry the triumph, strengthening the next contrast; S07 gives the empty sleeves and lowered heads the entire emotional focus; S09 lets the model's craft read before the creator/building comparison in S10.

Sequence check from the consultation: **Конечно. У меня хорошо получается. → Цена одного ответа → 22 года точности → Никакого повторения → Работа вне досягаемости → За зданием — человек → Ты будешь дальше работать архитектором?** Only the loop's short answer and question quote the narration directly; the other five are editorial condensations. The order does not reveal helpers or punishment before the matching spoken lines.

## Editorial adjustment

I changed only the S10 wording from `За зданием — человек` to `За шедевром — человек`. The earlier line can read as a literal spatial statement. The revised line more directly moves attention from the impressive building to its maker and remains within the accepted narration's description of the work as magnificent. This wording remains a draft until the user accepts the storyboard.
