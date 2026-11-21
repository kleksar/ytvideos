EDITORIAL_CANDIDATE_UNREGISTERED — independent review / runtime / approval НЕ проводились.

# Handoff: одна история Elmer McCurdy, три законченных EN/RU варианта

Baseline PR #120 HEAD `9648f83b42fc0d46a29ad622934bcd76c9168684`, оригинальный root EN Git blob `670e0891c8c07647353dc793b81fd20fd6c40e4f` и RU blob `1eea171088c6c96cb712357475ca339793667852`; сохранены без изменений. Исходные 17 точных EN/RU spans относятся только к root/02m, **НЕ** к новым 05m или 10m. Полные тексты и точные SHA-256: [review](story-review.md), источник: [research](research.md).

| Целевая длина | Полные тексты | EN words | Оценка |
|---|---|---:|---|
| 02m, Short 9:16 | [EN](variants/02m/script.en.txt) · [RU](variants/02m/script.ru.txt) | 253 | Сильный исходный Short сохранён |
| **05m, Long 16:9** | **[EN](variants/05m/script.en.txt) · [RU](variants/05m/script.ru.txt)** | 604 | **Предварительно рекомендована** |
| 10m, Long 16:9 | [EN](variants/10m/script.en.txt) · [RU](variants/10m/script.ru.txt) | 1369 | Документальная альтернатива с медленным периодом 1928–1967 |

Paper Detour: channel `paper_detour`, EN voice production; 02m Short 9:16 с narrative loop required, 05m/10m Long 16:9 с question-first, оба формата есть в main `channel.json`. 05m предварительно рекомендован по причинному развитию/человеческому payoff, а не по гарантированному удержанию. Хронометраж без фактической озвучки НЕ measured; 05m возможен недобор.

**Missing capabilities (GitHub-only host):** нет authorized runtime `uv run ytv start`/status/plan, реального pinned `read_next`/task claim/CAS, нет подлинной независимой сессии с сохранённым `ytv-script-review-v1`; наличие GitHub, локальной текстовой авторской проверки или веб-поиска этого не заменяет. `audio.listen`, генерация кадров, видеопровайдер, права и final MP4 здесь не вызывались.

**Safe transfer:** открыть официальный checkout, читать actual `AGENTS.md`/stage requirements и frozen pins *существующего* run, если он есть; не заменять checkout-ом pins. Если run отсутствует, отдельная согласованная регистрация по `uv run ytv start --channel paper_detour --format long --intent 'Проверить три редакции Elmer McCurdy из PR #120 и передать один exact master на согласование; без производства'`. После фактического `plan/read_next` прикрепить supporting `script_variant` для всех трёх, `story_review` с реальными IDs/hash; только затем выбрать exact script. Если нет поддерживаемого импорта кандидата, сохранить blocker, не фабриковать state/receipts.

Fresh independent reviewer получает exact текст **без** авторских scores/диагноза, источники после первого чтения; Short EN/RU читает дважды целиком + literal seam, для Long проверяет обещание → погружение → основной hook → последствия. Только reviewer создаёт собственный проверяемый response в имеющейся schema. После его результатов и выбора владельцем — новая storyboard на hash выбранного Long, обязательные visual/rights/crop/voice checks. Не выполнять merge, media/TTS/imagegen/MP4/upload/publication, не менять channel settings или расписание.
