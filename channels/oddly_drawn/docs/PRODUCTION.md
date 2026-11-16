# Oddly Drawn — граница исполнения

[ChannelSpec](../../two_ways_lab/channel.json) остаётся под ключом `two_ways_lab`. `illustrated` используется как общий narration/storyboard/image task graph. Новая ветка workflow с именем канала и второй автоматизированный канал не нужны. `active` разрешает новый сохранённый run для research/script; `profiles` не объявляет конфигурацию готовой к медиа.

| Область | Подтверждено | Не определено / что блокируется |
|---|---|---|
| Редактура | Человек рассказывает через рисунки; English; детектив и A/B необязательны | Для новой истории нужен обычный run, research и exact script gate |
| Визуальный вход | [Пустая доска и provenance](../brand/PROVENANCE.md) | Это reference 1672×941, не video master; actual files нужны для приёмки |
| Whiteboard исполнение | Художественное направление и общий illustrated graph | Метод изменения рисунков, provider/model/settings, assets/rights и recipe; не вызывать внешние providers по старым defaults |
| Рассказчик | Человек, который рисует | Model sheet, если человек видим; старый герой не используется по умолчанию |
| Звук | Narration предусмотрена общей схемой | Voice/provider/model/settings, конечная скорость и музыка не перенесены со старого бренда |
| Delivery | Общие codec/QA safeguards остаются | Canvas/fps Short и long, montage, титры/font/геометрия; landscape reference сам не активирует long |
| Внешние действия | Сохранён тот же YouTube ID; [read-only evidence](IDENTITY.md) | Handle и текущие permissions не проверены; календарь по прежней политике требует фактической сверки |

Unresolved поля `production` дают штатный `production requirements unresolved` до media dispatch и при сдаче storyboard/render. `visual_profile: null` и незаданный voice запрещают legacy helpers молча применять старые presets. `release_policy.ab_test: false` снимает автоматическое требование thumbnail A/B для будущих выпусков; это не отключает тесты на внешнем YouTube. Остальные release safeguards и календарная политика сохранены.

Нужные следующие входы — подтверждённый whiteboard recipe с точными допустимыми tools/параметрами, delivery по выбранному формату, voice/speed и caption settings. Их добавляют отдельным проверяемым maintenance-изменением по [development](../../../docs/development.md), затем проверяют doctor и actual assets/providers. Подмена null выдуманными значениями ради прохождения checks запрещена. Независимые research/script задачи доступны; media readiness и реальный выпуск пока UNVERIFIED.

Existing run использует pinned profile/references и прежний checkout. [Runtime migration](../../../docs/migration.md#миграция-runtime-сохранённого-run) сохраняет профиль: ею нельзя незаметно превратить прежний выпуск в Oddly Drawn. Ни данный PR, ни прочитанные инструкции не мигрируют старые runs и не дают нового production/upload/publication approval.
