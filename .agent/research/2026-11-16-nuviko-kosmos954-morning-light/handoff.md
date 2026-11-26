EDITORIAL_CANDIDATE_UNREGISTERED — только редакционная Git-очередь, официальный script gate **не** пройден.

Канал: `nuviko_history`. Рекомендованная редакция `05m`, English master `variants/05m/script.en.txt` (SHA-256 `a88542f8048bd694882b9c133117c068cc1a653bad6e40f52051940901c9ce2e`), RU editor `variants/05m/script.ru.txt`. Остальные версии — independent alternatives, не три запуска.

Source: GitHub remote `main` HEAD `ddafebf5aec10ff4158b4ea8aabac4dd1d576b67`. Предложенная ещё не слитая редакционная политика PR #124 `7d6bdf7702a2a241a33a21677fce29f26ada9b72` применена по прямому поручению владельца **только к этому новому пакету**. Runtime pins старых runs не менялись, общие docs/skills/ChannelSpec не затрагивались.

Недоступная здесь capability: исполняемый локальный `uv run ytv start` с project database/lease, `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, независимый reviewer по действующей schema. Git-only материалы не заменяют их. `start`, run_id, approvals и model receipts **не** эмулировались.

Локальный перенос только при явном выборе: 1) синхронизировать main и получить точные script bytes из MR; 2) выполнить `uv run ytv start --channel nuviko_history --format long --intent 'Produce approved exact script variant from editorial PR'` согласно текущему workflow; 3) выдать полные pinned inputs/guide и выполнить независимое чтение exact master без оценок из `story-review.md`; 4) при появлении принятого решения владельца передать exact `--source-script`, зарегистрировать применимые variants/review как реальные supporting artifacts, сохранить IDs и выполнить один script gate; 5) затем storyboard/prompts только выбранного текста и под реальными 2D-traveler PNG references/rights, без переноса timing другой редакции.

Никаких TTS, Flow, imagegen, MP4, upload, release, merge, расписаний или внешних платных действий. Не считать автоматическое CI художественной приемкой. Независимые показатели интереса и фактические voice timings UNVERIFIED.
