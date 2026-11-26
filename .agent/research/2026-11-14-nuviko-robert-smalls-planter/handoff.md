EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Handoff / capability limitation

Channel nuviko_history (not music Nuviko Videos) short 9:16, remote main 5d3222c8888c775d2195c8b2949949f2d992e98d, tree e92a9c5b9ee656aa1448f34264b217ca1d0cbe98. Editorial source directory .agent/research/2026-11-14-nuviko-robert-smalls-planter. Exact candidate EN SHA-256 f9bc0cdbb5f2a74314fd6d7aaf3cebf6f12e20218a34295a1c6915d1dc1732b8 and RU e62c60567d332c3f2a2b6af0d15138933daa00769025e818e1fbad26cb625a5a. No registered run or approvals.

Observed local CLI attempt: cd /mnt/data && uv run ytv start --channel nuviko_history --format short --intent 'Новая редакционная заготовка: Robert Smalls and Planter escape 1862; без производства' => exit 2, Failed to spawn: ytv (No such file or directory). The current host has no authorized runtime checkout or shared store. Fresh sessions.independent reviewer not available.

Transfer ONLY on authorized actual checkout: fetch this branch, reconcile main/PRs and existing run; if no matching run, execute uv run ytv start --channel nuviko_history --format short --intent 'Review Robert Smalls existing bilingual editorial draft; no production'. Read real plan_summary/read_next/task_guide and pinned reference_documents/skills; import script.en.txt and research.md via the actual described task contract (do not invent flags), keep exact hashes.

Require new independent blind ytv-script-review-v1 on exact EN hash, first opening then two complete readings; only after initial read show source ledger and strongest alternative. Read RU independently too; revised text invalidates old hashes, review and storyboard. Show owner full text for actual script approval at gate; this task never authorizes images, TTS, render, upload or publish.

UNVERIFIED: independent editorial/bilingual reader, official awaiting_script_approval, actual timings, presenter references, media, audio/visual loop, image copyright/reference bytes, YouTube analytics, CI until readback. No merge or shared docs/skill/channel changes.
## 2026-11-16 — три редакции; новые версии не подменяют master

Canonical main `4be3c6cbc0af7c625de0037bd87e2d2afa11e8c4`; это редакционное read-time основание, не новый runtime pin. Baseline PR HEAD `6a1f9ca360bcfa2c2d2df9b6aaf64d68426d8c2f`. Имеются 02m (original exact), 05m и 10m с полными EN/RU в `variants/*`; SHA-256 и сравнительные оценки — в `story-review.md`. Предварительно рекомендуем `05m/script.en.txt` SHA-256 `8b775a2b794bc03e24b82e835d544d3801293b4295020c29b0480e4403f209f1`; owner approval отсутствует.

В текущей подключённой среде доступен GitHub repo connector, но не авторизован workspace/runtime store ytv для `uv run ytv start` и не обнаружен отдельный инструмент `sessions.independent`/spawn-agent. Предыдущий зафиксированный сбой CLI в старом handoff — историческое свидетельство, **не** новая попытка этой сессии. Полноту активности сторонних Codex сессий вне GitHub эта проверка не устанавливает.

Перед переносом на фактическом production checkout: проверить PR HEAD, approvals и уже зарегистрированные runs; использовать canonical pinned docs через `ytv status` / `resume` для существующего run, иначе `ytv start` с `--channel nuviko_history --format long` только по явному выбору. Передать выбранный exact EN и связанные RU/research/story-review как supporting artifacts по реальному `task_guide` и `attach-artifact`, не изобретая ключей. Fresh independent reviewer должен прочитать точный текст, не видя авторских баллов, затем увидеть источники; сохранить его подлинный `ytv-script-review-v1`, а не самозаполненный. После owner approval — отдельный storyboard под exact hash выбранной версии. Оригинальный Short 14-scene storyboard только для unchanged 02m. Не запускать media по этой редакционной PR.


## 2026-11-26 — current 10m candidate
Baseline d131a3e8cd206d4f2e2cd35c3d7e81fafa372a59, main 7c779c4b2fd379c85166ae1b164fa53d1ea08843; 10m EN b7128464539c6410e9037a00dd175cf6ec675d74911ee17350414c9f84c6e177, RU e84fef36bba30ae0b19459165d9b956ff09bcdcd7e2d592ba2d30d307c291c93. Keep 02m/05m and original master untouched. Current 10m requires fresh independent review and new selected-variant scene spans; historical 10m evidence does not transfer. Recommendation 05m unchanged. No runtime/store or independent reviewer available; no approval.