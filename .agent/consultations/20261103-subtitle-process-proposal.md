# Subtitle process proposal consultation

Scope: user requested recommendations only, no implementation.
Visible mode immediately before request: Extra High.
URL: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aea3ab4-24e0-83eb-a84b-7eb8109767cc

Task supplied: evaluate a single subtitle generation entry through existing skill, JSON profiles and FFmpeg, final audio/speed before timing, binding inputs to output by hashes, mechanical preflight, separate semantics/sync evidence and stale-input upload protection. Supplied defects: episode-local 72 px renderer bypassed the 104 px profile, forced alignment lacked listening, the 1.1× narration request was unapplied in uploaded media. Preserve immediate handoff after full render and no new approval per step. First answer failed to display; short follow-up requested the same result.

Completed response:
1. Единый entrypoint. Генерировать субтитры только через canonical pipeline: skill → JSON-профиль → FFmpeg renderer. Запретить эпизодные скрипты и переопределение параметров (например, 72 вместо 104 px). Upload принимать только из официального pipeline.
2. Фиксировать финальное аудио до timing. Сохранять voice_id, фактическую скорость озвучки 1.1x и audio_sha256. Любое изменение аудио инвалидирует word map и требует повторного alignment.
3. Автоматический preflight до рендера. Проверять точность текста, максимум три слова в группе, ширину с реальным шрифтом, одно жёлтое текущее слово, непрерывность и отсутствие временных пересечений. Проблемные места проверять короткими пробами.
4. Разделить смысл и синхронизацию. Canonical skill отвечает за смысловую разбивку, SRT skill — за timing. Forced alignment без независимой проверки не означает PASS: использовать UNVERIFIED. Не вводить обязательное ручное approval каждого шага.
5. Минимальный build manifest. Связать хешами аудио, субтитры, timing, профиль и версию renderer. Устаревшие входы блокируют upload. Полный review MP4 выдавать сразу после рендера, без дополнительных проверок.
Избыточно: сложная система хеширования каждого промежуточного файла.
Не решает проблему: один entrypoint без контроля upload; автоматические проверки геометрии без проверки синхронизации.

Coordinator assessment: recommendations are a proposal, not enacted policy. Three-word maximum applies only to Paper Shorts. Voice ID applies only where known; source audio must not receive a fabricated voice ID. Re-alignment can be avoided for an exact proven speed/offset conform, while evidence must bind the resulting map to the final audio. Automated agreement does not establish listening. Preserve existing normal user review checkpoints and avoid creating new approvals. No production files or release state changed.
