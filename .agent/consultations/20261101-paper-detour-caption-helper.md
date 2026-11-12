# Paper Detour: контракт универсального helper титров

Дата: 2026-11-01. Личная консультация координатора в Google Chrome. Видимая маркировка перед отправкой: `Extra High`.
URL: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae79ed9-c81c-83eb-ba08-507600384bb2

Узкий запрос: проверить минимальные входы/выходы и границы извлечения renderer из028 в переиспользуемый CLI. Переданы реальные функции rasterize/face-alpha metrics/common optical height/proportional fit/scene composite, provisional статус SFNSRounded Black и отсутствие полного принятого font/atlas. Предложены manifest, existingPNG или explicit font+texture, реальные scene paths, anchors, ограничения, новые outputdir и отсутствие Palmier/audio/network. Код/новую систему/файлы консультанту не поручали.

## Завершённый ответ — проверенная сводка

1. Два backend: existingPNG без перерисовки и fontTexture с явно заданными шрифтом/текстурой/reference/статусом. Нет fallback на provisional SFNS. PNG-эталоны отдельных фраз не доказывают принятие целого шрифта.
2. Manifest: уникальные cueID, точные строки, backend, canvas, primary/alternate anchors, sceneIDs/реальные paths, maxWidth/maxHeight, внешние timing/provenance. Проверять входы, не угадывать пропуски.
3. Сохранить раздельные face/alpha bounds, пропорциональный fit и общую optical face height по самому ограничивающему cue. Не ужимать длинные титры независимо и не искажать буквы.
4. Все требуемые пары scene×cue получают actual preview, anchor, координаты, face/alpha metrics и scale. Смысловые коллизии автоматически не объявлять отсутствующими.
5. Новый outputdir, источники только читаются; входные hash, параметры и версия helper обеспечивают воспроизводимость.
6. Только файлы, rasterize/reuse, геометрия, composites, previews, отчёт. Не timeline, motion, audio, alignment, SRT, публикация или редакционное принятие.
7. Техническая проверка отдельно от визуальной/синхронизации; непроверенное UNVERIFIED. Успешный provisional PNG не утверждает шрифт или стиль.

Все7 пунктов прочитаны. Приняты границы и проверяемость. Новые enum APPROVED/TECHNICAL_PASS не вводим: входной provenance хранит статус/автора принятия ресурса; проверки используют canonical PASS/FAIL/UNVERIFIED/N_A, скрипт не повышает принятие. Проверка визуального результата может выполняться доступным компетентным reviewer; обязательный новый человеческий approval после каждого запуска не вводится. Matrix означает все реально назначенные scene×cue пары, а не бессмысленное декартово произведение всех сцен и всех фраз фильма. Одновременно обновлять timeline/helper не поручалось.
