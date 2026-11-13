# Ограниченная проверка примеров skills

Две свежие сессии GPT-6 Luna (medium, без предыдущего разговора) получили одни и те же шесть узких учебных задач. Baseline — `9b2f92c36b6c889f6628958a2b8192583e759ecf`, candidate — `42ce71eefce19a8951576110ac5118cc0f2c4be7`. Это текстовая проба применения инструкций, не полный production acceptance и не измерение качества канала.

## Материалы и протокол

- [Входы](inputs.json) содержат четыре сценарные задачи из существующего набора и два задания на production brief/план. Авторские expected observations участникам не передавались; `evals/` и `tests/` отсутствовали в их рабочих снимках.
- [Запуски](launches.json) сохраняют точные запросы, модель и параметры свежих сессий. Бюджет запроса — 180 секунд / до 10 инструментальных чтений; фактические tokens, число tool calls, active time и стоимость не экспортированы.
- [Baseline response](baseline-response.txt) и [candidate response](candidate-response.txt) скопированы byte-for-byte из файлов авторов. Исправления после ответа не внесены.
- [Слепое сравнение](comparison.md) получает входы, ответы A/B и одинаковые для обеих версий общие правила, без версии skill и заключения автора. Первый ответ reviewer без общего контекста сохранён в [initial review](comparison-initial.md); итоговая оценка учитывает профиль и standards. A = candidate, B = baseline; одна оценка в одном порядке, без статистического вывода.
- [Reported reads](reported-reads.json) — список открытых путей **со слов модели**, нормализованный координатором с hashes файлов. Это не экспортированный tool trace и не доказательство понимания инструкций.
- [Результат](result.json) фиксирует pins, hashes, проверки и оставшиеся границы.

## Результат сравнения

В одной слепой оценке baseline предпочли в двух задачах, candidate — в одной, три признали равными. Candidate дал более определённый camera intent и удобнее оформленный AI-edit brief; в его ответах также обнаружены ошибка знака в арифметическом объяснении и чрезмерный вывод о гипотетическом риске. Raw responses не исправлены. Общее повышение качества не установлено; результаты отдельных сессий не доказывают причинный эффект новых references.

## Наблюдаемые ограничения

Baseline сохранил ответ с ошибкой JSON: после пятого `answer` стоит типографская кавычка вместо закрывающей JSON-кавычки. Этот дефект сохранён в raw response. Candidate выдаёт parseable JSON с шестью ответами. Разница формата в одной пробе не доказывает эффект новой процедуры.

В reported reads candidate есть новый production reference, но нет `hook-patterns.md` и ряда обязательных standards. Baseline также не перечислил все необходимые skills/standards. Полнота чтения обеих сессий и усвоение hook reference остаются `UNVERIFIED`; их нельзя выводить из содержательно правдоподобных ответов. Поведенческая проба не заменяет проверку доставки pinned документов кодом.

Никаких фактических images, audio, MP4, независимого first-listener для полного сценария или audience metrics в этой пробе нет. Требуемый [полный сценарный acceptance на двух каналах](../../story_selection/README.md#живой-приёмочный-прогон-skill-not_run) остаётся `NOT_RUN`; draft не снимается по этому ограниченному сравнению.

## Проверки реализации

До изменения routing два адресных теста воспроизвели отсутствие новых references в task/native worker packet. После подключения они проходят и проверяют сохранение исходного snapshot после правки checkout.

- Documentation checker на source snapshot с проверенным списком remote paths: **PASS**, 88 документов / 7 skills.
- Suites `test_context`, `test_image_host`, `test_story_selection_contract`, `test_repository_check`, `test_natural_voice`, `test_editorial_contract`: **113 PASS, 47 PostgreSQL cases SKIPPED локально**.
- [CI](https://github.com/kleksar/ytvideos/actions/runs/43470434977) для candidate: **PASS**, включая lint, native runtime, SQLite/реальный PostgreSQL и все существующие automation suites.
- Независимый review обнаружил требование downstream image/MP4 на storyboard/audio. В candidate проверки разнесены по этапам; повторный review подтвердил устранение этой зависимости.
- Первоначальная попытка отдельного Codex CLI завершилась до модели с `Read-only file system`. Она не считается модельным прогоном; comparison выполнен доступными свежими subagent-сессиями.

Production runs не создавались и не мигрировались. Эти учебные inputs/outputs не являются принятыми сценариями, очередью выпусков или производственными receipts.
