EDITORIAL_CANDIDATE_UNREGISTERED — Git-only. Нет официального run/lease/receipt, independent reviewer, owner script approval, готовых media или проверенного audio timing.

# Handoff — Paper Detour / Fyre

- **Source main при подготовке:** `3b21444bc5bb125fc2f97dacd7028e5b8d38fd98`, remote проверен 2026-11-19. **#124 уже merged** 2026-11-16; использованы текущие main editorial/writer skill, **не** separate proposed revision из 7d6bdf77.
- **Соседние сюжетные PR:** последний #262 Two Ways; перед ним #260 Nuviko, #255 Paper. Следующим выбран Paper по rotation. Существующий **#100 McDonald's Monopoly** имеет свой полный пакет трёх вариантов: оригинальный сильный конкурент отсеян как дубль и НЕ изменён.
- **Новый материал:** [research](research.md) / [story-review](story-review.md) / [packaging](packaging-brief.md) / шесть EN/RU текстов в `variants/02m`, `05m`, `10m`. Точные SHA-256 в [review](story-review.md).
- **Рекомендуемый master proposal:** `variants/05m/script.en.txt`, SHA-256 `6708b7d4fb7b4e1ab2db9c11c57d324e0ccb1d69f1c3cdb46b5071f79a1427fb`; RU смысловая пара `variants/05m/script.ru.txt`, SHA-256 `9bda905ceb1cff7423971a0dcd504541855603940be7c815de91b5715b8a2215`. Это **только** рекомендация.
- **Actual runtime blocker:** команда `uv run ytv start` в доступном окружении ранее завершилась `Failed to spawn: ytv / No such file or directory`; текущий Git-only доступ не располагает checkout/runtime artifact store для производства. Не объявлять `ytv start` успешным.
- **Independent reviewer blocker:** отдельной подтверждённой сессии `sessions.independent` нет. Нужен blind-first-reading exact 05m EN/RU без авторской оценки/beat map, затем evidence source review и подлинный schema result; новый hash требует нового результата.
- **Transfer:** в авторизованном local repo сначала проверить существующие runs, `uv sync --locked`, затем `uv run ytv start --channel paper_detour --format long --intent 'Review Fyre Festival editorial candidate and select one exact script'` по актуальному CLI. Прочитать полученные plan_summary/read_next/task_guide/pinned docs, attached refs и exact SHA, затем зарегистрировать variants/review по task contract, получить owner approval одного exact master. Не создать дублирующий run при наличии уже активного.
- **Next tasks after gate:** проверить measured voice Lawrence 1.10×; выбрать 05m либо решение владельца; сделать подробный storyboard/prompts **только** для выбранного hash. Бумажные references и самолётик `References/paper_plane_20261112/scene_sample.png` пока **не загружены и не сверены** с эталонным SHA. Не выдумывать reference bytes.
- **Production state:** TTS, video generation, images, MP4, subtitles, packaging QA, publish/upload, release schedule, media rights, independent review and CI success **NOT_DONE / UNVERIFIED**. PR — Draft, без merge.

Не менять общие docs/skills, каналы, уже принятые master, чужие ветки/PR, старые spans и pins. При гонке ref остановиться и перечитать чужие изменения; никаких force-push.
