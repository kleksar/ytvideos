# Приёмка финального MP4

- Task ID `ytv-final-mp4-acceptance-rule`
- Source https://chatgpt.com/c/6aecc5ba-45fc-83ed-840e-424563eaebae
- Google Chrome, visible model `GPT-6`, effort `Extra High`
- Exact [prompt](2026-11-05-final-mp4-acceptance-prompt.txt). Initial composer empty under lock. Exact posted text and empty composer verified before releasing the lock. The completed answer was recovered through the visible reload-answer control and transcribed from its complete rendered accessibility text.

## Response

### Правило приёмки перед выпуском

**Одно подтверждение — один финальный MP4.**

Команда проводит внутренний QA до передачи владельцу. Подтверждение владельца «ролик хороший» после просмотра финального MP4 означает приёмку изображения, звука, монтажа и вшитых субтитров именно этой версии файла. Повторное подтверждение этих компонентов не требуется.

**Отдельный SRT не входит в эту приёмку**, поскольку не отображается при просмотре MP4. Его готовность подтверждается отдельно командой: соответствие финальному тексту, язык, тайминги, формат и успешная загрузка дорожки.

В журнале фиксируются:

- SHA-256 принятого MP4, подтверждение владельца и дата.
- Результаты внутреннего QA с указанием способа проверки.
- Результаты проверки SRT отдельно от приёмки MP4.

Автоматическая проверка не записывается как прослушивание. Подтверждение владельца не распространяется на непроверенные артефакты.

**Повторная приёмка требуется только при существенном изменении принятого видео.** Исправление отдельной SRT-дорожки не требует повторного просмотра неизменённого MP4.

### Спорный случай

После приёмки MP4 автоматическая проверка обнаружила предполагаемое расхождение тайминга вшитых субтитров на 300 мс.

Решение: предупреждение фиксируется, но само по себе не отменяет приёмку. Если подтверждён существенный дефект, выпуск блокируется до исправления; изменённый MP4 требует новой приёмки. Если дефект не подтверждён, повторный PASS владельца не нужен.

## Proposal for the project

One owner approval of the exact delivered final MP4 covers its picture, sound and burned-in captions, including perceived sync. Record the same approval as evidence for acceptance and playback coverage. Preserve the existing hash-bound rule for a replacement file, internal QA and separate SRT verification. A confirmed material defect still requires correction. The user requested discussion of the proposed wording.
