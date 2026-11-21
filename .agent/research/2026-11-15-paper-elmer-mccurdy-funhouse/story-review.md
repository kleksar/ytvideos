## Дополнение 2026-11-19 — 2 / 5 / 10 минут одной истории

**Baseline:** PR #120 head `9648f83b42fc0d46a29ad622934bcd76c9168684`; исходные `script.en.txt` Git blob `670e0891c8c07647353dc793b81fd20fd6c40e4f`, `script.ru.txt` blob `1eea171088c6c96cb712357475ca339793667852`. Root тексты и исходная 17-сценовая раскадровка сохранены побайтово. **Изменения:** полный 05m и 10m на двух языках, 02m точная копия Short. Не создан другой сюжет или PR. Exact hash каждой новой версии инвалидирует прежние timing/review/visual spans на *эту* версию.

### Готовые тексты, ссылки и хэши

| Цель / формат | Complete EN narration | Полный смысловой RU | EN words | Статус |
|---|---|---|---:|---|
| 02m / Short 9:16 | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 253 | Исходный текст сохранён |
| 05m / Long 16:9 | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 604 | **Рекомендована (предварительно)** |
| 10m / Long 16:9 | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1369 | Расширенная, уступает по темпу |

| Версия | EN SHA-256 | RU SHA-256 | Semantic paragraphs EN/RU |
|---|---|---|---|
| 02m | `2bd8745b5fc8de62f083c2304252aebad42de851de44ff36452002d7fc27be13` | `14ff329d2c231525efc3c926665aa9721db8c9798521faf80286c1d1891fd1dd` | 17/17 |
| 05m | `12d97afa3df633196c6d993cad37cdc2422bf82d3e08dcc72b91cb5b5548d6d3` | `6b0f4040eb84d0c47dc6e0a9a67e685eba9c777e9e4fadb17124c7183b988468` | 15/15 |
| 10m | `81a1fc67664ed3ed10ba19d6350623f75ad8f87a50910e9a29928832297c1411` | `968af0556f60fe478f1cfdc26bf05ed2e66807061a42f32ec2c41f269538c699` | 29/29 |

**Хронометраж оценочный**, не измеренный TTS. При 120–155 EN wpm без пауз: 02m ~1:38–2:07, 05m ~3:54–5:02, 10m ~8:50–11:24. Конечная канальная скорость 1.10×, паузы и Long end screen не измерены; 05m может оказаться короче целевых пяти минут, что нужно проверить после утверждения одного exact master. Long и Short подтверждены `channels/paper_detour/channel.json` main `0153e6c3965bb497e31e2f145bfb3cc8165ecb30`. Ни одна оценка не утверждает измеренных 2/5/10.

### Story maps и редакционная функция

**02m Short (unchanged).** В 1976-м ломается рука «манекена» → человеческая кость → 1924 penny + Museum of Crime tickets → имя McCurdy/гибель 1911 → ложные братья 1916 → карнавал → forensic skull comparison → захоронение 1977. Начало понятно без истории; ответ получен до `And that only happened because...`, возвращающего к действию съёмочной группы. Холодный вход, повтор EN/RU дважды и смысловой seam **только авторское text-only evidence**; реальный AV seam и независимый double read **UNVERIFIED**. Риск: переход между владельцами обобщён и финальная служебная связка.

**05m documentary Long.** Три вопроса «кто за манекеном / почему музейный билет / кто перевозил?» → съёмочная группа 1976, реальная кость → медицинские следы и билет как **основной hook** → Dan Sonney → 1911 грабёж, смерть → невостребованное тело и пять центов в рот → ложные братья Patterson 1916 → музей Sonney 1922 → утрата идентичности в funhouse → независимое подтверждение Clyde Snow → захоронение Guthrie 1977. Обобщённая середина после 1922-го слабее конкретных переходов. **Long loop N_A**.

**10m documentary Long.** Вопросы → 1976 body discovery → расследование → 1911 неудачные ограбления → похоронное бюро и плата → 1916 ложное родство → 1922 музей → 1928 Trans-American Footrace → фильм `Narcotic` с заведомо ложным образом зависимости → хранение после смерти Louis Sonney 1949 → `She Freak` 1967 → обесцененная восковая «декорация» → раздельная функция билета и skull comparison → похороны. Повороты подтверждены в едином research; ни вымышленной цитаты, ни мотива. **Long loop N_A**. Участок 1928–1967 может превратиться в каталог владельцев.

### Восемь критериев для каждой точной редакции

