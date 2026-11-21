EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — One Mug, Two Machines: The Minimum-Fill Flip

**Логлайн:** мне нужна всего одна кружка горячей воды. В модели микроволновка расходует меньше электричества, чем чайник, **только потому**, что чайник по инструкции должен нагреть ещё одну лишнюю кружку. Стоит взять чайник с меньшим минимальным объёмом — и победитель меняется. **Числа относятся к расчётной модели; физического эксперимента не было.**

**Channel:** `two_ways_lab`. **Canonical policy:** remote main `247ebe9245091972c5a93ecb84ce55ad8c15a211`; PR #124 **already merged**, not a proposed policy override. **Git-only queue:** no actual local `uv run ytv start`, plan_summary, read_next, task_guide, pinned reference_documents, local profile digest or independent reviewer were accessible in this environment. This exception has **no** script gate, approval, receipt or production authorization.

| Target | Complete RU | Complete EN production narration | Author-only assessment | Format/capability |
|---|---|---|---|---|
| **02m** | [Полный русский](variants/02m/script.ru.txt) | [Full English](variants/02m/script.en.txt) | **STRONG_CANDIDATE — recommended editorially** | Illustrated Short recipe exists; **2m exceeds 35–50s channel target, compatibility UNVERIFIED** |
| 05m | [Полный русский](variants/05m/script.ru.txt) | [Full English](variants/05m/script.en.txt) | STRONG_CANDIDATE | **Long production BLOCKED**, no enabled recipe/canvas/fps |
| 10m | [Полный русский](variants/10m/script.ru.txt) | [Full English](variants/10m/script.en.txt) | REWORK, complete but slower | **Long production BLOCKED**, likely overshoots exact 10m at normal speech |

**Рекомендация: две минуты, но не выпуск без format-check.** Двухминутная редакция сразу показывает первый выигрыш B (39 против 58 Wh), меняет единственный параметр — минимальный допустимый объём чайника — и получает честный переворот A (29 против 39 Wh). У пятиминутной есть дополнительная польза: порог 333 мл и сравнение для двух кружек. Десятиминутная подробно разбирает чувствительность модели и правила измерения, но проигрывает по темпу. **Ни один вариант не принят в производство**, и целевая длительность не измерена озвучкой.

**Files:** [Один общий research и источники](research.md) · [Отдельные восемь оценок каждой редакции, SHA-256 и статусы](story-review.md) · [Packaging brief](packaging-brief.md) · [Только рекомендованный 02m: подробный черновик кадров и prompts](variants/02m/storyboard-draft.md) · [Handoff и blockers](handoff.md).

**Critical model caveat:** 250mL useful water, 20→100°C theoretical temperature rise, `eta_kettle=0.8`, `eta_microwave=0.6` **illustrative not measured**; required 500mL kettle minimum in round one, 250mL low-min kettle in round two. Heating plain water in a microwave can superheat it; follow real manufacturer safety instructions and FDA guidance. Do not film an unsafe water-boiling experiment based on this thought experiment.

**Production blockers:** format compatibility for 2-minute Short, absent Long recipe for 5/10m, absent independent `ytv-script-review-v1`, no local ytv run/reviewer/owner-selected approved master, no available actual ref-image bytes/profile hash, no measured TTS or AV loop. **No** FFmpeg, TTS, imagegen, Flow, YouTube release, approvals or schedules performed.

**Local continuation (after owner authorizes the exact master):** check out this immutable commit; verify script SHA-256 from [story-review](story-review.md); run `uv run ytv start --channel two_ways_lab --format short --intent 'Produce explicitly owner-selected 02m script' --source-script .agent/research/2026-11-17-two-ways-one-mug-kettle-microwave/variants/02m/script.en.txt`; inspect returned `plan_summary/read_next/task_guide/reference_documents`; apply the accepted-source route with actual owner event (do not spoof it), attach verified supporting files and obtain a real independent review when appropriate. A new revised script hash invalidates related storyboard and review. Confirm format support or keep editorial-only.
