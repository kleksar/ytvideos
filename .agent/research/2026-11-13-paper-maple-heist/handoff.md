## Актуальный workflow — remote main

Сверено с `main` `96c8fa1573c02e8e7987e272a569bf34f037691e`. Этот старый текстовый сюжетный PR — **не зарегистрированный `ytv start` run**, а `storyboard.json` — только предложение визуальных сцен до approval. Авторский PASS и приведённые источники не подтверждают `sessions.independent`, `ytv-script-review-v1` или готовый `awaiting_script_approval`.

При выборе сюжета начать локально с `uv run ytv start --channel paper_detour --format short --intent 'Проверить неутверждённый сюжет PR #19'`, прочитать `plan_summary`, `read_next`, `task_guide` и pinned requirements. Завершать research/script только с настоящим независимым reviewer, полным двойным чтением Short и правдивыми checks/receipts. После реального script gate — отдельное одобрение точной версии пользователем, лишь затем TTS/imagegen, MP4 и отдельное разрешение на публикацию. [Workflow](https://github.com/kleksar/ytvideos/blob/main/docs/workflow.md) · [Task contract](https://github.com/kleksar/ytvideos/blob/main/docs/operations/task-contract.md).

Сценарии EN и RU остаются кандидатами, предварительные кадры/тайминги не измерены, AV-петля и качество не проходили независимую приёмку. Не придумывать run ID, reviewer ID, source hash, audio/probe, approvals и не менять старые pinned выпуски.

---
# Production handoff — no owner approval recorded

- **Channel:** Paper Detour, English Short 9:16; `main` channel config was active when story was researched.
- **Source of truth:** `script.en.txt` English narration for eventual TTS and SRT; `script.ru.txt` full Russian reading copy for owner. `storyboard.json` repeats both texts for 12 provisional scenes.
- **No official CLI run created** and no `approve` event exists. The Draft PR is for local model first-reader and owner review, not production authorization. A merge is not a script approval.
- **Research:** `research.md` lists the real 10-story selection, three finalists, comparative rationale, and public source-to-claim boundaries.
- **Current checks:** authorial progression and story packet alignment done; independent first-listener and bilingual model review NOT RUN; no actual YouTube topic CTR/retention measured.
- **Media:** none. Estimated scene grid is 64.9 seconds; this is NOT Lawrence audio duration. Use approved channel voice at the pinned 1.10× setting exactly once, then obtain actual per-word timing and re-split scenes to match 4–6 second compositions without padding.
- **Images:** after approved script, resolve real Paper reference PNG from verified media bundle, 4K source if possible, one full-frame tactile paper diorama per unique shot. S009 has one pale paper-plane cameo on investigator notes; do not make it part of historical evidence.
- **Loop:** S012 is designed as an exact reuse of S001 artwork at the transition, not an unnecessary second AI generation. Verify real pan/zoom end and start poses and narration/music/SRT seam in the exact MP4.
- **Research caveats:** reported near-fall from journalist, not court deposition; reserve producer-managed rather than national government. Theft $18m and 9,571 barrels confirmed by Supreme Court; fine >$9m is a court fine in lieu, not paid recovery.
- **Recommended local next step:** read RU script cold, English narration separately, conduct independent reader interest/reality check, compare to bats alternative, then choose to revise/reject/approve exact text. No paid imagegen/TTS/render until substantive approval.
- **Scope:** no new global docs or skills; do not silently modify channel status, YouTube settings or releases.
