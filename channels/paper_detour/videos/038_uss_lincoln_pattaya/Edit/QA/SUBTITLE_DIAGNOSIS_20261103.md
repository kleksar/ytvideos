# Subtitle diagnosis — study only

User scope: investigate current Paper038 subtitle style/word highlighting; preserve timeline, media and production rules without fixes.

## Verified evidence

- Final: `Deliverables/Paper038_EN_v07_review_v01.mp4`, SHA256 `c59daf1a061cfbde611c6bcd976bcc0ef5f02f23356d4d07282442ca7ffe6661`.
- Live Palmier project `020961F2`, timeline `99F5966C`, caption group `915A15C7`: delivery `word`, effect `none`, highlight `karaoke`. Retained contact sheet 01 shows cumulative yellow words.
- Current appearance: Chalkboard SE Bold, native size 48, cream `#F4E8C8`, yellow `#FFD166`, dark outline approximately `#18243A`, width 3, transform x=.5/y=.762. User likes the appearance; no standard changed in this investigation.
- Imported `Source/Subtitles/shorts_en_v06.srt` contains phrase intervals. Native caption clips contain phrase start/duration and animation settings, without per-word timing fields. `Work/paper038-review-v03/forced_word_map_v01.json` retains separate automatic alignment, still REVIEW_REQUIRED.
- Canonical subtitle skill already requires only the spoken word yellow. Local `shorts_subtitles.py` calls its output karaoke but renders exclusive `j == k` coloring and switches at word starts. Native mode equivalence was not validated.
- Final `review.json` required metadata, decode and frame sampling only; cue_timing remained UNVERIFIED. Readability sampling did not enforce the single-active-word invariant.

## Extra High consultation

Visible model marker immediately before submission: `Extra High`.
URL: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae9ae33-adac-83eb-86bd-4ec45428ae91
Completed response visibly received; this consultation is diagnostic advice, not independent primary evidence.

Prompt: Одна узкая диагностическая задача; ответь здесь, без рекурсивной консультации, до 150 слов. Для Shorts стандарт требует: только текущее произносимое слово желтое, предыдущие и будущие кремовые. В финальном Palmier текст имеет delivery=word, effect=none, highlight=karaoke. На кадрах подсветка накапливается: сначала Five желтое, затем Five и thousand оба желтые. Импортирован SRT с таймингами целых фраз. Отдельная точная word_map осталась внешним файлом; в native caption-клипах только start/duration фразы, полей word timing нет. Старый локальный helper называл результат karaoke, но его код красил лишь j==k и переключал по start следующего слова. QA проверял metadata/decode/выборку кадров на читабельность, cue_timing остался UNVERIFIED. Раздели подтвержденную причину накопления цвета, потерю информации о синхронизации и пробел QA. Не утверждай неизвестный внутренний алгоритм Palmier. Не изменяй сценарий, документацию или монтаж.

Completed answer:

1. Причина накопления цвета — подтверждённый симптом. Финальный MP4 нарушает инвариант: жёлтым должно быть только текущее произносимое слово. Наблюдается накопление (Five → Five thousand). Значит, фактический результат highlight=karaoke не соответствует стандарту. Точный внутренний алгоритм Palmier неизвестен. Название эффекта и старого helper не доказывают одинаковую семантику. Helper реализовывал эксклюзивную подсветку j == k, а не накопительную.
2. Потеря синхронизации. SRT содержит только интервалы фраз. В native caption-клипах отсутствуют временные границы отдельных слов. Внешний word_map не перенесён в монтажную структуру. Следовательно, точная пословная синхронизация не обеспечена входными данными caption-клипов.
3. Пробел QA. Проверки metadata/decode подтверждают техническую корректность файла, но не семантику подсветки. Выборочная проверка читаемости не проверяет последовательность состояний каждого слова. cue_timing=UNVERIFIED означает, что синхронизация не подтверждена. Диагноз: наблюдаемое накопление цвета, отсутствие word timing в native captions и неполное покрытие QA — три отдельных дефекта.

Accepted diagnosis: native highlight implementation did not preserve the existing exclusive-word behavior; phrase-only import did not carry alignment; QA did not close either check. No claim about Palmier's internal timing interpolation. Changing highlight mode alone is not established as a complete remedy.

No timeline, render, script or canonical procedure was modified. Only this compact diagnostic record was added.
