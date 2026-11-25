## Editorial A/B revision — new source candidates, no implied approval

EN and RU active scripts changed from prior HEAD `f4a2ea364a27bad35ff6ec34e70537935622f9d5`. Original A scripts preserved in `experiment/baseline.script.en.txt` and `experiment/baseline.script.ru.txt`. The currently proposed B script must be reviewed by a new independent reader against its exact hash; prior author/self/independent checks cannot be reused. The storyboard has 14 synchronized narrative spans, and its previous estimated 76s timing is invalidated pending actual TTS. This PR is NOT registered `ytv start` and has no trusted script/MP4 approval or production permission. [Experimental rationale](experiment/README.md).

## Актуальный workflow — удалённый main

Сверено с `main` `96c8fa1573c02e8e7987e272a569bf34f037691e`. Nuviko History **active** по current `channel.json`; старые строки ниже о `frozen` — история первоначального черновика, не актуальная блокировка канала. При этом этот PR — **не `ytv start` run**, и существующий `storyboard.json` только художественная схема до утверждения текста, не completed stage. Нельзя считать self-review независимой оценкой или script gate `awaiting_script_approval`.

При выборе сюжета локально: `uv run ytv start --channel nuviko_history --format short --intent 'Проверить неутверждённый сюжет PR #20'`. Сначала получить `plan_summary` и `read_next`, прочитать `task_guide` и pinned requirements. Для script нужен реальный `sessions.independent` reviewer, оригинальный `ytv-script-review-v1` с hash точной EN версии и полным двукратным чтением; без него оставить UNVERIFIED/Draft. Достигнуть настоящего `awaiting_script_approval` и получить подлинное пользовательское согласие до любого производства. [Workflow](https://github.com/kleksar/ytvideos/blob/main/docs/workflow.md).

RU остаётся смысловой редакторской копией, не русской TTS дорожкой; подготовленные кадры, 4–6 c и петля S014→S001 пока расчётные. Actual PNG references, звук, MP4 и AV стык НЕ проверены. Не придумывать run/media/approval/rights receipts, не переносить чужие pins.

---
# Local production handoff — Nuviko History / USS S-5

**This is an unapproved textual story proposal.** It is NOT a registered production run or a user approval and does not change the frozen channel's production permissions.

- **Channel:** nuviko_history, English Short portrait 9:16. At base main SHA 50bb35ecd4ad2e832be5451fd2fa909794f047ed, channels/nuviko_history/channel.json status = frozen. The user's current request grants a one-story research/PR exception, not automatic unfreezing.
- **Narration:** script.en.txt is the exact proposed English master for later TTS and English SRT; script.ru.txt is the full Russian reading copy for the owner, not a second language to voice.
- **Sources:** research.md contains 10 different candidates, three finalists, direct historical source-by-claim citations and objections; story-review.md is AUTHORIAL check only. Independent first-listener and independent bilingual review have not been run.
- **Preliminary scenes:** storyboard.json has 14 scene-specific self-contained AI-image prompts and paired EN/RU narration. The baseline A scene grid estimated 76.0 seconds; B narration replaced it. All per-scene durations are only editing placeholders pending actual voice, not valid final frame cuts or an official completed storyboard task.
- **Nuviko identity:** photoreal physical environments, photograph-like period people and objects; drawn 2D traveler only at S005 as a modern external narrator. Before that image can be generated, open and hash-check the two actual accepted traveler reference PNGs declared in channels/nuviko_history/brand/VISUAL_PROFILE.md.
- **Sea geometry:** the exposed stern rises about five metres while bow is still on seabed; never render entire submarine entirely vertical in free water. Navy photograph NH 41810 is a factual external geometry reference, NOT a license to use existing pixels as production images. Rights review required.
- **Loop:** S014 ends with a colon introducing what the passing captain saw, and the very next S001 phrase supplies the sight of the white T-shirt. The RU version has the same construction. S014 reuses the exact approved S001 image with matching final-to-opening camera pose. Need actual audio/music/subtitle/visual seam QA after MP4 exists; no loop tested now.
- **Truth boundaries:** 180 vs 194ft reported depth -> about 60m only; reported historical phrase is not an audio recording; a second tow attempt under USS Ohio ended in snapped cable; all sailors were already safe.
- **If user/local reviewer rejects theme:** record concrete losing interest and return to candidate research without writing more image prompts to justify the script.
- **Only after precise owner script approval and permitted channel status/exception:** local agent follows current ytvideos task contract and creates a run, pins references, measures actual voice at one 1.10x speed application, adapts scene count/timing, generates unique AI frames, reviews each visual, composes SRT/audio/music, and produces exact MP4 for separate owner approval. Publication requires separate explicit direction.
- **Scope:** no global docs, skills, runtime, channel status, credentials, voice files or media changed.
