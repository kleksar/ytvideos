## Актуальный workflow — remote main

Сверено с `main` `96c8fa1573c02e8e7987e272a569bf34f037691e`: Nuviko History **active** по актуальному channel.json; ранние упоминания заморозки ниже являются историей, не текущей конфигурацией. Этот PR — не `ytv start` run, `storyboard.json` — предварительные идеи, а не completed stage; самостоятельный review не подтверждает `awaiting_script_approval`.

Для выбранного сюжета локально создать `uv run ytv start --channel nuviko_history --format short --intent 'Проверить неутверждённый сюжет PR #22'`, прочитать `plan_summary`/`read_next` и pinned `task_guide`/requirements, завершить `research` и `script` только после независимой проверки EN (`sessions.independent`, оригинальный `ytv-script-review-v1` с hash точного текста и два прочтения полного Short). После реального script gate требуется подлинное approval пользователя; затем media/imagegen/TTS и отдельное согласие на release. См. [workflow](https://github.com/kleksar/ytvideos/blob/main/docs/workflow.md) и [task contract](https://github.com/kleksar/ytvideos/blob/main/docs/operations/task-contract.md).

Сценарий RU — редакторский перевод, а не TTS-дорожка; source assets/тайминги/видеопетля не проверены. Никаких придуманных run IDs, receipt, independent reviewer, media/rights или owner approvals. Сохранять чужие pinned выпуски и уже принятые тексты без самовольной правки.

---
# Local handoff: Castle Itter / Nuviko History

- New text-only proposal. Remote main source `44786bd929473cc06a724aefb4ad122f358c0aeb`; isolated branch `work/story-drafts/nuviko-castle-itter-20261113`; intended base `main`.
- Current channel status is **active** in verified `channels/nuviko_history/channel.json` (merged #12), although PROFILE still describes frozen state; this automation explicitly authorizes ONLY text drafts, no production.
- Language EN with full exact RU working translation; neither approved. No official episode/run, no script approval event or hashes for media.
- `script.en.txt`: 15 paragraphs, 209 English words; `script.ru.txt` exactly 15 aligned paragraphs. English master is future TTS/SRT source only after owner script approval.
- `storyboard.json`: 15 independent full-frame 9:16 historical compositions; ~75 seconds at *provisional* 5 s each. Speech timing is UNVERIFIED and must be remapped to actual voice, creating/splitting compositions where needed for 4–6 s per plan.
- S015 reuses exact S001 image with matching end-to-start camera pose; text loop in `story-review.md` is authored and checked, real sound/subtitle/visual seam not measured.
- Respect `channels/nuviko_history/PROFILE.md` and `brand/VISUAL_PROFILE.md` 2D traveler reference as an optional element in photorealistic historical world. No false archival imagery and no faked real personal likeness.
- Before production: owner must approve exact script; check live run/status, source docs, provider voice, actual image reference files, documentary uncertainty around deaths, bilingual cold reader. No TTS, image generation, SRT, MP4, upload, schedule or publishing was done by this PR.
- No shared docs/skills edited. No merge authorized.
