---
name: ytv-review-video
description: "Review the exact ytvideos MP4, cold opening, payoff and Shorts loop; record checks and repair defects. When packaging is ready, check its card, tone and first confirmation before presenting the MP4."
---

# Проверить и представить MP4

Прочитать context `review`: `task_guide`, `production_requirements`, выбранные документы, профиль/рецепт и уже выполненные checks. Открыть точный MP4 из `inputs` и принятые script/audio/storyboard из `supporting_inputs`. Проверять hash и фактическое содержание; критерии — [delivery](../../../docs/standards/delivery.md) и [editorial](../../../docs/standards/editorial.md).

1. Проверить decode/streams/каденцию/геометрию/цвет/аудио, каждую сцену, склейки, движение, титры и применимый end screen.
2. Для любого формата проверить, что монтаж сохранил развитие, кульминацию и развязку принятого текста по [editorial](../../../docs/standards/editorial.md#драматургия-для-всех-каналов); не исправлять сюжет самовольно. Для Short проверить холодное начало, отдачу до повтора и воспроизвести последние → первые секунды по [delivery](../../../docs/standards/delivery.md#петля-shorts-проверка-точного-mp4). Зафиксировать timecodes/hash, смысл, речь, музыку и subtitle seam. Раздельно отметить измерения, просмотр кадров, прослушивание и player playback: contact sheet/word map не доказывают AV sync всего ролика.
3. Связать каждую проверку с hash, методом, coverage, reviewer и evidence. Если упаковка готова, сверить полную карточку, тон, первое подтверждение и payoff по [thumbnail QA](../../../docs/standards/thumbnails.md#qa-файла-и-пары); сохранить timecodes MP4. Позднюю упаковку проверяет release. Невыполненное — `UNVERIFIED`, неприменимость требует причины; self-review не является independent review.
4. Исправить подтверждённые дефекты с сохранением остальных inputs/cache, повторить затронутые checks и получить новый exact MP4. После устранения конкретного риска не расширять проверки без причины.
5. Сохранить receipt и показать готовый файл. Приложить готовую упаковку, если она есть; не удерживать MP4 ради неё. Запросить одобрение точного файла.

Локальный координатор регистрирует явное решение владельца по [контракту](../../../docs/operations/task-contract.md#approval-и-продолжение), связывая его с показанными revision/hash MP4. Ключи/hooks не требуются. Reviewer не принимает своё видео и не выдумывает согласие. После принятия MP4 продолжить `next` в разрешённом scope; upload и публикация требуют прямого поручения на выпуск по [workflow](../../../docs/workflow.md).
