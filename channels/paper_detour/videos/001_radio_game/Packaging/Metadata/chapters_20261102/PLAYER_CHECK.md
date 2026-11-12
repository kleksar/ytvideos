# Проверка плеера — 2 ноября 2026

Координатор открыл https://www.youtube.com/watch?v=0RaC4t7yn5o в Chrome после API-записи, перезагрузил страницу и нажал кнопку текущей главы «A sound worth recording». В панели «В этом видео» → выбранная вкладка «Эпизоды» фактически прочитаны:

| Название | Время | Ссылка плеера |
|---|---|---|
| A sound worth recording | 0:00 | watch?v=0RaC4t7yn5o |
| The Brazilian radio show | 0:32 | t=32s |
| How a cassette carries data | 1:15 | t=75s |
| A program takes the air | 2:00 | t=120s |
| Decoding the recording | 2:43 | t=163s |
| The reported match | 3:21 | t=201s |
| The sound and the message | 3:54 | t=234s |

Плеер показывает 0:00 / 4:20. Это подтверждает распознавание и отображение семи глав YouTube, отдельно от API read-back. Непрерывное воспроизведение и субъективное прослушивание не выполнялись. Фактический текущий заголовок «How People Got Computer Programs From the Radio» сохранён из свежих metadata; этот проход не сочинял его.
