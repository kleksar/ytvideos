# Subtitle sync prevention — 2 November 2026

Visible mode: `Extra High`; coordinator personally used Chrome. [Project conversation](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0/c/6ae832dc-98ac-83eb-8b16-53a451b402c9).

Task: refine prevention of subtitle lag after the Minnie incident. User accepted the corrected review and asked how to avoid recurrence. Initial narrow request returned “Не удалось загрузить этот ответ”; one short retry produced a completed substantive response.

Retry prompt: «Короткий повтор: дай сам текст до 80 слов — какие 3 уточнения добавить в правило проверки синхронизации субтитров по точной записи до рендера и по финальному MP4 после, чтобы отличать постоянный сдвиг, дрейф и локальные ошибки? Не назначай универсальный сдвиг и не выдавай ASR за слуховую проверку.»

Visible response: «1. Привязка к источнику. Фиксировать SHA-256 точного аудио, версию монтажа и карту пословных таймингов. Изменение записи инвалидирует разметку. 2. Диагностика до рендера. Вручную сопоставлять начала слов с аудио в начале, середине, конце и при смене темпа. Постоянная разница — offset, нарастающая — дрейф, отдельные отклонения — локальные ошибки. ASR только вспомогательный инструмент. 3. Проверка после рендера. Прослушивать финальный MP4 с видимой подсветкой, проверять проблемные участки и границы фраз. При ошибках исправлять карту адресно, без универсального сдвига.»

Applied through canonical timing owner `ytv-srt`, linked by Paper subtitles and Shorts helper reference. Qualification: tempo variations in normal speech are not proof of edit speed changes; investigate timebase/conform before assigning drift cause. Preserve Paper offline QA policy and separate actual listening from machine evidence; no requirement to open a prohibited player. Early samples diagnose problems, not full-track acceptance. No fixed offset, model mandate or new audio authorization introduced.
