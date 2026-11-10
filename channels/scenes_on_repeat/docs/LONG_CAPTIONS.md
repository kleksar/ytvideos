# Screen captions длинного формата

Для long Scenes on Repeat: English word highlighting, Avenir Next Bold; обычные слова `#F9EED6`, текущее `#FF302A`, тёмная outline. Размер/положение постоянны при highlight, ширина/безопасная область выбраны под конкретный wide canvas и проверены.

[long_captions.py](../automation/pipeline/long_captions.py) применяет общий semantic grouping/render helper к actual final word map. Передавать границы сегментов, чтобы слова не перетекали на карточки или соседние фильмы. Группировка сохраняет exact speech, sentence/syntax и measured width; неоднозначности проверяются по всей последовательности.

Слуховой sync и отдельный SRT — [audio](../../../docs/standards/audio.md). На exact MP4 проверить слова, смены групп, contrast/placement и реальную речь. Автоматические тайминги сами по себе не проходят художественный/слуховой QA.