| Версия | Editorial criterion | Авторская оценка / конкретное основание |
|---|---|---|
| 02m | Интерес/значимость | **8** — Человеческая судьба, спрятанная за обычным манекеном |
| 02m | Начало | **9** — Сломанная рука и человеческая кость с первой реплики |
| 02m | Развитие/причина досмотреть | **8** — Кость → музейный билет → самозваные братья → погребение |
| 02m | Payoff | **8** — Опознание и захоронение показаны до петли |
| 02m | Свежесть угла | **6** — История неоднократно пересказана в EN Long |
| 02m | Визуальная выразительность | **8** — Кость, монета, билеты, аттракцион и могила |
| 02m | Естественность EN/RU | **7** — Естественные глаголы, но финал And that only happened because звучит как технический переход |
| 02m | Подтверждённый зрительский интерес | **UNVERIFIED** — Старые EN Long и Reddit не измеряют спрос на новый Short |
| 05m | Интерес/значимость | **8** — Дополнительно раскрыта эксплуатация тела как товара |
| 05m | Начало | **8** — Три содержательных вопроса перед конкретным действием 1976 года |
| 05m | Развитие/причина досмотреть | **8** — От судебных улик к экономике похоронного бюро, обману 1916 и музейной цепочке |
| 05m | Payoff | **8** — Сопоставление черепа с фото и похороны дают причинное закрытие |
| 05m | Свежесть угла | **6** — Тема известна, но фокус на причинных переходах |
| 05m | Визуальная выразительность | **8** — Бумажные миниатюры: морг, выставка, монета, архив, кладбище |
| 05m | Естественность EN/RU | **8** — Связный слуховой ритм и ограниченные оговорки; звуковой тест отсутствует |
| 05m | Подтверждённый зрительский интерес | **UNVERIFIED** — Own-channel CTR, retention и same-author Short comparables отсутствуют |
| 10m | Интерес/значимость | **8** — Тот же человек, плюс показ механизма смены рекламных биографий |
| 10m | Начало | **8** — Точные вступительные вопросы с последующими ответами |
| 10m | Развитие/причина досмотреть | **7** — 1911 ограбления, 1928 забег и 1930-е добавляют контекст, но 1949–1967 теряют динамику |
| 10m | Payoff | **8** — Форензика и похороны не уступают пяти минутам |
| 10m | Свежесть угла | **6** — Хронология экспоната не делает сам сюжет новым |
| 10m | Визуальная выразительность | **8** — Забег, киноафиши и воск дают разные визуальные задачи |
| 10m | Естественность EN/RU | **7** — Много имён, дат и повтор функции another owner |
| 10m | Подтверждённый зрительский интерес | **UNVERIFIED** — Публичные видеосчётчики не позволяют оценить вероятность удержания |


**Автор / confidence:** только авторская редакторская проверка точных прочитанных EN/RU; medium для драматургии и EN/RU, high для известности темы, low для спроса; independent reviewer НЕ получен. **Недостатки отдельно:** 02m — обобщена передача по шоу, петля звучит чуть служебно; 05m — общий период 1922–1976 и возможный недобор TTS; 10m — много дат и владений после уже понятного обмана, плюс меньше первичных документов.

**Разница 02→05:** реальный причинный смысл билета, более подробная история Паттерсонов и независимая криминалистика вместо телеграфных связок. **Разница 05→10:** неудачные ограбления, забег 1928, рекламная ложь `Narcotic`, кино/хранение 1967 — самостоятельные задокументированные события; после фильма главная функция каждого следующего звена повторяется и падает сюжетная ценность. Поэтому **предварительная рекомендация 05m Long**, а не максимальная длина; 02m остаётся сильной альтернативой для Short. Рекомендация НЕ approval.

### Hard checks (отдельно от баллов)

| Проверка | Реальный статус |
|---|---|
| Six complete EN/RU scripts | **PASS structural**, 17/17, 15/15, 29/29 EN/RU смысловых абзацев; SHA-256 выше по точным bytes |
| Новые факты | **AUTHOR FACT CHECK**, common research ниже, независимые архивные материалы не получены |
| Вступительные вопросы Long / payoff | **AUTHOR TEXT CHECK** по всем полным текстам; measured first-minute hook UNVERIFIED |
| Short literal seam и 2 полных цикла | Авторское text-only observation для root unchanged; не independent PASS; MP4 AV seam **UNVERIFIED** |
| Independent first-listener и bilingual reviewer | **UNVERIFIED**, подлинного `ytv-script-review-v1` не получено |
| Runtime / pin / acceptance | **EDITORIAL_CANDIDATE_UNREGISTERED**: реальный `ytv start`, verified review receipts, owner approval **NOT PERFORMED** |
| Existing storyboard | **Только** неизменённая 02m (17 старых сцен); Long нужна новая раскадровка с exact hashes |
| TTS, image, MP4, rights, CTR, retention | **NOT PERFORMED / UNVERIFIED** |

