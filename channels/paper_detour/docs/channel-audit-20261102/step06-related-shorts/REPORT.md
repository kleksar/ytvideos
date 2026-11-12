# Paper Detour — переходы Shorts → полный фильм

Проверка: 2 ноября 2026. Канал `UCMVfdfaNxV3ZkI3_J3Eejzw`, `@rarovista`.

**Итог: среди опубликованных роликов пропущенных прямых связей с полными фильмами не обнаружено.** Оба Shorts выпуска 001 уже связаны с его полным фильмом. У остальных 12 открытых Shorts соответствующего полного фильма в опубликованном каталоге Paper нет. Внешние изменения не выполнялись.

## Что проверено

Свежий API подтвердил точный авторизованный канал и каталог из 25 видео. Список Shorts в Studio полностью помещается на одной странице: 20 элементов, из них 14 Public и 6 Private. Для всех 14 Public прочитано поле «Видео по теме» после завершения загрузки формы; кнопка «Сохранить» оставалась отключённой. Private-копии и техническая трансляция исключены из проверки зрительских переходов.

Три опубликованных длинных фильма определены по фактическому списку Shorts Studio и API-каталогу:

- `0RaC4t7yn5o` — A Radio Signal with an Unexpected Listener, 4:21.
- `L7XCSsTc9vY` — We Found Their Tools. Where Are Their Clothes?, 3:11.
- `lRkxm3mij5o` — Galveston: The City That Raised Its Ground, 9:35.

Короткая длительность или слово #Shorts сами по себе не использовались для классификации: например, A Third Wheel on Every Date (2:09) фактически находится в разделе Shorts.

## Все открытые Shorts

| Short | ID | «Видео по теме» | Результат |
|---|---|---|---|
| When Radio Sent Software as Sound | `85dwIXy_lZs` | `0RaC4t7yn5o` | Правильный полный фильм; публичная ссылка проверена |
| An MSX Game in a Radio Recording? | `7DygREwtxfY` | `0RaC4t7yn5o` | Правильный полный фильм; публичная ссылка проверена |
| She Saved 13 Kids in a Blizzard | `L553TNYK6C4` | Нет | Соответствующего Public-фильма нет |
| They Shared a Burrow for 250 Million Years | `UkwqGIqvink` | Нет | Соответствующего Public-фильма нет |
| Mantis Shrimp Evolution: Spear or Hammer? | `Bfgcq4rxQT8` | Нет | Соответствующего Public-фильма нет |
| What If Time Stopped for 5 Seconds? | `YRnIpr9P3iE` | Нет | Соответствующего Public-фильма нет |
| A Diver Reached for a Hand in a Sunken Tugboat. It Grabbed Back. | `zA0kogtqoUs` | Нет | Соответствующего Public-фильма нет |
| The Taj Mahal Cost Him His Hands | `fvRm9Vxwagk` | Нет | Соответствующего Public-фильма нет |
| Why Is This Cat on a Monument? | `orQiLIvOL-8` | Нет | Соответствующего Public-фильма нет |
| 13 Famous People's Reported IQ Scores | `xYS2XBeR_Jc` | Нет | Соответствующего Public-фильма нет |
| A Third Wheel on Every Date | `sA-PYrDl5H8` | Нет | Соответствующего Public-фильма нет |
| One More Video. Half an Hour Gone. | `-KW8jgSoEz0` | Нет | Соответствующего Public-фильма нет |
| He Put Her Messages in an AI Chatbot | `WQw7ny9svrk` | Нет | Соответствующего Public-фильма нет |
| They Opened Her Coffin. She Sat Up. | `pdSgHe6ScTI` | Нет | Соответствующего Public-фильма нет |

Это проверка прямой связи с фильмом той же истории. Тематическое перенаправление самостоятельного Short на другую историю потребовало бы отдельного редакционного выбора и не считалось недостающей прямой связью. Длинным фильмам о Галвестоне и одежде пока не соответствует опубликованный поддерживающий Short из этого каталога.

## Публичный переход радио

В обоих Shorts-плеерах видна кликабельная ссылка **A Radio Signal with an Unexpected Listener**. Точные href ведут на `0RaC4t7yn5o`; у второго есть дополнительный параметр `pp`, video ID совпадает. Свежий API подтверждает Public и принадлежность фильма Paper Detour. В описаниях обоих Shorts также сохранён прямой URL этого фильма.

Переход из первого Short фактически открыт: адрес `https://www.youtube.com/watch?v=0RaC4t7yn5o`, на странице указан Paper Detour. На открывшейся странице отобразился заголовок **How People Got Computer Programs From the Radio**. Это другое отображаемое название того же ID; у выпуска ранее зафиксирован A/B-тест. Текущий статус/результаты теста в этой задаче не проверялись, эксперимент и метаданные не изменялись. Совпадение ID использовано как критерий правильной цели.

[Видимая ссылка в публичном Shorts-плеере](radio-related-public.jpg).

## Метод, доказательства и границы

- [API-каталог и авторизованная идентичность](api-before.json).
- [Полная страница Shorts Studio](shorts-catalog.txt), [поля всех 14 форм](studio-related-controls.json), [сводная проверка](validation.json). Полные снимки форм сохранены как `<video ID>.txt` в этом каталоге.
- [Публичный Short 1](85dwIXy_lZs-public.txt), [публичный Short 2](7DygREwtxfY-public.txt), [фактически открытая страница фильма](radio-target-public.txt).
- [Проверка покрытия API](api-capability.json): в свежей публичной discovery-схеме YouTube Data API v3 поле Related Video не обнаружено. Поэтому использовано чтение штатного Studio, а не недокументированные запросы.
- [Официальная справка Related Video](https://support.google.com/youtube/answer/14075157?hl=en): штатная связь в Shorts, advanced features, целевое видео Public или Unlisted. Проверена в этой задаче; изменения доступа не требовались.

Разрешение временно не использовать Extra High сохраняется из этой сессии. Новое производство, анализ переходов по метрикам, конечные заставки, подсказки, закреплённые комментарии и мобильное приложение в scope не входили. Принятые сюжеты не пересматривались, новых фильмов или поддерживающих Shorts не создавалось.

**Следующий отдельный пункт — проверить конечные заставки трёх открытых длинных фильмов.**
