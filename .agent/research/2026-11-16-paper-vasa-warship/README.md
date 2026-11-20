EDITORIAL_CANDIDATE_UNREGISTERED

# Paper Detour — Vasa: twenty minutes afloat, 333 years underwater

**Логлайн:** В 1628 году шведский военный корабль затонул на глазах у Стокгольма за двадцать минут: испытание на устойчивость заранее показало проблему, но судно всё же вышло. Спустя 333 года корабль извлекли практически целиком, вместе с тысячами вещей экипажа.

| Редакция одной истории | Полный русский | Full English production narration | EN words | Авторская классификация |
|---|---|---|---:|---|
| 2 мин, candidate Short | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | 276 | STRONG_CANDIDATE |
| **5 мин, Long** | **[RU](variants/05m/script.ru.txt)** | **[EN](variants/05m/script.en.txt)** | **807** | **STRONG_CANDIDATE — рекомендована** |
| 10 мин, Long | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | 1675 | Переработана 20.11; independent UNVERIFIED |

**Почему 05m:** после предупреждения на берегу есть две различные проблемы: внезапный крен/затопление в 1628 году и технический риск подъёма сохранившегося деревянного корпуса в 1956–1961 годах. 02m даёт полный, но сжатый результат; 10m теперь содержит новые причинные события: действия выживших, безнаказанное расследование, отказ от взрывного разбора судов, исправление района поиска и угрозу разрушения уже поднятого корпуса. Риск замедления переместился к эпилогу о консервации. Длина — редакционная цель, не TTS-measured duration.

[Research: первоисточники, конкурирующие темы, реальные публичные YouTube-сигналы](research.md) · [Story review: восемь критериев для каждой точной редакции, SHA-256, ограничения](story-review.md) · [Packaging для 05m](packaging-brief.md) · [Handoff](handoff.md).

**Authority / status.** Этот пакет — Git-only редакционная очередь, не реальный `uv run ytv start`; отсутствуют actual run/lease/plan_summary/read_next/task_guide/pinned reference_documents, независимый first-listener, approval, script gate, TTS, media, AV seam и measured duration. Официальный script gate **UNVERIFIED**. Не создавать три production run; только выбранный владельцем точный master может быть импортирован по действующему workflow.

**Base:** повторно проверенный перед записью remote `main` `3bd47ae64c6eee627e2822f5986e64d386c855ce`. [PR #124](https://github.com/kleksar/ytvideos/pull/124) **merged** в текущий `main`; его исходная предложенная редакция `7d6bdf7702a2a241a33a21677fce29f26ada9b72` стала каноническим правилом длительностей через merge-коммит. Старые pinned runs не обновляются автоматически и требуют отдельной migration. Общие docs/skills/channel config не менялись; никакого merge/production/upload/schedule.

## Продолжение ревизии 2026-11-20

Baseline HEAD `c5a921426897c17c2c7b890db89736f1873b05c0`; изменена только редакция 10m EN `2eaa4e6c2840bcebe4a5f7feebe4564e51f343cc0b0d3b84caba505fdde66124` / RU `7f4bbad366149a6e26db3aa0ca21d1343537e1a53237098968f5e49c16d467e4` (SHA-256). 02m/05m и packaging для рекомендуемой 05m сохранены. Три текста → проверка автором → 05m рекомендована; independent reviewer, runtime, TTS, owner approval UNVERIFIED. Точное было→стало, story map и факты: [story-review](story-review.md), [research](research.md). Новая 10m требует новой раскадровки/спанов по точному hash, старые не переносить.