**Visual intent для Long (не готовая раскадровка):** 05m — бумажная миниатюра дома ужасов → улики в лаборатории → монета / музейный билет → похоронное бюро → владельцы карнавала → судебная сверка рентгена → могила; 10m добавляет неудачные ограбления, 1928 забег, 1930s кинотеатр, архив и склад, но не имитирует настоящие архивные фотографии. Число сцен должно следовать точному тексту и подтверждённым refs. Никаких media assets не создавалось.

**Следующий gate:** независимый first-listener, bilingual check, фактическая длительность будущего approved master, выбор владельца, затем поддерживаемая регистрация artifacts в pinned runtime. В этом GitHub-only доступе нельзя считать локальный `uv run ytv start` или реально создать reviewer session; не приписывать авторский review независимому. Нет production permissions.

---

# audience-first-v1 — Elmer McCurdy (authorial editorial card)

**Binding:** full EN narration is exact Git blob `670e0891c8c07647353dc793b81fd20fd6c40e4f` (`.agent/research/2026-11-15-paper-elmer-mccurdy-funhouse/script.en.txt`); RU Git blob `1eea171088c6c96cb712357475ca339793667852` (`.agent/research/2026-11-15-paper-elmer-mccurdy-funhouse/script.ru.txt`); reviewed on 2026-11-15 against the written text, not any audio. Base remote main `cc47270b107c503c08ec56d374c5075205bb752f`. Author: **this automation's single editorial author**, NOT independent reviewer. Methods: fact ledger / storyline re-read / EN+RU back-to-back text loop, no audience test. **Class: STRONG_CANDIDATE / experimentally hypothesized English Short demand**. Not an official ytv gate or authorization.

## Eight separate scores after full script

| Criterion | 1–10 or UNVERIFIED | Confidence | Specific evidence | Biggest drawback |
|---|---:|---|---|---|
| 1. Интерес и значимость | **8** | medium | Переход «декорация → человеческая кость» и вопрос об имени человека обращаются к аудитории true-story mysteries; документированная судьба экспоната добавляет человеческую цену. | Мрачный предмет оттолкнёт часть аудитории Paper; демография фактически не измерена. |
| 2. Честное начало | **9** | medium | «A TV crew tried to move a cowboy mannequin ... Its arm snapped off, exposing human bone.» — конкретный физический факт, не выдуманная угроза; задаёт загадку личности. | Шоковый кадр потребует не-графического бумажного решения; возможна повышенная чувствительность. |
| 3. Развитие и причина досмотреть | **8** | medium | Покрытие, мышьяк и рана → монета/билеты → сын владельца → мнимые братья-карнавальщики → переход к восковой фигуре. Каждый шаг меняет ответ на «как это произошло». | Ownership-переходы S013–S014 всё ещё сжаты, без отдельных проверенных персональных решений. |
| 4. Payoff | **8** | medium | После подтверждения личности и судьбы тела «In April 1977, McCurdy was finally buried in Oklahoma» даёт законченный и значимый результат, а не ещё одну справку. | Эмоциональный эффект мягче, чем у сильных спасательных историй #116/#113. |
| 5. Свежесть и отличие | **6** | high | Не повторяет сюжеты #116/#114/отказы; вместо простого факта — расследование и самозваные братья. | Elmer уже разобран Sam O'Nella, Thoughty2 и подкастами, поэтому сама история не новая. |
| 6. Визуальная выразительность | **8** | medium | Отломанная рука, улика-монета, билет, вывеска ярмарки, рентген/портрет и могила могут объяснить причинность именно изображением. | Без качественной бумажной глубины тела/музея сцены станут обычной иллюстрацией; реальные reference bytes ещё не проверены. |
| 7. Естественность EN/RU | **8** | medium | Разная длина фраз: «They called the police», «The undertaker let them take him...», предметные детали вместо слов «невероятно», точный смысл RU. | S008 задаёт дополнительный вопрос вслух, возможно чуть прямолинейно; реальный слуховой review и TTS недоступны. |
| 8. Подтверждённый зрительский интерес | **UNVERIFIED** | low | Два независимых EN Long + 2021 Reddit; Sam 12.84m приблизительно обычен для 2019, Thoughty2 ~369K ниже малого same-author baseline. Это не English Short evidence. | Ни Shorts-baseline, ни собственных retention/CTR/comments нет. Не присваиваем балл. |

No overall average, no fake probability of virality. Required editorial floor: criterion 1=8, criterion 3=8, criterion 4=8. These numbers are **self-evaluations**. The eighth is intentionally UNVERIFIED.

## Pre-script / post-script distinction

At shortlist stage: interest 8, beginning 9, development 8, payoff 8, freshness 6, visual expressiveness 8, **speech UNVERIFIED**, **demand UNVERIFIED**. Only after the exact EN/RU master above was written was speech given an author's 8. Zero external independent numerical scoring. This is one authored draft after one speech pass; no revision cycle and no hidden “independent” persona.

## Narrative audit with exact locations

- First public promise S001: a mannequin hides genuine human remains; audience needs **who, how, whether he can be identified**.
- S003–S006: paint/arsenic/wound establish age and mystery; 1924 penny and crime-museum tickets yield a traceable provenance and person who recognizes the exhibit.
- S007 + S008: identity revealed without artificially delaying the name; the question changes to why someone killed in 1911 was still a funhouse object.
- S009–S012: unattended funeral body → nickels → impostor brothers (new reversal) → carnival; each answers part of the current question.
- S013–S015: chain of owners and the mistaken wax-object status; separate forensic comparison confirms identity.
- S016: **full payoff on first pass** — burial in Oklahoma, 65 years after his death.
- S017→S001: return to the ordinary crew action that physically triggered rediscovery. Not a second withheld answer.

Point of possible attention loss: S013 is a summary; it is the weakest beat, and requires a brief transition rather than gratuitous invented trades. First EN line has no biographical dependency. Claim not made that all sixty-five years were spent as an unidentified mannequin. No author-imagined reactions, official quote or fabricated motives.

## Hard gates (separate, not part of the score)

| Check | Status | Exact scope and unresolved portion |
|---|---|---|
| Channel status/format | **PASS** author check | Paper Detour active ChannelSpec English short 1440×2560; future approval not implied |
| Key facts and chronology | **PASS** for claims in script against modern published secondary sources | HISTORY / Staab / Infobae with caveats in `research.md`; original case records **UNVERIFIED**, do not claim primary archive |
| No duplicate / owner refusal | **PASS** current remote title/tree scan | All PRs 1–119 and non-truncated main tree; does not imply full visual similarity review of past episodes |
| EN/RU semantic equivalence | **PASS (author only)** | 17 aligned narrative paragraphs: same names, date, coin/ticket, actors, cause, result, qualification. Independent translation reviewer **UNVERIFIED** |
| Natural text loop | **PASS (author only, full repeated script)** | Actual last EN `And that only happened because...` → first `A TV crew tried to move a cowboy mannequin in a California funhouse. Its arm snapped off, exposing human bone.`; RU `И всё это произошло только потому, что...` → `Съёмочная группа попыталась передвинуть ковбойский манекен в калифорнийском доме ужасов. Рука отломилась, а внутри оказалась человеческая кость.`. Ending expresses causal why of burial, opening supplies real crew discovery; no repeated reveal withheld. Entire 17-paragraph EN and entire 17-paragraph RU read twice in order; scene start after one cycle is not a cold-start dependency. **AV seam UNVERIFIED** without MP4 |
| Source rights and actual visual references | **UNVERIFIED for production** | External text paraphrased; no licensed photo or channel image bytes provided or generated; original paper plane actual reference must be verified in production |
| Scope permissions | **PASS** limited to text-only Draft | No merger, TTS, imagegen, render, provider call or upload. No user approvals |
| Independent first listener and `ytv-script-review-v1` | **UNVERIFIED** | No `sessions.independent` or equivalent permitted fresh reviewer in this host. Self-check cannot pass gate |
| Official runtime `ytv start` | **UNVERIFIED / NOT PERFORMED** | This host has GitHub connector, not local `uv run ytv start` with checkout/pinned `plan_summary/read_next`. Never invent run/receipts |
| Narration duration, timing, AV loop | **UNVERIFIED** | Word count 253; scene 4–6 s only placeholders; no actual voice/video |

**Author note:** two full textual sequences and their stitch were inspected; an independent reading must repeat these steps without this table/beat map and may reject the whole idea. The input EN blob above is the only version for which this scorecard applies. If EN changes, invalidate review, spans, storyboard and any guessed durations; save previous version.
