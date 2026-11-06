# END_SCREEN_PLAN — <episode / version>

Заполнить по [стандарту Paper](paper-end-screens.md) или [Nuviko History](nuviko-end-screens.md); в выпуске заменить относительную ссылку на реальный путь к нему. Шаблон не является проверенной конфигурацией.

- Channel ID / canonical episode:
- Язык / формат / применимость: `REQUIRED_NEW_LONG | NOT_APPLICABLE_SHORT | NOT_APPLICABLE_POST | EXEMPT_EXISTING`.
- Основание scope / решения / принявший:
- Сценарий и последняя смысловая реплика / время её окончания:
- Saved project / timeline / edit version:
- Финальный MP4, SHA-256 / uploaded video ID (до загрузки `NOT_ASSIGNED`):
- Холст / FPS / end frame exclusive / фактическая длительность:
- Хвост `[start_frame, end_frame)` и соответствующие секунды:
- Финальная композиция / PNG / hash / интервал (10 секунд):
- Геометрия резервов / protected areas / допустимое движение:
- Реальный звук хвоста / разрешение audio owner либо тишина:
- Субтитры фактической речи / время последней группы:

| Элемент | Точная цель | Почему подходит | Public/channel/long проверены когда и чем | Интервал / позиция |
|---|---|---|---|---|
| Subscribe | Собственный channel ID | Подписка на целевой канал | | |
| Video 1 | video ID или `UNRESOLVED` до отбора | | | |
| Video 2 | video ID или причина отсутствия | | | |

- `background_qa=PLANNED | PASS | FAIL | UNVERIFIED`: принятая edit-версия, начало/середина/конец хвоста, геометрия, фактическое покрытие и ссылка на приёмку MP4.
- `native_end_screen=NOT_CONFIGURED | SAVED_VERIFIED | UNVERIFIED | NOT_APPLICABLE`: точная причина, если исключение.
- API capability check / дата / Studio selected channel / ограничения функции:
- Saved Studio read-back: число/типы, цели, интервалы, геометрия; пути скриншотов и время:
- `public_render_and_links=NOT_CHECKED | VERIFIED | UNVERIFIED | NOT_APPLICABLE`: фактический просмотр/переходы и ограничения; не наследовать из saved read-back.
- Сохранность исходного доступа/расписания и других полей:
- Открытые зависимости / следующий шаг / текущий указатель выпуска:
