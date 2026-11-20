# Story review — Pig War / редакционный пакет 2–5–10 минут

**EDITORIAL_CANDIDATE_UNREGISTERED — не официальный ytv script gate.** No independent first-listener, no production run, no MP4, no measured timing. Authorial scores are NOT independent receipts.

## Baseline and revision

PR #31 baseline HEAD `fcbabe0596d42f773cc296d94d040cb0f92e00c7`, immutable source `script.en.txt` Git blob `b43515f3c08079c06061311674b3d57de1ab5952`, SHA-256 `c24049b6ad3eeb8bbc47a14d53531456a7982c66498e29a1a9ed1f4593169ab4`; `script.ru.txt` blob `48c84f281fb2749c44ccac26e12c471f235aa432`, SHA-256 `0613ca9f58e9588fbe15949ad3d9a0b495692b2cdef14707e1e9fce672354836`. Old 17-scene storyboard anchored to these two exact root files, NOT variants.

Было: 191-word English Short, полный RU, авторская петля через двоеточие, предварительная S001–S017; нет самостоятельных длинных версий. Стало: три новых полных композиции EN/RU и честное сравнение без перезаписи root master и original storyboard. Старые оценки/петля не переносятся на новые hashes. Владелец не принимал exact PR #31 source и запуск production по наблюдаемым комментариям/PR не установлен; внешние runtime/sessions недоступны из GitHub connector.

## Тексты и хронометраж

| Цель | Полные версии | EN words | RU words | Решение |
|---|---|---:|---:|---|
| 02m | [RU](variants/02m/script.ru.txt) · [EN](variants/02m/script.en.txt) | 243 | 213 | Новое независимое Short с текстовой петлёй |
| 05m | [RU](variants/05m/script.ru.txt) · [EN](variants/05m/script.en.txt) | 666 | 581 | **Рекомендуется для editorial selection; не approval** |
| 10m | [RU](variants/10m/script.ru.txt) · [EN](variants/10m/script.en.txt) | 1368 | 1213 | Содержательная альтернатива; проигрывает темпом |

Темп до озвучки **допущение 125–155 английских слов/мин** с паузами вне подсчёта. Результаты не measured: 02m 1.6–1.9 мин; 05m 3.9–4.9 мин; 10m 8.8–10.9 мин. Профиль задаёт final speech speed 1.10×, но нет measured voice output; оценка требует последующего уточнения.

| Exact path | SHA-256 of final UTF-8 bytes with terminal LF | Words |
|---|---|---:|
| `variants/02m/script.en.txt` | `0e60e56b9486d8b6469fc13c2a749f3154a6626eaab7d0fc9775eede2c663a44` | 243 |
| `variants/02m/script.ru.txt` | `9e581c4bba5e8c5cf80a7bbcb984bf3b123863de24ead99f864fa14e4a56fb07` | 213 |
| `variants/05m/script.en.txt` | `9361947a5fa3ddaf242fd7d410622328697cfa3d4a4f19fdb907bd910783fab6` | 666 |
| `variants/05m/script.ru.txt` | `3e06103157b021c35a38b2906fc1ea08fbd8719483bda3b836f529ee69d2e520` | 581 |
| `variants/10m/script.en.txt` | `830c41deb7fcf1e7f52301ec7ddbc1da918617d7a1bbbabdf0e52cacd3d46d9a` | 1368 |
| `variants/10m/script.ru.txt` | `11f1cd8dcc0444b719477904799e4c298e83f70e79fdf47563bd33cc4b252607` | 1213 |

## Story maps — именно готовые версии

### 02m
1. pig in disputed garden → treaty with two possible channels
2. arrest threat → US protection → Royal Navy escalation
3. Scott de-escalates → garrisons coexist → Haro arbitration → no human combat deaths
4. loop: “because” → “A pig…” after complete payoff

### 05m
1. opening questions → literal 1846 channel geometry → inhabited disputed farmland
2. Cutlar compensation/arrest → Harney sends Pickett → Douglas demands removal → Hornby resists a landing and waits for Baynes
3. Baynes cancels the landing plan → reinforcements and training fire without combat → Scott negotiates drawdown
4. two camps in 1860 → Washington Treaty 1871 → 1872 Haro award → meaning of the pig

### 10m
1. three concrete questions → Oregon Treaty ambiguity → sheep farm and American settlers
2. Cutlar payment / $100 threat → authority question → 64 men land
3. Douglas/Hornby refusal to force clash → British naval buildup → 461 Americans + cannons
4. naval target drills + officer social contact → Baynes refuses escalation → Scott negotiates
5. British camp 1860 → daily coexistence during Civil War → 1871 referral → Geneva panel
6. 21 Oct 1872 Haro award → staggered withdrawals in 1872/1874 → distinction between trigger and cause

## Оценки по восьми критериям

### 02m: авторские редакционные оценки (не independent)

| Критерий | Оценка | Основание и недостаток | Уверенность |
|---|---:|---|---|
| Интерес и значимость | 8/10 | Свинья на огороде → международный кризис за две фразы; спор известен массовой аудитории | moderate |
| Начало | 8/10 | «A pig wandered into a potato patch…» самостоятельный контекст и мгновенное появление кораблей | moderate |
| Развитие/причина досмотреть | 7/10 | Договор → арест → 64 солдата → три судна → дипломатия; середина вынужденно сжата | moderate |
| Payoff | 8/10 | Харо + отсутствие боевых человеческих потерь; объясняет, почему всё произошло | high |
| Свежесть угла | 6/10 | Факт широко известен через OverSimplified; отличие — юридическая подоплёка | moderate |
| Визуальная выразительность | 8/10 | Огород, два пролива, корабли, артиллерия и пустые пушки | moderate |
| Естественность и ясность речи | 8/10 | Короткие связные действия без риторических троек; стык требует independent read | moderate |
| Подтверждённость интереса зрителей | **UNVERIFIED** | Публичный успех чужого видео не доказывает спрос, retention или CTR нового канала | нет собственных данных |

**Слабое место:** после военно-морской эскалации согласование занимает всего несколько строк; фактический темп петли не прослушан. Текстовая фактологическая проверка: author-checked against shared research; независимый reviewer UNVERIFIED. Уверенность в художественной оценке: умеренная.

### 05m: авторские редакционные оценки (не independent)

| Критерий | Оценка | Основание и недостаток | Уверенность |
|---|---:|---|---|
| Интерес и значимость | 8/10 | Реальные последствия частного инцидента меняют смысл от комедии к пограничной дипломатии | moderate |
| Начало | 8/10 | Три конкретных вопроса получают ответы в событиях; карта вводится без отвлечений | moderate |
| Развитие/причина досмотреть | 8/10 | Cutlar → Harney/Pickett → отказ Хорнби от высадки → отмена плана Бейнсом → подкрепления → Скотт → арбитраж; плотность имён сохраняется | moderate |
| Payoff | 9/10 | Установлена конкретная линия Haro, указана дата и ограничение "1859 standoff" | high |
| Свежесть угла | 7/10 | Двусмысленность одного юридического слова и опасный приказ Hornby; факт не нов | moderate |
| Визуальная выразительность | 8/10 | Два морских пути, выгрузка, корабли, пушки, два лагеря, дипломатическое решение | moderate |
| Естественность и ясность речи | 8/10 | Понятные причинные глаголы; фамилии могут затруднить восприятие на слух | moderate |
| Подтверждённость интереса зрителей | **UNVERIFIED** | Публичный успех чужого видео не доказывает спрос, retention или CTR нового канала | нет собственных данных |

**Слабое место:** два имени военных руководителей подряд могут ощущаться справочным блоком; уточнить после first-listener. Текстовая фактологическая проверка: author-checked against shared research; независимый reviewer UNVERIFIED. Уверенность в художественной оценке: умеренная.

### 10m: авторские редакционные оценки (не independent)

| Критерий | Оценка | Основание и недостаток | Уверенность |
|---|---:|---|---|
| Интерес и значимость | 8/10 | Детально раскрывается не только анекдот, но и долгий конфликт суверенитета | moderate |
| Начало | 8/10 | Вопросы об угрозе, мирном соседстве и арбитраже; глубокое погружение затягивается | moderate |
| Развитие/причина досмотреть | 7/10 | Дополнительные эскалации и Baynes сильны, но быт лагерей замедляет переход к решению | moderate |
| Payoff | 8/10 | Haro/1872 и раздельные уходы 1872/1874 объясняют последствия | high |
| Свежесть угла | 7/10 | Офицеры общаются на фоне корабельных учений и лагеря стоят во время Гражданской войны | moderate |
| Визуальная выразительность | 8/10 | Масштаб фермы, два пролива, 31-пушечный фрегат, артиллерия, лагеря | moderate |
| Естественность и ясность речи | 7/10 | Устная причинность выдержана, но обилие дат и имён усложняет 10m | moderate |
| Подтверждённость интереса зрителей | **UNVERIFIED** | Публичный успех чужого видео не доказывает спрос, retention или CTR нового канала | нет собственных данных |

**Слабое место:** после разговора о мирном сокращении войск блок об устройстве лагерей замедляет переход к арбитражу. Текстовая фактологическая проверка: author-checked against shared research; независимый reviewer UNVERIFIED. Уверенность в художественной оценке: умеренная.


## Hard checks (не усреднять оценками)

| Проверка | 02m | 05m | 10m |
|---|---|---|---|
| Full self-contained EN/RU and semantic consistency | AUTHOR CHECKED, independent UNVERIFIED | AUTHOR CHECKED, independent UNVERIFIED | AUTHOR CHECKED, independent UNVERIFIED |
| Claimed historical facts | AUTHOR CHECKED; original legal/NPS sources | AUTHOR CHECKED; NPS and 1872 original | AUTHOR CHECKED; NPS + camps/commission |
| First element of documentary Long: questions → substantive immersion → main hook | N_A (Short) | AUTHOR CHECKED; questions precede 1846 map, main hook at Cutlar/arrest | AUTHOR CHECKED; questions precede treaty/farm, main hook at claim/arrest |
| Cold opening | AUTHOR CHECKED; single sentence comprehensible | AUTHOR CHECKED | AUTHOR CHECKED |
| Short payoff before repeat, full EN and RU twice, literal seam | AUTHOR TEXT CHECKED, independent UNVERIFIED | N_A | N_A |
| Actual MP4, TTS, AV seam, measured timing | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Independent first-listener / ytv-script-review-v1 | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Format / channel compatibility | Short 9:16 supported by current ChannelSpec | Long 16:9 supported | Long 16:9 supported |
| Runtime registration/approval | UNREGISTERED / not approved | UNREGISTERED / not approved | UNREGISTERED / not approved |

**Short literal EN seam:** “And an international confrontation had begun because” → “A pig wandered into a potato patch on an island that Britain and America both claimed.” This is syntactically continuous and the legal resolution is already delivered; it is not an AV proof. **RU:** «А международное противостояние началось из-за того, что» → «Свинья забрела на картофельную грядку на острове, который одновременно считали своим Британия и Америка.» Сначала пользователь слышит самостоятельное предложение, после повтора оно завершает финальную связку. Прочитано автором дважды; независимое double-read UNVERIFIED.

## Comparison: marginal value, drop-off hypotheses, recommendation

- **02 → 05:** география двух проливов раскрыта до выстрела; мотивация отправки войск, приказ Hornby избежать столкновения, настоящие учения и Scott дают последовательные новые причины, а не удлинённый пересказ. Уязвимый участок 02m — быстрая смена кораблей и дипломатов до того, как возникла человеческая линия.
- **05 → 10:** ферма с тысячами овец, восемнадцать американских поселенцев, претензия $100, Baynes, взаимные богослужения, детали двух лагерей, Гражданская война, комиссия в Женеве и разный уход войск подтверждают длительный кризис. Однако начиная с «Imagine the practical result» история переключается на жизнь гарнизонов; после решения Scott зритель может перестать ждать ответа. Это гипотеза авторского чтения, не измеренное удержание.
- **Рекомендовать 05m** как наиболее ясную причинную дугу и законченную отдачу; исходный 191-word Short оставить как archival source, новую 02m версию рассматривать отдельно для Short. Десять минут не выбирать по номинальной длительности. Recommended ≠ approved, all six editorial candidates not production masters.

## Required next steps

Independent cold first-listener reviews of exact six scripts, **without** the author verdict and scores; sources after first read. Revalidate exact hash after any revision. At production handoff choose ONE exact master and register a normal ytv run and proper receipts with pinned context, then seek owner script approval. Existing S001–S017 references only the archived root script hashes and must not be repurposed. No provider calls permitted by this editorial update.

## 2026-11-20 — exact 05m r2 (author only; previous hash invalid)

**Was → now:** 05m EN `dc64cec4088ca63df21942be05fd0a450011a7a0fefd86373bc67af15c682af4` / RU `9eca52cfa1e8ac984c4692f08e592a44ab6ee74049318e88156c9a0c146fd888` (607/531 words) → EN `9361947a5fa3ddaf242fd7d410622328697cfa3d4a4f19fdb907bd910783fab6` / RU `3e06103157b021c35a38b2906fc1ea08fbd8719483bda3b836f529ee69d2e520` (666/581 words). Base original HEAD `fcbabe0596d42f773cc296d94d040cb0f92e00c7` and previous editorial branch HEAD `e3f37b49d2ed0ad8cec071ce0729e4c1718abe67` preserved as history. Root source EN/RU, 17-scene root storyboard and all four 02m/10m texts remain unchanged.

**New causal map:** ambiguous treaty → farm and pig → competing arrest claim → Pickett lands → Douglas orders removal → Hornby waits rather than launch marines → Baynes cancels the landing order → reinforced standoff, drills and social contact, but no combat → Scott negotiates de-escalation → joint presence → 1871 arbitration referral → 1872 Haro ruling. Main factual addition is an actual officer decision and consequence, correcting the older implication that social civility explained the absence of battle. Research above records NPS/HistoryLink evidence, without inventing orders' precise quoted words or erasing Scott's separate role.

**Eight new 05m author criteria (each out of ten, not independent results):**
| Editorial criterion | Assessment / exact ground and weakness | Confidence |
|---|---|---|
| Interest | 8/10 — armed standoff from pig and ambiguous border; famous story, no measured demand | medium |
| Opening | 8/10 — asks about ships, non-shooting and a German decision; map intro can delay the pig | medium |
| Development | 8/10 — Hornby and Baynes both make actions preventing a landing; two naval names close together require clear visuals | medium |
| Payoff | 8/10 — Haro decision and no human combat deaths answer opening; years of occupation less immediate | medium |
| Freshness | 7/10 — command refusal as mechanism beyond quirky animal headline; incident widely covered | medium |
| Visual potential | 8/10 — ships waiting offshore, an unexecuted landing order, opposing guns and later camps; no frames produced | medium |
| Spoken clarity | 7/10 — actions distinguish captain/governor/admiral in EN and RU, but name-heavy center still vulnerable | medium |
| Verified audience interest | UNVERIFIED — no matched Nuviko CTR, retention, audience tests or listener receipt | none |

**Hard checks (r2 only):** EN/RU same order, officials, month and cancelled landing: **AUTHOR CHECKED**, independent bilingual UNVERIFIED. Facts map to NPS summaries and corroborating HistoryLink; original Admiralty dispatch UNVERIFIED. 05m Long begins question → 1846 channels and settlement → pig and main armed hook → refusal and consequences: **AUTHOR CHECKED**. Short loop N_A. Fresh independent first-listener/\`ytv-script-review-v1\`, TTS length, 16:9 scene spans, owner approval, runtime registration, public demand and viewer response all **UNVERIFIED**. 666 English words at hypothetical 125–155 words/min yields 4.3–5.3 minutes before pauses; profile 1.10× does not provide measured timing.

**Marginal value:** 02→05 earns the extra length by supplying Hornby's and Baynes's two recorded decisions before Scott, not a list of friendly meetings. 05→10 includes farm scale, fuller buildup, camp life, military routine and post-verdict troop withdrawals, but audience attention may weaken after Scott's negotiated drawdown and especially in the camp chronology. **Author recommends 05m** as best causal Long; 02m and 10m unchanged and available. Independent reviewer may prefer old 05m, new 05m, 02m, 10m or none. Present exact texts blind before this author review, sources after first reading. No permission for production or three master runs.
