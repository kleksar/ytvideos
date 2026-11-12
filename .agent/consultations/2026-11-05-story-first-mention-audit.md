# First meaningful mention — procedure audit

- Date: 2026-11-05. Scope: discuss general story procedures and propose options; shared instructions and narration have not been changed.
- Trigger: the user asked who Nicolas Appert is at the opening of v12. His confectioner role appears only in paragraph 3. This is concrete reader feedback that the earlier model PASS did not resolve.
- Read: root AGENTS.md; bootstrap; storycraft; ChatGPT session; channel entry points and catalog/documentation routing. The canonical procedure already requires timely role/context, a name-to-X check, and first-listener review before scores. The issue is execution and verification, not a missing general principle.
- Consultation: Google Chrome, https://chatgpt.com/c/6aebe9fe-72c4-83eb-a814-332e0738d7da . Completed answer. GPT-6 was visibly selected but showed a usage limit; the available GPT-5.6 Sol was selected. Exact visible pre-send label: `5.6 Extra High`; menu effort label: `Extra High, 4 из 5`.
- Prior review URL inspected: https://chatgpt.com/c/6aebe682-0580-83eb-ae37-6ad13dc112f8 . It currently displays “Не удалось загрузить этот ответ.” Its earlier recorded PASS is preserved as history; its exact reasoning could not be recovered in this audit.

## Exact narrow request

Проведи узкий редакционный аудит общего сценарного процесса всех каналов. Пользователь заметил, что начало «В Бресте пища, приготовленная по способу Николя Аппера, три месяца хранилась…» вводит имя без роли: слушатель спрашивает «Кто такой Аппер?». Кондитерская профессия объясняется лишь в третьем абзаце. Ранее отдельная модель дала этому полному тексту PASS по понятности. Действующие правила уже требуют: не предполагать знания конкретной истории; вводить незнакомого человека через нужную для события роль при первом смысловом использовании; позднее пояснение не исправляет начало; автор временно заменяет незнакомое имя на X; независимый оценщик цитирует только опоры, доступные к данному моменту, и не заполняет пробел своим знанием. Рейтинг не отменяет конкретного сообщения пользователя «не понял». Не нужно механически объяснять все слова и давать биографии. Задача: выяви возможную причину такого ложного PASS, отделяя наблюдаемое от гипотезы; предложи 3 практических варианта общего улучшения процедуры для многих будущих сессий, с достоинствами и издержками; рекомендуй минимальный набор. Дай 2 коротких варианта нового входа на Аппере (первое упоминание с ролью либо имя позже после понятного действия), без новых исторических утверждений сверх кондитерской профессии и метода хранения пищи в закрытых стеклянных сосудах. Не переписывай весь сюжет, не выдавай проверку моделью за измеренное понимание аудитории и не предлагай обязательное определение каждого имени независимо от контекста. Ответ на русском.

## Completed answer retained

Consultant's conclusion: the local first-perception defect was probably not treated as a blocker. The model may have read the later role and evaluated the whole text retrospectively. This is a hypothesis; the precise cause cannot be established from the available prior response.

Observed: name without role at the opening; role in paragraph 3; user question; earlier model PASS; existing rule against late repair. Hypotheses: retrospective comprehension, excessive FAIL threshold, aggregate clarity hiding a local blocker, or treating the name as decorative despite its place in “по способу”.

Three proposed options:

1. A mandatory local gate at first meaningful use: is the participant's necessary role already clear when the name enters the event/causal explanation? If not, the overall PASS cannot close that gap. This does not require a biography or explanations for every name. Cost: distinguish a meaningful dependency from incidental names.
2. Review the opening in isolation before revealing the full text. Record who acts and what happens, then show the rest. This prevents late explanation from silently repairing first perception. Cost: another step; not necessary for every minor name.
3. A targeted name-to-X probe: what does the listener know about X at this moment? “X has some method” may be insufficient to establish a participant. Cost: noise if applied mechanically to all proper names.

Consultant recommendation: options 1 and 2; keep the X-probe within option 1. User feedback invalidates the blanket conclusion that there is no comprehension problem, while numerical ratings remain a separate result.

Suggested opening 1: “В Бресте пища, приготовленная по способу кондитера Николя Аппера, три месяца хранилась в закрытых стеклянных сосудах.”

Suggested opening 2: “В Бресте три месяца проверяли способ хранения пищи в закрытых стеклянных сосудах. Его предложил кондитер Николя Аппер.”

## Coordinator decisions and limits

- Implemented after the user's follow-up instruction: added the general audience-context requirement to root §11 and the operational checks to the canonical storycraft skill. Channel entry points already route through that owner, so no duplicated channel procedure was needed.
- The opening check now uses a fragment boundary before any later explanatory passage rather than an automatic 2–3 paragraph window. The evaluator records what it understood from that fragment before receiving the full text.
- Did not adopt consultant opening 2 verbatim: “three months tested” is stronger than the source-supported “stored for three months” account. Storage and inspection remain distinct.
- Revised the Appert opening in v13: “Кондитер Николя Аппер искал способ надолго сохранять продукты. В Бресте пища, приготовленная по его способу, три месяца хранилась…” The role and practical aim now precede the name's explanatory use.
- The v13 opening-only independent check remains pending. A Chrome tab opened for it exposed another task's unsent draft; it was left untouched and no check is claimed. The user's direct question already established the v12 comprehension gap.
- Optional stronger evidence remains an unprepared human listener's retelling; model review does not establish real audience comprehension.
