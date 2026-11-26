EDITORIAL_CANDIDATE_UNREGISTERED

# Paper Detour — The Bank Police Checked but Could Not Open (1971)

**RU логлайн:** Радиолюбитель услышал, как грабители общаются из лондонского банковского хранилища. Полиция обошла сотни банков, дошла и до нужного Lloyds, но запертая дверь выглядела целой; настоящий пролом был в полу. Преступники вскрыли 268 ячеек, а впоследствии их выдал договор аренды магазина, подписанный настоящим именем.

Это **одна** реальная история с тремя завершёнными EN/RU редакциями, а не три разных сюжета. Документальная ретроспектива, не реконструированные записи преступников и не вымышленный секрет королевской семьи. Первое прохождение и оценки — авторские, не independent review.

| Длительность | Полный EN production narration | Полный RU смысловой текст | Редакторский статус и формат |
|---|---|---|---|
| 2 минуты | [Full EN](variants/02m/script.en.txt) | [Полный RU](variants/02m/script.ru.txt) | STRONG_CANDIDATE текста, Short; independent и AV loop **UNVERIFIED** |
| **5 минут** | **[Full EN](variants/05m/script.en.txt)** | **[Полный RU](variants/05m/script.ru.txt)** | **STRONG_CANDIDATE — рекомендована, Long** |
| 10 минут | [Full EN](variants/10m/script.en.txt) | [Полный RU](variants/10m/script.ru.txt) | REWORK по динамике финальной трети, Long |

**Почему пять минут:** в коротком видео остаётся базовый парадокс, а в пятиминутном появляется реальное развитие: замеры зонтом → тоннель под рестораном → провал домкрата и термического резака → взрыв → случайный перехват переговоров → сотни банков → проверка нужной двери без доступа внутрь → находка на следующий день и след по аренде. 10m добавляет последствия для владельцев ячеек, но затягивает сюжет после основной разгадки. Наличие шести файлов **не** означает принятие master или измеренный хронометраж.

[Исследование: 10 историй, 3 сильных конкурента, фактический ledger, YouTube с реальными URL и baseline limits](research.md) · [Оценки всех редакций по 8 критериям, точные SHA-256, отдельные checks](story-review.md) · [Packaging promise/first actions/payoff](packaging-brief.md) · [Handoff / перенос в локальный runtime](handoff.md).

**Source remote main:** `09fa62d02a85f5fdcbfcc73c5acb2dcbe99aa035`; policy #124 **merged** 2026-11-16, только current canonical docs/main. Все файлы создаются в отдельной story-папке. Перед записью ещё раз проверить main и concurrent PR; при изменении main не коммитить от старой базы.

**Production blockers:** `uv run ytv start` в доступной среде не запускается — `Failed to spawn: ytv` / ENOENT, нет локального checkout/entrypoint. В tool registry также отсутствует поддерживаемая независимая session/spawn capability; `sessions.independent` **UNVERIFIED**, не симулировать reviewer. Не получены actual media bytes, TTS durations, licensed references, AV seam, owner script approval или MP4 acceptance. Paper Long-рецепт в ChannelSpec есть, но это не разрешение производства. Конкретные действия переноса в [handoff](handoff.md).

**Draft editorial queue only**: не merge, не TTS, не imagegen, не внешние видеопровайдеры, не рендер, не загрузка, не публикация, не изменение календаря.

