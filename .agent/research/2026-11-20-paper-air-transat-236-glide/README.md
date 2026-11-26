EDITORIAL_CANDIDATE_UNREGISTERED

# Paper Detour — The Plane Ran Out of Fuel. Then It Had to Lose Height.

**RU логлайн:** В августе 2001 года пассажирский Airbus с 306 людьми потерял оба двигателя над Атлантикой. Пока экипаж пытался выровнять топливо между баками, оно уходило через треснувшую трубку. Без тяги самолёт спланировал к Азорским островам; расследование объяснило, почему попытка исправить показания увеличила утечку.

**Формат:** Paper Detour, English documentary **Long 16:9**; RU — полный смысловой перевод. Версии — редакционные альтернативы, не три production runs. Ни одна не получила официального script approval.

| Версия | Full English | Полный русский | Оценка редактора | Production |
|---|---|---|---|---|
| 2m | [EN](https://github.com/kleksar/ytvideos/blob/story/paper-air-transat-236-glide-20261120/.agent/research/2026-11-20-paper-air-transat-236-glide/variants/02m/script.en.txt) | [RU](https://github.com/kleksar/ytvideos/blob/story/paper-air-transat-236-glide-20261120/.agent/research/2026-11-20-paper-air-transat-236-glide/variants/02m/script.ru.txt) | STRONG_CANDIDATE | Long 16:9; duration estimated |
| **5m** | **[EN](https://github.com/kleksar/ytvideos/blob/story/paper-air-transat-236-glide-20261120/.agent/research/2026-11-20-paper-air-transat-236-glide/variants/05m/script.en.txt)** | **[RU](https://github.com/kleksar/ytvideos/blob/story/paper-air-transat-236-glide-20261120/.agent/research/2026-11-20-paper-air-transat-236-glide/variants/05m/script.ru.txt)** | **STRONG_CANDIDATE — RECOMMENDED** | Long 16:9; duration estimated |
| 10m | [EN](https://github.com/kleksar/ytvideos/blob/story/paper-air-transat-236-glide-20261120/.agent/research/2026-11-20-paper-air-transat-236-glide/variants/10m/script.en.txt) | [RU](https://github.com/kleksar/ytvideos/blob/story/paper-air-transat-236-glide-20261120/.agent/research/2026-11-20-paper-air-transat-236-glide/variants/10m/script.ru.txt) | REWORK | Long 16:9; duration estimated |

**Рекомендация:** 5 минут. Её действие развивается от странных показаний масла через ошибку в балансировке и поворот на Азоры к планированию, сложной посадке и двойному вердикту расследования. В 2m сокращён механизм ранних предупреждений. 10m завершена, но новые технические блоки замедляют путь к посадке.

**Достоверность:** первичный расследовательский отчёт GPIAA (Portugal, 18 октября 2004; FAA hosting): https://www.faa.gov/sites/faa.gov/files/2022-11/AirTransat236_AccidentReport.pdf ; Air Transat, background factual summary: https://www.transat.com/getmedia/583479f2-7f91-425a-b0c0-601c0fc11409/Emergency-landing-of-Air-Transat-Flight-TS-236-on-August-24%2C-2001.pdf . Источники и границы — research.md; контрсигналы и 8 критериев — story-review.md. Видео/комментарии и сопоставимый baseline не просматривались в плеере; CTR/retention UNVERIFIED.

**Capability blocker:** `UV_OFFLINE=1 uv run ytv start --channel paper_detour --format long ...` → `Failed to spawn: ytv; No such file or directory (os error 2)`. `sessions.independent`: инструменты создания независимой модельной сессии не обнаружены в доступном registry, review UNVERIFIED. **Не** было run/lease/receipt/owner approval/script gate, TTS, изображений, MP4, upload или публикации.

**Дальше:** перенести неизменные UTF-8 версии и evidence в настоящий локальный checkout, сначала `uv sync`, затем `uv run ytv start --channel paper_detour --format long --intent 'Paper Detour Air Transat 236; editorial PR provenance'`; прочитать `plan_summary/read_next/task_guide/pinned reference_documents`, прикрепить варианты как supporting artifacts по task contract, провести независимый review точных sha256; предложить один 05m master на обычный script gate. Не подменять старые pins.
