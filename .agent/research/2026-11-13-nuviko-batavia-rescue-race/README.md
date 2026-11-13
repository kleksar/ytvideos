EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate

# The Batavia rescue race — Nuviko History / editorial candidate v01

Это **отдельная редакционная гипотеза**. Она не зарегистрирована в штатном ytv runtime и не является production script, утверждённым независимым reviewer или пользователем.

**Логлайн:** у берегов Австралии мятежники пытались захватить корабль, пришедший спасать жертв кораблекрушения. Но 22 солдата, которых их предводитель бросил без оружия на соседнем острове, сумели отбить атаки, а затем первыми доплыли до спасателей и предупредили их о заговоре.

- Канал: `nuviko_history`; формат: English Short 9:16; статус в remote main: `active`. Production scope НЕ выдан.
- Полный текст для чтения владельца: [script.ru.txt](script.ru.txt); оригинал narration EN: [script.en.txt](script.en.txt).
- [research.md](research.md) — девять фактически рассмотренных направлений, три финалиста, мотивы выбора, источники, сигналы спроса и неопределённость.
- [story-review.md](story-review.md) — отдельные самопроверки истории и точный EN/RU loop; независимый review UNVERIFIED.
- [storyboard.md](storyboard.md) — предварительные композиции/промпты до официального script approval.
- [packaging-brief.md](packaging-brief.md) — 3 названия и обещание обложки.
- [handoff.md](handoff.md) — ограничения, base SHA, перенос в локальный ytv runtime.

**Отсутствующая capability:** на текущем host нет исходного checkout `ytvideos` и возможности запустить `uv run ytv start` с сохранённым store/read_next; отдельная свежая host session / `sessions.independent` недоступна. Отсутствуют actual run ID, research/script task receipts, exact `ytv-script-review-v1` (полное чтение Short дважды), независимая двуязычная проверка и approval. Нельзя создавать несуществующее `awaiting_script_approval`.

**Точный переносимый путь:** `.agent/research/2026-11-13-nuviko-batavia-rescue-race/`. Локальный агент должен заново начать по `handoff.md` и текущему runtime; ни этот Draft PR, ни его возможный merge **не разрешают** TTS, изображения, монтаж, upload или публикацию.
