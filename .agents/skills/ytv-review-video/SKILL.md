---
name: ytv-review-video
description: "Review the exact ytvideos MP4, cold opening, payoff and Shorts loop; record checks and repair defects. When packaging is ready, check its card, tone and first confirmation before presenting the MP4."
---

# Проверить и представить MP4

Прочитать context `review`, [delivery](../../../docs/standards/delivery.md), [editorial](../../../docs/standards/editorial.md), применимый профиль канала и evidence уже выполненных checks. Проверять exact MP4/hash с теми inputs, из которых он создан.

1. Выполнить необходимые decode/stream/каденция/геометрия/цвет/аудио checks. Проверить первый/последний кадры, каждую сцену, склейки, движение, титры и применимый end screen.
2. Для Short проверить холодное начало, отдачу до повтора и воспроизвести последние → первые секунды точного MP4 по [delivery](../../../docs/standards/delivery.md). Зафиксировать timecodes/hash, смысл, речь, музыку и subtitle seam; текстовый review не заменяет этот просмотр. Проверить реальное изображение и полный звук доступным способом. Отдельно записать измерения, просмотр кадров, фактическое прослушивание и player playback. Автоматическая word map и contact sheet не доказывают AV sync всего ролика.
3. Связать каждую проверку с artifact hash, методом, coverage, reviewer и evidence. Если упаковка уже готова, проверить полную карточку, первый акцент/узнаваемость в уменьшении, ожидаемый жанр, первое подтверждение обещания и отдельный payoff в exact MP4; сохранить наблюдённые timecodes. Это не dependency review и не новый gate; позднюю упаковку сверяет release. Сам thumbnail принимается в image task/release. Локальный helper `automation/helpers/youtube-thumbnails/scripts/thumbnail_previews.py --card-json FILE` собирает mock; порядок — [thumbnail standard](../../../docs/standards/thumbnails.md#локальный-макет-карточки). Manifest/HTML не доказывает просмотр или фактический показ. Невыполненное — UNVERIFIED; неприменимость требует причины. Авторская самопроверка не становится independent review.
4. Исправить подтверждённые дефекты минимально, используя сохранённые inputs. Повторить затронутые checks и получить новый exact MP4. Не наращивать необязательный testing после устранения конкретного риска.
5. Сохранить receipt и представить готовый файл пользователю. Если упаковка уже готова, приложить выбранное название/обложку/описание; не удерживать видео в ожидании пакета. Запросить только одобрение MP4.

Approval поступает от реального пользовательского события через trusted bridge и связывается с hash файла. Не подписывать событие от имени пользователя и не создавать ложное подтверждение. После approval продолжить `next`: завершение релиза по политике не требует нового обычного согласования.
