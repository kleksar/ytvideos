## Актуальный workflow — сверено с remote main

Обновлено по `main` `96c8fa1573c02e8e7987e272a569bf34f037691e`. Этот старый текстовый пакет **не является `ytv start` run**, а `storyboard.json` — предварительное художественное задание, не завершённый runtime stage. Редакторская самооценка не является независимым review или `awaiting_script_approval`.

**Текущий статус Nuviko History: `active`** в `channels/nuviko_history/channel.json`. Старые упоминания `frozen` ниже отражают состояние во время создания первоначального черновика; сейчас они не действуют. Они никогда не подтверждали ни approval пользователя, ни разрешения на upload.

При выборе этого сюжета локально создать новый сохранённый run: `uv run ytv start --channel nuviko_history --format short --intent 'Проверить неутверждённый сценарий PR #17'`. Прочитать `plan_summary`/`read_next` и настоящий pinned task context, выполнить research/script по [workflow](https://github.com/kleksar/ytvideos/blob/main/docs/workflow.md) и [task contract](https://github.com/kleksar/ytvideos/blob/main/docs/operations/task-contract.md). Фактически получить независимую сессию reviewer (`sessions.independent`), точный `ytv-script-review-v1` и полный двухкратный проход Short с подтверждёнными bytes/hashes/receipts. До этого script gate `awaiting_script_approval` НЕ достигнут; после него требуется подлинное согласие владельца. Не регистрировать авторскую оценку как независимую и не генерировать фальшивый user event.

English master и полный русский перевод остаются кандидатами; все изображения/тайминги и loop AV пока UNVERIFIED. Не переписывать pinned версии чужих выпусков; media, TTS, publish не запускались и не разрешены этим PR.

---
# Handoff — text-only candidate, not production

- **Channel ID:** `nuviko_history` — **status=frozen in main** (read 2026-11-13); this PR's mandate allows only research and scenario drafts; it does not unfreeze a channel or create an episode. #12 proposes reactivation but remains OPEN at branch creation and has not changed this main's frozen ChannelSpec. #16 (audience-first selection) IS merged into this base.
- **Base SHA:** 50bb35ecd4ad2e832be5451fd2fa909794f047ed (at branch creation time). **Story packet revision:** independent Git commit on the draft branch; PR does not equal script approval.
- **Voice source:** `script.en.txt` only (full unannotated English narration). **Owner's Russian copy:** `script.ru.txt` mirrors all 12 paragraphs; no Russian TTS. After any substantive English change, update each paired RU paragraph and storyboard narration.
- **Research:** `research.md` (11 real candidates, 3 finalists, audience/hook/development/payoff/objection, source limitations and duplicates); `story-review.md` (author PASS vs independent UNVERIFIED), `packaging-brief.md` (3 concepts), `storyboard.json` (pre-approval planning only).
- **Visual standard:** Nuviko History is a hand-drawn 2D traveler (when present) in a fully photorealistic world; accepted PNG files `channels/nuviko_history/brand/References/traveler_turnaround_20261104.png` and `traveler_emotions_20261104.png` must be attached/verified for presenter scene S012. No fake archive, no cardboard treatment from Paper Detour; whole-frame camera only. Do not auto substitute Nuviko Videos/Stories identities.
- **No actual media or signed receipts:** no research/run ID, episode ID, script approval event, TTS, measured word alignment, imagegen jobs, final storyboard, MP4, upload or schedule was created. Current timings are hypothetical 4–6s per shot.
- **Next editorial gate:** owner reads full RU/EN; fresh blind first listener then fact review; if weak/boring, reject concept and return to candidate selection. If ever owner explicitly authorizes thaw/production, follow *current* status → next → context and workflow with genuine approvals. **No automatic merge or production from this PR.**
