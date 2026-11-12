# Paper Detour 006 — сценарно-постановочный пакет v1.4

**Статус:** рабочая версия с условной человеческой линией P03 → P22 → P25 → P26 и её фактическими ограничениями; также внесены исправления независимого фактчека, визуального и операторского аудитов. Независимый обзор самой интеграции и техническая проверка композита ещё необходимы. Озвучка, новый звук и монтаж не созданы.

**Тайминги:** расчётные при 140 словах в минуту и исходных паузах; их нельзя воспринимать как фактическую синхронизацию. Все границы планов и удержания требуют пересмотра по реальному исполнению. Аудио можно генерировать только по прямому разрешению пользователя.

[Проверенный чистый текст](VO_EN_v1_3.txt) · [Режиссёрские исправления](DIRECTOR_CORRECTIONS_v1_3.md) · [Исходный пакет Pro v1.2](GPT_PRO_PACKAGE_v1_2.md) · [Независимый фактчек](../Research/INDEPENDENT_FACT_CHECK.md)

## Общие правила
- **typography:** Фирменные акценты строить по реальным бумажным PNG выпуска 001 и channels/paper_detour/brand/TYPOGRAPHY_STANDARD.md; существующие глифы переиспользовать, недостающие изготовить и визуально сверить. Подтверждённого полного цифрового шрифта нет. Source Sans 3 не является основой акцентов; для предметных служебных паспортов допустимо отдельное оформление с проверкой лицензии.
- **format:** 16:9; конкретный размер и FPS определить по отдельному активному и видимому проекту 006. 3840×2160/24 и 1920×1080/30 — предложения, а не подтверждённые параметры.
- **minimum_shot:** Каждый новый основной план ≥3 с, кроме прямо согласованных пользователем исключений. Бит не равен склейке; непрерывные планы из v1.3 помечены в картах. Проверить всю длительность после получения разрешённой речи.
- **layers:** Совместимые FG/MG/BG, независимое движение, контактные тени, достроенный фон, настоящие маски и непрерывное движущееся мягкое зерно включая титры. Общий зум не заменяет параллакс.
- **text_timing:** Акцент синхронизировать с произнесённым маркером, дать осмысленное полное открытие и читаемую остановку. Чаще один крупный акцент; два окна P51 допускают краткое перекрытие при проверенной читаемости.
- **sound:** До прямого разрешения пользователя не генерировать и не рендерить новый звук, в том числе озвучку, музыку, эффекты и пробы. Запланированные SFX — указания, не готовая звуковая дорожка.
- **continuity:** Paris 4 и PHerc. 1667 — отдельные модели и подписи. При замене сцен под маской сначала добиться полного покрытия. P50 — один мастер с пятью станциями и фоном с запасом; P52/P53 — одна модель 1667.
- **production_gates:** До финальных активов проверить беззвучные пробы P02, P12→P13, P41→P42, P50 и деформации P13/P35–P39; проверить альфу, контакты, края, свет, параллакс и чтение в движении. После аудио пересчитать и прослушать весь фильм.
- **provenance:** Архивный исходный ответ Pro: GPT_PRO_PACKAGE_v1_2.md и GPT_PRO_PRODUCTION_v1_2.json. Адресные исправления: DIRECTOR_CORRECTIONS_v1_3.md. Сценарий: VO_EN_v1_3.txt и независимый INDEPENDENT_FACT_CHECK.md.

- **human_thread:** P03 → P22 → P25 → P26: общий условный силуэт с узнаваемым профилем, пропорциями и срезанным углом отдельного основания; это графический мотив, не документальный портрет. Фигура, рука и телефон имеют отдельные слои и опоры. P03 отделяет студента и его телефон от модели 1667; в P22 фигура появляется без имени и телефона только при расширении сообщества после запуска конкурса. В P25 имя звучит вместе с подписью, в P26 показана последовательность: уведомление о цифровом участке → удалённый запуск → поездка → просмотр у парковки. Не выдумывать внешность, одежду, интерфейс, буквы, точный текст сообщений, маршруты, реплики или эмоции.

## Музыкальная драматургия M1–M6

Это план; любые новые звуки, включая пробы, требуют прямого разрешения пользователя.

Музыка задумана как **одна заказная или специально лицензированная композиция с шестью движениями**, без перезапуска на границе каждого абзаца. Это конкретное композиционное задание, а не утверждение, что готовая фонограмма уже существует или была прослушана. Мотив — редкие ноты D–A–C–E; гармония допускает неразрешённые интервалы, чтобы финал не звучал как окончательная разгадка всей библиотеки.

| Движение | Абзацы | Музыкальное решение | Переход |
|---|---|---|---|
| M1 | P01–P11 | Редкое мягкое фортепиано, тихий смычковый слой; ощущение пространства и хрупкости. Условный пульс 64 BPM, без навязчивого такта. | На входе почти тишина; к P12 добавить мягкую пульсацию за 3 с. |
| M2 | P12–P24 | Тихий щипковый рисунок и ненавязчивая зернистая перкуссия, 72 BPM. Геометрия получает движение, диктор остаётся главным. | Пульс не изображает работающий сканер. К P25 3 с постепенной смены плотности. |
| M3 | P25–P34 | Более живой, но тихий рисунок 76 BPM; на P31 расширение гармонии без победного удара. На P33 тёплые устойчивые ноты. | P34 уменьшает плотность; P35 начинает M4 через 3 с наложения. |
| M4 | P35–P42 | Сдержанный ритм 70 BPM, длинные низкие ноты и редкие верхние ответы. Выделить труд и сравнение доказательств. | На P41 не устраивать финальную фанфару. К P43 3 с раскрытия регистра. |
| M5 | P43–P48 | Открытые гармоники на объявлении, затем меньше инструментов; условный пульс 60 BPM. Ограничения слышны так же ясно, как достижение. | P48 не уходит в тревожную музыку. К P49 мягкий возврат начальной темы за 4 с. |
| M6 | P49–P53 и титры | Фортепиано и тёплый протяжный слой 64 BPM; у последней строки почти неподвижная гармония. | После последней фразы 2 с смысловой выдержки, затем тихая 20-секундная кода титров. |

**Фоли и акценты:** каждая карта содержит конкретный звук либо NONE. Звуки привязаны только к видимому действию: короткий контакт ложемента, остановка инструмента, натяжение нити, рамка, один тихий интерфейсный щелчок. Вулкан — один дальний низкий гул без голосов жертв. Нет бесконечного шороха бумаги, фонового листания, звона на каждой букве или звука «раскрытия» физического 1667.

**Микс:** диктор по центру, без искусственного «античного» эха. Фоли располагается по сценическому источнику и остаётся тише голоса. Музыка под речью приглушается плавно, без заметного насосного эффекта. Предварительная инженерная цель — интегральная громкость мастера около −16 LUFS и true peak не выше −1 dBTP; итог проверить на слух и измерителем после реальной записи, не считать это выполненной проверкой. Отдать отдельные стемы VO / MUSIC / SFX, 48 кГц, 24 bit WAV.

**Хронометраж:** см. текущие расчётные времена v1.3; точная длительность определится после получения разрешённой озвучки.

## Полный английский текст озвучки

On this table is what remains of a book. It is small enough to disappear inside your hand. Its surface is black, cracked, and folded into itself. Somewhere inside, ink still rests on papyrus. Touch the wrong layer, and the evidence may break away.

This particular object has already survived several attempts to open it. Some material was removed. Some fragments were preserved separately. What remains is a tight inner core, catalogued as Papyrus sixteen sixty-seven. The book that once surrounded it is no longer complete.

How do you read the words that remain without pulling their fragile surface apart? The answer will depend on X-rays, painstaking geometry, a student checking his phone, and people who can tell a Greek letter from a convincing mistake.

The story begins beneath Mount Vesuvius. In the year seventy-nine, the eruption buried the Roman town of Herculaneum. Near the town stood a villa containing a collection of papyrus rolls. Heat transformed the rolls into carbonized objects, preserving material that had become extraordinarily difficult to handle.

These books were sheets of papyrus joined into rolls, with writing arranged in columns. A reader gradually uncovered the next section. After the eruption, that familiar movement became dangerous. The writing surface remained inside, but it could no longer behave like a fresh sheet.

Excavators reached the villa in the eighteenth century. The dark rolls revealed that the building had contained a library. Recovering the objects created another problem: possession did not provide access. To read them, someone had to confront the layers.

Early methods sometimes sacrificed one surface to expose the next. Camillo Paderni cut rolls lengthwise. The exposed writing was copied, and material was scraped away to reveal the next layer. Text could be rescued in a drawing while the physical surface carrying it was being lost.

Antonio Piaggio developed a more controlled way to unwind the rolls, using a mechanism that lifted the delicate material gradually. He arrived in Naples in seventeen fifty-three. The following year, one successful opening revealed a work by Philodemus about music. Reading these scrolls has a history stretching back centuries.

Those efforts gave scholars real ancient texts. They also left damaged rolls, separated pieces, and difficult records of each intervention. The collection preserves the history of ancient writing and the history of attempts to reach it. Both shape what survives.

Papyrus sixteen sixty-seven carries that second history particularly clearly. A nineteenth-century opening attempt was unsuccessful. Anton Fackelmann tried again in nineteen sixty-nine. Another intervention followed in nineteen eighty-seven, using the Oslo method. Ten separated pieces were preserved in a frame. A rolled core remained.

The core is roughly eight centimetres high and two centimetres across. Its reduced height was already recorded in the eighteenth century. Later interventions further reduced the roll. Researchers cannot rewind this damage. They must work with the material that remains.

Computer scientist Brent Seales and his collaborators pursued another route. If an instrument could measure the layers inside a damaged manuscript, perhaps a computer could build a copy of their shape. The physical object could stay rolled while the copy was opened on a screen.

Computed tomography is the starting point. X-ray measurements from different angles are combined into a three-dimensional volume. Researchers can move through virtual slices of that volume. A cross-section reveals a compressed maze of nested surfaces, carrying the shape of the papyrus inside.

But a scan is only a measurement. It does not arrive with the pages neatly separated. The first task is to locate a writing surface and follow it through the volume. This is segmentation: deciding which parts of the three-dimensional data belong to the same piece of papyrus.

Imagine tracing a road through a crushed city. Neighbouring layers nearly touch; elsewhere, the surface tears or folds sharply. Follow the wrong route, and the computer can jump between parts of the sheet, scrambling the relationship between the marks.

Once a reliable surface has been traced, its digital geometry can be flattened. The coordinates change; the original does not move. A curved strip becomes a plane. Yet that unfolded surface can still look almost empty. Finding the page and finding the ink are different problems.

Much of the ink in these manuscripts is carbon-based. So is the papyrus after carbonization. In many scans, the writing produces only a subtle signal against its background. Increasing the contrast on a screen cannot simply turn every ambiguous texture into a trustworthy letter.

Virtual unwrapping already had an important success. A study published in twenty sixteen described Hebrew text recovered from a burned scroll at En-Gedi. Written on animal skin, its ink stood out more clearly in the scan. Herculaneum presented a harder imaging problem.

There were earlier claims at Herculaneum, too. Vito Mocella and colleagues reported letters inside rolled papyri in twenty fifteen. In twenty nineteen, Seales and colleagues argued that those readings had not yet been confirmed or developed into complete passages. Suggestive images needed stronger tests.

One promising approach began with fragments whose writing was already exposed. Researchers could photograph the ink, scan the same material, and align the two views. This created examples linking visible writing to subtle features in the X-ray data. A machine-learning model could learn from those correspondences.

The model estimated where ink might be present. Reading the language came later. Its images still needed checking against the scan, the surface geometry, and the judgment of specialists in ancient handwriting. An attractive output was a beginning, not a verdict.

In March twenty twenty-three, Seales, Nat Friedman, and Daniel Gross launched the Vesuvius Challenge. Scans, software, and prizes brought a wider community into the effort. Progress could come from someone improving the geometry, someone finding an imaging clue, or someone building a better way to detect ink.

The roll at the centre of the next breakthrough was Paris Four. It is a different object from sixteen sixty-seven, the damaged core on our table. Their stories connect through the methods. The words recovered from each must stay attached to that particular roll.

Looking through an already mapped section, Casey Handmer noticed a distinctive cracked texture. In places it seemed to form strokes. He shared the observation. It was a clue within data that other people had already scanned and segmented, and it gave the next person something specific to investigate.

Luke Farritor, a computer science student in Nebraska, marked examples and trained a model to seek the pattern elsewhere. He improved the model, then inspected another result. Each newly mapped section gave him another opportunity to test whether the clue held up.

Farritor later described receiving news of a new digital section while attending a birthday party in Omaha. He used his phone to start a remote run. After driving friends home, he checked the result near a parking garage. On the screen were more recognizable letters. The ancient object itself had stayed safely elsewhere.

One sequence was read as a Greek word associated with purple. The First Letters prizes were announced in October twenty twenty-three. A colour had become evidence that the signal could be followed. The inside was beginning to yield readable writing.

Youssef Nader produced another clear result from the same region using his own approach. He knew about the earlier findings and investigated the clue further. Different methods could now be compared. The question was whether those promising strokes could hold together as readable text.

Julian Schilliger worked on another essential part: making more of the wound surface available for analysis. Better segmentation exposed larger digital regions. For the grand prize, Nader, Farritor, and Schilliger combined their work. The readable image depended on geometry, ink detection, and the labour that connected them.

Judging required more than a striking picture. Specialists examined anonymized submissions while the technical team reproduced methods. The letters had to be distinguishable, without filling the gaps simply because a particular Greek sentence would make sense. The evidence had to support the reading.

On February fifth, twenty twenty-four, the organizers announced the winners of the twenty twenty-three grand prize. Nader, Farritor, and Schilliger shared the seven-hundred-thousand-dollar award. Their combined work had passed the examination. The object behind this breakthrough was still Paris Four.

At that point, the organizers estimated that about five percent of Paris Four had been unwrapped and read. Parts of multiple columns were visible. Most of the roll remained beyond reach, but there was enough writing to begin following an ancient argument.

The passages discuss pleasure and perception, with references to food and music. One question is whether scarcity makes something more enjoyable. The author resists the idea that rare food must automatically provide greater pleasure than food available in abundance. Across the damaged surface, a recognizably human disagreement had survived.

Paris Four still has no secure author or title. What survives gives us part of a text and its argument. A convincing story about who wrote it cannot substitute for the missing identification. That question remains open.

The next challenge was scale. Recovering patches does not mean every turn of a damaged roll can be followed. A collapsed layer, tear, or misleading junction can interrupt the path. The method had to work beyond the regions where it first succeeded.

Return to Papyrus sixteen sixty-seven. Could researchers trace the entire surviving surface inside this small core, then recover the writing across it? The task required continuity without concealment: follow what remained, while leaving the real losses and damage visible.

For the work released in twenty twenty-six, researchers used high-resolution scans from the European Synchrotron Radiation Facility in Grenoble. The improved measurements and reconstruction gave them a more detailed volume to work with. Paul Tafforeau and Alessandro Mirone helped develop and carry out the imaging at the facility.

Better data still needed patient work. The paper describes thirty-one windings and roughly twenty-five hours of manual annotation per winding, alongside computational tools. People checked the paths through the papyrus. Much of the achievement happened before a reader saw a sentence.

The ink detectors searched for local physical signals, without completing Greek sentences. That distinction matters, but it does not make every output correct. Weak signals, damaged surfaces, and mistakes in the geometry can still mislead. Every recovered image needs to be examined.

Federica Nicolardi led the papyrological work. Eight specialists examined the text, checking letterforms across renderings and their position on the papyrus. Readings were accepted through independent agreement or discussion. The computer supplied images; people remained responsible for reading and interpreting them.

A separate check came from Paris Four. In improved scans of that roll, ink deposits could be seen directly in the three-dimensional data. Projecting them onto the digital surface produced marks that matched the earlier reading. Another kind of physical evidence now supported what the previous images had shown.

That check belongs to Paris Four. It supports the approach, but does not independently certify every letter of sixteen sixty-seven. Each object needs its own geometry, images, and scholarly reading. Keeping those chains of evidence separate makes the result stronger.

On June twenty-fifth, twenty twenty-six, the team announced the complete virtual unwrapping of the surviving core of sixteen sixty-seven. The technical manuscript followed on arXiv two days later. The researchers reported a reconstructed writing surface extending across twenty-two columns or column-equivalents, with the surviving text available for close study.

Complete needs a boundary. This core preserves lower portions of the final columns of a larger roll. Missing material has not returned. A continuous reconstruction of what survives cannot become a complete copy of the original book.

Nor has every trace been securely read. Small regions in the first three columns remain without transcription. Gaps and uncertain letters persist elsewhere. These absences belong in the result. Filling them with confident-looking text would blur the distinction between recovery and invention.

What can be read points toward a philosophical discussion of ethics: human nature, action, practical wisdom, and moral progress. The researchers interpret the evidence as belonging to a Stoic context. In a preserved final column, they identify a reference to Aristocreon, associated with the Stoic philosopher Chrysippus.

A person named inside a book is not automatically its author. The author and title remain unknown. Scholars can now examine the surviving argument, compare interpretations, and disagree about what the damaged passages allow. Access to the evidence makes that conversation possible.

At the end of October twenty twenty-six, the work remains available as a preprint; publication in a peer-reviewed journal has not been confirmed. The specialists’ examination of the text is a different process. The published methods and readings remain open to further scrutiny.

A larger library waits behind this result. Reaching it means repeating the hard parts: measuring, tracing, checking, and reading. Some rolls will be harder. Some passages may stay lost. The achievement is a way to investigate writing while preserving the fragile object carrying it.

Generations of work brought the project here. Early scholars copied exposed writing. Conservators preserved objects and fragments. Imaging researchers made measurements. Programmers made surfaces and signals accessible. Papyrologists produced readings that others could examine. Each contribution made the next one possible.

The reward is unexpectedly intimate. In Paris Four, someone argues about pleasure. In sixteen sixty-seven, someone considers human conduct. Their names are uncertain; their pages are damaged. Parts of their thinking can enter a conversation again because enough physical traces survive to be questioned.

Look again at the black core. It has not become fresh papyrus. Its lost edges are still lost. The digital surface preserves that damage while making room for recoverable words. Reading has changed what we can know without undoing what happened.

For this surviving core, the successful new act of reading required a different kind of touch: a beam, a measured surface, and a careful decision about each mark. The roll stayed closed. Its surviving words no longer had to remain silent.

## Сквозная партитура — 53 абзаца / 230 речевых битов

### P01 · оценочно 00:00.0–00:19.2 · SET-A

**Реплика:** On this table is what remains of a book. It is small enough to disappear inside your hand. Its surface is black, cracked, and folded into itself. Somewhere inside, ink still rests on papyrus. Touch the wrong layer, and the evidence may break away.

**Цель и тип:** Зритель знакомится с маленьким повреждённым предметом, который всё ещё содержит недоступный текст. (fact model).

**Передний план:** Размытая кромка кремового стола снизу; она перекрывает нижние опоры ложемента.

**Средний план:** Модель сердцевины 1667 размером примерно 8 × 2 см лежит по диагонали на двух опорах индивидуального ложемента; бирка PHerc. 1667 справа, вне силуэта предмета. Позади ложемента, чуть левее сердцевины, в собственном пазу стоит отдельная вертикальная карточка масштаба с силуэтом взрослой ладони.

**Задний план:** Тёмные архивные полки на трёх плоскостях; тёплый боковой свет слева. Маленькая постоянная подпись STYLIZED MODEL.

**Перекрытия и опоры:** Кромка стола закрывает нижние опоры, но сердцевина отбрасывает контактную тень на ложемент. Карточка ладони находится за предметом и служит только масштабом; никакая рука его не берёт. Дополнение v1.3: Отдельная круглая непрозрачная заслонка должна закрыть весь экран до смены сцены; её видимая и скрытая геометрия подготовлены с запасом.

#### P01.B01 · оценочно 00:00.0–00:03.9

> On this table is what remains of a book.

**Кадр:** MS, три четверти сверху, предмет немного правее центра

**Камера:** Медленный наезд на 5 см.

**Действие:** Свет открывает край ложемента и чёрную сердцевину; бирка остаётся видимой. Предмет неподвижен.

**Акцент:** WHAT REMAINS · речевой маркер «what remains» · расчётное начало 00:01.7. Маска: Ближний бортик ложемента скрывает нижнюю часть букв; буквы поднимаются из-за него. Место: Слева внизу, на свободной поверхности стола. Уход: На последнем слове предложения буквы опускаются обратно за бортик.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P01.B02 · оценочно 00:03.9–00:07.7

> It is small enough to disappear inside your hand.

**Кадр:** WS, строго боковой вид стола и карточки масштаба

**Камера:** Статично после явной смены ракурса.

**Действие:** Плоская карточка ладони выдвигается вверх из собственной прорези позади ложемента; её основание остаётся в прорези. По высоте ладонь заметно больше сердцевины.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P01.B03 · оценочно 00:07.7–00:11.6

> Its surface is black, cracked, and folded into itself.

**Кадр:** ECU, косой взгляд на верхнюю треть модели

**Камера:** Проезд вправо на 2 см.

**Действие:** В боковом свете становятся различимы рваный край, трещины и тесные складки гладкой тёмной бумаги; поверхности не раздвигаются.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P01.B04 · оценочно 00:11.6–00:14.6

> Somewhere inside, ink still rests on papyrus.

**Кадр:** MS, верхний взгляд на модель справа и круглый учебный разрез слева; начало непрерывного плана B04–B05.

**Камера:** Плавное сближение к учебному разрезу без склейки; модель остаётся справа в глубине.

**Действие:** Кремовая круглая заслонка слева открывает отдельный увеличенный разрез с подписью SCHEMATIC. В нём видны две вложенные дуги и один тёмный след на поверхности; это не буква и не скан.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P01.B05 · оценочно 00:14.6–00:18.9

> Touch the wrong layer, and the evidence may break away.

**Кадр:** CU как конечный масштаб непрерывного плана B04–B05; учебный разрез слева, модель 1667 справа в глубине.

**Камера:** Завершить наезд B04 и удержать композицию до полного закрытия круглой заслонкой.

**Действие:** Условный бумажный указатель приближается к хрупкому краю разреза и останавливается до контакта. Ни разрез, ни модель не ломаются.

**Акцент:** FRAGILE EVIDENCE · речевой маркер «evidence may break away» · расчётное начало 00:17.1. Маска: Дуга увеличенного слоя скрывает буквы; они выходят из-за её нижнего края. Место: Нижняя левая четверть, под разрезом, без перекрытия следа. Уход: После читаемой остановки акцент остаётся на своей опоре; круглая непрозрачная заслонка закрывает разрез и буквы, затем весь кадр до склейки на P02.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Непрозрачная круглая заслонка полностью перекрывает кадр. Под перекрытием открыть более широкий ракурс модели 1667 в шкафу SET-D; бирка и опора остаются идентичными.

**Музыкальный замысел:** M1: начать с тихого низкого тона и редких нот мягкого фортепиано; не делать отдельного удара при появлении предмета.

**Активы:** A_CORE1667 — самостоятельная модель сердцевины 8 × 2 см; A_CRADLE1667 — ложемент с двумя опорами; A_TAG1667 — небольшая инвентарная бирка; A_HAND_SCALE — плоская карточка масштаба с безличным силуэтом ладони; A_LAYER_RISK — отдельный учебный разрез со следом и указателем; A_ARCHIVE_DEPTH — три плоскости полок; REV13_P01_SHUTTER — Отдельная круглая непрозрачная заслонка должна закрыть весь экран до смены сцены; её видимая и скрытая геометрия подготовлены с запасом..

**Граница достоверности:** Предмет здесь — стилизованная модель. Внутренний след показан только как SCHEMATIC, не как доступная наружному взгляду надпись. Возможность повреждения обозначена остановкой указателя; реальное повреждение не инсценируется.

**Источники:** S01, S02.

### P02 · оценочно 00:19.2–00:37.6 · SET-D

**Реплика:** This particular object has already survived several attempts to open it. Some material was removed. Some fragments were preserved separately. What remains is a tight inner core, catalogued as Papyrus sixteen sixty-seven. The book that once surrounded it is no longer complete.

**Цель и тип:** Зритель различает сохранившуюся сердцевину, отделённые фрагменты и утраченные части исходной книги. (evidence graphic).

**Передний план:** Левая стойка бумажного архивного шкафа и нижняя направляющая выдвижного лотка.

**Средний план:** Сердцевина 1667 в ложементе в правом отсеке; слева отдельная рама с десятью условными фрагментами. Над ними три пока не датированные ячейки истории вмешательств.

**Задний план:** Матовое охристое поле шкафа; постоянная подпись OBJECT HISTORY • SCHEMATIC. Бирка PHerc. 1667 принадлежит только правому ложементу.

**Перекрытия и опоры:** Каждая рама имеет собственную глубину и контакт с направляющей. Фрагменты лежат на подложке; их не притягивает обратно к сердцевине. Условный внешний контур исходного рулона стоит на отдельной прозрачной плоскости за сердцевиной. Дополнение v1.3: Две независимые ячейки и подвижная левая рама на направляющей; перекладина движется вместе с рамой и закрывает привязанный к ней текст. Ядро и бирка остаются на отдельной правой опоре.

#### P02.B01 · оценочно 00:19.2–00:23.9

> This particular object has already survived several attempts to open it.

**Кадр:** WS, фронтально на два отсека шкафа

**Камера:** Плавный проезд вправо на 6 см.

**Действие:** Три верхние ячейки последовательно открывают по одному одинаковому символу вмешательства; без людей, инструментов и дат. Сердцевина остаётся в правом отсеке.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P02.B02 · оценочно 00:23.9–00:25.6

> Some material was removed.

**Кадр:** MS, фронтальный непрерывный план двух отсеков шкафа.

**Камера:** Удержать общий ракурс; мягко сместить внимание к правому отсеку без склейки.

**Действие:** За ядром на отдельной плоскости появляется условный пунктирный контур и нейтральная заливка утраты с подписью LOST MATERIAL; схема не изображает момент утраты.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P02.B03 · оценочно 00:25.6–00:27.8

> Some fragments were preserved separately.

**Кадр:** MS, продолжение непрерывного плана B02 с двумя отсеками.

**Камера:** Мягко перевести внимание влево без смены ракурса; обе ячейки остаются различимы.

**Действие:** Левая рама выдвигается по направляющей до упора, открывая отдельные фрагменты; ядро остаётся на своей правой опоре.

**Акцент:** PRESERVED FRAGMENTS · речевой маркер «Some fragments» · расчётное начало 00:25.6. Маска: Верхняя непрозрачная перекладина левой рамы скрывает буквы; они поднимаются позади неё. Место: Свободное поле над левой рамой, вне ядра и бирок. Уход: После читаемой остановки опускаются за ту же перекладину в продолжающемся плане B04 до входа INNER CORE.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P02.B04 · оценочно 00:27.8–00:32.9

> What remains is a tight inner core, catalogued as Papyrus sixteen sixty-seven.

**Кадр:** MS, продолжение того же плана двух отсеков; ядро и бирка справа.

**Камера:** Мягко перевести внимание обратно вправо без склейки.

**Действие:** Выделить светом ядро и бирку PHerc. 1667; условный контур отдельно позади, рама фрагментов слева.

**Акцент:** INNER CORE · речевой маркер «tight inner core» · расчётное начало 00:29.5. Маска: Нижняя кромка инвентарной бирки скрывает буквы; они поднимаются за ней. Место: Свободная зона справа внизу, не поверх предмета и бирки. Уход: После читаемой остановки опустить за ту же кромку до следующей склейки.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P02.B05 · оценочно 00:32.9–00:37.2

> The book that once surrounded it is no longer complete.

**Кадр:** WS, весь шкаф, вид сверху под 45°

**Камера:** Статично после явного расширения кадра.

**Действие:** Сердцевина и отдельная рама остаются в разных ячейках; вокруг условного большого контура видны пустые участки. Ни одна из лакун не заполняется.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Камера останавливается на всём шкафу; жёсткая склейка на низкий боковой вид отдельного лабораторного учебного стола SET-F. Номер 1667 сохраняется только у миниатюры исходного предмета.

**Музыкальный замысел:** M1: продолжить тот же тихий слой; добавить одну редкую высокую ноту при показе отдельной рамы, без перезапуска темы.

**Активы:** A_CORE1667 — самостоятельная модель сердцевины 8 × 2 см; A_CRADLE1667 — ложемент с двумя опорами; A_TAG1667 — небольшая инвентарная бирка; D_CABINET1667 — шкаф с отдельными отсеками истории объекта; D_FRAGMENT_FRAME — рама с десятью условными сохранившимися кусками; D_LOSS_OUTLINE — отдельный условный контур утраченной массы рулона; REV13_P02_FRAME — Две независимые ячейки и подвижная левая рама на направляющей; перекладина движется вместе с рамой и закрывает привязанный к ней текст. Ядро и бирка остаются на отдельной правой опоре..

**Граница достоверности:** Схема не выдаёт размеры исчезнувших частей за измеренную реконструкцию. Отделённые фрагменты и утраченный материал не смешиваются; не утверждается, что все ранние попытки уничтожили всё снятое.

**Источники:** S01, S03.

### P03 · оценочно 00:37.6–00:55.3 · SET-F

**Реплика:** How do you read the words that remain without pulling their fragile surface apart? The answer will depend on X-rays, painstaking geometry, a student checking his phone, and people who can tell a Greek letter from a convincing mistake.

**Цель и тип:** Вопрос о сохранности раскрывается как задача измерения, вычисления и человеческой проверки. (explanatory metaphor).

**Передний план:** Три невысокие кремовые перегородки учебного стола, стоящие поперёк движения камеры.

**Средний план:** Слева модель 1667 в независимой ячейке PHYSICAL ORIGINAL; далее отдельные карточки луча, сетки, студента и стола чтения. Безымянный студент держит телефон с пустым экраном; отдельная перегородка отделяет его карточку от модели 1667.

**Задний план:** Тёплое чистое поле; над карточками одна маленькая подпись PROCESS PREVIEW • SCHEMATIC, без дат и имён.

**Перекрытия и опоры:** Карточки закреплены в отдельных пазах, передние перегородки перекрывают их в непрерывном проезде. Студент, его телефон и физическая модель 1667 не соединены. Это разные будущие этапы, а не одна встреча или один объект.

#### P03.B01 · оценочно 00:37.6–00:43.6

> How do you read the words that remain without pulling their fragile surface apart?

**Кадр:** MS, низкий боковой вид закрытой сердцевины и пустого пространства над ней

**Камера:** Медленный наезд на 4 см.

**Действие:** Над оригинальной моделью появляется светлый бумажный контур вопроса без букв внутри; его две дуги остаются сомкнутыми и не тянут физический предмет.

**Акцент:** READ WITHOUT OPENING · речевой маркер «without pulling» · расчётное начало 00:41.0. Маска: Передняя стенка ячейки PHYSICAL ORIGINAL скрывает буквы; они поднимаются наружу с отдельной задней направляющей. Место: Слева вверху от ложемента, в пустом фоне. Уход: Буквы уходят за первую перегородку при начале следующего проезда.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P03.B02 · оценочно 00:43.6–00:47.0

> The answer will depend on X-rays, painstaking geometry,

**Кадр:** WS, последовательность учебных карточек под 30°

**Камера:** Один непрерывный проезд вправо на 9 см.

**Действие:** Из-за первой перегородки последовательно открываются карточка условного луча и светлая искривлённая сетка. Оригинальная миниатюра остаётся видимой далеко слева; никакого раскрытия текста ещё нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P03.B03 · оценочно 00:47.0–00:49.1

> a student checking his phone,

**Кадр:** MS, продолжение того же проезда, карточка телефона

**Камера:** Продолжить тот же проезд вправо на 4 см.

**Действие:** В непрерывном проезде открывается карточка безымянного условного силуэта с общим профилем, пропорциями и срезанным углом отдельного основания. Отдельная рука держит телефон с пустым светлым экраном. Перегородка отделяет карточку от модели 1667; имени, сообщений, результатов и букв нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P03.B04 · оценочно 00:49.1–00:54.3

> and people who can tell a Greek letter from a convincing mistake.

**Кадр:** MS, финальная карточка стола чтения, три четверти

**Камера:** Замедлить тот же проезд вправо до остановки за 5 см.

**Действие:** Две прозрачные бумажные рамки сравнения сходятся над условным фрагментом; одна обводит устойчивый след, другая остаётся пустой. Следы абстрактны, не образуют греческих букв.

**Акцент:** HUMAN JUDGEMENT · речевой маркер «people who can tell» · расчётное начало 00:49.6. Маска: Ближняя рамка сравнения скрывает буквы, которые выдвигаются из-за её правого ребра. Место: В правой верхней четверти рядом со столом чтения. Уход: Все буквы закрывает вертикальная боковая стенка театра, проходящая перед объективом.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Боковая стенка полностью перекрывает изображение; из её охристого цвета открыть широкий силуэт Везувия в SET-B. Новый кадр сразу получает маркировку HISTORICAL RECONSTRUCTION.

**Музыкальный замысел:** M1: удержать лёгкое напряжение; на вопросе убрать верхние ноты, затем вернуть одну тонкую фактуру. Подъёма к ответу пока нет.

**Активы:** F_PREVIEW_STAGE — четыре учебные карточки в последовательных пазах; A_CORE1667 — самостоятельная модель сердцевины 8 × 2 см; F_PHYSICAL_BAY — отдельная ячейка исходного предмета; F_PREVIEW_BEAM — условный луч; F_PREVIEW_MESH — искривлённая бумажная сетка; F_PREVIEW_PHONE — безымянная карточка общего условного силуэта и отдельного телефона с пустым экраном; перегородка отделяет её от 1667; F_REVIEW_FRAMES — пара рамок сравнения без букв; MASTER_LUKE_SILHOUETTE — условный профиль, пропорции и срезанный угол основания; фигура и рука раздельно; MASTER_LUKE_PHONE — отдельный телефон с пустым экраном и опорой к руке.

**Граница достоверности:** PROCESS PREVIEW • SCHEMATIC: графический мотив не является портретом, конкретной встречей или местом. Студент не держит 1667 и не изучает его данные: его конкурсная работа относится к Paris 4. На телефоне нет сообщений, интерфейса и букв.

**Источники:** S01, S04.

### P04 · оценочно 00:55.3–01:15.3 · SET-B

**Реплика:** The story begins beneath Mount Vesuvius. In the year seventy-nine, the eruption buried the Roman town of Herculaneum. Near the town stood a villa containing a collection of papyrus rolls. Heat transformed the rolls into carbonized objects, preserving material that had become extraordinarily difficult to handle.

**Цель и тип:** Зритель понимает, почему свитки физически сохранились после извержения и стали труднодоступными. (historical reconstruction).

**Передний план:** Низкий тёмный рельеф берега слева и разрез грунта по нижнему краю.

**Средний план:** Условная римская городская застройка слева; отдельная вилла справа, не соединённая с конкретным историческим адресом. В учебном разрезе виллы три подноса с рулонами.

**Задний план:** Многослойный профиль Везувия, дымчато-кремовое небо, мягкий свет справа. Постоянная подпись HISTORICAL RECONSTRUCTION; на учебном разрезе дополнительно SCHEMATIC.

**Перекрытия и опоры:** Берег закрывает нижние основания домов. Передняя стенка виллы снимается только как отдельная учебная заслонка, не как физическое разрушение. Пепельные плоскости проходят перед и позади построек с согласованным параллаксом.

#### P04.B01 · оценочно 00:55.3–00:57.8

> The story begins beneath Mount Vesuvius.

**Кадр:** WS, низкий широкий вид с Везувием на заднем плане

**Камера:** Медленный боковой проезд вправо на 7 см.

**Действие:** Профиль вулкана проявляется между двумя передними слоями берега; город и вилла остаются маленькими относительно горы.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P04.B02 · оценочно 00:57.8–01:03.0

> In the year seventy-nine, the eruption buried the Roman town of Herculaneum.

**Кадр:** WS, тот же ландшафт с чуть более близкой средней плоскостью

**Камера:** Продолжить тот же проезд вправо на 4 см.

**Действие:** На произнесении года появляется маленькая фактологическая бирка AD 79. Серые пепельные слои постепенно закрывают нижнюю застройку; у вершины растёт широкий приглушённый столб.

**Акцент:** HERCULANEUM · речевой маркер «Herculaneum» · расчётное начало 01:02.6. Маска: Передняя гряда берега скрывает буквы; они поднимаются за грядой в небо слева от вулкана. Место: Верхняя левая четверть, вне пепельного столба. Уход: Пепельная передняя плоскость проходит перед буквами и закрывает их.

**Звуковой замысел:** На появлении первого пепельного слоя — один тихий дальний низкий гул, плавно затихающий к концу следующей фразы. (нового звука пока нет).

#### P04.B03 · оценочно 01:03.0–01:08.1

> Near the town stood a villa containing a collection of papyrus rolls.

**Кадр:** MS, разрез виллы справа, камера под 35°

**Камера:** Статично после склейки с явным изменением масштаба.

**Действие:** Условная передняя стенка виллы уходит в свой паз вниз, открывая три подноса с плотно лежащими рулонами. Нет владельца, читателя или сцены последних минут.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P04.B04 · оценочно 01:08.1–01:15.0

> Heat transformed the rolls into carbonized objects, preserving material that had become extraordinarily difficult to handle.

**Кадр:** CU, один учебный поднос с рулонами

**Камера:** Медленный наезд на 3 см.

**Действие:** Тёплый свет гаснет до угольного; сменная внешняя оболочка моделей становится тёмной и неровной под проходящей пепельной маской. Поднос и опоры не двигаются.

**Акцент:** CARBONIZED · речевой маркер «carbonized objects» · расчётное начало 01:10.3. Маска: Передняя стенка подноса скрывает буквы; они появляются за её правым краем. Место: Свободное поле справа от подноса. Уход: Буквы и поднос закрываются охристой горизонтальной плоскостью осадка.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Плоскость осадка заполняет кадр. Склейка на плоский кремовый учебный лист папируса сверху в SET-F; вместо исторической маркировки появляется SCHEMATIC.

**Музыкальный замысел:** M1: оставить низкий слой и сократить фортепиано на время глухого гула; затем вернуть прежнюю громкость без катастрофического музыкального удара.

**Активы:** B_VESUVIUS_PROFILE — многослойный профиль вулкана; B_COAST_RELIEF — передние береговые слои; B_ROMAN_BLOCKS — условная городская застройка; B_VILLA_CUTAWAY — условный разрез виллы с отдельной передней стенкой; B_ROLL_TRAYS — подносы с учебными рулонами; B_ASH_PLANES — мягкие пепельные и осадочные плоскости; B_DATE79 — небольшая бирка AD 79.

**Граница достоверности:** Схематический интерьер не заявлен точной археологической планировкой. Извержение показано через нагрев, пепел и отложения; лавы в библиотеке, людей в момент гибели и выдуманного владельца нет.

**Источники:** S05, S06.

### P05 · оценочно 01:15.3–01:34.5 · SET-F

**Реплика:** These books were sheets of papyrus joined into rolls, with writing arranged in columns. A reader gradually uncovered the next section. After the eruption, that familiar movement became dangerous. The writing surface remained inside, but it could no longer behave like a fresh sheet.

**Цель и тип:** Зритель понимает устройство книжного рулона и разницу между гибким папирусом и обугленным материалом. (fact model).

**Передний план:** Нижняя кремовая планка учебного планшета; справа отдельный тёмный бортик второй ячейки.

**Средний план:** Слева светлая учебная полоса папируса с видимыми соединениями листов и группами условных штрихов; справа отдельная обугленная модель в подставке.

**Задний план:** Спокойное тёплое поле; маленькие подписи SCHEMATIC, FRESH PAPYRUS слева и CARBONIZED MATERIAL справа.

**Перекрытия и опоры:** Две модели стоят на разных подложках и не превращаются одна в другую. Условные штрихи используются только в схеме. При движении полосы её конец проходит за настоящей боковой катушкой, а не исчезает произвольно.

#### P05.B01 · оценочно 01:15.3–01:21.3

> These books were sheets of papyrus joined into rolls, with writing arranged in columns.

**Кадр:** WS, строго сверху на левую учебную полосу

**Камера:** Статично.

**Действие:** Три прямоугольные секции сводятся краями на общей подложке; тонкие вертикальные швы показывают соединения. Группы абстрактных горизонтальных штрихов занимают отдельные колонки.

**Акцент:** COLUMNS · речевой маркер «columns» · расчётное начало 01:20.9. Маска: Правая вертикальная скрутка полосы скрывает буквы; они выходят из-за её внешнего края. Место: Справа над светлой полосой, вне строк. Уход: Буквы скользят обратно за вертикальную скрутку.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P05.B02 · оценочно 01:21.3–01:24.3

> A reader gradually uncovered the next section.

**Кадр:** CU, косой боковой вид свежей полосы и двух скруток

**Камера:** Плавный проезд влево на 3 см.

**Действие:** Левая скрутка медленно принимает небольшой участок полосы, правая отпускает следующий. Полоса натянута между опорами; контакты и направление движения согласованы. Реального древнего читателя нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P05.B03 · оценочно 01:24.3–01:27.8

> After the eruption, that familiar movement became dangerous.

**Кадр:** WS, обе ячейки сверху

**Камера:** Статично после смены масштаба.

**Действие:** Свет левой ячейки снижается. Тёмный бортик справа уходит вниз и открывает другую, угольную модель с неровными краями; она не раскручивается.

**Акцент:** FRAGILE SURFACE · речевой маркер «dangerous» · расчётное начало 01:27.3. Маска: Ближний тёмный бортик правой ячейки скрывает буквы до своего опускания. Место: Ниже правой модели, на пустой подложке. Уход: Буквы закрывает возвращающийся бортик в конце абзаца.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P05.B04 · оценочно 01:27.8–01:34.2

> The writing surface remained inside, but it could no longer behave like a fresh sheet.

**Кадр:** CU, торец обугленной модели под 20°

**Камера:** Медленный наезд на 2 см.

**Действие:** Отдельная кремовая рамка увеличения открывает нарисованные вложенные слои внутри; у внешнего слоя показана трещина. Изображение не пробует разгибать хрупкий край.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Правый бортик закрывает модель и поднимается до заполнения кадра; склейка на вертикальную стену земляного разреза раскопа SET-B, в новом широком масштабе.

**Музыкальный замысел:** M1: сохранить редкое фортепиано; при переходе между ячейками кратко оставить один низкий тон, не вводить новый музыкальный раздел.

**Активы:** F_PAPYRUS_STRIP — учебная светлая полоса с соединениями листов; F_ROLL_SUPPORTS — две неподвижные опоры для учебных скруток; F_COLUMN_MARKS — заведомо неалфавитные штрихи для схемы колонок; F_BURNT_COMPARISON — отдельная обугленная модель без инвентарного номера; F_LAYER_WINDOW — увеличивающая учебная рамка.

**Граница достоверности:** Разворачивается только модель свежего папируса. Обугленная модель остаётся закрытой. Не изображается конкретный читатель виллы или реальный письменный фрагмент; псевдогреческого текста нет.

**Источники:** S05, S06.

### P06 · оценочно 01:34.5–01:51.6 · SET-B

**Реплика:** Excavators reached the villa in the eighteenth century. The dark rolls revealed that the building had contained a library. Recovering the objects created another problem: possession did not provide access. To read them, someone had to confront the layers.

**Цель и тип:** Открытие библиотеки меняет вопрос с поиска предметов на возможность добраться до их содержания. (historical reconstruction).

**Передний план:** Две тёмные стенки условной подземной галереи, образующие узкий проход; позже передний край музейного лотка.

**Средний план:** Условный разрез виллы и несколько тёмных рулонов на неровной поверхности; два безликих силуэта стоят в глубине у прохода, не касаясь рулонов.

**Задний план:** Слои грунта и маленькая освещённая поверхность над тоннелем. На входе сцены HISTORICAL RECONSTRUCTION; отдельная календарная бирка 18TH CENTURY.

**Перекрытия и опоры:** Стенки галереи перекрывают часть условного интерьера и дают глубину; тела не проходят сквозь грунт. Поздний архивный лоток вводится отдельной склейкой, а не непрерывной переноской найденных предметов.

#### P06.B01 · оценочно 01:34.5–01:38.0

> Excavators reached the villa in the eighteenth century.

**Кадр:** WS, боковой разрез грунта и виллы

**Камера:** Медленный проезд вправо на 6 см.

**Действие:** Сквозь переднюю стенку галереи открывается участок условной виллы; силуэты остаются на уровне пола. Календарная бирка закреплена на верхнем грунтовом слое.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P06.B02 · оценочно 01:38.0–01:42.7

> The dark rolls revealed that the building had contained a library.

**Кадр:** MS, взгляд из прохода на группу тёмных рулонов

**Камера:** Медленный наезд на 4 см.

**Действие:** Передний контур галереи отступает за край кадра, открывая несколько раздельных рулонов; над ними освобождается пространство.

**Акцент:** A LIBRARY · речевой маркер «a library» · расчётное начало 01:41.8. Маска: Верхняя каменная перемычка тоннеля скрывает буквы; они опускаются из-за неё. Место: В верхнем свободном поле над предметами. Уход: Буквы закрывает затемняющая передняя стенка галереи перед следующей склейкой.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P06.B03 · оценочно 01:42.7–01:47.4

> Recovering the objects created another problem: possession did not provide access.

**Кадр:** WS, отдельный архивный лоток сверху, без исторических фигур

**Камера:** Статично после явной временной и пространственной склейки.

**Действие:** Подпись меняется на COLLECTION • SCHEMATIC. Лоток с неподвижными закрытыми моделями доезжает по направляющей до упора; пустая прямоугольная рамка чтения остаётся без текста.

**Акцент:** STILL CLOSED · речевой маркер «possession did not provide access» · расчётное начало 01:45.3. Маска: Передний борт лотка закрывает буквы; они поднимаются сзади него. Место: Под пустой рамкой чтения, не поверх рулонов. Уход: Буквы опускаются за борт, оставляя пустую рамку.

**Звуковой замысел:** В момент остановки лотка — один тихий деревянный стук направляющей. (нового звука пока нет).

#### P06.B04 · оценочно 01:47.4–01:51.3

> To read them, someone had to confront the layers.

**Кадр:** ECU, торец одного условного рулона, вид под углом

**Камера:** Медленный наезд на 2 см.

**Действие:** Узкий боковой свет обозначает вложенные края. В глубине не появляется ни буква, ни готовая страница; камера останавливается перед тёмным промежутком.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Тёмный промежуток торца заполняет центр; склейка на верхний вид другого условного рулона на методическом столе SET-C. Сразу видны GENERAL METHOD и RECONSTRUCTION; бирки 1667 нет.

**Музыкальный замысел:** M1: продолжить спокойную низкую фактуру; перед крупным торцом оставить короткое пространство без новых нот, сохранив фон.

**Активы:** B_EXCAVATION_SECTION — условный разрез грунта и галереи; B_EXCAVATOR_SILHOUETTES — два безликих силуэта без детализации одежды; B_DISCOVERY_ROLLS — самостоятельные закрытые модели рулонов; B_CENTURY_CARD — бирка 18TH CENTURY; D_COLLECTION_TRAY — архивный лоток с направляющей; F_EMPTY_READING_FRAME — пустая учебная рамка чтения.

**Граница достоверности:** Нет точной реконструкции комнаты, даты находки отдельного свитка, действий конкретного работника или сцены сжигания. Архивный лоток — отдельная объясняющая сцена, не мгновенный перенос находки.

**Источники:** S05, S06.

### P07 · оценочно 01:51.6–02:11.7 · SET-C

**Реплика:** Early methods sometimes sacrificed one surface to expose the next. Camillo Paderni cut rolls lengthwise. The exposed writing was copied, and material was scraped away to reveal the next layer. Text could be rescued in a drawing while the physical surface carrying it was being lost.

**Цель и тип:** Зритель видит цену раннего доступа к тексту: рисунок мог пережить саму поверхность, с которой его копировали. (documented-action reconstruction).

**Передний план:** Нижняя кромка методического стола; неглубокий лоток для снятого материала слева.

**Средний план:** Условная половина рулона на фиксированной подставке в центре; справа отдельный кремовый лист для копии; две нейтральные бумажные кисти рук без портрета.

**Задний план:** Тёмная стенка с маркировками GENERAL METHOD • RECONSTRUCTION и SCHEMATIC MARKS. Карточка CAMILLO PADERNI относится только к этапу разрезания; последующее копирование и снятие слоя показаны без приписывания исполнителя.

**Перекрытия и опоры:** Пластина режет отдельный условный рулон; лист и лоток стоят раздельно. Сменой нейтральных рук или фокуса не приписывать копирование и соскабливание Падерни. Модель не является PHerc. 1667. Дополнение v1.3: Отдельная широкая непрозрачная плоскость закрывает весь экран после ухода A COPY SURVIVES; она не является листом, повёрнутым ребром.

#### P07.B01 · оценочно 01:51.6–01:55.9

> Early methods sometimes sacrificed one surface to expose the next.

**Кадр:** CU, низкий взгляд на вложенные края условной половины рулона

**Камера:** Медленный боковой проезд вправо на 3 см.

**Действие:** Передний учебный край отодвигается, открывая следующий слой; оба края опираются на подставку. Изменение показано как схема общего метода.

**Акцент:** EXPOSE THE NEXT · речевой маркер «expose the next» · расчётное начало 01:54.6. Маска: Передний край условного слоя закрывает буквы; они выходят за его правый торец. Место: Внизу справа от подставки, вне поверхности. Уход: Буквы опускаются за переднюю кромку подставки до следующей склейки.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P07.B02 · оценочно 01:55.9–02:04.5

> Camillo Paderni cut rolls lengthwise. The exposed writing was copied, and material was scraped away to reveal the next layer.

**Кадр:** WS, строго сверху на рабочую зону

**Камера:** Статично после явной смены ракурса.

**Действие:** На отдельной условной модели режущая пластина проходит вдоль рулона; затем отдельный лист получает копию неалфавитных штрихов, а скребок сдвигает материал, открывая следующий слой. Не обозначать исполнителей копирования и соскабливания как Падерни; не связывать пример с конкретно 1667.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** На движении скребка — один очень тихий сухой скребущий звук, без повторов. (нового звука пока нет).

#### P07.B03 · оценочно 02:04.5–02:11.3

> Text could be rescued in a drawing while the physical surface carrying it was being lost.

**Кадр:** MS, вид из-за левой стороны лотка на лист копии справа

**Камера:** Плавный проезд вправо на 5 см.

**Действие:** Снятый материал остаётся в лотке слева, а лист с соответствующей группой условных штрихов поднимается на наклонную подставку справа. На исходной модели эта поверхность уже отсутствует.

**Акцент:** A COPY SURVIVES · речевой маркер «rescued in a drawing» · расчётное начало 02:05.7. Маска: Поднимаемый лист скрывает буквы за своим нижним краем; буквы становятся видны, когда лист занимает подставку. Место: Над правым краем листа, не поверх штрихов. Уход: Буквы прячутся за нижний край листа. Затем отдельная широкая непрозрачная плоскость проходит перед объективом и полностью закрывает кадр.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Отдельная широкая непрозрачная плоскость полностью закрывает кадр; под ней склейка на вертикальную стойку механизма Piaggio. Карточка Paderni исчезает вместе с предыдущей сценой.

**Музыкальный замысел:** M1: продолжить прежний низкий слой, без обвинительного или страшного музыкального акцента; дать скребущему звуку короткое свободное место.

**Активы:** C_PADERNI_SAMPLE — условный рулон для общего метода, без номера 1667; C_METHOD_HANDS — безличные кисти рук на одной плоскости рабочего пространства; C_CUTTING_PLATE — условная режущая пластина; C_SCRAPER — условный скребок; C_REMOVAL_TRAY — лоток снятого материала; C_COPY_SHEET — отдельный лист с неалфавитными учебными штрихами; C_PADERNI_LABEL — карточка имени и маркировок; REV13_P07_TRANSITION — Отдельная широкая непрозрачная плоскость закрывает весь экран после ухода A COPY SURVIVES; она не является листом, повёрнутым ребром..

**Граница достоверности:** Падерни приписано только разрезание. Копирование и снятие материала показаны без указания конкретного исполнителя; общий метод не привязан к 1667. Реконструкция условная, штрихи не являются греческим текстом.

**Источники:** S05.

### P08 · оценочно 02:11.7–02:33.0 · SET-C

**Реплика:** Antonio Piaggio developed a more controlled way to unwind the rolls, using a mechanism that lifted the delicate material gradually. He arrived in Naples in seventeen fifty-three. The following year, one successful opening revealed a work by Philodemus about music. Reading these scrolls has a history stretching back centuries.

**Цель и тип:** Управляемое натяжение позволило читать часть свитков задолго до компьютеров, сохраняя ограничения физического раскрытия. (documented-action reconstruction).

**Передний план:** Тонкая передняя стойка учебного механизма слева и поперечина внизу.

**Средний план:** Другой условный рулон в опоре; над ним вертикальная рама с несколькими натянутыми нитями и отдельной поддерживающей полосой, поднимающей край. Справа закреплённая карточка ANTONIO PIAGGIO.

**Задний план:** Охристая стенка, две маленькие исторические бирки NAPLES • 1753 и 1754, пока закрытые заслонками. Постоянные подписи RECONSTRUCTION и SCHEMATIC MECHANISM.

**Перекрытия и опоры:** Нити физически соединяют раму и поддерживающую полосу; поднимаемый край остаётся соединён с рулоном и поддержан снизу. Рама не изображает точную копию без чертежа. Исторические карточки открываются собственными заслонками.

#### P08.B01 · оценочно 02:11.7–02:16.4

> Antonio Piaggio developed a more controlled way to unwind the rolls,

**Кадр:** MS, три четверти на раму и поддержанный рулон

**Камера:** Медленный наезд на 4 см.

**Действие:** Нити постепенно натягиваются, а поддерживающая полоса поднимает самый край модели на несколько миллиметров. Из рулона не возникает большой целый лист.

**Акцент:** CONTROLLED TENSION · речевой маркер «more controlled» · расчётное начало 02:13.4. Маска: Ближняя вертикальная стойка механизма скрывает буквы; они выходят за её правый край. Место: Справа вверху, вне нитей и рабочего края. Уход: Буквы возвращаются за стойку на следующей фразе.

**Звуковой замысел:** В момент натяжения нитей — один тихий короткий звук натянутой нити, без скрипа механизма. (нового звука пока нет).

#### P08.B02 · оценочно 02:16.4–02:20.2

> using a mechanism that lifted the delicate material gradually.

**Кадр:** CU, рабочий край, продолжение того же ракурса

**Камера:** Продолжить тот же наезд ещё на 2 см.

**Действие:** Край модели поднимается ещё на несколько миллиметров, пока основная масса остаётся в опоре; видны контакт поддерживающей полосы и угол натяжения нитей.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P08.B03 · оценочно 02:20.2–02:23.2

> He arrived in Naples in seventeen fifty-three.

**Кадр:** WS, механизм слева и историческая карточка справа

**Камера:** Статично после явной смены масштаба.

**Действие:** Маленькая заслонка справа открывает NAPLES • 1753. Никакая сцена приезда, карета или порт не инсценируются.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P08.B04 · оценочно 02:23.2–02:28.8

> The following year, one successful opening revealed a work by Philodemus about music.

**Кадр:** MS, отдельная полка результата справа от механизма

**Камера:** Плавный проезд вправо на 6 см.

**Действие:** Вторая заслонка открывает 1754; на полке лежит отдельный условный раскрытый фрагмент. Над ним появляется фактическая карточка PHILODEMUS • WORK ON MUSIC, без греческого текста и музыкальных нот на папирусе.

**Акцент:** ABOUT MUSIC · речевой маркер «about music» · расчётное начало 02:28.0. Маска: Край полки и задняя карточка 1754 образуют реальную маску; буквы поднимаются из-за полки. Место: В свободном нижнем правом поле, ниже фактической карточки. Уход: Буквы опускаются за полку перед расширением кадра.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P08.B05 · оценочно 02:28.8–02:32.7

> Reading these scrolls has a history stretching back centuries.

**Кадр:** WS, весь методический стол и две исторические карточки

**Камера:** Медленный отъезд на 5 см.

**Действие:** В кадре одновременно остаются механизм, поддержанный материал и полка прочитанного результата; к ним присоединяется нейтральная горизонтальная линия времени, уходящая за правую стенку.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Линия времени упирается в правую стенку; склейка на широкий архивный шкаф SET-D с несколькими раздельными видами сохранившегося материала. Масштаб и высота камеры меняются.

**Музыкальный замысел:** M1: слегка высветлить гармонию на успешном чтении о музыке, сохраняя медленный темп; не включать отдельную мелодию как будто музыку древнего произведения.

**Активы:** C_PIAGGIO_SCHEME — собственная объясняющая рама с натянутыми нитями; C_PIAGGIO_SUPPORT — поддерживающая полоса и опора условного рулона; C_PIAGGIO_LABEL — карточка имени; C_NAPLES1753 — историческая бирка; C_MUSIC1754 — отдельная полка результата 1754; C_WORK_MUSIC — фактическая карточка Philodemus / work on music; D_HISTORY_LINE — нейтральная линия времени.

**Граница достоверности:** Не точная музейная реплика механизма. Не приписывать этот метод 1667 и не показывать его безопасным для всех свитков. Результат 1754 изображён отдельным условным фрагментом; никаких изобретённых древних нот или цитат.

**Источники:** S05, S06.

### P09 · оценочно 02:33.0–02:50.5 · SET-D

**Реплика:** Those efforts gave scholars real ancient texts. They also left damaged rolls, separated pieces, and difficult records of each intervention. The collection preserves the history of ancient writing and the history of attempts to reach it. Both shape what survives.

**Цель и тип:** Сохранившаяся коллекция несёт следы и древней письменности, и последующих попыток её прочесть. (evidence graphic).

**Передний план:** Две вертикальные стойки шкафа; выдвижная передняя рамка ниже уровня основных материалов.

**Средний план:** Три ячейки: условный открытый фрагмент слева, закрытый повреждённый рулон в центре, пачка карточек истории справа. У каждой ячейки своя подложка.

**Задний план:** Тёплое поле с двумя параллельными заголовками ANCIENT WRITING и LATER INTERVENTIONS. Постоянная подпись COLLECTION MODEL • SCHEMATIC.

**Перекрытия и опоры:** Рамки удерживаются стойками и направляющими. Карточки истории не накладываются на папирус как будто его часть. Две линии истории проходят по задней стенке, не прорезают физические предметы.

#### P09.B01 · оценочно 02:33.0–02:36.0

> Those efforts gave scholars real ancient texts.

**Кадр:** MS, левая ячейка, вид чуть сверху

**Камера:** Медленный проезд вправо на 3 см.

**Действие:** Левая рамка отходит в паз и открывает условный фрагмент с группами неалфавитных штрихов; маленькая подпись фиксирует RECOVERED TEXT • DIAGRAM.

**Акцент:** ANCIENT TEXTS · речевой маркер «real ancient texts» · расчётное начало 02:34.7. Маска: Верхняя перекладина левой рамки скрывает буквы; они поднимаются над ней. Место: Слева вверху, на пустом поле шкафа. Уход: Буквы закрывает следующая стойка по ходу проезда.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P09.B02 · оценочно 02:36.0–02:41.6

> They also left damaged rolls, separated pieces, and difficult records of each intervention.

**Кадр:** WS, все три ячейки в одном кадре

**Камера:** Продолжить проезд вправо на 6 см.

**Действие:** Открываются отдельный повреждённый рулон, несколько фрагментов на собственных подложках и карточки с нейтральными полями DATE / METHOD / CONDITION; конкретных выдуманных записей нет.

**Акцент:** ALTERED OBJECTS · речевой маркер «damaged rolls» · расчётное начало 02:37.3. Маска: Передний край центральной подложки скрывает буквы; они выходят вперёд и вверх из-за него. Место: Ниже центральной ячейки, не поверх повреждений. Уход: Буквы опускаются за подложку при переходе к двум линиям.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P09.B03 · оценочно 02:41.6–02:48.4

> The collection preserves the history of ancient writing and the history of attempts to reach it.

**Кадр:** WS, фронтальный план шкафа; обе исторические линии и рамка фрагмента видны вместе.

**Камера:** Медленно приблизить внимание к рамке фрагмента без смены плана.

**Действие:** Две линии истории письма и вмешательств остаются раздельными; рамка с условным фрагментом удерживается на собственной опоре.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P09.B04 · оценочно 02:48.4–02:50.2

> Both shape what survives.

**Кадр:** WS/MS, непрерывное продолжение B03 с видимой деталью рамки.

**Камера:** Продолжить плавное сближение B03 без склейки; не терять обе линии.

**Действие:** На той же рамке боковой свет выделяет край условного фрагмента; обе исторические линии остаются видны.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Жёсткая склейка на новый общий план конкретного шкафа 1667; номер 1667 впервые в этом переходе читается полностью, а обобщённые карточки исчезают.

**Музыкальный замысел:** M1: удержать светлую, но сдержанную гармонию после Piaggio; на короткой последней фразе не добавлять нот.

**Активы:** D_COLLECTION_CABINET — архивный шкаф с тремя раздельными ячейками; D_OPEN_FRAGMENT_MODEL — условный открытый фрагмент; D_DAMAGED_ROLL_MODEL — отдельная повреждённая модель без номера; D_INTERVENTION_CARDS — пустые учебные поля истории; D_TWO_HISTORY_LINES — две линии с фактическими заголовками.

**Граница достоверности:** Это схема состава и истории собрания, не факсимиле конкретных архивных записей. Условные следы письма не названы реальной транскрипцией. Ни один неизвестный фрагмент не приписан 1667.

**Источники:** S05, S06, S01.

### P10 · оценочно 02:50.5–03:09.7 · SET-D

**Реплика:** Papyrus sixteen sixty-seven carries that second history particularly clearly. A nineteenth-century opening attempt was unsuccessful. Anton Fackelmann tried again in nineteen sixty-nine. Another intervention followed in nineteen eighty-seven, using the Oslo method. Ten separated pieces were preserved in a frame. A rolled core remained.

**Цель и тип:** Биография 1667 становится конкретной последовательностью документированных попыток и сохранившихся результатов. (evidence graphic).

**Передний план:** Нижняя направляющая шкафа и три широкие вертикальные заслонки над временной шкалой.

**Средний план:** Неподвижная сердцевина 1667 в правом ложементе; слева рама с десятью условными кусками, пока частично закрытая. На средней высоте три карточки:1800s,1969,1987.

**Задний план:** Матовое поле шкафа; подписи PHerc. 1667 и OBJECT HISTORY • SCHEMATIC. Вся шкала прикреплена к одной задней поверхности.

**Перекрытия и опоры:** Заслонки закрывают отдельные даты, а не физический свиток. Появление карточки не меняет размеры сердцевины. Десять фрагментов лежат в одной собственной раме на направляющей.

#### P10.B01 · оценочно 02:50.5–02:54.4

> Papyrus sixteen sixty-seven carries that second history particularly clearly.

**Кадр:** WS, фронтально на весь шкаф 1667

**Камера:** Медленный проезд вправо на 4 см.

**Действие:** Открывается общая инвентарная бирка; зритель снова узнаёт тот же ложемент и отдельную раму, показанные в начале.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P10.B02 · оценочно 02:54.4–02:56.9

> A nineteenth-century opening attempt was unsuccessful.

**Кадр:** MS, начало временной шкалы, продолжение общего проезда

**Камера:** Продолжить проезд вправо на 3 см.

**Действие:** Первая заслонка открывает 1800s и небольшую подпись UNSUCCESSFUL ATTEMPT. Инструмента и человека у объекта нет.

**Акцент:** OPENING ATTEMPTS · речевой маркер «opening attempt» · расчётное начало 02:55.2. Маска: Первая вертикальная заслонка скрывает буквы; они выдвигаются из-за её бокового края. Место: Над шкалой слева, вне даты. Уход: Буквы закрывает вторая заслонка по ходу проезда.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P10.B03 · оценочно 02:56.9–02:59.9

> Anton Fackelmann tried again in nineteen sixty-nine.

**Кадр:** MS, середина той же шкалы

**Камера:** Продолжить проезд вправо на 3 см.

**Действие:** Вторая заслонка открывает 1969 и имя ANTON FACKELMANN. Карточка не иллюстрирует незафиксированный момент процедуры.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P10.B04 · оценочно 02:59.9–03:04.2

> Another intervention followed in nineteen eighty-seven, using the Oslo method.

**Кадр:** MS, правый конец шкалы

**Камера:** Продолжить проезд вправо на 4 см.

**Действие:** Третья заслонка открывает 1987 и OSLO METHOD. Из её нижней кромки идёт тонкая схема связи к отдельной раме, не к исчезающим слоям.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P10.B05 · оценочно 03:04.2–03:07.7

> Ten separated pieces were preserved in a frame.

**Кадр:** MS, шкала и рама в одном ракурсе

**Камера:** Плавно снизить камеру на 3 см, сохраняя горизонтальный ракурс.

**Действие:** Рама с ровно десятью различимыми условными кусками выдвигается до упора. Формы кусков нейтральные, не повторяют музейное фото.

**Акцент:** PRESERVED PIECES · речевой маркер «Ten separated pieces» · расчётное начало 03:04.2. Маска: Верхняя кромка выдвигаемой рамы скрывает буквы; они поднимаются из-за неё после остановки. Место: Над рамой, ниже шкалы и вдали от отдельных кусков. Уход: Буквы опускаются за раму на следующей короткой фразе.

**Звуковой замысел:** При достижении рамой упора — один мягкий стук дерева. (нового звука пока нет).

#### P10.B06 · оценочно 03:07.7–03:09.4

> A rolled core remained.

**Кадр:** MS, тот же непрерывный план, сердцевина справа полностью видна

**Камера:** Статично.

**Действие:** Световой акцент возвращается к неподвижной сердцевине; рама и все даты остаются в кадре. Никакого раскрытия или уменьшения объекта.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Склейка с общего шкафа на верхний крупный вид сердцевины и двух измерительных карточек в том же отсеке; изменение ракурса явное, положение бирки сохранено.

**Музыкальный замысел:** M1: продолжить ровный слой без драматических ударов на датах; инструментальная плотность постепенно уменьшается перед объяснением размеров.

**Активы:** D_CABINET1667 — шкаф с отдельными отсеками истории объекта; A_CORE1667 — самостоятельная модель сердцевины 8 × 2 см; A_CRADLE1667 — ложемент с двумя опорами; A_TAG1667 — небольшая инвентарная бирка; D_FRAGMENT_FRAME — рама с десятью условными сохранившимися кусками; D_1667_TIMELINE — три документированные карточки 1800s/1969/1987; D_TIMELINE_SHUTTERS — три независимые заслонки.

**Граница достоверности:** Для первой попытки указан только XIX век; не придуманы дата, исполнитель или scorzatura. 1969 — Fackelmann;1987 — Oslo method. Рама содержит десять условных фрагментов; их точная форма не заявлена.

**Источники:** S01, S03.

### P11 · оценочно 03:09.7–03:27.2 · SET-D

**Реплика:** The core is roughly eight centimetres high and two centimetres across. Its reduced height was already recorded in the eighteenth century. Later interventions further reduced the roll. Researchers cannot rewind this damage. They must work with the material that remains.

**Цель и тип:** Размеры и ранняя утрата части свитка задают предел тому, что современное исследование может вернуть. (evidence graphic).

**Передний план:** Нижняя планка измерительного планшета; тонкая передняя заслонка исторической карточки слева.

**Средний план:** Сердцевина 1667 в том же ложементе; вдоль её оси линейка 8cm, поперёк торца отдельная скоба 2cm, обе без контакта с материалом.

**Задний план:** Слева прикреплённая карточка 1782 с условным боковым силуэтом сохранившегося объекта; справа пустое поле утрат. Постоянная подпись DIMENSIONS • SCHEMATIC.

**Перекрытия и опоры:** Измерительные карточки закреплены на планшете, а не на сердцевине. Исторический силуэт лежит на отдельной задней плоскости и не сливается с современным физическим объектом.

#### P11.B01 · оценочно 03:09.7–03:14.4

> The core is roughly eight centimetres high and two centimetres across.

**Кадр:** CU, вид сверху вдоль оси лежащей сердцевины

**Камера:** Статично.

**Действие:** На словах о высоте открывается продольная шкала 8cm; на словах о ширине — поперечная скоба 2cm. Метки показывают приблизительный размер, не измерение реального музейного объекта.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P11.B02 · оценочно 03:14.4–03:18.7

> Its reduced height was already recorded in the eighteenth century.

**Кадр:** MS, измерительный планшет и карточка 1782 слева

**Камера:** Медленный проезд влево на 4 см.

**Действие:** Заслонка открывает 1782 и небольшой силуэт с той же высотой; тонкая линия сопоставляет только высоту двух отдельных изображений.

**Акцент:** ALREADY REDUCED · речевой маркер «already recorded» · расчётное начало 03:16.2. Маска: Передняя заслонка карточки 1782 скрывает буквы; они выходят из-за её верхнего края. Место: Над исторической карточкой, не поверх даты или линии. Уход: Буквы опускаются за карточку после следующей фразы.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P11.B03 · оценочно 03:18.7–03:21.3

> Later interventions further reduced the roll.

**Кадр:** MS, тот же планшет

**Камера:** Статично.

**Действие:** За современной сердцевиной открывается отдельный более широкий условный контур прежнего состояния. Подпись DIAGRAM фиксирует, что это сравнение; реальная модель не сжимается и верх не отрезается.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P11.B04 · оценочно 03:21.3–03:23.4

> Researchers cannot rewind this damage.

**Кадр:** CU, рваный край современной модели и пустое поле справа

**Камера:** Медленный наезд на 2 см.

**Действие:** Контур прежнего состояния закрывает маленькая непрозрачная заслонка; пустоты возле нынешнего края остаются пустыми, никакой обратной сборки не происходит.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P11.B05 · оценочно 03:23.4–03:26.9

> They must work with the material that remains.

**Кадр:** MS, модель в ложементе, три четверти

**Камера:** Статично после смены ракурса.

**Действие:** Измерительные карточки тихо убираются в свои пазы, оставляя только сохранившуюся сердцевину и её бирку.

**Акцент:** WHAT REMAINS · речевой маркер «material that remains» · расчётное начало 03:25.6. Маска: Ближний край измерительного планшета скрывает буквы; они поднимаются за ним. Место: Внизу слева от ложемента. Уход: Буквы уходят за переднюю планку; та заполняет нижнюю половину кадра и задаёт переход.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Передняя планка проходит вверх как физическая маска; открывается новый широкий современный рабочий стол SET-H с бумажной моделью экрана. Оригинальная сердцевина далее существует в отдельной учебной ячейке, не в руках учёного.

**Музыкальный замысел:** M1: оставить редкие низкие ноты и постепенно убрать смычковую фактуру; подготовить M2, но не начать её до следующего абзаца.

**Активы:** A_CORE1667 — самостоятельная модель сердцевины 8 × 2 см; A_CRADLE1667 — ложемент с двумя опорами; A_TAG1667 — небольшая инвентарная бирка; D_DIMENSION_BOARD — планшет с продольной и поперечной шкалами; D_1782_HEIGHT — отдельная историческая карточка 1782; D_EARLIER_DIAMETER — условный сравнительный контур прежнего диаметра.

**Граница достоверности:** Высота рулона — длина вдоль его оси, даже когда модель лежит. Потеря верхней части не приписана вмешательствам 1969/1987; ранняя высота отмечена отдельно. Не восстанавливаются неизвестные размеры первоначальной античной книги.

**Источники:** S01, S02.

### P12 · оценочно 03:27.2–03:46.8 · SET-H

**Реплика:** Computer scientist Brent Seales and his collaborators pursued another route. If an instrument could measure the layers inside a damaged manuscript, perhaps a computer could build a copy of their shape. The physical object could stay rolled while the copy was opened on a screen.

**Цель и тип:** Главный принцип нового подхода — работать с измеренной цифровой формой, оставляя физический свиток закрытым. (explanatory metaphor).

**Передний план:** Нижняя кромка современного рабочего стола и стойка бумажного монитора справа.

**Средний план:** Слева стилизованный безличный силуэт с карточкой BRENT SEALES • COMPUTER SCIENTIST; на столе отдельные карточки COLLABORATORS. Справа монитор с кремовой изогнутой сеткой; в маленькой отдельной ячейке чёрная модель с биркой PHYSICAL ORIGINAL.

**Задний план:** Нейтральная современная плоскость без узнаваемой архитектуры; постоянные подписи ILLUSTRATION и DIGITAL MODEL. Никакой даты первого опыта не ставится.

**Перекрытия и опоры:** Монитор и физическая ячейка имеют разные основания. Светлая сетка существует только внутри экранной рамки. Силуэт не берёт настоящий папирус; карточки соавторов не изображают документированную встречу. Дополнение v1.3: Крупная отдельная непрозрачная рамка полностью покрывает экран с запасом, прежде чем открывается томограф P13.

#### P12.B01 · оценочно 03:27.2–03:31.5

> Computer scientist Brent Seales and his collaborators pursued another route.

**Кадр:** WS, современный стол, силуэт слева и экран справа

**Камера:** Медленный боковой проезд вправо на 5 см.

**Действие:** Имя Brent Seales открывается за стойкой стола; рядом выдвигаются две нейтральные карточки COLLABORATORS, без придуманных имён и сообщений.

**Акцент:** ANOTHER ROUTE · речевой маркер «another route» · расчётное начало 03:30.6. Маска: Левая вертикальная стойка монитора скрывает буквы; они выходят за её внешнее ребро. Место: Над монитором справа, не поверх силуэта. Уход: Буквы опускаются за верхнюю рамку монитора на следующей фразе.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P12.B02 · оценочно 03:31.5–03:36.2

> If an instrument could measure the layers inside a damaged manuscript,

**Кадр:** MS, ячейка физического предмета и экран в одном поле

**Камера:** Продолжить тот же проезд вправо на 4 см.

**Действие:** Возле неподвижной чёрной модели возникают три отдельные учебные карточки сечения. Они соединены тонкой линией измерения с монитором и не вынимаются из физического предмета.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P12.B03 · оценочно 03:36.2–03:40.5

> perhaps a computer could build a copy of their shape.

**Кадр:** CU, монитор, вид под 25°

**Камера:** Медленный наезд на 3 см.

**Действие:** Внутри рамки монитора из трёх контуров строится светлая сетка искривлённой поверхности. Маленькая подпись DIGITAL COPY закрепляется в верхнем углу экрана.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P12.B04 · оценочно 03:40.5–03:46.5

> The physical object could stay rolled while the copy was opened on a screen.

**Кадр:** WS, экран и отдельная ячейка исходного предмета

**Камера:** Статично после расширения кадра.

**Действие:** Светлая цифровая сетка разворачивается внутри экрана до неровной полосы; чёрная модель в отдельной ячейке сохраняет форму и положение.

**Акцент:** DIGITAL COPY · речевой маркер «copy was opened» · расчётное начало 03:43.9. Маска: Нижняя отдельная непрозрачная передняя кромка рамки монитора скрывает буквы; они поднимаются позади кромки, оставаясь вне изображения сетки. Место: В нижней правой четверти под монитором. Уход: Буквы опускаются позади той же передней кромки; затем отдельная непрозрачная рамка полностью перекрывает кадр для перехода.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Отдельная крупная непрозрачная рамка полностью перекрывает экран с запасом; после полного покрытия открыть отдельный широкий учебный томограф SET-E. При невозможности использовать мотивированную явную склейку с выдержкой нового плана ≥3 с.

**Музыкальный замысел:** M2: за первые 3 секунды плавно примешать мягкий щипковый пульс к затухающему M1; продолжить единый музыкальный фон, без нового вступления.

**Активы:** H_SEALES_SILHOUETTE — стилизованная иллюстрация учёного с фактической карточкой роли; H_GENERIC_WORKSPACE — современный стол и бумажный монитор; H_COLLABORATOR_CARDS — нейтральные карточки сотрудничества; F_PHYSICAL_BAY — отдельная ячейка исходного предмета; F_MEASURED_CONTOURS — три учебных контура сечения; F_DIGITAL_MESH — светлая сетка с неровными границами; F_DIGITAL_LABEL — постоянная подпись DIGITAL COPY; REV13_P12_SCREEN_MASK — Крупная отдельная непрозрачная рамка полностью покрывает экран с запасом, прежде чем открывается томограф P13..

**Граница достоверности:** Объяснение принципа, не точная реконструкция первой лаборатории Seales и не утверждение, что ранний опыт был проведён именно на 1667. На экране разворачивается только цифровая форма; неизвестный текст не появляется.

**Источники:** S07, S08.

### P13 · оценочно 03:46.8–04:05.2 · SET-E

**Реплика:** Computed tomography is the starting point. X-ray measurements from different angles are combined into a three-dimensional volume. Researchers can move through virtual slices of that volume. A cross-section reveals a compressed maze of nested surfaces, carrying the shape of the papyrus inside.

**Цель и тип:** Томография даёт объём измерений и виртуальные сечения, а не готовую раскрытую страницу. (fact model).

**Передний план:** Ближняя стойка условного детектора справа и кромка неподвижного основания томографа.

**Средний план:** Закрытая модель свитка без номера в защитной опоре на вращательной площадке; слева условный источник, справа детектор. За детектором отдельный кремовый объём данных.

**Задний план:** Спокойная современная лабораторная плоскость; постоянная подпись TOMOGRAPHY • SCHEMATIC. Условный оранжевый луч имеет отдельную подпись X-RAYS • DIAGRAM.

**Перекрытия и опоры:** Опора вращается вместе с предметом вокруг одной закреплённой оси; источник и детектор неподвижны. Условный луч проходит позади ближней стойки детектора. Объём данных находится на отдельной подставке и не извлекается из предмета.

#### P13.B01 · оценочно 03:46.8–03:49.4

> Computed tomography is the starting point.

**Кадр:** WS, боковой вид измерительной схемы; начало непрерывного плана B01–B02.

**Камера:** После полного перекрытия предыдущего кадра плавно приблизиться к вращательной опоре и детектору без склейки.

**Действие:** Показать измерительную схему как условную модель; предмет, опора и детектор имеют раздельные опоры.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P13.B02 · оценочно 03:49.4–03:54.1

> X-ray measurements from different angles are combined into a three-dimensional volume.

**Кадр:** MS как конечный масштаб непрерывного плана B01–B02; опора и детектор под углом.

**Камера:** Продолжить сближение B01 и удержать детектор и объём раздельными слоями.

**Действие:** Результаты измерений с разных направлений собираются в отдельный условный объём данных, не раскрывая физический рулон.

**Акцент:** 3D VOLUME · речевой маркер «three-dimensional volume» · расчётное начало 03:53.3. Маска: Ближняя стойка детектора скрывает буквы; они выходят из-за её наружного края. Место: Справа сверху от объёма данных, вне луча. Уход: Буквы уходят за заднюю стенку объёма при переходе к сечениям.

**Звуковой замысел:** С началом поворота опоры — один тихий ровный механический гул, плавно затихающий после остановки. (нового звука пока нет).

#### P13.B03 · оценочно 03:54.1–03:58.0

> Researchers can move through virtual slices of that volume.

**Кадр:** CU, отдельный цифровой объём, вид под 25°

**Камера:** Медленный наезд на 3 см.

**Действие:** Тонкая светлая плоскость сечения перемещается по цифровому объёму на несколько сантиметров; в ней меняются контуры вложенных слоёв. Физический предмет виден вдали слева и не разрезается.

**Акцент:** VIRTUAL SLICES · речевой маркер «virtual slices» · расчётное начало 03:55.9. Маска: Верхняя грань объёма данных скрывает буквы; они поднимаются над ней. Место: В верхнем правом поле, не поверх сечения. Уход: Буквы скрывает продвигающаяся непрозрачная рамка плоскости сечения.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P13.B04 · оценочно 03:58.0–04:04.8

> A cross-section reveals a compressed maze of nested surfaces, carrying the shape of the papyrus inside.

**Кадр:** ECU, одна виртуальная поперечная плоскость фронтально

**Камера:** Плавный наезд на 2 см.

**Действие:** Сечение останавливается. Неровные вложенные контуры, местами почти соприкасающиеся, занимают кадр; рядом сохраняется маленькая подпись SCHEMATIC CROSS-SECTION. Письма пока нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Край плоскости сечения движется влево как настоящая бумажная рамка и закрывает изображение; за ним — другой ракурс того же цифрового объёма в SET-F, без появления физических страниц.

**Музыкальный замысел:** M2: продолжить мягкий щипковый пульс, немного убрать нижние частоты во время механического гула; после остановки вернуть прежнюю плотность.

**Активы:** E_TOMO_STAGE — учебный томограф с неподвижными источником и детектором; E_ROTATION_CRADLE — защитная опора на одной оси вращения; E_GENERIC_ROLL — самостоятельная закрытая модель без инвентарного номера; E_BEAM_DIAGRAM — условный луч с явной маркировкой; E_PROJECTION_CARDS — отдельные карточки угловых проекций; F_DIGITAL_VOLUME — кремовый объём данных; F_SECTION_PLANE — независимая виртуальная плоскость сечения.

**Граница достоверности:** Рентгеновский луч — объясняющее обозначение, не видимый свет реальной съёмки. Томография показана как измерение и реконструкция объёма; физический предмет не режут и не раскрывают.

**Источники:** S07, S08, S01.

### P14 · оценочно 04:05.2–04:26.1 · SET-F

**Реплика:** But a scan is only a measurement. It does not arrive with the pages neatly separated. The first task is to locate a writing surface and follow it through the volume. This is segmentation: deciding which parts of the three-dimensional data belong to the same piece of papyrus.

**Цель и тип:** Зритель понимает сегментацию как выделение одной непрерывной поверхности среди тесно сложенных слоёв. (fact model).

**Передний план:** Непрозрачная кремовая рамка цифрового объёма слева; маленькая подставка указателя внизу.

**Средний план:** Тот же цифровой объём с неровными вложенными поверхностями; оранжевая линия разметки лежит на одной из них, пока скрытая. Справа отдельная пустая карточка ONE SURFACE.

**Задний план:** Тёплый экран без программы конкретного производителя; подписи DIGITAL MODEL и SCHEMATIC. В нижнем углу отдельная маленькая ячейка PHYSICAL ORIGINAL с неподвижной чёрной моделью.

**Перекрытия и опоры:** Линия разметки скрывается соседними поверхностями там, где проходит за ними; она не светится сквозь все слои. Указатель стоит вне объёма. Маленькая физическая модель не соединяется геометрически с цифровой. Дополнение v1.3: Наружная непрозрачная кромка рамки на отдельном переднем слое скрывает TRACE THE SURFACE; начальное и конечное положение текста и кромки связаны.

#### P14.B01 · оценочно 04:05.2–04:08.2

> But a scan is only a measurement.

**Кадр:** MS, цифровой объём и его рамка под 35°

**Камера:** Статично.

**Действие:** Сетка координат появляется только на рамке; внутри остаётся неоднозначный набор контуров, без готовых колонок текста.

**Акцент:** MEASURED DATA · речевой маркер «only a measurement» · расчётное начало 04:06.9. Маска: Левая непрозрачная рамка объёма скрывает буквы; они выходят из-за её внутреннего ребра. Место: Внизу слева вне области сечений. Уход: Буквы закрываются рамкой при следующем боковом движении.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P14.B02 · оценочно 04:08.2–04:12.1

> It does not arrive with the pages neatly separated.

**Кадр:** CU, плотный участок цифрового объёма

**Камера:** Медленный боковой проезд вправо на 3 см.

**Действие:** Две близкие поверхности остаются сжатыми; камера меняет параллакс, показывая сложность их различения. Никаких аккуратно разложенных физических листов.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P14.B03 · оценочно 04:12.1–04:18.5

> The first task is to locate a writing surface and follow it through the volume.

**Кадр:** CU, тот же участок под тем же углом

**Камера:** Продолжить проезд вправо на 3 см.

**Действие:** Короткая оранжевая метка появляется на одной поверхности и последовательно удлиняется по её ходу; в местах перекрытия она исчезает за соседней поверхностью и появляется снова.

**Акцент:** TRACE THE SURFACE · речевой маркер «follow it through the volume» · расчётное начало 04:16.3. Маска: Наружная непрозрачная кромка рамки скрывает буквы; они выдвигаются из-за неё. Место: Свободная область у внешней рамки, вне линии на поверхности. Уход: После читаемой остановки скрыть за той же кромкой в начале продолжающего смысл плана B04, до входа ONE SURFACE.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P14.B04 · оценочно 04:18.5–04:25.8

> This is segmentation: deciding which parts of the three-dimensional data belong to the same piece of papyrus.

**Кадр:** WS, весь цифровой объём и отдельная карточка справа

**Камера:** Плавный отъезд на 5 см.

**Действие:** Выбранная поверхность подсвечивается от начала до конца видимого участка; соседние остаются кремовыми. На отдельной карточке появляется только контур выбранной геометрии, без чернил.

**Акцент:** ONE SURFACE · речевой маркер «same piece of papyrus» · расчётное начало 04:24.1. Маска: Правая карточка ONE SURFACE скрывает буквы за нижним краем; они выдвигаются вверх из-за неё. Место: В свободной правой четверти над контурной карточкой. Уход: Карточка закрывает буквы своим поворотом на 90° и становится маской перехода.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Повернувшаяся карточка на мгновение заполняет кадр; за ней открыть явно подписанную миниатюру дороги METAPHOR, с новым широким ракурсом.

**Музыкальный замысел:** M2: продолжить тот же пульс, без отдельного удара при появлении оранжевой линии; немного разредить фактуру к слову segmentation.

**Активы:** F_DIGITAL_VOLUME — кремовый объём данных; F_SECTION_PLANE — независимая виртуальная плоскость сечения; F_SURFACE_TRACE — оранжевая линия одной поверхности с корректными масками; F_SURFACE_CARD — отдельная контурная карточка; F_PHYSICAL_BAY — отдельная ячейка исходного предмета; F_REFERENCE_GRID — сетка координат на рамке; REV13_P14_MASK — Наружная непрозрачная кромка рамки на отдельном переднем слое скрывает TRACE THE SURFACE; начальное и конечное положение текста и кромки связаны..

**Граница достоверности:** Сегментация выделяет геометрию, а не распознаёт текст. Выбранная поверхность условна и не выдаётся за конкретную найденную страницу 1667. Оранжевая линия не перескакивает на соседний слой в этом правильном примере.

**Источники:** S08, S09.

### P15 · оценочно 04:26.1–04:43.2 · SET-F

**Реплика:** Imagine tracing a road through a crushed city. Neighbouring layers nearly touch; elsewhere, the surface tears or folds sharply. Follow the wrong route, and the computer can jump between parts of the sheet, scrambling the relationship between the marks.

**Цель и тип:** Зритель понимает, как ошибочный переход между витками портит расположение будущих письменных следов. (explanatory metaphor).

**Передний план:** Передний бортик учебного стола и непрозрачная центральная перегородка между двумя моделями.

**Средний план:** Слева условная сложенная городская дорога из кремовой бумаги без античных деталей; справа отдельная схема тесных витков папируса, связанная с маленькой выходной карточкой.

**Задний план:** Слева постоянная подпись METAPHOR; справа DIGITAL MODEL • SCHEMATIC. Никаких жителей, домов виллы, букв или конкретного исторического города.

**Перекрытия и опоры:** Дорога и модель слоёв находятся на разных подложках, разделённых перегородкой. Они не морфятся друг в друга. На схеме неверный путь пересекает реальный промежуток между двумя соседними витками; абстрактные метки закреплены на своих поверхностях.

#### P15.B01 · оценочно 04:26.1–04:29.6

> Imagine tracing a road through a crushed city.

**Кадр:** WS, косой верхний вид условной дороги слева

**Камера:** Медленный наезд на 3 см.

**Действие:** На сложенной дорожной ленте короткий светлый маркер следует одному маршруту и останавливается у тесного сгиба. Бирка METAPHOR всё время читается.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P15.B02 · оценочно 04:29.6–04:34.3

> Neighbouring layers nearly touch; elsewhere, the surface tears or folds sharply.

**Кадр:** MS, отдельная схема витков справа

**Камера:** Плавный боковой проезд вправо на 8 см, через центральную перегородку.

**Действие:** После маски перегородкой открываются две соседние дуги и разрыв на третьем участке; в конце проезда камера показывает острый сгиб, не выпрямляя его.

**Акцент:** NEIGHBOURING LAYERS · речевой маркер «Neighbouring layers» · расчётное начало 04:29.6. Маска: Центральная перегородка скрывает буквы; они появляются из-за её правого края после открытия схемы. Место: Внизу справа от дуг, вне разрыва. Уход: Буквы закрываются нижним бортиком учебного стола перед показом ошибки.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P15.B03 · оценочно 04:34.3–04:40.3

> Follow the wrong route, and the computer can jump between parts of the sheet,

**Кадр:** CU, место сближения двух витков, косой ракурс

**Камера:** Медленный наезд на 2 см.

**Действие:** Оранжевая линия идёт по одному витку, затем ошибочно переходит через промежуток на соседний участок. Поперечный ошибочный отрезок имеет пунктир и маленькую подпись WRONG PATH, чтобы не принять его за нормальный слой.

**Акцент:** WRONG ROUTE · речевой маркер «wrong route» · расчётное начало 04:35.1. Маска: Ближняя дуга папируса скрывает буквы; они выходят за её нижний край. Место: В нижней левой четверти, не поверх ошибочного перехода. Уход: Буквы остаются на продолжении действия и исчезают за входящей рамкой выходной карточки.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P15.B04 · оценочно 04:40.3–04:42.8

> scrambling the relationship between the marks.

**Кадр:** CU, тот же ракурс с выходной карточкой на правом краю

**Камера:** Продолжить тот же наезд ещё на 1 см, без склейки.

**Действие:** На отдельной выходной карточке две группы квадратных и круглых условных меток оказываются рядом в неверном порядке; тонкие линии показывают, из каких разных участков они взяты. Никаких букв не возникает.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Непрозрачная рамка выходной карточки закрывает весь пример ошибки; склейка на другую, явно правильную непрерывную поверхность в широком DIGITAL MODEL плане P16. Неверная геометрия не превращается незаметно в успешный результат.

**Музыкальный замысел:** M2: пульс остаётся ровным; при неверном пути убрать одну верхнюю ноту, без тревожного звукового сигнала или игровой ошибки.

**Активы:** F_ROAD_METAPHOR — отдельная сложенная дорожная лента; F_MODEL_DIVIDER — перегородка между метафорой и технической схемой; F_ADJACENT_WRAPS — схема тесных соседних витков; F_WRONG_PATH — линия с явно пунктирным неправильным переходом; F_ABSTRACT_MARKS — квадратные и круглые метки без букв; F_SCRAMBLED_OUTPUT — отдельная выходная карточка неверного порядка.

**Граница достоверности:** Город — явная метафора, не реконструкция разрушения Геркуланума. Ошибочное сопоставление показано на условных метках; это не выдуманное древнее слово и не реальный результат модели.

**Источники:** S01, S09.

### P16 · оценочно 04:43.2–05:03.9 · SET-F

**Реплика:** Once a reliable surface has been traced, its digital geometry can be flattened. The coordinates change; the original does not move. A curved strip becomes a plane. Yet that unfolded surface can still look almost empty. Finding the page and finding the ink are different problems.

**Цель и тип:** Цифровую поверхность можно распрямить, но это ещё не означает, что на ней обнаружены чернила. (fact model).

**Передний план:** Две нижние направляющие бумажного театра, одна для цифровой сетки, другая для карточек задач.

**Средний план:** Светлая искривлённая сетка с неровными краями слева; справа в отдельной ячейке неподвижная тёмная модель PHYSICAL ORIGINAL. Ниже две отдельные карточки SURFACE и INK SIGNAL.

**Задний план:** Матовое поле с постоянной подписью DIGITAL MODEL • SCHEMATIC. Цифровая сетка имеет мелкую координатную разметку, не текст.

**Перекрытия и опоры:** Светлая сетка и физическая модель находятся на разных подложках с раздельными тенями. Во время распрямления двигаются только узлы сетки; оригинальная модель и её ложемент неподвижны. Неровные края и дыры сохраняются.

#### P16.B01 · оценочно 04:43.2–04:48.8

> Once a reliable surface has been traced, its digital geometry can be flattened.

**Кадр:** MS, искривлённая сетка под 30°, физическая ячейка видна справа

**Камера:** Медленный наезд на 3 см.

**Действие:** Узлы сетки начинают перераспределяться в одной непрерывной анимации; верхний изгиб постепенно уменьшается, а отверстие в поверхности остаётся на месте относительно соседних узлов.

**Акцент:** DIGITAL GEOMETRY · речевой маркер «digital geometry» · расчётное начало 04:46.6. Маска: Передняя направляющая сетки скрывает буквы; они поднимаются за ней. Место: Нижняя левая четверть под сеткой. Уход: Буквы уходят за направляющую перед расширением кадра.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P16.B02 · оценочно 04:48.8–04:52.2

> The coordinates change; the original does not move.

**Кадр:** WS, обе отдельные подложки в одном поле, высокий угол45°

**Камера:** Статично после смены масштаба.

**Действие:** На светлой сетке меняются координатные точки; справа неподвижные контур и контактная тень оригинальной модели подчёркивают отсутствие физического движения.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P16.B03 · оценочно 04:52.2–04:54.8

> A curved strip becomes a plane.

**Кадр:** WS, тот же непрерывный план

**Камера:** Статично.

**Действие:** Последний изгиб светлой сетки мягко распрямляется до плоскости на своей подложке. Углы остаются неровными; оригинал не реагирует.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P16.B04 · оценочно 04:54.8–04:58.6

> Yet that unfolded surface can still look almost empty.

**Кадр:** CU, плоская цифровая поверхность сверху

**Камера:** Медленный наезд на 2 см после явной смены ракурса.

**Действие:** На плоскости видна только слабая условная фактура и геометрические дефекты; камера проходит над пустой областью. Никакая надпись не проявляется.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P16.B05 · оценочно 04:58.6–05:02.9

> Finding the page and finding the ink are different problems.

**Кадр:** MS, нижние карточки задач и край цифровой поверхности

**Камера:** Плавный проезд вниз на 4 см.

**Действие:** Карточка SURFACE открывается с контуром геометрии; карточка INK SIGNAL рядом остаётся с пустой рамкой. Это две задачи, а не две древние страницы.

**Акцент:** FIND THE INK · речевой маркер «finding the ink» · расчётное начало 05:00.3. Маска: Передняя кромка второй карточки скрывает буквы; они поднимаются над ней. Место: Справа внизу возле карточки INK SIGNAL, не поверх цифровой поверхности. Уход: Буквы опускаются за карточку; карточка поднимается до заполнения кадра.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Пустая карточка INK SIGNAL становится полноэкранной маской; склейка на два увеличенных учебных образца чернил и основы в SET-G, под общей маркировкой SCHEMATIC.

**Музыкальный замысел:** M2: после распрямления не давать победного разрешения; разредить пульс на почти пустой поверхности и сохранить движение к следующей задаче.

**Активы:** F_DIGITAL_MESH — светлая сетка с неровными границами; F_PHYSICAL_BAY — отдельная ячейка исходного предмета; F_REFERENCE_GRID — сетка координат на рамке; F_TASK_SURFACE — карточка задачи геометрии; F_TASK_INK — отдельная карточка задачи чернил; F_GEOMETRY_RAILS — направляющие двух раздельных задач.

**Граница достоверности:** Распрямляется цифровая геометрия, не физический папирус. Сохранены дыры и неровные края. Пустая поверхность иллюстрирует разделение задач, а не утверждение, что все реальные сканы выглядят одинаково пустыми.

**Источники:** S07, S08, S09.

### P17 · оценочно 05:03.9–05:23.1 · SET-G

**Реплика:** Much of the ink in these manuscripts is carbon-based. So is the papyrus after carbonization. In many scans, the writing produces only a subtle signal against its background. Increasing the contrast on a screen cannot simply turn every ambiguous texture into a trustworthy letter.

**Цель и тип:** Похожесть углеродных чернил и обугленного основания объясняет слабый сигнал и необходимость осторожной интерпретации. (fact model).

**Передний план:** Передняя планка учебного сравнения; справа ребро бумажного экрана с отдельным ползунком CONTRAST.

**Средний план:** Две увеличенные условные поверхности на разных подложках: сверху отдельный неалфавитный след INK, снизу PAPYRUS AFTER CARBONIZATION. Справа экран со слабой фактурой, без букв.

**Задний план:** Кремовое поле; постоянные маркировки SCHEMATIC MATERIAL COMPARISON и SIMULATED DISPLAY • NOT A SCAN. Нет факсимиле или точных чернильных составов.

**Перекрытия и опоры:** След чернил лежит на отдельной учебной плоскости над основой. Подписи закреплены на краях подложек; ползунок встроен в рамку условного дисплея. При изменении контраста структура остаётся той же, новые линии не создаются.

#### P17.B01 · оценочно 05:03.9–05:07.8

> Much of the ink in these manuscripts is carbon-based.

**Кадр:** CU, верхний учебный образец чернил под 20°

**Камера:** Медленный проезд вправо на 2 см.

**Действие:** Открывается один неровный тёмный след и небольшая карточка CARBON-BASED INK; след не похож на знак алфавита.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P17.B02 · оценочно 05:07.8–05:10.3

> So is the papyrus after carbonization.

**Кадр:** MS, два образца и дисплей справа в одном кадре; начало непрерывного плана B02–B03.

**Камера:** Без склейки плавно перевести внимание от образцов к дисплею.

**Действие:** Оба образца остаются на отдельных подложках; виден дисплей сравнения.

**Акцент:** CARBON ON CARBON · речевой маркер «So is the papyrus» · расчётное начало 05:07.8. Маска: Передний край нижней подложки скрывает буквы; они поднимаются из-за него. Место: Внизу между образцами, не на самих поверхностях. Уход: После читаемой остановки буквы опускаются за передний край своей подложки в продолжающемся плане.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P17.B03 · оценочно 05:10.3–05:15.9

> In many scans, the writing produces only a subtle signal against its background.

**Кадр:** MS, продолжение плана B02 с образцами и дисплеем.

**Камера:** Удержать общий ракурс; мягким светом выделить дисплей без нового CU.

**Действие:** На дисплее проявляется слабое условное различие сигнала и фона; образцы сохраняются в кадре.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P17.B04 · оценочно 05:15.9–05:22.8

> Increasing the contrast on a screen cannot simply turn every ambiguous texture into a trustworthy letter.

**Кадр:** MS, дисплей и ползунок в одном кадре

**Камера:** Статично.

**Действие:** Ползунок CONTRAST поднимается на короткий участок: усиливаются и след, и соседняя неоднородность. Курсорная рамка останавливается над неоднозначной областью; буквенная транскрипция не появляется.

**Акцент:** AMBIGUOUS SIGNALS · речевой маркер «ambiguous texture» · расчётное начало 05:20.2. Маска: Правая стойка условного дисплея скрывает буквы; они выдвигаются за её внешнее ребро. Место: Правое свободное поле рядом с экраном, без перекрытия области сравнения. Уход: Стойка дисплея проходит перед буквами и закрывает кадр для перехода.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Непрозрачная стойка экрана полностью закрывает изображение; открыть новую широкую галерею SET-L с отдельной сине-серой ячейкой EN-GEDI. Тёмные учебные образцы предыдущего кадра не переименовываются в другой артефакт.

**Музыкальный замысел:** M2: сохранить лёгкий пульс, уменьшить яркость верхних звуков при усилении контраста; не озвучивать движение ползунка.

**Активы:** G_INK_SAMPLE — самостоятельная схема углеродного следа; G_CARBONIZED_SUBSTRATE — отдельная схема обугленного основания; G_SIMULATED_DISPLAY — бумажный дисплей неоднозначного сигнала; G_CONTRAST_SLIDER — ползунок в реальной рамке; G_NO_SCAN_LABEL — постоянная маркировка учебного изображения.

**Граница достоверности:** Не утверждается, что все чернила одинаковы или совсем невидимы рентгену. Усиление контраста меняет видимость уже имеющейся структуры, а не создаёт достоверную букву. Здесь нет настоящего скана.

**Источники:** S08, S09.

### P18 · оценочно 05:23.1–05:41.5 · SET-L

**Реплика:** Virtual unwrapping already had an important success. A study published in twenty sixteen described Hebrew text recovered from a burned scroll at En-Gedi. Written on animal skin, its ink stood out more clearly in the scan. Herculaneum presented a harder imaging problem.

**Цель и тип:** Успех с Эн-Геди показывает работоспособность виртуального разворачивания и одновременно объясняет отдельную трудность Геркуланума. (evidence graphic).

**Передний план:** Широкая сине-серая стойка левой ячейки и тёплая непрозрачная перегородка между двумя объектами.

**Средний план:** Слева отдельная стилизованная модель обгоревшего рулона EN-GEDI на собственной опоре; справа отдельная условная модель HERCULANEUM на охристой подложке. Между ними нет соединения. Над левой ячейкой закрытая карточка исследования 2016.

**Задний план:** В левой ячейке сине-серое поле, в правой тёплое; общая подпись EVIDENCE SUMMARY • SCHEMATIC. Сравнительные сигналы имеют постоянную подпись NOT A SCAN.

**Перекрытия и опоры:** Перегородка отделяет объекты и действительно закрывает один при боковом движении. Каждая модель сохраняет собственный номер или название, подложку и свет. Никакое движение не превращает Эн-Геди в Геркуланум.

#### P18.B01 · оценочно 05:23.1–05:26.1

> Virtual unwrapping already had an important success.

**Кадр:** WS, новая галерея, левая ячейка в центре

**Камера:** Медленный наезд на 3 см.

**Действие:** Открывается сине-серая ячейка с отдельной моделью; её форма и опора отличаются от 1667. Справа виден только край закрытого тёплого отделения.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P18.B02 · оценочно 05:26.1–05:33.0

> A study published in twenty sixteen described Hebrew text recovered from a burned scroll at En-Gedi.

**Кадр:** MS, левая ячейка и карточка над ней

**Камера:** Статично.

**Действие:** Карточка 2016 опускается в свой паз и показывает краткий факт HEBREW TEXT RECOVERED; ниже открывается табличка EN-GEDI. Древнееврейские буквы и библейский текст не имитируются.

**Акцент:** EN-GEDI · речевой маркер «En-Gedi» · расчётное начало 05:32.5. Маска: Сине-серая передняя стойка ячейки скрывает буквы; они выходят за её правый край. Место: В верхнем левом свободном поле, отдельно от фактической карточки 2016. Уход: Буквы уходят за стойку перед открытием учебного материала.

**Звуковой замысел:** Когда карточка 2016 достигает паза — один тихий бумажно-деревянный контакт. (нового звука пока нет).

#### P18.B03 · оценочно 05:33.0–05:38.5

> Written on animal skin, its ink stood out more clearly in the scan.

**Кадр:** CU, отдельная учебная карточка материала под ячейкой Эн-Геди

**Камера:** Медленный проезд вниз на 3 см.

**Действие:** Заслонка открывает фактическую подпись ANIMAL SKIN и два условных участка: основу и отчётливый тёмный след. На соседнем маленьком дисплее тот же след сильнее отделён от фона; это учебная схема, не результат нового сканирования.

**Акцент:** STRONGER CONTRAST · речевой маркер «stood out more clearly» · расчётное начало 05:35.5. Маска: Нижняя кромка карточки материала скрывает буквы; они поднимаются из-за неё. Место: Справа от сравнительного дисплея, без перекрытия сигнала. Уход: Буквы опускаются за карточку до перехода к правой ячейке.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P18.B04 · оценочно 05:38.5–05:41.1

> Herculaneum presented a harder imaging problem.

**Кадр:** WS, обе ячейки в одном поле

**Камера:** Плавный боковой проезд вправо на 5 см.

**Действие:** Тёплая заслонка правого отделения открывается: отдельная модель HERCULANEUM стоит рядом с учебным дисплеем более слабого сигнала. EN-GEDI и его 2016 остаются слева; предметы не двигаются между отделениями.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Тёплая центральная перегородка проходит перед объективом слева направо и полностью закрывает обе ячейки. P19 начинается новым общим планом отделения HERCULANEUM с другой высоты камеры; модель Эн-Геди остаётся за перегородкой и не переименовывается.

**Музыкальный замысел:** M2: чуть высветлить гармонию на подтверждённом успехе 2016, затем вернуть прежнюю сдержанную плотность на Herculaneum; без фанфар и перезапуска трека.

**Активы:** L_ENGEDI_BAY — отдельная сине-серая ячейка Эн-Геди; L_ENGEDI_MODEL — самостоятельная стилизованная модель обгоревшего рулона на отдельной опоре; L_ENGEDI2016 — фактическая карточка исследования 2016; L_ANIMAL_SKIN_CARD — объясняющая карточка материала; L_CONTRAST_COMPARISON — пара условных дисплеев с различным отделением сигнала от фона; L_HERCULANEUM_BAY — отдельная тёплая ячейка Геркуланума; L_WARM_DIVIDER — непрозрачная подвижная перегородка.

**Граница достоверности:** Эн-Геди — отдельный объект на животной коже, не папирус Геркуланума и не 1667. 2016 относится к опубликованному исследованию. Сигналы схематические; не утверждаются конкретный химический состав его чернил или тождество этих учебных штрихов древнееврейскому тексту.

**Источники:** S07, S08.

### P19 · оценочно 05:41.5–06:00.7 · SET-L

**Реплика:** There were earlier claims at Herculaneum, too. Vito Mocella and colleagues reported letters inside rolled papyri in twenty fifteen. In twenty nineteen, Seales and colleagues argued that those readings had not yet been confirmed or developed into complete passages. Suggestive images needed stronger tests.

**Цель и тип:** Зритель отличает раннее сообщение о буквах от подтверждённого чтения связного текста. (evidence graphic).

**Передний план:** В нижней левой четверти — толстая кромка синего отсека EN-GEDI, унаследованная от P18; справа ближе к камере — вертикальный разделитель шкафа.

**Средний план:** Две отдельные кремовые карточки 2015 / MOCELLA ET AL. и 2019 / PARKER, SEALES ET AL. в направляющих; между ними свободное место.

**Задний план:** Тёплая стенка исследовательского шкафа; маленькая постоянная надпись RESEARCH TIMELINE. Никаких имитаций скриншотов статей.

**Перекрытия и опоры:** Разделитель полностью закрывает карточку, пока та не проходит его грань. Карточки опираются на нижнюю рейку; движутся по ней, а не парят. Отсек EN-GEDI остаётся отдельным.

#### P19.B01 · оценочно 05:41.5–05:44.5

> There were earlier claims at Herculaneum, too.

**Кадр:** WS, фронтально с небольшим углом сверху; видны соседние отсеки.

**Камера:** Плавный проезд вправо на 10% ширины кадра.

**Действие:** Синий отсек уходит к левому краю; за разделителем открывается новый отсек HERCULANEUM с пустой временной линией.

**Акцент:** EARLIER CLAIMS · речевой маркер «earlier claims» · расчётное начало 05:42.3. Маска: Буквы выходят справа из-за вертикального разделителя шкафа. Место: Верхняя левая треть нового отсека, над линией дат. Уход: Уходят обратно за разделитель до появления карточки 2019.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P19.B02 · оценочно 05:44.5–05:49.6

> Vito Mocella and colleagues reported letters inside rolled papyri in twenty fifteen.

**Кадр:** MS, под углом 25° слева на карточку 2015.

**Камера:** Статика.

**Действие:** Карточка MOCELLA ET AL. / 2015 входит в направляющие. На ней только редакционная формулировка LETTERS REPORTED, без рисунка предполагаемых букв.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** Один тихий деревянный контакт на момент остановки карточки в направляющей. (нового звука пока нет).

#### P19.B03 · оценочно 05:49.6–05:53.0

> In twenty nineteen, Seales and colleagues argued that

**Кадр:** MS, тот же непрерывный план и те же направляющие.

**Камера:** Статика.

**Действие:** Следующая карточка 2019 появляется за правым разделителем; видимое расстояние между датами сохраняется.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P19.B04 · оценочно 05:53.0–05:58.2

> those readings had not yet been confirmed or developed into complete passages.

**Кадр:** CU, с противоположной стороны шкафа, карточка 2019 и край предыдущей.

**Камера:** Медленный наезд на 4%.

**Действие:** На карточке 2019 открывается выдвижная полоска CONFIRMATION / COMPLETE PASSAGES; обе графы остаются незаполненными. Старую карточку не перечёркивают и не выбрасывают.

**Акцент:** NOT YET CONFIRMED · речевой маркер «not yet been confirmed» · расчётное начало 05:54.3. Маска: Оранжевая подложка поднимается из-за нижнего борта лотка 2019. Место: Нижняя правая свободная четверть, вне текста карточек. Уход: Опускается за борт перед финальным планом.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P19.B05 · оценочно 05:58.2–06:00.3

> Suggestive images needed stronger tests.

**Кадр:** ECU, вид сверху на пустую рамку проверки рядом с карточками.

**Камера:** Статика.

**Действие:** Бумажная рамка с четырьмя регистрационными углами ложится поверх нейтрального серого поля; внутри ничего не дорисовывается.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Прямой переход по форме рамки: её четыре угла становятся регистрационными углами пары видов фрагмента в P20; меняются масштаб и угол на строго верхний.

**Музыкальный замысел:** M2 — непрерывная спокойная пульсация; последние две фразы чуть разрежены, без нового вступления.

**Активы:** P19-A01: шкаф с синей ячейкой EN-GEDI и отдельным отсеком HERCULANEUM; P19-A02: собственные редакционные карточки исследований 2015 и 2019; P19-A03: реечная рамка проверки и два набора бумажных акцентов.

**Граница достоверности:** Схема истории исследований, не факсимиле публикаций. Не объявлять заявления 2015 доказанно ложными; имя Parker добавлено в фактическую подпись к работе 2019.

**Источники:** S10, S08.

### P20 · оценочно 06:00.7–06:20.7 · SET-G

**Реплика:** One promising approach began with fragments whose writing was already exposed. Researchers could photograph the ink, scan the same material, and align the two views. This created examples linking visible writing to subtle features in the X-ray data. A machine-learning model could learn from those correspondences.

**Цель и тип:** Зритель понимает, откуда берётся проверяемый обучающий пример: один и тот же фрагмент виден двумя способами. (fact model).

**Передний план:** Нижняя кромка матовой держательной рамы перекрывает края левого и правого окон; справа на переднем плане — маленькая регистрационная линейка.

**Средний план:** Слева собственный условный бумажный фрагмент с тремя неписьменными чернильными штрихами; справа его схематический CT-вид с тем же контуром и отверстиями.

**Задний план:** Плоская тёплая подложка с отдельными подписями PHOTO / CT / SCHEMATIC TRAINING EXAMPLE.

**Перекрытия и опоры:** Левый и правый виды закреплены на двух одинаковых держателях. Прозрачная регистрационная плёнка находится физически выше обоих и отбрасывает слабую тень; она не меняет форму фрагмента.

#### P20.B01 · оценочно 06:00.7–06:05.4

> One promising approach began with fragments whose writing was already exposed.

**Кадр:** CU, строго сверху на левый фрагмент.

**Камера:** Отъезд на 8%, открывающий парное окно справа.

**Действие:** Три штриха уже видны на открытой поверхности. Надпись SCHEMATIC показывает, что это учебный пример, а не новый древний текст.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P20.B02 · оценочно 06:05.4–06:11.4

> Researchers could photograph the ink, scan the same material, and align the two views.

**Кадр:** MS, сверху на оба окна.

**Камера:** Статика.

**Действие:** Над левым окном закрывается и открывается простой затвор рамки PHOTO; затем правая карточка CT устанавливается рядом. Регистрационная плёнка совмещает контуры и отверстия.

**Акцент:** VISIBLE INK · речевой маркер «photograph the ink» · расчётное начало 06:06.2. Маска: Буквы выдвигаются из-за верхней планки держателя PHOTO. Место: Над левым окном; сами штрихи и отверстия остаются открыты. Уход: Буквы уходят за ту же планку после совмещения.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P20.B03 · оценочно 06:11.4–06:16.9

> This created examples linking visible writing to subtle features in the X-ray data.

**Кадр:** ECU, наклонный вид 30° на один и тот же участок в двух окнах.

**Камера:** Плавный проезд вправо на 6%.

**Действие:** Одна тонкая бумажная скоба соединяет соответствующие точки. На CT-карточке подсвечивается рельефная точка именно под выбранным штрихом.

**Акцент:** LINKED VIEWS · речевой маркер «linking visible writing» · расчётное начало 06:12.7. Маска: Акцент раскрывается из-за стойки регистрационной линейки, как короткая боковая вкладка. Место: В нижнем свободном поле между окнами, не на данных. Уход: Вкладка задвигается за линейку к следующему предложению.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P20.B04 · оценочно 06:16.9–06:20.4

> A machine-learning model could learn from those correspondences.

**Кадр:** WS, сверху на учебную пару и третий небольшой лоток.

**Камера:** Статика.

**Действие:** Пара связанных мини-карточек переносится на бумажном ползунке к лотку MODEL. Исходный фрагмент остаётся в своём держателе; перемещаются только обозначения данных.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Лоток MODEL закрывается до тонкой горизонтальной щели; монтажный стык на другой угол той же щели в P21 открывает поле предсказания.

**Музыкальный замысел:** M2 — пульс продолжается; появляется один тихий высокий музыкальный тон на совмещении, это часть музыкальной фразы, не отдельный SFX.

**Активы:** P20-A01: собственный схематический фрагмент без букв с тремя штрихами и отверстиями; P20-A02: парные держатели PHOTO и CT с регистрационной плёнкой; P20-A03: лоток MODEL, ползунок и бумажные акценты.

**Граница достоверности:** Все изображения собственные и помечены SCHEMATIC; никакой имитации реального скана. Не подписывать учебный фрагмент Paris4 или 1667.

**Источники:** S08, S09.

### P21 · оценочно 06:20.7–06:38.6 · SET-F

**Реплика:** The model estimated where ink might be present. Reading the language came later. Its images still needed checking against the scan, the surface geometry, and the judgment of specialists in ancient handwriting. An attractive output was a beginning, not a verdict.

**Цель и тип:** Зритель видит предсказание чернил как начало проверки, а не как готовый перевод. (fact model).

**Передний план:** Низкая створка лотка MODEL у нижнего края; справа ближе к камере — вертикальная рамка контрольного окна.

**Средний план:** На плоской цифровой карточке небольшие серые и оранжевые точки вероятного сигнала; три контрольных окна SCAN / SURFACE / READING разнесены по глубине.

**Задний план:** Тёмно-кремовая геометрическая сцена с постоянной подписью INK PREDICTION — SCHEMATIC.

**Перекрытия и опоры:** Створка маскирует только бумажные данные, не физический свиток. Окна проверки остаются на стойках и при движении камеры перекрывают друг друга согласно глубине. Дополнение v1.3: Пустая графа VERIFIED и её непрозрачная стойка с маской для NOT A VERDICT отдельно от контрольных окон; кадр удерживается до начала P22.

#### P21.B01 · оценочно 06:20.7–06:24.2

> The model estimated where ink might be present.

**Кадр:** CU, косой верхний вид на прогноз в лотке.

**Камера:** Плавный наезд на 4%.

**Действие:** Створка открывает поле небольших пятен разной насыщенности; никакие буквы или слова из них не возникают.

**Акцент:** INK? · речевой маркер «where ink might be present» · расчётное начало 06:22.0. Маска: Буква и знак вопроса появляются из-за переднего борта лотка. Место: Слева в нижнем свободном углу, вне поля пятен. Уход: Карточка акцента опускается за борт перед проверкой.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P21.B02 · оценочно 06:24.2–06:26.3

> Reading the language came later.

**Кадр:** MS, продолжение сцены со свободным местом справа.

**Камера:** Статика.

**Действие:** Пустая карточка READING остаётся в правой рамке; между полем сигнала и чтением сохраняется видимый разрыв.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P21.B03 · оценочно 06:26.3–06:31.0

> Its images still needed checking against the scan, the surface geometry,

**Кадр:** MS, с уровня контрольных окон.

**Камера:** Проезд вправо на 7%, последовательно открывающий SCAN и SURFACE.

**Действие:** Контрольный ползунок показывает тот же локальный участок в объёмной сетке, затем на цифровой поверхности; два угловых маркера подтверждают совпадение места.

**Акцент:** CHECK THE EVIDENCE · речевой маркер «checking against the scan» · расчётное начало 06:28.0. Маска: Акцент выходит из-за левой вертикальной стойки окна SURFACE. Место: Над нижней рейкой, под двумя окнами; не закрывает маркеры. Уход: Уходит за правую стойку при завершении проезда.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P21.B04 · оценочно 06:31.0–06:34.4

> and the judgment of specialists in ancient handwriting.

**Кадр:** CU, боковой вид на отдельное окно READING.

**Камера:** Статика.

**Действие:** Условная рука специалиста на своей панели опускает лупу к печатной рабочей карточке. Подпись INDEPENDENT READING обозначает функцию, не конкретное заседание.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P21.B05 · оценочно 06:34.4–06:38.3

> An attractive output was a beginning, not a verdict.

**Кадр:** WS, фронтально на все три контрольных окна.

**Камера:** Удержать контрольные окна в начале следующей фразы P22.B01 до завершения акцента; затем закрыть кадр боковой стенкой и открыть коллаж P22.

**Действие:** Красивое поле предсказания остаётся только в первом окне; финальная графа VERIFIED не заполняется автоматически.

**Акцент:** NOT A VERDICT · речевой маркер «not a verdict» · расчётное начало 06:37.0. Маска: Непрозрачная стойка пустой графы VERIFIED скрывает буквы; они выходят из-за её внешнего края. Место: Свободное поле рядом с графой, вне контрольных окон. Уход: После читаемой остановки в начале P22.B01 буквы уходят обратно за стойку; графа VERIFIED остаётся незаполненной.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Удержать контрольные окна и пустую графу VERIFIED в начале P22.B01 до читаемого ухода NOT A VERDICT; затем боковая стенка полностью перекрывает кадр и открывает рабочие места конкурса.

**Музыкальный замысел:** M2 — без перезапуска; на последней фразе убрать один слой пульса, оставив движение гармонии.

**Активы:** P21-A01: собственная карта вероятного сигнала без букв; P21-A02: три контрольных окна со стойками и регистрационным ползунком; P21-A03: условная рука, лупа и пустая финальная графа; P21-A04: два бумажных акцента; REV13_P21_VERIFIED — Пустая графа VERIFIED и её непрозрачная стойка с маской для NOT A VERDICT отдельно от контрольных окон; кадр удерживается до начала P22..

**Граница достоверности:** Предсказание не показано как перевод или распознавание языка. Все технические изображения схематические, проверка не представлена автоматически успешной.

**Источники:** S08, S01, S11.

### P22 · оценочно 06:38.6–06:59.1 · SET-H

**Реплика:** In March twenty twenty-three, Seales, Nat Friedman, and Daniel Gross launched the Vesuvius Challenge. Scans, software, and prizes brought a wider community into the effort. Progress could come from someone improving the geometry, someone finding an imaging clue, or someone building a better way to detect ink.

**Цель и тип:** Зритель понимает, что конкурс соединил разные виды труда и расширил круг участников. (evidence graphic).

**Передний план:** Слева близко к камере — торец общей доски; внизу — направляющая для пакетов данных.

**Средний план:** Три отдельные узкие ниши с условными силуэтами и именными табличками BRENT SEALES / NAT FRIEDMAN / DANIEL GROSS; в центре пакет VESUVIUS CHALLENGE.

**Задний план:** За нишами основателей четыре раздельных малых окна участников; в B01 окно студента пустое, затем в B02 только на словах о расширении сообщества появляется общий безымянный силуэт без телефона. Постоянные подписи MARCH 2023 и ILLUSTRATED CONTRIBUTIONS.

**Перекрытия и опоры:** Ниши основателей и окна участников разделены непрозрачными стенками; это не совместная встреча. Фигура появляется в отдельном окне только после речевой фразы о запуске, на словах о расширении сообщества. Пакеты и доска на независимых опорах.

#### P22.B01 · оценочно 06:38.6–06:44.6

> In March twenty twenty-three, Seales, Nat Friedman, and Daniel Gross launched the Vesuvius Challenge.

**Кадр:** Начало фразы: продолжающийся WS контрольных окон P21; после ухода акцента и полного перекрытия — широкий план коллажа рабочих мест P22.

**Камера:** Сначала удержать P21, затем открыть новую сцену после перекрытия; не прерывать речь и не подменять её паузой.

**Действие:** До перехода графа VERIFIED остаётся пустой; затем представить рабочие места конкурса как условный коллаж.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P22.B02 · оценочно 06:44.6–06:49.4

> Scans, software, and prizes brought a wider community into the effort.

**Кадр:** MS, с угла 30° справа на рейку и дополнительные окна.

**Камера:** Статика.

**Действие:** Три пакета SCANS / SOFTWARE / PRIZES доходят до рейки; за ней открываются четыре малых окна. На словах a wider community в одном появляется неназванная карточка общего силуэта со срезанным углом основания, без телефона. Окно отдельно от основателей и других участников, крупный план фигуры не выделяется.

**Акцент:** WIDER COMMUNITY · речевой маркер «a wider community» · расчётное начало 06:46.8. Маска: Буквы разворачиваются из-за торца общей доски слева. Место: В верхней левой четверти, над пакетами и вне силуэтов. Уход: Закрываются назад за торец, когда вид переходит к ролям.

**Звуковой замысел:** Один мягкий щелчок фиксатора на остановке центрального пакета данных. (нового звука пока нет).

#### P22.B03 · оценочно 06:49.4–06:54.9

> Progress could come from someone improving the geometry, someone finding an imaging clue,

**Кадр:** CU, наклонно сверху на две маленькие панели.

**Камера:** Проезд слева направо на 8%.

**Действие:** В первой панели условная поверхность получает непрерывную линию контура; во второй открывается увеличенный кусочек текстуры. Обе панели подписаны SCHEMATIC.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P22.B04 · оценочно 06:54.9–06:58.8

> or someone building a better way to detect ink.

**Кадр:** CU, продолжение того же проезда к третьей панели.

**Камера:** Продолжение равномерного проезда вправо на 5%.

**Действие:** Третья панель отделяет несколько локальных пятен от фона; три разные панели остаются рядом, не превращаясь в один волшебный прибор.

**Акцент:** MANY WAYS IN · речевой маркер «a better way to detect ink» · расчётное начало 06:56.2. Маска: Акцент появляется из-за нижней опоры третьей панели. Место: Нижнее правое свободное поле. Уход: Уходит за опору вместе с закрывающейся крышкой панели.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Крышка третьей панели закрывает весь кадр; она открывается как дверца шкафа SET-L в P23, сразу показывая две разные объектные ячейки.

**Музыкальный замысел:** M2 — аккуратно добавить тихую пульсацию к появлению новых рабочих окон; трек продолжает начатую музыкальную фразу.

**Активы:** P22-A01: три именные ниши основателей без реконструкции конкретной встречи; P22-A02: пакеты SCANS / SOFTWARE / PRIZES и распределительная рейка; P22-A03: три собственные схематические панели геометрии, текстуры и сигнала; P22-A04: карточка даты и два бумажных акцента; P22_COMMUNITY_WINDOW — отдельное окно условного неназванного участника, входит после фразы о запуске; MASTER_LUKE_SILHOUETTE — общий условный профиль на независимом основании, без телефона.

**Граница достоверности:** Условная схема расширения сообщества после запуска, не запись конкретного времени, встречи или места. Фигура не показана основателем или работником организаторов; интервью относит знакомство Фарритора с конкурсом примерно к неделе после запуска. Окна и другие персонажи обобщённые.

**Источники:** S11, S12, S32.

### P23 · оценочно 06:59.1–07:18.4 · SET-L

**Реплика:** The roll at the centre of the next breakthrough was Paris Four. It is a different object from sixteen sixty-seven, the damaged core on our table. Their stories connect through the methods. The words recovered from each must stay attached to that particular roll.

**Цель и тип:** Зритель уверенно связывает следующий эпизод с Paris4, сохраняя 1667 отдельным объектом. (fact model).

**Передний план:** Вертикальный разделитель двух ячеек занимает ближний центральный план; нижние кромки ячеек имеют разные тёплые цвета.

**Средний план:** Слева — условный закрытый рулон в поддерживающей подставке с охристой карточкой PARIS FOUR / PHerc. Paris.4; справа — короткий тёмный сердечник в отдельной подставке с рыжей карточкой PHerc.1667.

**Задний план:** Спокойная стенка шкафа; наверху маленькая подпись DISTINCT OBJECTS — STYLIZED MODELS.

**Перекрытия и опоры:** Разделитель физически пересекает линию взгляда между предметами; никакого морфа одного в другой. Каждый предмет остаётся на собственной подставке. Общая полоса метода проходит только под ячейками.

#### P23.B01 · оценочно 06:59.1–07:04.3

> The roll at the centre of the next breakthrough was Paris Four.

**Кадр:** CU, три четверти слева на ячейку Paris4.

**Камера:** Наезд на 4%.

**Действие:** Дверца левой ячейки открывается, полностью показывая охристую объектную карточку и неподвижный закрытый рулон.

**Акцент:** PARIS FOUR · речевой маркер «Paris Four» · расчётное начало 07:03.4. Маска: Акцент поднимается из-за нижнего охристого борта ячейки. Место: Слева над подставкой, не перекрывая объект. Уход: Складывается за борт, когда открывается вторая ячейка.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P23.B02 · оценочно 07:04.3–07:10.3

> It is a different object from sixteen sixty-seven, the damaged core on our table.

**Кадр:** WS, фронтальный непрерывный план обеих подписанных ячеек и полосы METHOD.

**Камера:** Удержать общий ракурс обеих площадок без склейки до завершения B03.

**Действие:** Обе модели остаются на своих подписанных опорах; между площадками видна отдельная полоса метода.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P23.B03 · оценочно 07:10.3–07:12.9

> Their stories connect through the methods.

**Кадр:** WS, непрерывное продолжение B02.

**Камера:** Небольшой боковой проезд внутри общего плана; обе бирки остаются видимы.

**Действие:** Полоса METHOD соединяет отдельные схемы метода, не физические свитки и не их тексты.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P23.B04 · оценочно 07:12.9–07:18.0

> The words recovered from each must stay attached to that particular roll.

**Кадр:** MS, тот же шкаф с угла 35° справа.

**Камера:** Короткий проезд влево на 5%.

**Действие:** От левой карточки к её собственной рабочей папке идёт охристая бумажная дорожка; правая рыжая дорожка ведёт только к папке 1667. На концах дорожек остаются разные идентификаторы.

**Акцент:** THAT PARTICULAR ROLL · речевой маркер «that particular roll» · расчётное начало 07:16.7. Маска: Буквы выходят из-за центрального разделителя влево. Место: Низ левой ячейки, под её дорожкой и вне бирки. Уход: Уходят обратно за разделитель перед переходом в рабочую область Paris4.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Левая папка Paris4 раскрывается на весь кадр как маска; внутри уже цифровая текстура P24 с тем же охристым идентификатором, без перемещения физического рулона.

**Музыкальный замысел:** M2 — удержать ровный тихий фон; на момент двух предметов убрать лишнюю ритмическую ноту, позволяя рассмотреть идентификаторы.

**Активы:** P23-A01: двухъячеечный шкаф с непрозрачным разделителем; P23-A02: отдельный стилизованный Paris4 и его охристый комплект бирок; P23-A03: отдельный короткий сердечник 1667 и рыжий комплект бирок; P23-A04: общая полоса метода и две раздельные дорожки данных; P23-A05: два бумажных акцента.

**Граница достоверности:** Размеры Paris4 не утверждаются точной масштабной моделью; 1667 сохраняет короткую форму из SET-A. Объекты не меняются местами и не превращаются друг в друга.

**Источники:** S11, S12, S01.

### P24 · оценочно 07:18.4–07:39.3 · SET-H

**Реплика:** Looking through an already mapped section, Casey Handmer noticed a distinctive cracked texture. In places it seemed to form strokes. He shared the observation. It was a clue within data that other people had already scanned and segmented, and it gave the next person something specific to investigate.

**Цель и тип:** Зритель видит, как наблюдение Handmer стало конкретной передаваемой подсказкой внутри коллективно подготовленных данных. (documented-action reconstruction).

**Передний план:** Слева внизу — край рабочего стола и корпус простого устройства просмотра; справа — ближайшая грань увеличительной рамки.

**Средний план:** Условный силуэт CASEY HANDMER за неподвижным столом; крупная цифровая карточка с собственным неписьменным рисунком волокон и растрескавшегося налёта.

**Задний план:** На стене три раздельные карточки SCANNED / SEGMENTED / OBSERVATION, маленькие подписи RECONSTRUCTION и PARIS FOUR DATA — SCHEMATIC.

**Перекрытия и опоры:** Текстура существует на отдельной плоской карточке, не на физически открытом оригинале. Увеличительная рамка перекрывает её край и отбрасывает тень; руки опираются на стол и двигают только рамку. Дополнение v1.3: Единая рейка и отдельные карточки OBSERVATION, SCANNED и SEGMENTED; стойка OBSERVATION перекрывает SHARED CLUE. Текст привязан к этой движущейся карточке.

#### P24.B01 · оценочно 07:18.4–07:23.9

> Looking through an already mapped section, Casey Handmer noticed a distinctive cracked texture.

**Кадр:** MS, через плечо условного Handmer на рабочую карточку.

**Камера:** Плавный наезд на 6%.

**Действие:** Рамка медленно проходит над полосой волокон и останавливается на группе угловатых разрывов; на стене остаётся карточка SEGMENTED.

**Акцент:** CRACKED TEXTURE · речевой маркер «a distinctive cracked texture» · расчётное начало 07:22.2. Маска: Акцент выдвигается из-за правой толстой грани увеличительной рамки. Место: Правая верхняя пустая треть, вне самого исследуемого участка. Уход: Убирается под грань рамки до следующего крупного плана.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P24.B02 · оценочно 07:23.9–07:26.9

> In places it seemed to form strokes.

**Кадр:** ECU, строго сверху на условную текстуру.

**Камера:** Статика.

**Действие:** Маленькие светлые фрагменты налёта образуют несколько линейных направлений; не складываются в выдуманную греческую букву. Тонкая скоба отмечает только их направление.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P24.B03 · оценочно 07:26.9–07:28.6

> He shared the observation.

**Кадр:** WS/MS, фронтально на доску и общую рейку; начало непрерывного плана B03–B04.

**Камера:** Удержать ракурс так, чтобы карточка наблюдения и две предыдущие стадии были раздельны.

**Действие:** Карточка OBSERVATION с условным узором движется по рейке; SCANNED и SEGMENTED остаются на собственных местах.

**Акцент:** SHARED CLUE · речевой маркер «shared the observation» · расчётное начало 07:27.3. Маска: Передняя непрозрачная стойка карточки OBSERVATION скрывает буквы; они выходят позади её края. Место: Свободная нижняя зона у карточки, вне надписей предыдущих этапов. Уход: После читаемой остановки буквы уходят за ту же стойку в продолжающемся плане B04; не перекрывать SCANNED и SEGMENTED.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P24.B04 · оценочно 07:28.6–07:34.6

> It was a clue within data that other people had already scanned and segmented,

**Кадр:** WS/MS, непрерывное продолжение B03 с общей доской.

**Камера:** Мягко перевести внимание от наблюдения к двум карточкам без склейки.

**Действие:** Поочерёдно выделить уже существующие карточки SCANNED и SEGMENTED перед OBSERVATION; работа этих этапов не приписывается Handmer.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P24.B05 · оценочно 07:34.6–07:38.9

> and it gave the next person something specific to investigate.

**Кадр:** CU, верхний вид на конец общей рейки.

**Камера:** Статика.

**Действие:** Карточка наблюдения останавливается у пустого держателя NEXT TEST. Его боковая створка начинает открываться, не показывая будущий ответ.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Створка NEXT TEST перекрывает объектив; за ней рабочий стол Farritor P25 под другим углом. Охристая метка Paris4 остаётся неизменной.

**Музыкальный замысел:** M2 — мягкий небольшой подъём гармонии на передаче наблюдения; музыка не имитирует момент озарения ударом.

**Активы:** P24-A01: условный силуэт Handmer и современный стол без конкретных деталей одежды; P24-A02: собственная схематическая текстура волокон и трещин без букв; P24-A03: объёмная рамка, скоба направления и общая рейка; P24-A04: карточки этапов и два бумажных акцента; REV13_P24_RAIL — Единая рейка и отдельные карточки OBSERVATION, SCANNED и SEGMENTED; стойка OBSERVATION перекрывает SHARED CLUE. Текст привязан к этой движущейся карточке..

**Граница достоверности:** Документировано наблюдение и его публикация; пространственная постановка условна. Не показывать неизвестный точный день открытия, мысли, реплики или истинный скан, созданный генератором.

**Источники:** S12, S13.

### P25 · оценочно 07:39.3–07:57.6 · SET-H

**Реплика:** Luke Farritor, a computer science student in Nebraska, marked examples and trained a model to seek the pattern elsewhere. He improved the model, then inspected another result. Each newly mapped section gave him another opportunity to test whether the clue held up.

**Цель и тип:** Зритель понимает цикл Farritor: разметить пример, обучить, проверить на другом участке. (documented-action reconstruction).

**Передний план:** У переднего края — низкий лоток EXAMPLES; слева корпус рабочего экрана закрывает четверть задней панели.

**Средний план:** Общий условный профиль и срезанный угол отдельного основания за неподвижным столом; при первом произнесении имени отдельная подпись LUKE FARRITOR. Отдельная рука со стилусом и два лотка EXAMPLES / NEW SECTION с неписьменными штрихами; телефона и физического свитка нет.

**Задний план:** Маленькие подписи NEBRASKA, RECONSTRUCTION и SCHEMATIC INTERFACE; охристая объектная метка PARIS FOUR.

**Перекрытия и опоры:** Фигура, рука, стилус и стол закреплены раздельно с физическими точками опоры; рука размечает только бумажную карточку. Экран и стол неподвижны, новая область и примеры разделены бортиком.

#### P25.B01 · оценочно 07:39.3–07:43.6

> Luke Farritor, a computer science student in Nebraska, marked examples

**Кадр:** MS, боковой трёхчетвертной вид на Farritor и стол.

**Камера:** Наезд на 4%.

**Действие:** На первом произнесении Luke Farritor появляется подпись LUKE FARRITOR рядом с общим условным профилем и срезанным углом основания. Отдельная рука со стилусом отмечает условные неписьменные штрихи в лотке EXAMPLES. Телефона и физического свитка нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P25.B02 · оценочно 07:43.6–07:47.4

> and trained a model to seek the pattern elsewhere.

**Кадр:** CU, сверху на два раздельных лотка.

**Камера:** Статика.

**Действие:** Полоска с размеченными примерами входит в щель MODEL; в соседнем лотке NEW SECTION появляются небольшие вероятностные пятна.

**Акцент:** FIND THE PATTERN · речевой маркер «seek the pattern elsewhere» · расчётное начало 07:45.7. Маска: Акцент выходит из-за бортика между EXAMPLES и NEW SECTION. Место: Верхняя свободная полоса над новым участком. Уход: Опускается за разделительный бортик перед заменой результата.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P25.B03 · оценочно 07:47.4–07:50.8

> He improved the model, then inspected another result.

**Кадр:** CU, с уровня края экрана.

**Камера:** Статика.

**Действие:** Старая карточка результата сдвигается в задний лоток, новая устанавливается на её место; силуэт наклоняется только в пределах неподвижного стула.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P25.B04 · оценочно 07:50.8–07:57.3

> Each newly mapped section gave him another opportunity to test whether the clue held up.

**Кадр:** WS, через плечо на экран и подающий лоток.

**Камера:** Медленный отъезд на 5%.

**Действие:** В лоток входит ещё один NEW SECTION с другой формой контура; указатель перемещается к непроверенной области, а не возвращается к уже размеченным образцам.

**Акцент:** TEST AGAIN · речевой маркер «test whether the clue held up» · расчётное начало 07:54.7. Маска: Буквы появляются из-за правой боковой стенки подающего лотка. Место: Нижняя правая треть, вне руки и экрана. Уход: Задвигаются за стенку; лоток остаётся пустым до следующего эпизода.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Монтажная склейка с рабочего устройства на широкий план отдельной условной вечеринки P26. Экран не матчится с реальным интерфейсом. Телефон впервые появляется в реконструкции этого действия; P03 было метафорическим превью.

**Музыкальный замысел:** M3 — за первые 3 секунды плавно добавить более частый тихий пульс поверх продолжающейся M2, без обрыва основной гармонии.

**Активы:** P25-A01: общий условный профиль с отдельным основанием и подписью имени, фигура и рука отдельно; P25-A02: разделённые лотки EXAMPLES / NEW SECTION и стилус; P25-A03: собственные схематические штрихи и карты вероятного сигнала; P25-A04: подписи реконструкции и два бумажных акцента; MASTER_LUKE_SILHOUETTE — общий условный профиль со срезанным углом основания, без телефона.

**Граница достоверности:** Документированный цикл разметки, модели и проверки показан условно, не как точный интерфейс или внешность. Не приписывать студенту исходное сканирование или всю сегментацию; не помещать физический Paris 4 рядом и не показывать завершённый перевод.

**Источники:** S04, S12.

### P26 · оценочно 07:57.6–08:20.7 · SET-I

**Реплика:** Farritor later described receiving news of a new digital section while attending a birthday party in Omaha. He used his phone to start a remote run. After driving friends home, he checked the result near a parking garage. On the screen were more recognizable letters. The ancient object itself had stayed safely elsewhere.

**Цель и тип:** Зритель переживает документированную смену масштаба: современный телефон показывает результат работы с недоступным древним объектом. (documented-action reconstruction).

**Передний план:** Вечеринка: отдельная передняя перегородка и грань телефона; после явной смены места — отдельная стойка парковочного прохода.

**Средний план:** Одинаковый условный профиль и срезанный угол основания: сначала в комнате, позже у парковки. Фигура, рука и телефон раздельны, телефон имеет ту же условную форму, что в P03. Физический Paris 4 только в отдельной архивной ячейке.

**Задний план:** Неназванные условные фигуры и отдельная архивная ячейка Paris 4; маркировки RECONSTRUCTION / SCHEMATIC. OMAHA относится к вечеринке, не к поздней парковке. Интерьер, погода и час не конкретизируются.

**Перекрытия и опоры:** Телефон связан с отдельной рукой, рука — с телом, ноги стоят на опоре. Вечеринка и поздняя проверка у парковки разделены явной сменой места. Схемы не изображают реальный интерфейс или факсимиле; физический свиток не рядом с героем.

#### P26.B01 · оценочно 07:57.6–08:04.9

> Farritor later described receiving news of a new digital section while attending a birthday party in Omaha.

**Кадр:** WS, через перегородку на условную общую комнату.

**Камера:** Небольшой проезд вправо на 5%.

**Действие:** Герой держит телефон в общей комнате; на пустом светлом экране только ненадписанная условная пиктограмма уведомления о новом цифровом участке, с маркировкой SCHEMATIC вне устройства. Нет букв, точного текста сообщения, результата, реплик и выдуманных эмоций.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P26.B02 · оценочно 08:04.9–08:08.8

> He used his phone to start a remote run.

**Кадр:** ECU, через плечо на телефон и палец.

**Камера:** Статика.

**Действие:** Палец касается нейтрального пустого экрана; вне устройства отдельная помеченная SCHEMATIC линия соединяет телефон со значком удалённого компьютера. Это условное объяснение дистанционного запуска после уведомления, не реконструированный интерфейс и не вычисление на самом телефоне.

**Акцент:** REMOTE RUN · речевой маркер «a remote run» · расчётное начало 08:07.5. Маска: Буквы выдвигаются из-за правого торца объёмного телефона. Место: Справа от телефона, в чистом поле; не поверх интерфейса. Уход: Скрываются за его торцом перед монтажной сменой места.

**Звуковой замысел:** Один очень тихий короткий электронный щелчок, синхронный видимому касанию пустого экрана; звук пока не создан. (нового звука пока нет).

#### P26.B03 · оценочно 08:08.8–08:13.9

> After driving friends home, he checked the result near a parking garage.

**Кадр:** WS, новый план на нейтральный парковочный проход.

**Камера:** Статика.

**Действие:** После вечеринки и поездки, сообщаемой речью, явная смена места открывает нейтральный парковочный проход. Тот же условный персонаж на собственной опоре поднимает тот же телефон для проверки. Маршрут, адрес, погода и часы не показываются.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P26.B04 · оценочно 08:13.9–08:16.9

> On the screen were more recognizable letters.

**Кадр:** CU, профиль силуэта и телефон ниже линии лица.

**Камера:** Плавный наезд на 4%.

**Действие:** Только после поездки и проверки у парковки на экране возникают абстрактные неписьменные штрихи; отдельная метка RESULT — SCHEMATIC поясняет, что это не реальный интерфейс, фотография или последовательность найденных букв. Полного слова нет.

**Акцент:** MORE LETTERS · речевой маркер «more recognizable letters» · расчётное начало 08:15.6. Маска: Буквы поднимаются из-за нижнего края корпуса телефона. Место: Нижний левый свободный участок кадра, вдали от лица. Уход: Возвращаются за корпус до последнего предложения.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P26.B05 · оценочно 08:16.9–08:20.3

> The ancient object itself had stayed safely elsewhere.

**Кадр:** WS, фронтально на отдельный макет архивной ячейки.

**Камера:** Статика.

**Действие:** Монтажный стык в другой масштаб: закрытый стилизованный Paris4 неподвижен в подставке, рядом карточка PHYSICAL OBJECT / INSTITUT DE FRANCE. Телефона и Farritor здесь нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Охристая карточка Paris4 задвигается в передний паз и заполняет кадр; на другой стороне карточки в P27 появляется редакционная транскрипция, без превращения оригинала в экран.

**Музыкальный замысел:** M3 — пульс тихо держит действие; на появлении результата лёгкое гармоническое раскрытие без победного удара, на архивной ячейке один слой пульса убирается.

**Активы:** P26-A01: нейтральная комната с перегородкой и неназванными силуэтами; P26-A02: тот же условный силуэт, отдельные рука и телефон; пустой экран, безымянное условное уведомление и внешняя схема удалённого компьютера; P26-A03: отдельная нейтральная гаражная стойка и проход; P26-A04: самостоятельная архивная ячейка Paris4 с подставкой; P26-A05: подписи RECONSTRUCTION / SCHEMATIC и два бумажных акцента; MASTER_LUKE_SILHOUETTE — общий условный профиль и срезанный угол основания; MASTER_LUKE_PHONE — та же форма отдельного телефона с пустым экраном, крепление к руке.

**Граница достоверности:** Две публикации передают рассказ одного участника, не независимые свидетельства очевидцев. Порядок: уведомление о цифровом участке на вечеринке в Омахе → удалённый запуск на другом компьютере → поездка → просмотр у парковки. Не уточнять дату, маршрут, интерьер, одежду, время, погоду, диалоги, эмоции и буквы. Paris 4 показан только в отдельной ячейке.

**Источники:** S04, S32.

### P27 · оценочно 08:20.7–08:38.8 · SET-J

**Реплика:** One sequence was read as a Greek word associated with purple. The First Letters prizes were announced in October twenty twenty-three. A colour had become evidence that the signal could be followed. The inside was beginning to yield readable writing.

**Цель и тип:** Зритель получает первое узнаваемое слово и видит его как ограниченное, проверяемое доказательство. (evidence graphic).

**Передний план:** Ближайшая часть — нижний бортик держателя транскрипции; слева — толстая стойка маленького календарного окна.

**Средний план:** Собственная наборная карточка ΠΟΡΦΥΡΑϹ / porphyras с меткой TRANSCRIPTION, NOT FACSIMILE; охристая бирка PARIS FOUR.

**Задний план:** Сдержанная рабочая доска с маленькой подписью SOURCE: VESUVIUS CHALLENGE, 12 OCT 2023; рядом отдельное окно OCTOBER 2023.

**Перекрытия и опоры:** Слово закреплено в держателе; окно даты находится глубже. Акцент PURPLE выходит только на произнесённом purple и не закрывает ни один знак транскрипции.

#### P27.B01 · оценочно 08:20.7–08:25.4

> One sequence was read as a Greek word associated with purple.

**Кадр:** ECU, фронтально на проверенную транскрипцию.

**Камера:** Медленный отъезд на 4%, открывающий метку TRANSCRIPTION.

**Действие:** Восемь вручную набранных знаков ΠΟΡΦΥΡΑϹ неподвижны; на слове purple рядом открывается небольшая цветовая карточка. Никакой анимации угадывания букв.

**Акцент:** PURPLE · речевой маркер «purple» · расчётное начало 08:25.0. Маска: Акцент выходит слева из-за нижнего бортика держателя. Место: Снизу под строкой транскрипции, в отдельном свободном поле. Уход: Уходит под бортик перед календарным планом.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P27.B02 · оценочно 08:25.4–08:29.7

> The First Letters prizes were announced in October twenty twenty-three.

**Кадр:** MS, с угла 30° справа на календарное окно.

**Камера:** Статика.

**Действие:** Створка открывает OCTOBER 2023 и небольшую редакционную карточку FIRST LETTERS PRIZES. Без сцены вручения и без придуманных аплодисментов.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P27.B03 · оценочно 08:29.7–08:34.4

> A colour had become evidence that the signal could be followed.

**Кадр:** CU, сверху на транскрипцию и маленькую полосу цифровой поверхности.

**Камера:** Проезд вправо на 5%.

**Действие:** От слова к обозначенному участку Paris4 проходит бумажная скоба; на поверхности используются только схематические метки расположения, а не выдуманный скан.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P27.B04 · оценочно 08:34.4–08:37.8

> The inside was beginning to yield readable writing.

**Кадр:** WS, сверху на закрытую миниатюру Paris4 в отдельном отсеке и её цифровую карточку.

**Камера:** Статика.

**Действие:** Открывается узкое контрольное окно только в цифровой карточке; миниатюра оригинала остаётся свёрнутой.

**Акцент:** READABLE WRITING · речевой маркер «readable writing» · расчётное начало 08:37.0. Маска: Акцент выдвигается из-за рамки цифрового контрольного окна. Место: Правая верхняя свободная четверть, вне оригинала и транскрипции. Уход: Скрывается за рамкой, которая остаётся открытой для сравнения в P28.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Контрольное окно остаётся на том же месте; явный монтажный переход на значительно более широкий парный сравнительный стенд P28. Бирка Paris4 передаётся без смены объекта.

**Музыкальный замысел:** M3 — короткое тёплое разрешение гармонии на purple; затем вернуть тихий рабочий пульс без фанфар и остановки.

**Активы:** P27-A01: собственная посимвольная векторная транскрипция ΠΟΡΦΥΡΑϹ / porphyras по официальному First Letters, без копирования скана; P27-A02: бумажный держатель, окно даты OCTOBER 2023 и подпись источника; P27-A03: отдельный закрытый макет Paris4 и цифровое контрольное окно; P27-A04: цветовая карточка и два бумажных акцента.

**Граница достоверности:** Греческая последовательность проверена по S12 / https://scrollprize.org/firstletters; собственные векторные знаки не факсимиле чужого изображения. Перевод связан с purple, точная грамматическая форма и граница слова первоначально обсуждались. Не изображать конкретный пурпурный предмет, рецепт или владельца.

**Источники:** S12, S14.

### P28 · оценочно 08:38.8–08:58.0 · SET-H

**Реплика:** Youssef Nader produced another clear result from the same region using his own approach. He knew about the earlier findings and investigated the clue further. Different methods could now be compared. The question was whether those promising strokes could hold together as readable text.

**Цель и тип:** Зритель видит дополнительный результат Nader и понимает, что сравниваются методы работы с одним участком. (documented-action reconstruction).

**Передний план:** Внизу слева — непрозрачный бортик лотка сравнения; справа — край переднего держателя карточек.

**Средний план:** Две схематические карты одной области с одинаковым контуром и регистрационными вырезами; за правой — условный силуэт YOUSSEF NADER у отдельного рабочего стола.

**Задний план:** Маленькие подписи RECONSTRUCTION / METHOD COMPARISON — SCHEMATIC / PARIS FOUR. Отдельная карточка EARLIER RESULT видна с краю.

**Перекрытия и опоры:** Две карты закреплены в соседних держателях, ни одна не появляется поверх лица. Рамки могут выдвигаться к общей линии регистрации, но сохраняют физическую толщину и отдельные тени.

#### P28.B01 · оценочно 08:38.8–08:44.8

> Youssef Nader produced another clear result from the same region using his own approach.

**Кадр:** MS, фронтально на парные карты и правую рабочую нишу.

**Камера:** Плавный наезд на 5%.

**Действие:** Правая карта NADER устанавливается рядом с предыдущей; одинаковые регистрационные вырезы показывают, что область та же, а распределение условных пятен слегка отличается.

**Акцент:** SAME REGION · речевой маркер «the same region» · расчётное начало 08:41.8. Маска: Акцент выходит из-за переднего бортика сравнительного лотка. Место: Нижняя центральная свободная полоса под картами. Уход: Уходит вниз за бортик до смены угла.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P28.B02 · оценочно 08:44.8–08:49.5

> He knew about the earlier findings and investigated the clue further.

**Кадр:** CU, через плечо условного Nader на край рабочего места.

**Камера:** Статика.

**Действие:** Карточка EARLIER RESULT открыта рядом с новыми заметками. Палец переходит от её выреза к совпадающему вырезу нового участка; сообщения и цитаты не показываются.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P28.B03 · оценочно 08:49.5–08:52.1

> Different methods could now be compared.

**Кадр:** ECU, сверху на совпадающие контуры двух карт.

**Камера:** Проезд вправо на 5%.

**Действие:** Общая регистрационная линейка проходит между картами. Две маленькие метки останавливаются напротив соответствующих участков, не сливая данные в одну выдуманную картинку.

**Акцент:** COMPARE METHODS · речевой маркер «Different methods» · расчётное начало 08:49.5. Маска: Буквы выезжают из-за правой стойки переднего держателя. Место: Верхний правый свободный угол, за пределами карт. Уход: Карточка акцента скрывается за стойкой при переходе к последнему плану.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P28.B04 · оценочно 08:52.1–08:57.7

> The question was whether those promising strokes could hold together as readable text.

**Кадр:** WS, с верхней точки на сравнение и пустое поле READING.

**Камера:** Медленный отъезд на 6%.

**Действие:** Две карты остаются рядом; под ними открывается длинный, пока пустой держатель для связного чтения. Отдельные пятна не превращаются автоматически в предложение.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Длинный пустой держатель проходит горизонтально перед объективом; монтажный переход на значительно более крупный держатель цифровой поверхности P29, с той же охристой меткой Paris4.

**Музыкальный замысел:** M3 — тихий пульс продолжается; сравнительная сцена получает более устойчивую гармонию без дополнительного ускорения.

**Активы:** P28-A01: условный силуэт Nader и отдельный рабочий стол; P28-A02: две собственные карты одной области с регистрационными вырезами; P28-A03: карточка EARLIER RESULT, линейка и пустой держатель READING; P28-A04: подписи схемы и два бумажных акцента.

**Граница достоверности:** Nader знал ранние результаты; постановка не представляет открытие как слепое совпадение. Сравниваемые изображения — собственная схема, не факсимиле результатов разных команд.

**Источники:** S12, S15.

### P29 · оценочно 08:58.0–09:18.5 · SET-F

**Реплика:** Julian Schilliger worked on another essential part: making more of the wound surface available for analysis. Better segmentation exposed larger digital regions. For the grand prize, Nader, Farritor, and Schilliger combined their work. The readable image depended on geometry, ink detection, and the labour that connected them.

**Цель и тип:** Зритель понимает вклад Schilliger и видит, что читаемый результат требует совместной работы с геометрией и сигналом. (fact model).

**Передний план:** Слева близко к камере — толстый край цифрового смотрового окна; внизу — рейка с тремя независимыми входными лотками.

**Средний план:** Большая охристая цифровая поверхность с изгибами, отдельная светлая развёртка и маленькая карточка JULIAN SCHILLIGER / SEGMENTATION.

**Задний план:** В отдельном заднем отсеке неподвижен закрытый стилизованный Paris4 с подписью PHYSICAL ORIGINAL; большие формы помечены DIGITAL MODEL.

**Перекрытия и опоры:** Разворачивается только светлая цифровая копия на своём держателе. Чёрный оригинал в задней ячейке не соединён физическим листом с моделью и не меняет форму. Передняя оконная рама действительно перекрывает края цифровой поверхности.

#### P29.B01 · оценочно 08:58.0–09:04.9

> Julian Schilliger worked on another essential part: making more of the wound surface available for analysis.

**Кадр:** MS, косой верхний вид на изогнутую цифровую поверхность.

**Камера:** Проезд вправо на 7%.

**Действие:** Тонкая линия следует вдоль одного уже видимого изгиба; рядом устанавливается именная карточка Schilliger с указанием роли, без сцены его присутствия в лаборатории.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P29.B02 · оценочно 09:04.9–09:07.5

> Better segmentation exposed larger digital regions.

**Кадр:** WS, фронтально на цифровое смотровое окно.

**Камера:** Плавный отъезд на 6%.

**Действие:** Две боковые створки смотрового окна расходятся, показывая более длинную часть цифровой поверхности; под ней расширяется её плоское отображение.

**Акцент:** MORE SURFACE · речевой маркер «larger digital regions» · расчётное начало 09:06.2. Маска: Акцент поднимается из-за нижней кромки большого цифрового окна. Место: В нижнем правом свободном поле, вне поверхности. Уход: Уходит за кромку к началу следующей фразы.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P29.B03 · оценочно 09:07.5–09:12.2

> For the grand prize, Nader, Farritor, and Schilliger combined their work.

**Кадр:** CU, сверху на три входных лотка.

**Камера:** Статика.

**Действие:** Карточки NADER / FARRITOR / SCHILLIGER сходятся к общей рейке, оставаясь тремя отдельными подписанными вкладами.

**Акцент:** COMBINED WORK · речевой маркер «combined their work» · расчётное начало 09:10.9. Маска: Буквы выходят из-за переднего борта общей рейки. Место: Над нижней направляющей, не поверх имён. Уход: Уходят под направляющую после стыковки.

**Звуковой замысел:** Один тихий деревянный щелчок на стыковке центрального фиксатора общей рейки. (нового звука пока нет).

#### P29.B04 · оценочно 09:12.2–09:18.2

> The readable image depended on geometry, ink detection, and the labour that connected them.

**Кадр:** MS, с низкого угла на последовательность трёх рабочих панелей.

**Камера:** Плавный проезд влево на 6%.

**Действие:** Панель GEOMETRY совмещает контуры, INK DETECTION выделяет местные пятна, CHECKED IMAGE принимает готовую карточку. Между панелями остаются видимые ручные контрольные метки; никакой кнопки мгновенного перевода.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Конверт на собственной опоре полностью перекрывает экран до смены ракурса и пространства; после перекрытия открыть отдельную схему проверки P30.

**Музыкальный замысел:** M3 — добавить сдержанный подъём на соединении вкладов; удержать тихий рабочий ритм, не переходить к победной теме раньше проверки.

**Активы:** P29-A01: собственная изогнутая цифровая поверхность и отдельная плоская развёртка; P29-A02: отдельный задний отсек с закрытым стилизованным Paris4; P29-A03: три именные карточки и общая рейка вкладов; P29-A04: панели GEOMETRY / INK DETECTION / CHECKED IMAGE; P29-A05: большой смотровой портал и два бумажных акцента.

**Граница достоверности:** Схема метода, не точное воспроизведение программы или конкретной сегментации. Не приписывать одному Schilliger всю разметку; командные карточки не означают документированную встречу в одном месте.

**Источники:** S11, S16.

### P30 · оценочно 09:18.5–09:37.3 · SET-J

**Реплика:** Judging required more than a striking picture. Specialists examined anonymized submissions while the technical team reproduced methods. The letters had to be distinguishable, without filling the gaps simply because a particular Greek sentence would make sense. The evidence had to support the reading.

**Цель и тип:** Зритель понимает проверку как воспроизводимость изображения и чтение наблюдаемых букв без заполнения пробелов догадкой. (evidence graphic).

**Передний план:** Внизу — передний край отдельного контрольного стола; слева — непрозрачный клапан конверта SUBMISSION.

**Средний план:** Несколько разнесённых карточек ANONYMOUS SUBMISSION, CODE RE-RUN и INDEPENDENT READING; маленькие окна условных штрихов и пустых мест.

**Задний план:** Нейтральная доска с подписью REVIEW PROCESS — SCHEMATIC. Независимые чтения представлены разделёнными панелями, а не общей встречей людей.

**Перекрытия и опоры:** Клапаны закрывают имена участников на заявках. Данные и экспертные панели имеют собственные опоры. Пустые окна — настоящие прорези, через которые виден фон, а не область для автоматического появления текста.

#### P30.B01 · оценочно 09:18.5–09:21.5

> Judging required more than a striking picture.

**Кадр:** CU, сверху на закрытый конверт и край яркого изображения.

**Камера:** Статика.

**Действие:** Конверт открывает красивую схематическую картинку, но рядом остаётся незаполненная контрольная карточка; само появление изображения не включает знак успеха.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P30.B02 · оценочно 09:21.5–09:25.8

> Specialists examined anonymized submissions while the technical team reproduced methods.

**Кадр:** WS, фронтально на разделённые панели проверки; продолжить этот план в начало речи B03.

**Камера:** Удержать общий план до завершения остановки и ухода REPRODUCE; затем склейка на макро B03–B04.

**Действие:** В левых независимых панелях рассматриваются обезличенные карты; справа из лотка CODE RE-RUN выходит второй экземпляр условного результата. В начале B03 общий план сохраняется до завершения надписи.

**Акцент:** REPRODUCE · речевой маркер «reproduced methods» · расчётное начало 09:25.0. Маска: Акцент выдвигается из-за передней стенки лотка CODE RE-RUN. Место: Нижняя правая свободная четверть, вне карт. Уход: После полной читаемой остановки опустить за стенку CODE RE-RUN; лишь затем перейти на макроплан.

**Звуковой замысел:** Один мягкий контакт бумажной карты с упором лотка на завершении повторного вывода. (нового звука пока нет).

#### P30.B03 · оценочно 09:25.8–09:28.4

> The letters had to be distinguishable,

**Кадр:** ECU сверху на контрольную рамку и прорезь; склейка на него возможна уже после начала фразы.

**Камера:** Статично; затем продолжить тот же план в B04.

**Действие:** Рамка охватывает видимый штрих и останавливается у пустой прорези; подпись SCHEMATIC остаётся читаемой.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P30.B04 · оценочно 09:28.4–09:34.0

> without filling the gaps simply because a particular Greek sentence would make sense.

**Кадр:** ECU, продолжение того же плана без склейки.

**Камера:** Медленный боковой проезд на 3%, показывающий глубину прорези.

**Действие:** Пустой промежуток остаётся настоящим отверстием до конца фразы. Изображение не достраивается, не появляются призрачные или угаданные буквы.

**Акцент:** NO FILLING GAPS · речевой маркер «without filling the gaps» · расчётное начало 09:28.4. Маска: Буквы поднимаются из-за нижнего внешнего борта контрольной рамки. Место: Под рамкой, не поверх пустоты или наблюдаемого штриха. Уход: Складываются за борт, оставляя пустой промежуток видимым.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P30.B05 · оценочно 09:34.0–09:37.0

> The evidence had to support the reading.

**Кадр:** MS, сбоку на отдельные результаты проверки.

**Камера:** Статика.

**Действие:** Картинки повторного вывода и чтений устанавливаются в один держатель рядом с исходной картой. Их подписи сохраняются; итоговая карточка готова к объявлению, но не превращается в доказательство безошибочности каждого знака.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Сдвиг верхней планки держателя создаёт сплошную кремовую маску; в P31 планка становится кромкой календарного окна с другой композицией и более широким планом.

**Музыкальный замысел:** M3 — заметно разредить пульс, чтобы процедура проверки звучала спокойно; гармония продолжается без паузы и перезапуска.

**Активы:** P30-A01: конверты заявок с непрозрачными именными клапанами; P30-A02: раздельные панели воспроизведения и независимых чтений; P30-A03: собственная схематическая контрольная карта без букв с настоящими прорезями; P30-A04: держатель результата и два бумажных акцента.

**Граница достоверности:** Схема отражает анонимизированную папирологическую проверку и техническое воспроизведение. Не инсценируется документальная групповая встреча; условные штрихи не являются подлинной транскрипцией Paris4.

**Источники:** S11, S17.

### P31 · оценочно 09:37.3–09:54.8 · SET-J

**Реплика:** On February fifth, twenty twenty-four, the organizers announced the winners of the twenty twenty-three grand prize. Nader, Farritor, and Schilliger shared the seven-hundred-thousand-dollar award. Their combined work had passed the examination. The object behind this breakthrough was still Paris Four.

**Цель и тип:** Зритель различает год конкурса и дату объявления, а победу связывает с командой и Paris4. (evidence graphic).

**Передний план:** Слева близко к камере — боковина календарного окна; снизу — передний борт общей наградной плашки.

**Средний план:** Отдельная карточка 5 FEBRUARY 2024, под ней 2023 GRAND PRIZE; три именные карточки NADER / FARRITOR / SCHILLIGER связаны одной плашкой $700,000.

**Задний план:** В правой глубине — закрытая охристая папка PARIS FOUR и небольшой стилизованный рулон в самостоятельной опоре; подпись EDITORIAL TIMELINE.

**Перекрытия и опоры:** Дата и год приза находятся на разных бумажных уровнях. Общая сумма — одна плашка под тремя именами; её не делят на равные конверты. Paris4 остаётся отдельным закрытым предметом.

#### P31.B01 · оценочно 09:37.3–09:44.2

> On February fifth, twenty twenty-four, the organizers announced the winners of the twenty twenty-three grand prize.

**Кадр:** WS, фронтально на календарное окно и общую композицию.

**Камера:** Плавный наезд на 5%.

**Действие:** Календарная створка открывает 5 FEBRUARY 2024; ниже уже закреплена отдельная строка 2023 GRAND PRIZE. На словах announced the winners именные клапаны становятся открытыми.

**Акцент:** WINNERS · речевой маркер «the winners» · расчётное начало 09:40.7. Маска: Акцент выходит из-за левой боковины календарного окна. Место: Верхняя левая свободная треть, вне даты. Уход: Скрывается за боковиной к переходу на сумму.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P31.B02 · оценочно 09:44.2–09:47.6

> Nader, Farritor, and Schilliger shared the seven-hundred-thousand-dollar award.

**Кадр:** MS, сверху под углом 25° на три имени и одну сумму.

**Камера:** Статика.

**Действие:** Общая плашка $700,000 поднимается до нижней линии всех трёх имён; одинаковые тонкие скобы соединяют её с командой, не обозначая доли распределения.

**Акцент:** SHARED AWARD · речевой маркер «shared the seven-hundred-thousand-dollar award» · расчётное начало 09:45.9. Маска: Буквы поднимаются из-за переднего борта общей плашки. Место: Под суммой, в нижнем свободном поле. Уход: Уходят под борт перед возвращением к проверке.

**Звуковой замысел:** Один тихий глухой контакт при остановке наградной плашки на держателе. (нового звука пока нет).

#### P31.B03 · оценочно 09:47.6–09:50.6

> Their combined work had passed the examination.

**Кадр:** CU, сбоку на держатель проверок из P30.

**Камера:** Статика.

**Действие:** Карточка REVIEW COMPLETED устанавливается перед сохранёнными раздельными проверками. Никакой печати PERFECT или EVERY LETTER CORRECT не появляется.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P31.B04 · оценочно 09:50.6–09:54.5

> The object behind this breakthrough was still Paris Four.

**Кадр:** CU, с правой стороны на охристую бирку и закрытый Paris4.

**Камера:** Медленный отъезд на 4%.

**Действие:** Вся наградная графика остаётся в нерезком фоне; на переднем плане чётко читается PARIS FOUR. Оригинал не раскрывается.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Прямой переход с бирки Paris4 на верхний план статистической карточки с тем же названием, но меньшим масштабом. Дата FEBRUARY 2024 остаётся в углу для P32.

**Музыкальный замысел:** M3 — короткое сдержанное гармоническое раскрытие на общей награде; без фанфар, аплодисментов и нового музыкального старта.

**Активы:** P31-A01: календарное окно и раздельные карточки даты объявления и года конкурса; P31-A02: три именные карточки и одна общая плашка $700,000; P31-A03: сохранённый держатель проверок с редакционной карточкой REVIEW COMPLETED; P31-A04: отдельная папка и стилизованный закрытый Paris4; P31-A05: два бумажных акцента.

**Граница достоверности:** Объявление состоялось 5 февраля 2024 за конкурс 2023. Общая сумма не означает равные доли. Нет реконструкции церемонии, денежной передачи или реального документа о награждении.

**Источники:** S11.

### P32 · оценочно 09:54.8–10:13.1 · SET-L

**Реплика:** At that point, the organizers estimated that about five percent of Paris Four had been unwrapped and read. Parts of multiple columns were visible. Most of the roll remained beyond reach, but there was enough writing to begin following an ancient argument.

**Цель и тип:** Зритель воспринимает пять процентов как оценку конкретного этапа 2024 года и понимает ценность неполного текста. (evidence graphic).

**Передний план:** Нижний охристый борт статистического лотка; справа ближе к камере — рамка отдельного цифрового окна.

**Средний план:** Сетка из двадцати одинаковых бумажных плиток; рядом три условных колоночных окна с неровными краями и неписьменными полосами.

**Задний план:** Закрытая папка PARIS FOUR; постоянные подписи ESTIMATE AT ANNOUNCEMENT / FEBRUARY 2024 / SCHEMATIC PROPORTION.

**Перекрытия и опоры:** Сетка — отдельная диаграмма, не карта физического места прочтения. Одна из двадцати плиток окрашивается как доля, но не вынимается из древнего свитка. Рамки колонок реально скрывают края цифровых полос.

#### P32.B01 · оценочно 09:54.8–10:02.5

> At that point, the organizers estimated that about five percent of Paris Four had been unwrapped and read.

**Кадр:** WS, строго сверху на сетку и подписи.

**Камера:** Плавный наезд на 5%.

**Действие:** На about five percent одна плитка из двадцати становится тёпло-охристой; остальные остаются нейтральными. Подпись FEBRUARY 2024 не исчезает.

**Акцент:** ABOUT FIVE PERCENT · речевой маркер «about five percent» · расчётное начало 09:57.8. Маска: Акцент выдвигается из-за нижнего охристого борта лотка. Место: Нижняя треть вне сетки и даты. Уход: Уходит за борт до смены изображения.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P32.B02 · оценочно 10:02.5–10:05.1

> Parts of multiple columns were visible.

**Кадр:** CU, наклонный вид на три разные колоночные рамки.

**Камера:** Статика.

**Действие:** В каждой рамке видны только части собственных условных полос; высота и сохранность разные. Новые строки не дорисовываются по краям.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P32.B03 · оценочно 10:05.1–10:12.8

> Most of the roll remained beyond reach, but there was enough writing to begin following an ancient argument.

**Кадр:** MS, фронтально на колоночные окна и отдельную редакционную карточку.

**Камера:** Медленный отъезд на 6%.

**Действие:** Большая нейтральная область остаётся закрыта; из нескольких видимых окон к карточке ARGUMENT идёт одна тонкая полоса связи. Карточка пока не сообщает конкретного содержания.

**Акцент:** ANCIENT ARGUMENT · речевой маркер «an ancient argument» · расчётное начало 10:11.5. Маска: Буквы появляются из-за правой толстой стойки цифрового окна. Место: Верхняя правая пустая четверть. Уход: Скрываются за стойкой, пока карточка ARGUMENT поворачивается к следующей сцене.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Редакционная карточка ARGUMENT поворачивается своей чистой оборотной стороной к камере и полностью закрывает кадр; обратная сторона в P33 становится отдельной сценой PARAPHRASE, без превращения оригинала в философский театр.

**Музыкальный замысел:** M3 — уменьшить частоту пульса и открыть тёплые гармоники; музыкальная фраза ведёт к содержанию текста.

**Активы:** P32-A01: сетка из двадцати одинаковых плиток, ровно одна выделенная; P32-A02: три собственных схематических колоночных окна без древнего текста; P32-A03: карточка ARGUMENT, рамки и постоянная дата FEBRUARY 2024; P32-A04: два бумажных акцента.

**Граница достоверности:** Пять процентов — приблизительная оценка февраля 2024, не нынешняя доля чтения и не точная пространственная карта. Три окна — схема нескольких частей колонок, не заявление об их общем количестве.

**Источники:** S11, S14.

### P33 · оценочно 10:13.1–10:35.1 · SET-K

**Реплика:** The passages discuss pleasure and perception, with references to food and music. One question is whether scarcity makes something more enjoyable. The author resists the idea that rare food must automatically provide greater pleasure than food available in abundance. Across the damaged surface, a recognizably human disagreement had survived.

**Цель и тип:** Зритель узнаёт в древнем рассуждении знакомый вопрос о том, почему редкое кажется более желанным. (explanatory metaphor).

**Передний план:** Внизу — край низкой театральной сцены; слева и справа ближе к камере — небольшие боковые кулисы.

**Средний план:** Две одинаковые условные чаши: в одной один нейтральный бумажный кусочек, в другой пять одинаковых; рядом два безымянных плоских профиля без исторической одежды.

**Задний план:** Отдельные маленькие знаки FOOD / MUSIC / PERCEPTION; постоянная метка ILLUSTRATION — PARAPHRASE OF PARIS FOUR, без древних цитат.

**Перекрытия и опоры:** Чаши стоят на общей неподвижной поверхности и не меняют объём. Фигуры остаются безымянными условными знаками. Любой текст акцента выходит из реальной кулисы, не изо рта персонажа.

#### P33.B01 · оценочно 10:13.1–10:18.3

> The passages discuss pleasure and perception, with references to food and music.

**Кадр:** WS, фронтально на маленький философский театр.

**Камера:** Медленный проезд вправо на 5%.

**Действие:** Три отдельные створки открывают знаки еды, музыкальной струны и восприятия; затем в центре остаются две чаши.

**Акцент:** PLEASURE · речевой маркер «pleasure» · расчётное начало 10:14.4. Маска: Акцент появляется из-за левой боковой кулисы. Место: Верхняя левая свободная зона, выше знаков. Уход: Уходит за кулису до сравнения количества.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P33.B02 · оценочно 10:18.3–10:22.1

> One question is whether scarcity makes something more enjoyable.

**Кадр:** CU, сверху на две одинаковые чаши.

**Камера:** Статика.

**Действие:** Между чашами поднимается небольшая карточка с вопросительным знаком; один кусочек и пять кусочков остаются одинакового вида. Никакой цены или шкалы вкуса нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P33.B03 · оценочно 10:22.1–10:29.9

> The author resists the idea that rare food must automatically provide greater pleasure than food available in abundance.

**Кадр:** MS, с низкой точки через край сцены.

**Камера:** Плавный наезд на 4%.

**Действие:** Над чашей с одним кусочком начинается стрелка к слову BETTER, но между ними выдвигается бумажный вопросительный разделитель; стрелка не завершается. Обе чаши остаются на одном уровне.

**Акцент:** NOT AUTOMATICALLY · речевой маркер «automatically provide greater pleasure» · расчётное начало 10:26.0. Маска: Буквы выезжают из-за правой кулисы. Место: Нижняя правая свободная четверть, вне чаш и условных лиц. Уход: Уходят за кулису перед возвращением к повреждённой поверхности.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P33.B04 · оценочно 10:29.9–10:34.1

> Across the damaged surface, a recognizably human disagreement had survived.

**Кадр:** ECU, сверху на отдельную редакционную карточку пересказа за неровной рамкой.

**Камера:** Статика.

**Действие:** Монтажный переход к схематической цифровой полосе с утратами; за её отдельным держателем лежит карточка SCARCITY DOES NOT GUARANTEE GREATER PLEASURE / PARAPHRASE. Неровные края остаются видимыми, а подпись не выдаётся за перевод строки.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Неровная рамка закрывается двумя боковыми створками; в P34 они открывают шкаф идентификации с отдельными пустыми полями автора и названия. Масштаб меняется с макро на средний.

**Музыкальный замысел:** M3 — тёплая разрешённая гармония, пульс становится редким; на последнем предложении сохранить длинную спокойную ноту, без звуков условной еды и разговора.

**Активы:** P33-A01: собственный условный театр с двумя одинаковыми чашами и шестью одинаковыми бумажными кусочками; P33-A02: два безымянных профиля и знаки FOOD / MUSIC / PERCEPTION; P33-A03: вопросительная перегородка и незавершённая стрелка; P33-A04: редакционная карточка пересказа и отдельная неровная цифровая рамка; P33-A05: два бумажных акцента.

**Граница достоверности:** Это явно помеченный пересказ философского содержания, не конкретная еда, пир, эксперимент или реконструкция поведения автора. Никому не приписаны имя и реплики. Редакционная английская карточка не представлена дословной древней цитатой.

**Источники:** S11, S14.

### P34 · оценочно 10:35.1–10:51.4 · SET-L

**Реплика:** Paris Four still has no secure author or title. What survives gives us part of a text and its argument. A convincing story about who wrote it cannot substitute for the missing identification. That question remains open.

**Цель и тип:** Зритель принимает неизвестное авторство и название как сохраняющуюся границу результата. (evidence graphic).

**Передний план:** Внизу — широкий охристый бортик карточного ящика; слева перед ним — толстая рамка регистрационной карточки.

**Средний план:** Карточка PARIS FOUR с двумя пустыми полями AUTHOR / TITLE; отдельно видимая папка CONTENT с маленькой карточкой PLEASURE / PERCEPTION.

**Задний план:** Неподвижный закрытый стилизованный Paris4 в своей ячейке, мягкий свет без портрета предполагаемого автора.

**Перекрытия и опоры:** Поля автора и названия — реальные пустые прорези карточки. Карточка содержания находится на другом уровне и физически не может закрыть эти поля. Предмет и его идентификатор сохраняются в кадре. Дополнение v1.3: Отдельная регистрационная рамка и её вертикальная стойка перекрывают NO SUBSTITUTE; поля AUTHOR и TITLE не заполняются.

#### P34.B01 · оценочно 10:35.1–10:39.0

> Paris Four still has no secure author or title.

**Кадр:** MS, фронтально на регистрационную карточку и отдельный объект.

**Камера:** Наезд на 4%.

**Действие:** Открываются два поля AUTHOR / TITLE, оба пустые; маленькая подпись UNIDENTIFIED остаётся рядом с ними.

**Акцент:** AUTHOR UNKNOWN · речевой маркер «no secure author» · расчётное начало 10:36.9. Маска: Акцент поднимается из-за нижнего борта карточного ящика. Место: Нижняя левая свободная треть, не закрывая пустые поля. Уход: Уходит вниз перед планом содержания.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P34.B02 · оценочно 10:39.0–10:43.7

> What survives gives us part of a text and its argument.

**Кадр:** CU, сверху на отдельную папку CONTENT.

**Камера:** Статика.

**Действие:** Из папки выдвигается краткая редакционная карточка PLEASURE / PERCEPTION. Она останавливается ниже регистрационной карточки, не замещая недостающую атрибуцию.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P34.B03 · оценочно 10:43.7–10:49.3

> A convincing story about who wrote it cannot substitute for the missing identification.

**Кадр:** MS под углом к разделителю, полям AUTHOR/TITLE и папке CONTENT; начало непрерывного плана B03–B04.

**Камера:** Удержать общий ракурс с видимой толщиной разделителя.

**Действие:** Между содержанием и пустыми полями стоит непрозрачная перегородка IDENTIFICATION NEEDED; никакое имя не предлагается.

**Акцент:** NO SUBSTITUTE · речевой маркер «cannot substitute» · расчётное начало 10:46.7. Маска: Наружная вертикальная стойка регистрационной рамки скрывает буквы; они выходят из-за неё. Место: Свободное поле справа от рамки, не поверх поля TITLE. Уход: После читаемой остановки скрыть буквы за той же стойкой в продолжающемся B04; поле остаётся пустым до перехода.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P34.B04 · оценочно 10:49.3–10:51.0

> That question remains open.

**Кадр:** MS, продолжение B03; пустое поле TITLE различимо внутри кадра.

**Камера:** Удержать тот же ракурс без короткого ECU до завершения акцента и перехода.

**Действие:** Боковая тень подчёркивает пустое поле; оно остаётся реально незаполненным.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Боковая дверца шкафа медленно закрывает кадр; прямой монтажный переход к широкому схематическому сечению P35. Никакой пустой карточке не присваивается новый объект.

**Музыкальный замысел:** M3 — убрать последний активный пульс, оставить тёплую незавершённую гармонию; дать последнему вопросу короткий спокойный хвост.

**Активы:** P34-A01: регистрационная карточка Paris4 с физическими пустыми полями AUTHOR / TITLE; P34-A02: отдельная папка CONTENT и редакционная карточка темы; P34-A03: жёсткая перегородка IDENTIFICATION NEEDED и отдельный закрытый макет Paris4; P34-A04: два бумажных акцента; REV13_P34_FRAME — Отдельная регистрационная рамка и её вертикальная стойка перекрывают NO SUBSTITUTE; поля AUTHOR и TITLE не заполняются..

**Граница достоверности:** Не появляется Philodemus или название On Pleasure даже в виде кандидата. Содержание и атрибуция показаны раздельно. Статус неизвестности соответствует актуальной проверке к концу октября 2026.

**Источники:** S18, S14.

### P35 · оценочно 10:51.4–11:10.4 · SET-F

**Реплика:** The next challenge was scale. Recovering patches does not mean every turn of a damaged roll can be followed. A collapsed layer, tear, or misleading junction can interrupt the path. The method had to work beyond the regions where it first succeeded.

**Цель и тип:** Зритель видит, почему успешные участки ещё не дают непрерывной реконструкции всего повреждённого рулона. (fact model).

**Передний план:** Передний план — крупный обрез бумажного технического макета; три независимые направляющие уходят от нижнего края внутрь сцены.

**Средний план:** Обобщённое сечение повреждённой рулонной геометрии: несколько прослеженных охристых участков среди нейтральных слоёв; ниже три увеличенных окна дефектов.

**Задний план:** Спокойная тёмно-кремовая панель с подписью SCHEMATIC GEOMETRY — NOT A SPECIFIC SCAN. Никакой объектной бирки Paris4 или 1667 здесь нет.

**Перекрытия и опоры:** Слои находятся на разных глубинах и действительно закрывают линии за собой. Дефекты уже присутствуют в модели; анимация не разрушает подлинник. Указатели движутся по отдельным направляющим и останавливаются у препятствий.

#### P35.B01 · оценочно 10:51.4–10:53.5

> The next challenge was scale.

**Кадр:** WS, фронтально с верхней точки на всё техническое сечение.

**Камера:** Плавный отъезд на 8%.

**Действие:** Ранее видимый небольшой охристый участок оказывается одним из нескольких участков в значительно более сложной общей структуре.

**Акцент:** SCALE · речевой маркер «scale» · расчётное начало 10:53.1. Маска: Акцент выдвигается из-за левого переднего обреза макета. Место: Верхняя левая пустая четверть, вне слоёв. Уход: Уходит за обрез при открытии окон дефектов.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P35.B02 · оценочно 10:53.5–10:59.5

> Recovering patches does not mean every turn of a damaged roll can be followed.

**Кадр:** MS, касательный угол к изгибам сечения.

**Камера:** Проезд вправо на 6%.

**Действие:** Охристая линия заканчивается на границе прослеженного участка; за ней продолжаются нейтральные слои. Линия не перескакивает на соседний виток.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P35.B03 · оценочно 10:59.5–11:04.2

> A collapsed layer, tear, or misleading junction can interrupt the path.

**Кадр:** CU, сверху на три увеличенных окна.

**Камера:** Статика.

**Действие:** В трёх окнах видны уже существующие складка, разрыв и сближенные поверхности. Три маленьких указателя по очереди останавливаются перед препятствием; никакая поверхность не сминается заново.

**Акцент:** BROKEN PATH · речевой маркер «interrupt the path» · расчётное начало 11:02.9. Маска: Буквы поднимаются из-за переднего борта центрального окна разрыва. Место: Ниже трёх окон, не закрывая места остановки. Уход: Опускаются за борт к финальному предложению.

**Звуковой замысел:** Один тихий сухой щелчок на остановке центрального указателя перед разрывом. (нового звука пока нет).

#### P35.B04 · оценочно 11:04.2–11:09.4

> The method had to work beyond the regions where it first succeeded.

**Кадр:** WS, тот же макет с противоположного трёхчетвертного угла.

**Камера:** Медленный наезд на 4%.

**Действие:** По внешней направляющей к непрослеженному участку подходит пустая контрольная рамка. Она обозначает следующую область работы, но не заполняет её линией заранее.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Пустая контрольная рамка проходит перед объективом и закрывается матовой створкой. После полной маски P36 возвращает SET-A с чёткой биркой 1667; геометрический макет ни во что не морфится.

**Музыкальный замысел:** M4 — в течение 3 секунд плавно перейти от тёплого разрешения M3 к более редкому сосредоточенному рисунку, сохраняя общий гармонический тон.

**Активы:** P35-A01: собственный обобщённый макет рулонной геометрии с несколькими прослеженными участками; P35-A02: три окна уже существующих дефектов и независимые указатели; P35-A03: контрольная рамка, направляющие и матовая створка; P35-A04: два бумажных акцента.

**Граница достоверности:** Объяснительная модель не объявлена реальным сечением конкретного свитка. Нет анимации нового разрушения оригинала и нет притворно точного пути через неизвестный участок.

**Источники:** S01, S09.

### P36 · оценочно 11:10.4–11:27.4 · SET-A

**Реплика:** Return to Papyrus sixteen sixty-seven. Could researchers trace the entire surviving surface inside this small core, then recover the writing across it? The task required continuity without concealment: follow what remained, while leaving the real losses and damage visible.

**Цель и тип:** Зритель возвращается к 1667 и удерживает задачу: восстановить весь сохранившийся путь, не скрыв его утраты. (fact model).

**Передний план:** Нижняя передняя кромка консервационного стола; справа ближе к камере — толстый край отдельного бокового светового окна.

**Средний план:** Короткий тёмный сердечник 1667 в неподвижной поддерживающей подставке; рядом закреплена рыжая инвентарная бирка PHerc.1667. Сбоку — отдельная светлая схематическая цифровая карточка.

**Задний план:** Размытые архивные полки и тёплый боковой свет SET-A; маленькая подпись STYLIZED MODEL, у цифрового окна — DIGITAL MODEL.

**Перекрытия и опоры:** Оригинал постоянно опирается на подставку и не разворачивается. Цифровая карточка появляется в отдельном боковом окне, между ней и сердечником остаётся воздух. Потери показаны прорезями только в модели; они не закрываются акцентами.

#### P36.B01 · оценочно 11:10.4–11:12.5

> Return to Papyrus sixteen sixty-seven.

**Кадр:** MS, три четверти спереди, узнаваемый SET-A.

**Камера:** Плавный наезд на 4%.

**Действие:** Створка предыдущей сцены полностью исчезает; первыми читаются рыжая бирка PHerc.1667 и короткая форма сердечника. Paris4 в кадре нет.

**Акцент:** SIXTEEN SIXTY-SEVEN · речевой маркер «sixteen sixty-seven» · расчётное начало 11:11.6. Маска: Акцент поднимается из-за передней кромки консервационного стола. Место: Нижняя левая свободная зона, вдали от подставки и бирки. Уход: Уходит за кромку перед вопросом о поверхности.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P36.B02 · оценочно 11:12.5–11:19.8

> Could researchers trace the entire surviving surface inside this small core, then recover the writing across it?

**Кадр:** WS, сверху под углом 35°, одновременно видны сердечник и отдельное цифровое окно.

**Камера:** Медленный отъезд на 7%.

**Действие:** Боковое окно открывает схематический частичный контур внутренних слоёв; движущийся указатель начинает путь, но останавливается у непрослеженной области. Полного результата ещё нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P36.B03 · оценочно 11:19.8–11:27.1

> The task required continuity without concealment: follow what remained, while leaving the real losses and damage visible.

**Кадр:** CU, косой верхний вид на цифровую карточку с пустотами; оригинал виден отдельно в глубине.

**Камера:** Плавный проезд вправо на 5%.

**Действие:** Рамка следует вдоль сохранившихся участков карточки и оставляет прорези насквозь открытыми. Края повреждения остаются неровными, поверхность не становится свежей и цельной.

**Акцент:** KEEP THE GAPS · речевой маркер «leaving the real losses and damage visible» · расчётное начало 11:24.1. Маска: Акцент появляется из-за внешней стойки бокового светового окна. Место: Верхняя правая свободная полоса вне цифровой поверхности. Уход: Уходит за стойку; прорези сохраняются видимыми до закрытия створки.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Матовая створка бокового цифрового окна проходит слева направо перед объективом и на миг оставляет узкую вертикальную светлую щель. Монтажный стык к широкому плану ESRF в P37; объект не превращается в аппарат и не переносится невидимой рукой.

**Музыкальный замысел:** M4 — сохранять сосредоточенную редкую пульсацию, слегка открывая верхний регистр на вопросе; закончить фразу без разрешающего удара, чтобы P37 продолжил поиск.

**Активы:** P36-A01: существующий короткий стилизованный сердечник 1667 и поддерживающая подставка SET-A; P36-A02: рыжая бирка PHerc.1667 и постоянный фактический идентификатор; P36-A03: отдельное цифровое боковое окно с собственным контуром и настоящими прорезями; P36-A04: матовая переходная створка и два бумажных акцента.

**Граница достоверности:** Идентичность явно возвращена к 1667. Вопрос о полном пути ещё не показан как готовый успех. Копия отдельна от физического предмета; никакие утраченные части оригинального большого свитка не восстанавливаются.

**Источники:** S01, S02.

### P37 · оценочно 11:27.4–11:48.3 · SET-E

**Реплика:** For the work released in twenty twenty-six, researchers used high-resolution scans from the European Synchrotron Radiation Facility in Grenoble. The improved measurements and reconstruction gave them a more detailed volume to work with. Paul Tafforeau and Alessandro Mirone helped develop and carry out the imaging at the facility.

**Цель и тип:** Зритель связывает более подробные измерения для результата, объявленного в 2026 году, с работой конкретной установки и людей, сохраняя различие между предметом и данными. (fact model).

**Передний план:** Слева внизу — неподвижная опора источника; справа внизу — край рамки детектора. На нижней планке постоянная подпись SCHEMATIC — ESRF, GRENOBLE.

**Средний план:** В центре — закрытая угольная модель PHerc. 1667 в охватывающей колыбели на поворотном столике; отдельная табличка PHerc. 1667 закреплена на основании. Справа от установки — кремовый куб данных на собственном постаменте.

**Задний план:** Нейтральная бумажная стена современной лаборатории с мягкой вертикальной полосой света; над кубом две отдельные именные планки Paul Tafforeau и Alessandro Mirone, первоначально скрытые за верхней перемычкой.

**Перекрытия и опоры:** Передняя опора закрывает нижнюю часть столика, рамка детектора — край куба данных. Колыбель, предмет и диск вращаются одним узлом; лабораторный стол и стопы опор неподвижны. Условный луч ограничен плоскостью между источником и детектором.

#### P37.B01 · оценочно 11:27.4–11:30.4

> For the work released in twenty twenty-six,

**Кадр:** WS, три четверти сверху, вся установка и отдельный куб данных.

**Камера:** Непрерывный въезд на 5 см по оси установки, начало общего движения первого и второго beats.

**Действие:** После полного перекрытия предыдущей сцены опора открывает современную установку. На основании уже читается SCHEMATIC; карточка RESULT RELEASED 2026 поворачивается на своей нижней оси. Предмет остаётся неподвижным внутри колыбели относительно держателя.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P37.B02 · оценочно 11:30.4–11:35.6

> researchers used high-resolution scans from the European Synchrotron Radiation Facility in Grenoble.

**Кадр:** WS, тот же ракурс и та же непрерывная сцена.

**Камера:** Продолжить въезд ещё на 6 см без смены оптики.

**Действие:** На слове scans столик начинает один медленный поворот держателя; полупрозрачная узкая плоскость между источником и детектором обозначает условный рентгеновский пучок. За детектором последовательно становятся видны три карточки разных проекций.

**Акцент:** GRENOBLE · речевой маркер «Grenoble» · расчётное начало 11:35.1. Маска: Буквы на оранжевой подложке поднимаются из-за непрозрачного правого края детектора. Место: Свободное поле справа вверху, выше куба данных. Уход: Планка скользит обратно за детектор при переходе к отдельному плану объёма.

**Звуковой замысел:** На начале видимого вращения — один тихий ровный звук мотора; затихает вместе с остановкой диска в конце beat. (нового звука пока нет).

#### P37.B03 · оценочно 11:35.6–11:41.6

> The improved measurements and reconstruction gave them a more detailed volume to work with.

**Кадр:** CU, отдельный куб данных под углом 45 градусов; установка видна далеко слева.

**Камера:** Статично после прямого монтажного перехода с общего плана на отдельный объект.

**Действие:** Три карточки проекций проходят за боковую стенку куба. Внутри куба открывается более мелкая сетка на сменной прозрачной вставке. Это собственная модель объёма без букв, шкал реального разрешения и воспроизведения научного скана.

**Акцент:** MORE DETAIL · речевой маркер «a more detailed volume» · расчётное начало 11:38.6. Маска: Нижний непрозрачный бортик постамента находится перед буквами по глубине; буквы поднимаются из-за бортика в свободное поле справа от куба. Место: Нижнее правое поле, вне сетки. Уход: Уходит за нижний бортик постамента на последнем слове предложения.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P37.B04 · оценочно 11:41.6–11:48.0

> Paul Tafforeau and Alessandro Mirone helped develop and carry out the imaging at the facility.

**Кадр:** MS, фронтально к двум именным планкам, установка ниже них.

**Камера:** Плавный подъём камеры на 7 см без изменения фокусного расстояния.

**Действие:** Именные планки Paul Tafforeau и Alessandro Mirone опускаются из-за верхней перемычки и останавливаются в отдельных пазах. Под ними видны небольшие собственные пиктограммы измерений и реконструкции; они не распределяют исключительное авторство операций между двумя людьми.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Камера продолжает подъём к боковой стенке куба. Стенка полностью закрывает кадр; под перекрытием — переход к крупной сетке SET-F. Движение следующей сцены продолжает тот же подъём.

**Музыкальный замысел:** M4 продолжается без перезапуска; на появлении более мелкой сетки немного раскрыть средний регистр, не усиливая ритм. Мотор остаётся тише VO.

**Активы:** CORE-1667 — постоянная стилизованная закрытая модель примерно 8 × 2 см; CRADLE-1667 — колыбель и отдельная инвентарная бирка; E37-BEAMLINE — собственные источник, детектор и вращающийся держатель; E37-DATA-CUBE — модель объёма со сменной сеткой; E37-CREDITS — две именные бумажные планки.

**Граница достоверности:** SCHEMATIC, не документальные кадры ESRF. Вращается поддерживаемый предмет, а не больничное кольцо вокруг неподвижной койки. Луч условно видим только для объяснения. Нельзя обозначать собственный куб как подлинный CT или приписывать учёным показанный момент работы.

**Источники:** S01, S19.

### P38 · оценочно 11:48.3–12:06.3 · SET-F

**Реплика:** Better data still needed patient work. The paper describes thirty-one windings and roughly twenty-five hours of manual annotation per winding, alongside computational tools. People checked the paths through the papyrus. Much of the achievement happened before a reader saw a sentence.

**Цель и тип:** Зритель понимает, что непрерывная геометрия получена длительной человеческой проверкой наряду с вычислениями. (fact model).

**Передний план:** Нижний край рабочего окна и небольшой неподвижный зажим слева; за ним спрятана первая акцентная планка.

**Средний план:** На наклонной доске — неровные контуры поверхности без букв; справа в отдельном веере ровно 31 узкая нумерованная вкладка. Над ними закреплено поле для фактической подписи приблизительного времени.

**Задний план:** Куб данных из P37 остаётся далеко слева, физический оригинал в собственной маленькой нише справа; над доской постоянная подпись DIGITAL MODEL — SURFACE ANNOTATION.

**Перекрытия и опоры:** Рамка закрывает края условной сетки, но не скрывает место ошибки. Вкладки имеют самостоятельные шарниры и не толкают доску. Ведущий указатель закреплён на короткой направляющей, а не висит в воздухе.

#### P38.B01 · оценочно 11:48.3–11:50.9

> Better data still needed patient work.

**Кадр:** MS, три четверти к наклонной доске.

**Камера:** Продолжить подъём из перехода на 3 см и мягко остановиться.

**Действие:** Рабочее окно открывается; указатель замирает перед сложным местом между двумя соседними контурами. Доска не выпрямляет повреждение автоматически.

**Акцент:** PATIENT WORK · речевой маркер «patient work» · расчётное начало 11:50.1. Маска: Планка выходит из-за нижнего неподвижного зажима и ложится параллельно краю доски. Место: Нижнее левое свободное поле. Уход: Зажим остаётся маской, за которую планка возвращается при открытии веера.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P38.B02 · оценочно 11:50.9–11:58.2

> The paper describes thirty-one windings and roughly twenty-five hours of manual annotation per winding, alongside computational tools.

**Кадр:** MS, тот же непрерывный план.

**Камера:** Медленный боковой проезд вправо на 8 см.

**Действие:** На thirty-one windings раскрывается веер из 31 вкладки. На roughly twenty-five hours поворачивается узкая фактическая табличка ≈25 h MANUAL ANNOTATION PER WINDING. Ни часов обратного отсчёта, ни арифметического итога на экране нет. Рядом остаётся маленькая схема вычислительной сетки.

**Акцент:** THIRTY-ONE WINDINGS · речевой маркер «thirty-one windings» · расчётное начало 11:52.2. Маска: Акцент поднимается из-за непрозрачной крайней вкладки веера; её край действительно перекрывает буквы. Место: Верхнее правое поле, выше фактической таблички времени. Уход: Планка складывается за крайнюю вкладку перед переходом к крупному месту проверки.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P38.B03 · оценочно 11:58.2–12:01.2

> People checked the paths through the papyrus.

**Кадр:** ECU, почти сверху на место сближения двух условных слоёв.

**Камера:** Статично; смена масштаба более чем вдвое и нового угла исключает повтор предыдущего кадра.

**Действие:** Указатель слегка смещает один контрольный штифт к тому же контуру. Соседний слой не двигается. Непрерывная цветная линия после коррекции остаётся на одной поверхности.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** Один тихий контакт штифта с пазом точно в момент его фиксации. (нового звука пока нет).

#### P38.B04 · оценочно 12:01.2–12:05.9

> Much of the achievement happened before a reader saw a sentence.

**Кадр:** ECU, тот же участок.

**Камера:** Медленное отдаление на 4 см, оставаясь над доской.

**Действие:** От исправленного участка становится виден следующий отрезок поверхности. Поле будущего чтения за доской остаётся пустым; в него ещё не поступает ни одного слова.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Ближайшая перемычка рабочего окна закрывает верхнюю половину, затем весь кадр. Под ней — переход к меньшему квадратному окну детектора P39; сохраняется направление движения вниз по условной поверхности.

**Музыкальный замысел:** M4 без нового начала; сократить число пульсов и оставить ровную сдержанную гармонию под количественными данными.

**Активы:** F38-TRACE — собственная доска неровных контуров без письма; F38-TABS31 — веер ровно из 31 вкладки; F38-TIME — фактическая табличка приблизительного времени на виток; F38-PIN — механический указатель и контрольный штифт; CORE-1667 — оригинал сохраняет отдельную нишу.

**Граница достоверности:** Все контуры — DIGITAL MODEL, не точная геометрия опубликованного датасета. Примерно 25 часов относятся к ручной аннотации одного витка, не ко всему проекту и не ко времени сканирования. Не изображать весь процесс исключительно ручным.

**Источники:** S01.

### P39 · оценочно 12:06.3–12:24.6 · SET-F

**Реплика:** The ink detectors searched for local physical signals, without completing Greek sentences. That distinction matters, but it does not make every output correct. Weak signals, damaged surfaces, and mistakes in the geometry can still mislead. Every recovered image needs to be examined.

**Цель и тип:** Зритель отличает поиск физического сигнала от языкового достраивания и понимает необходимость проверки результата. (explanatory metaphor).

**Передний план:** Четырёхугольное бумажное окно на направляющей, непрозрачная ручка слева и маленькая шторка справа.

**Средний план:** Три небольших участка условной фактуры: неоднородная поверхность, реальный вырез в бумаге и неверно проведённая соседняя линия. Над ними отдельная прозрачная плёнка условного предсказания без букв.

**Задний план:** Кремовая панель DIGITAL MODEL — SIGNAL, NOT TRANSCRIPTION; за ней в расфокусе геометрическая доска P38.

**Перекрытия и опоры:** Окно действительно закрывает окружающую фактуру и открывает только малую область. Прозрачная карта лежит над поверхностью с небольшим зазором; отверстие в основе видно через оба слоя. Маски не заменяют тёмные области выдуманными буквами.

#### P39.B01 · оценочно 12:06.3–12:11.4

> The ink detectors searched for local physical signals, without completing Greek sentences.

**Кадр:** CU, 45 градусов к малому окну и поверхности.

**Камера:** Небольшой проезд вдоль поверхности на 5 см.

**Действие:** Окно проходит над отдельными неодинаковыми пятнами. На верхней прозрачной карте появляются соответствующие условные точки; никакой целой буквы, греческой строки или словаря в кадре нет.

**Акцент:** LOCAL SIGNALS · речевой маркер «local physical signals» · расчётное начало 12:08.4. Маска: Планка вытягивается вправо из-за непрозрачной ручки окна. Место: Слева внизу за пределами исследуемого участка. Уход: Возвращается под ручку, когда окно останавливается.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P39.B02 · оценочно 12:11.4–12:16.1

> That distinction matters, but it does not make every output correct.

**Кадр:** CU, тот же непрерывный план.

**Камера:** Статично после остановки проезда.

**Действие:** Одно пятно на прозрачной карте остаётся выделенным тонким незамкнутым кольцом проверки. Кольцо не превращается в галочку. Рядом открывается пустая ячейка VERIFIED только как подпись категории, без отметки.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P39.B03 · оценочно 12:16.1–12:21.3

> Weak signals, damaged surfaces, and mistakes in the geometry can still mislead.

**Кадр:** ECU, сверху на три условных участка, каждый в своём маленьком окне.

**Камера:** Статично после смены угла на верхний.

**Действие:** На weak signals ослабляется только прозрачная метка; на damaged surfaces виден вырез основы; на mistakes in the geometry цветная линия подходит к соседнему контуру и останавливается. Три причины различимы, но ничего не объявлено реальной ошибкой конкретного скана.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P39.B04 · оценочно 12:21.3–12:24.3

> Every recovered image needs to be examined.

**Кадр:** MS, сбоку от всей доски с тремя участками.

**Камера:** Плавное отдаление на 6 см.

**Действие:** Над доской опускается большая рамка проверки, не скрывающая поверхность. Малое окно остаётся внутри неё; незамкнутое кольцо всё ещё требует решения.

**Акцент:** NEEDS EXAMINATION · речевой маркер «needs to be examined» · расчётное начало 12:22.5. Маска: Буквы выходят из-за нижней перекладины большой рамки. Место: Нижний центр, в пустом поле перед доской. Уход: На переходе большая рамка опускается перед планкой и закрывает её.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Опускающаяся рамка закрывает весь видимый участок. После полного перекрытия открывается другой масштаб: край стола SET-J и восемь отдельных лотков проверки, без превращения схемы в настоящий научный снимок.

**Музыкальный замысел:** M4 продолжается; убрать короткие высокие ноты на перечислении ошибок, оставить спокойный удержанный тон без тревожного акцента.

**Активы:** F39-WINDOW — малое исследующее окно и направляющая; F39-PATCHES — три собственных условных образца поверхности; F39-PREDICTION — прозрачная карта точек без текста; F39-REVIEW — большая рамка и незамкнутое кольцо проверки.

**Граница достоверности:** SCHEMATIC, не восстановленный текст. Современный detector использует локальные физические признаки; отсутствие языковой модели не гарантирует отсутствие ложного сигнала. Изображённые повреждения и ошибка пути — объясняющие примеры, не обнаружения на PHerc. 1667.

**Источники:** S01, S08.

### P40 · оценочно 12:24.6–12:42.5 · SET-J

**Реплика:** Federica Nicolardi led the papyrological work. Eight specialists examined the text, checking letterforms across renderings and their position on the papyrus. Readings were accepted through independent agreement or discussion. The computer supplied images; people remained responsible for reading and interpreting them.

**Цель и тип:** Зритель видит, что ответственность за чтение принадлежит специалистам, а не изображению, которое выдала модель. (explanatory metaphor).

**Передний план:** Ближняя кромка стола и пустой лоток для акцентной планки; стол занимает нижнюю пятую часть кадра.

**Средний план:** Слева — нейтральная бумажная фигура за столом с именной карточкой Federica Nicolardi. Справа — восемь раздельных прозрачных лотков, не образующих круглый стол заседания; в них условные фрагменты разметки без греческих букв.

**Задний план:** На вертикальной панели подпись ILLUSTRATION — SEPARATE EXPERT READINGS. Два образца рендера обозначены A и B как условные виды, без внешнего вида настоящего научного интерфейса.

**Перекрытия и опоры:** Фигура и руки опираются на стол; передняя кромка закрывает нижние части лотков. Лотки имеют собственные стойки и могут независимо наклоняться. Карта сопоставления располагается перед лотками, не закрывая именную карточку.

#### P40.B01 · оценочно 12:24.6–12:27.2

> Federica Nicolardi led the papyrological work.

**Кадр:** MS, три четверти слева к столу и имени.

**Камера:** Небольшой въезд на 4 см.

**Действие:** После открытия края стола именная карточка становится полностью видимой. Фигура остаётся символом роли руководителя; рядом стоит рамка условного рендера, а не оригинальный папирус в руках.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P40.B02 · оценочно 12:27.2–12:33.6

> Eight specialists examined the text, checking letterforms across renderings and their position on the papyrus.

**Кадр:** WS, весь стол и восемь лотков под углом сверху.

**Камера:** Плавный подъём на 7 см.

**Действие:** Восемь лотков раскрываются на разных стойках. Между условными видами A и B движется один указатель координаты, сопоставляя одно и то же место. Внутри видны абстрактные короткие дуги с постоянной подписью SCHEMATIC — NO TRANSCRIPTION.

**Акцент:** EIGHT SPECIALISTS · речевой маркер «Eight specialists» · расчётное начало 12:27.2. Маска: Буквы поднимаются из-за дальней стенки восьмого лотка. Место: Верхнее правое свободное поле. Уход: Планка опускается за ту же стенку при переходе к результатам сопоставления.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P40.B03 · оценочно 12:33.6–12:37.0

> Readings were accepted through independent agreement or discussion.

**Кадр:** CU, справа к двум соседним лоткам и связующей рамке.

**Камера:** Статично после смены стороны и масштаба.

**Действие:** Два условных указателя сходятся к одному положению, а третий остаётся в отдельной рамке DISCUSSION. Прозрачная связующая рамка встаёт в паз. Нет подсчёта голосов, выдуманного единогласия или записанной беседы.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** Один негромкий контакт связующей рамки с пазом при её остановке. (нового звука пока нет).

#### P40.B04 · оценочно 12:37.0–12:42.2

> The computer supplied images; people remained responsible for reading and interpreting them.

**Кадр:** MS, тот же правый ракурс шире, компьютерная рамка слева, человеческая рабочая зона справа.

**Камера:** Отъезд на 6 см.

**Действие:** Карточка IMAGE остаётся под условным монитором; отдельная карточка READING ложится в рабочий лоток фигуры. Между ними сохраняется промежуток, обозначающий человеческое решение.

**Акцент:** PEOPLE READ · речевой маркер «people remained responsible» · расчётное начало 12:38.8. Маска: Акцент выходит из-за передней кромки рабочего лотка фигуры. Место: Нижнее правое поле, не над руками и не над сравнением. Уход: Кромка нового предметного постамента перекрывает планку на переходе.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Камера уходит вправо за высокую боковую стенку стола. Полное перекрытие скрывает смену декорации; открывается охристый постамент Paris 4 в SET-L с другим ракурсом и ясной табличкой.

**Музыкальный замысел:** M4 продолжается; мягко вывести одну тёплую струнную ноту на человеческой ответственности, без музыкального утверждения окончательной истинности каждого чтения.

**Активы:** J40-NICOLARDI — именная карточка и нейтральная иллюстрация роли; J40-TRAYS8 — восемь самостоятельных лотков; J40-RENDS — условные виды A и B без букв; J40-REVIEW — рамки сопоставления и DISCUSSION.

**Граница достоверности:** Не документальная групповая встреча и не портрет, заявленный как точное сходство. Восемь специалистов показаны отдельными чтениями. Для этого эпизода не используются чужие сканы; собственные дуги не объявляются восстановленными греческими буквами.

**Источники:** S01, S02.

### P41 · оценочно 12:42.5–13:03.9 · SET-L

**Реплика:** A separate check came from Paris Four. In improved scans of that roll, ink deposits could be seen directly in the three-dimensional data. Projecting them onto the digital surface produced marks that matched the earlier reading. Another kind of physical evidence now supported what the previous images had shown.

**Цель и тип:** Зритель понимает, какое отдельное физическое свидетельство получили на Paris 4, и не переносит его на другой свиток. (fact model).

**Передний план:** Охристая боковая заслонка постамента Paris 4 и нижний край отдельной рамки сравнения.

**Средний план:** Слева — условная закрытая модель Paris 4 в своей колыбели с постоянным ярлыком PHerc. Paris 4. Над постаментом — собственный прозрачный куб с тремя неодинаковыми условными пятнами и отдельная плоская координатная сетка. Справа далеко — закрытая ниша PHerc. 1667 другого цвета.

**Задний план:** Панель SCHEMATIC — PARIS 4 VALIDATION PRINCIPLE; между двумя постаментами глухая вертикальная перегородка. Ниша 1667 остаётся темнее и не участвует в операции.

**Перекрытия и опоры:** Заслонка закрывает только постамент Paris 4. Пятна находятся на разных внутренних прозрачных плоскостях куба; передний каркас действительно маскирует их при движении камеры. Сетка и куб имеют отдельные опоры. Никакая линия не соединяет это сравнение с 1667.

#### P41.B01 · оценочно 12:42.5–12:45.5

> A separate check came from Paris Four.

**Кадр:** MS, три четверти справа к отдельному постаменту Paris 4; план продолжается в начало B02.

**Камера:** Удержать постамент до завершения чтения PARIS FOUR; отдельный CU куба начинается только после ухода акцента.

**Действие:** Открываются табличка PHerc. Paris 4 и собственная закрытая модель; ниша 1667 отделена перегородкой.

**Акцент:** PARIS FOUR · речевой маркер «Paris Four» · расчётное начало 12:44.7. Маска: Акцент появляется из-за охристой заслонки, одновременно с открытием постамента. Место: Верхнее левое поле внутри зоны Paris 4. Уход: После полной читаемой остановки вернуть буквы за ту же охристую заслонку; после этого перейти на куб.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P41.B02 · оценочно 12:45.5–12:48.1

> In improved scans of that roll,

**Кадр:** CU собственного прозрачного куба сверху сбоку; начало изображения может следовать за началом этой фразы.

**Камера:** Начать отдельный CU после исчезновения PARIS FOUR; сохранить подпись Paris 4 на основании.

**Действие:** Куб открывается с отдельными внутренними плоскостями; подписи PHerc. Paris 4 и SCHEMATIC остаются читаемыми.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P41.B03 · оценочно 12:48.1–12:52.4

> ink deposits could be seen directly in the three-dimensional data.

**Кадр:** CU, тот же непрерывный план.

**Камера:** Продолжить боковой проезд ещё на 4 см.

**Действие:** Внутренние условные пятна разделяются параллаксом. Один тонкий указатель подводится к пятну, не превращая его в букву. Основной монтаж использует только эту собственную модель; подлинная разрешённая иллюстрация при замене получает отдельный неподвижный evidence insert с полным объектным ярлыком.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P41.B04 · оценочно 12:52.4–12:58.0

> Projecting them onto the digital surface produced marks that matched the earlier reading.

**Кадр:** MS, сверху под углом к кубу и отдельной плоской сетке.

**Камера:** Статично после заметного расширения плана.

**Действие:** Три вертикальные бумажные направляющие соединяют условные пятна куба с тремя положениями на плоской сетке. Рядом раскрывается собственная схема прежнего изображения с теми же условными положениями. Над обеими схемами остаётся SCHEMATIC; это иллюстрация соответствия, а не изготовленное доказательство.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P41.B05 · оценочно 12:58.0–13:03.5

> Another kind of physical evidence now supported what the previous images had shown.

**Кадр:** MS, боковой ракурс Paris 4, на дальнем правом краю видно отдельную закрытую нишу 1667.

**Камера:** Медленно отъехать на 5 см.

**Действие:** Куб, сетка и схема прежнего изображения остаются различимыми на одном охристом постаменте. Окружающая рамка объединяет только эту тройку; не пересекает перегородку.

**Акцент:** PHYSICAL EVIDENCE · речевой маркер «physical evidence» · расчётное начало 12:59.2. Маска: Акцент выдвигается из-за нижней перекладины рамки сравнения. Место: Нижнее левое поле зоны Paris 4, вдали от условных пятен. Уход: Уходит за перекладину во время дальнейшего отъезда к двум постаментам.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Один непрерывный отъезд открывает два раздельных постамента с паспортами Paris 4 и PHerc. 1667 в общей системе координат. Обе модели и их подписи сохраняются в P42; морфинг запрещён.

**Музыкальный замысел:** M4 сохраняет сдержанный пульс; добавить только один более открытый гармонический интервал, не делать фанфары или победного удара.

**Активы:** L41-PARIS4 — отдельная обобщённая модель без заявленного масштаба и охристый постамент; L41-CUBE — прозрачный собственный куб условного сигнала; L41-PROJECTION — собственные сетка и схема соответствий без букв; L41-DIVIDER — глухая перегородка между объектами; L41-OPTIONAL-EVIDENCE — необязательный проверенный asset именно Paris 4 после разрешения; fallback полностью задан собственными L41-CUBE и L41-PROJECTION.

**Граница достоверности:** Основной кадр — SCHEMATIC, не точная копия данных и не вымышленные греческие буквы. Опциональный научный снимок требует установленного права, точного объекта и подписи метода; без него сцена полностью исполнима. Проверка Paris 4 не является независимой верификацией каждой буквы 1667.

**Источники:** S01, S20.

### P42 · оценочно 13:03.9–13:21.4 · SET-L

**Реплика:** That check belongs to Paris Four. It supports the approach, but does not independently certify every letter of sixteen sixty-seven. Each object needs its own geometry, images, and scholarly reading. Keeping those chains of evidence separate makes the result stronger.

**Цель и тип:** Зритель сохраняет две отдельные цепочки доказательств, даже когда оба объекта используют родственный метод. (fact model).

**Передний план:** Ближние края двух постаментов, разделённые пустым промежутком; у каждого своя нижняя заслонка.

**Средний план:** Слева — охристый Paris 4 с уже выполненной схемой сравнения, справа — ржаво-оранжевый PHerc. 1667 с собственной закрытой моделью. Перед каждым лежит по три отдельные карточки GEOMETRY, IMAGES, READING.

**Задний план:** Вертикальная перегородка и две независимые бумажные направляющие; сверху общая нейтральная надпись METHOD, не соединённая с отметкой правильности конкретного текста.

**Перекрытия и опоры:** Перегородка физически перекрывает край каждого постамента при боковом взгляде. Все связи заканчиваются внутри своего основания. Пустой промежуток не заполняется стрелкой подтверждения.

#### P42.B01 · оценочно 13:03.9–13:06.5

> That check belongs to Paris Four.

**Кадр:** WS, два постамента под углом 35 градусов сверху.

**Камера:** Завершить непрерывный подъём из P41 на 4 см и остановиться.

**Действие:** Свет остаётся на охристой цепочке Paris 4; её рамка замыкается только вокруг собственного основания.

**Акцент:** THIS ROLL · речевой маркер «Paris Four» · расчётное начало 13:05.6. Маска: Акцент выходит из-за передней охристой заслонки. Место: Нижнее левое поле под Paris 4. Уход: Возвращается за охристую заслонку до смещения внимания к 1667.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P42.B02 · оценочно 13:06.5–13:12.5

> It supports the approach, but does not independently certify every letter of sixteen sixty-seven.

**Кадр:** WS, тот же план.

**Камера:** Статично.

**Действие:** Небольшая схема общей операции остаётся над обоими постаментами, но независимая рамка Paris 4 не движется вправо. У 1667 нет заимствованной галочки или печати; его карточки остаются отдельными.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P42.B03 · оценочно 13:12.5–13:16.7

> Each object needs its own geometry, images, and scholarly reading.

**Кадр:** MS, фронтально к двум тройкам карточек, сами закрытые предметы позади.

**Камера:** Ровный боковой проезд вправо на 7 см.

**Действие:** На geometry поднимается первая карточка каждого набора, на images — вторая, на scholarly reading — третья. Карточки одного набора соединены своим коротким шнуром, не пересекающим зазор.

**Акцент:** EACH OBJECT · речевой маркер «Each object» · расчётное начало 13:12.5. Маска: Буквы выходят из-за передней ржаво-оранжевой заслонки 1667. Место: Нижний центр под правым набором, вне обоих шнуров. Уход: Планка уходит вниз за заслонку перед финальным общим взглядом.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P42.B04 · оценочно 13:16.7–13:21.0

> Keeping those chains of evidence separate makes the result stronger.

**Кадр:** WS, сверху, обе цепочки целиком.

**Камера:** Статично после смены угла и масштаба.

**Действие:** Две тройки карточек остаются на месте; тонкий световой акцент подчёркивает пустой промежуток и оба самостоятельных ярлыка. Никакие поверхности или письмена не перетекают между объектами.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Передняя ржаво-оранжевая заслонка 1667 поднимается до полного перекрытия кадра. Под её цветом — переход к датированной объявляющей карточке P43; ярлык 1667 вновь открывается на том же правом постаменте.

**Музыкальный замысел:** M4 идёт непрерывно; сохранить одинаковую громкость на двух объектах, без победной каденции после слова stronger.

**Активы:** L42-TWO-CHAINS — два независимых набора GEOMETRY, IMAGES, READING; L41-PARIS4 — отдельный охристый постамент; CORE-1667 — неизменный закрытый предмет правой ниши; L42-GAP — физический промежуток и перегородка.

**Граница достоверности:** Оба набора — поясняющая схема, не фактические протоколы проверки. Поддержка общего подхода не превращается в сертификацию каждого знака другого свитка.

**Источники:** S01, S20.

### P43 · оценочно 13:21.4–13:43.4 · SET-L

**Реплика:** On June twenty-fifth, twenty twenty-six, the team announced the complete virtual unwrapping of the surviving core of sixteen sixty-seven. The technical manuscript followed on arXiv two days later. The researchers reported a reconstructed writing surface extending across twenty-two columns or column-equivalents, with the surviving text available for close study.

**Цель и тип:** Зритель получает точную дату объявления и масштаб реконструкции сохранившегося материала без обещания целой первоначальной книги. (fact model).

**Передний план:** Ржаво-оранжевая заслонка, кромка датированной карточки и нижняя рейка развёртки.

**Средний план:** На постаменте 1667 — закрытая модель; справа от неё собственная кремовая развёртка с 22 условными колонками или их эквивалентами, разорванным верхним контуром и без букв. Слева две отдельные календарные карточки для объявления и препринта.

**Задний план:** Панель DIGITAL MODEL — SURVIVING MATERIAL; над развёрткой постоянная подпись SCHEMATIC COLUMN EXTENT, NOT TRANSCRIPTION. Пустое пространство над неровным краем остаётся видимым.

**Перекрытия и опоры:** Заслонка сначала закрывает весь предметный постамент, затем опускается. Колонки закреплены на одной цифровой подложке и не выходят из физического рулона. Карточки дат стоят на самостоятельных ступенчатых пазах.

#### P43.B01 · оценочно 13:21.4–13:23.5

> On June twenty-fifth, twenty twenty-six,

**Кадр:** MS, фронтально к датам и краю постамента.

**Камера:** Медленный въезд на 3 см.

**Действие:** Заслонка опускается, открывая фактическую бумажную карточку 25 JUN 2026 — ANNOUNCEMENT. Это собственная типографика, не копия пресс-релиза.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P43.B02 · оценочно 13:23.5–13:29.5

> the team announced the complete virtual unwrapping of the surviving core of sixteen sixty-seven.

**Кадр:** MS, тот же непрерывный план.

**Камера:** Продолжить въезд ещё на 4 см.

**Действие:** Рядом с неизменным закрытым ядром раскрывается отдельная цифровая подложка. Её неровный верхний край остаётся неровным; она не вырастает в первоначально целый рулон.

**Акцент:** SURVIVING CORE · речевой маркер «surviving core» · расчётное начало 13:27.4. Маска: Акцент поднимается из-за передней рейки постамента 1667. Место: Нижнее левое поле рядом с инвентарной табличкой, не перед предметом. Уход: Уходит обратно за рейку при появлении второй даты.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P43.B03 · оценочно 13:29.5–13:33.4

> The technical manuscript followed on arXiv two days later.

**Кадр:** CU, сверху сбоку к двум датированным карточкам.

**Камера:** Статично после отдельного монтажного перехода к календарным фактам.

**Действие:** В соседний паз входит карточка 27 JUN 2026 — arXiv PREPRINT. Два последовательных интервала на линейке дат поясняют переход 25 → 26 → 27 июня; нет значка журнального принятия или копии обложки статьи.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P43.B04 · оценочно 13:33.4–13:39.0

> The researchers reported a reconstructed writing surface extending across twenty-two columns or column-equivalents,

**Кадр:** WS, сверху под углом к собственной развёртке и отдельному ядру.

**Камера:** Плавный проезд вдоль развёртки на 9 см.

**Действие:** Лёгкая верхняя планка поднимается и открывает 22 узких условных зоны, обозначенных только малыми номерами. Это схема охвата сохранившейся поверхности; размеры зон и разрывы не претендуют на воспроизведение конкретного датасета.

**Акцент:** TWENTY-TWO COLUMNS · речевой маркер «twenty-two columns» · расчётное начало 13:37.2. Маска: Акцент появляется из-за поднятой верхней планки, затем останавливается над ней. Место: Верхний правый пустой сектор, не внутри колонок. Уход: Планка акцента прячется за верхнюю рейку до перехода к локальному рассмотрению.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P43.B05 · оценочно 13:39.0–13:42.4

> with the surviving text available for close study.

**Кадр:** CU, под углом к одной условной зоне и краю рамки рассмотрения.

**Камера:** Статично.

**Действие:** Маленькая рамка рассмотрения аккуратно опускается в паз перед одной зоной. Внутри остаётся схематический контур без сгенерированного текста; на фоне виден отдельный закрытый предмет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** Один тихий контакт рамки рассмотрения с её пазом. (нового звука пока нет).

**Переход:** На паузе камера поднимается к неровному верхнему краю развёртки. Прямой переход на заметно более широкий верхний план SET-F сохраняет край по направлению, но открывает большое пустое поле над ним.

**Музыкальный замысел:** В начале P43 перевести M4 в M5 кроссфейдом примерно за 3 секунды. На объявлении раскрыть гармоники; уже к close study уменьшить плотность, готовя объяснение границ результата.

**Активы:** L43-DATES — собственные карточки 25 JUN и 27 JUN 2026; L43-COLUMNS22 — развёртка из 22 условных зон без букв; L43-STUDY-FRAME — рамка рассмотрения с пазом; CORE-1667 — постоянное закрытое ядро; L43-LABELS — SURVIVING MATERIAL и маркировка схемы.

**Граница достоверности:** Это графическое изложение опубликованного результата, не подлинный скан. Колонки представлены условно и не подразумевают одинаковую сохранность. Complete относится к сохранившемуся ядру. Дата arXiv не обозначает прохождение журнального рецензирования.

**Источники:** S01, S20, S21.

### P44 · оценочно 13:43.4–13:59.6 · SET-F

**Реплика:** Complete needs a boundary. This core preserves lower portions of the final columns of a larger roll. Missing material has not returned. A continuous reconstruction of what survives cannot become a complete copy of the original book.

**Цель и тип:** Зритель понимает границу слова complete: восстановлена непрерывная сохранившаяся поверхность, а утраты остаются утратами. (fact model).

**Передний план:** Нижняя рейка цифровой развёртки и отдельная тонкая рамка, закрывающая только внешнюю кромку схемы.

**Средний план:** Сохранившиеся нижние участки условных колонок лежат в нижней трети большой пустой плоскости; выше и слева видны лишь прерывистые элементы приблизительной рамки прежнего более крупного рулона. Физическое ядро и цифровая схема размещены раздельно и одновременно.

**Задний план:** Нейтральное кремовое пустое поле без второй модели. Подписи DIGITAL MODEL и APPROXIMATE EXTENT — NOT A RESTORATION постоянны.

**Перекрытия и опоры:** Тонкая рамка перекрывает только периферию и не закрывает пустоту утраченного материала. Сохранившийся участок закреплён на собственной опоре; отодвигаемая приблизительная рамка не тянет его за собой. Дополнение v1.3: Физическое ядро на отдельном ложементе и цифровая схема на отдельной опоре видны одновременно; внешняя рейка является маской A BOUNDARY.

#### P44.B01 · оценочно 13:43.4–13:45.1

> Complete needs a boundary.

**Кадр:** WS высокого угла: физическое ядро и цифровая схема отдельно, большой пустой участок сверху; начало непрерывного плана B01–B02.

**Камера:** Удержать ракурс без склейки, затем мягко приблизиться к нижним участкам.

**Действие:** На внешней рейке появляется тонкая условная граница у последнего сохранившегося края; утраты остаются пустыми.

**Акцент:** A BOUNDARY · речевой маркер «a boundary» · расчётное начало 13:44.2. Маска: Акцент выходит из-за левой стойки внешней рамки. Место: Верхнее левое свободное поле, не над сохранившейся поверхностью. Уход: После читаемой остановки скрыть акцент за той же стойкой в продолжающемся плане B02.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P44.B02 · оценочно 13:45.1–13:50.7

> This core preserves lower portions of the final columns of a larger roll.

**Кадр:** WS/MS, продолжение B01 с раздельными физической опорой и цифровой схемой.

**Камера:** Продолжить плавное сближение без смены ракурса.

**Действие:** Приблизительная пунктирная рамка отходит назад по своей направляющей; верхние продолжения колонок не дорисовываются.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P44.B03 · оценочно 13:50.7–13:52.8

> Missing material has not returned.

**Кадр:** MS, тот же план.

**Камера:** Статично, намеренная короткая выдержка.

**Действие:** Всё движение останавливается. Пустой верх и оборванные края остаются видны; ни текст, ни материал в них не проявляются.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P44.B04 · оценочно 13:52.8–13:59.2

> A continuous reconstruction of what survives cannot become a complete copy of the original book.

**Кадр:** WS, снова высокий угол, физическое ядро и цифровая схема в отдельных зонах.

**Камера:** Медленное отдаление на 6 см.

**Действие:** Тонкая подсветка обходит только фактически представленную нижнюю поверхность. Полный внешний прямоугольник не замыкается и не превращается в целый документ.

**Акцент:** WHAT SURVIVES · речевой маркер «what survives» · расчётное начало 13:54.5. Маска: Буквы поднимаются из-за нижней несущей рейки цифровой поверхности. Место: Нижний центр под поверхностью. Уход: Уходят за рейку, когда передний край рамки приближается к камере на переходе.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Непрозрачная передняя рамка полностью покрывает экран до смены ракурса; затем открыть отдельный стол условной карты читаемости P45. Новая схема не претендует на точные координаты прежней.

**Музыкальный замысел:** M5 продолжается с уменьшенным числом инструментов; на Missing material has not returned оставить VO почти без движения гармонии, затем вернуть мягкую опору.

**Активы:** F44-LOWER-PORTIONS — собственная схема нижних частей колонок; F44-APPROX-FRAME — прерывистая рамка приблизительного прежнего объёма; F44-GAPS — реальные пустые пространства, не белая заливка поверх текста; CORE-1667 — отдельная закрытая модель; REV13_P44_SEPARATE — Физическое ядро на отдельном ложементе и цифровая схема на отдельной опоре видны одновременно; внешняя рейка является маской A BOUNDARY..

**Граница достоверности:** Схема не задаёт точных неизвестных размеров всей книги и не реконструирует утраченные строки. Нельзя показывать, будто высота ядра уменьшилась именно при операции 1969 или 1987 года. Нет физического раскрытия оригинала.

**Источники:** S01, S02, S03.

### P45 · оценочно 13:59.6–14:18.6 · SET-J

**Реплика:** Nor has every trace been securely read. Small regions in the first three columns remain without transcription. Gaps and uncertain letters persist elsewhere. These absences belong in the result. Filling them with confident-looking text would blur the distinction between recovery and invention.

**Цель и тип:** Зритель воспринимает непрочитанные места как честную часть результата, а не как дефект, который нужно скрыть красивым текстом. (fact model).

**Передний план:** Ближний бортик стола и небольшая пустая подложка, лежащая вне зоны доказательств.

**Средний план:** На столе — собственная условная карта читаемости: три первые колонки с обозначениями 1–3 и несколько последующих зон. В ней физически вырезаны небольшие пустые окна; никакой транскрипции нет.

**Задний план:** Постоянная надпись SCHEMATIC READABILITY MAP — NOT TRANSCRIPTION, REGIONS NOT TO SCALE. На отдельной стойке — закрытая инвентарная карточка 1667.

**Перекрытия и опоры:** Пустые окна действительно прорезаны, через них виден фон. Любая подложка проходит перед ними и заметно заслоняет их; отсутствие материала нельзя имитировать невидимым стиранием. Бортик скрывает основание акцентных планок.

#### P45.B01 · оценочно 13:59.6–14:02.6

> Nor has every trace been securely read.

**Кадр:** MS, сверху под углом к карте читаемости.

**Камера:** Плавный въезд на 4 см.

**Действие:** Рамка предыдущей сцены открывает карту. Указатель проходит по поверхности и останавливается у первого пустого окна; ничего в нём не возникает.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P45.B02 · оценочно 14:02.6–14:06.9

> Small regions in the first three columns remain without transcription.

**Кадр:** CU, сверху на зоны 1–3.

**Камера:** Статично после изменения масштаба и угла.

**Действие:** Три короткие механические метки поворачиваются к пустым окнам в первых трёх условных колонках. Подпись REGIONS NOT TO SCALE остаётся читаемой, не позволяя принять расположение окон за точную карту статьи.

**Акцент:** NO TRANSCRIPTION · речевой маркер «without transcription» · расчётное начало 14:06.0. Маска: Планка выходит из-за верхней стенки лотка трёх колонок. Место: Верхнее правое поле вне самих окон. Уход: Опускается за стенку на переходе внимания к остальным зонам.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P45.B03 · оценочно 14:06.9–14:09.4

> Gaps and uncertain letters persist elsewhere.

**Кадр:** CU, тот же верхний ракурс.

**Камера:** Небольшой боковой проезд вправо на 5 см.

**Действие:** В следующей условной зоне открывается ещё один вырез и незамкнутая тонкая рамка неопределённости. Никаких конкретных букв внутри нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P45.B04 · оценочно 14:09.4–14:12.0

> These absences belong in the result.

**Кадр:** CU, тот же план.

**Камера:** Статично.

**Действие:** Указатель отходит в безопасное пустое поле стола. Все окна и незамкнутая рамка остаются открытыми и не закрываются декором.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P45.B05 · оценочно 14:12.0–14:17.6

> Filling them with confident-looking text would blur the distinction between recovery and invention.

**Кадр:** MS, более низкий боковой угол, видны зазор над картой и отдельная пустая подложка.

**Камера:** Статично после явной смены ракурса.

**Действие:** Непрозрачная кремовая подложка подходит к одному вырезу, на мгновение закрывая только пустоту; затем явно отводится обратно и ложится вне карты. На подложке нет греческих букв или сгенерированной транскрипции. Последний вид сохраняет настоящий открытый вырез.

**Акцент:** RECOVERY AND INVENTION · речевой маркер «recovery and invention» · расчётное начало 14:16.3. Маска: Буквы появляются из-за ближнего бортика стола, когда пустая подложка уже убрана. Место: Нижнее левое поле под картой. Уход: Возвращаются за бортик в конце паузы, прежде чем карта покинет сцену.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Пустая отведённая подложка поворачивается широкой непрозрачной стороной к камере, затем проходит перед объективом и полностью закрывает кадр. Под полным перекрытием меняется декорация; в следующем кадре открывается явно обозначенная иллюстрация философских тем, без превращения пробела в найденный текст.

**Музыкальный замысел:** M5 остаётся редким; на These absences belong in the result убрать подвижную фактуру, а на паузе после invention удержать только мягкую гармоническую основу.

**Активы:** J45-READABILITY — собственная условная карта с вырезами и номерами 1–3; J45-UNCERTAINTY — незамкнутая рамка неопределённости; J45-BLANK — пустая непрозрачная подложка без текста; J45-LABEL — постоянное обозначение схематичности и отсутствия масштаба.

**Граница достоверности:** Расположение и форма лакун здесь условны; только заявление об отсутствии транскрипции небольших регионов первых трёх колонок является фактом из VO. Даже для иллюстрации соблазна заполнения не генерировать правдоподобную греческую строку.

**Источники:** S01.

### P46 · оценочно 14:18.6–14:39.1 · SET-K

**Реплика:** What can be read points toward a philosophical discussion of ethics: human nature, action, practical wisdom, and moral progress. The researchers interpret the evidence as belonging to a Stoic context. In a preserved final column, they identify a reference to Aristocreon, associated with the Stoic philosopher Chrysippus.

**Цель и тип:** Зритель получает содержание сохранившегося аргумента как осторожную исследовательскую интерпретацию, не как сенсационный тайный текст. (explanatory metaphor).

**Передний план:** Нижняя кромка небольшой театральной площадки и левая вертикальная кулиса.

**Средний план:** Четыре собственных условных мотива на отдельных подставках: нейтральный человеческий профиль, две сближающиеся ладони, развилка из двух дорожек и низкие ступени. Справа — отдельная карточка упоминания имени, пока скрытая боковой шторкой.

**Задний план:** Кремовый задник ILLUSTRATION — ENGLISH PARAPHRASE. Верхняя незамкнутая рамка интерпретации и дальняя полка с объектным ярлыком PHerc. 1667.

**Перекрытия и опоры:** Кулиса маскирует вход акцента, но не предметный ярлык. У каждого мотива своя закреплённая опора и контактная тень. Карточка имён лежит в другой плоскости, не становится лицом или авторской подписью фигур.

#### P46.B01 · оценочно 14:18.6–14:23.3

> What can be read points toward a philosophical discussion of ethics:

**Кадр:** WS, фронтально к всей небольшой площадке.

**Камера:** Медленный въезд на 5 см.

**Действие:** Подложка предыдущей сцены открывает четыре пока неподвижных мотива. Постоянная маркировка PARAPHRASE уже видна; никаких цитат из уст персонажа нет.

**Акцент:** ETHICS · речевой маркер «ethics» · расчётное начало 14:22.9. Маска: Буквы выходят из-за левой кулисы и останавливаются на собственном небольшом основании. Место: Верхнее левое свободное поле. Уход: Уходят обратно за кулису после последовательного выделения мотивов.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P46.B02 · оценочно 14:23.3–14:26.7

> human nature, action, practical wisdom, and moral progress.

**Кадр:** WS, тот же непрерывный план.

**Камера:** Продолжить въезд ещё на 3 см.

**Действие:** На каждом названном понятии слегка наклоняется соответствующая подставка: профиль, ладони, развилка, ступени. Сами человеческие силуэты не разыгрывают якобы описанный в тексте конкретный исторический эпизод.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P46.B03 · оценочно 14:26.7–14:31.4

> The researchers interpret the evidence as belonging to a Stoic context.

**Кадр:** MS, под углом к верхней незамкнутой рамке и мотивам.

**Камера:** Статично после смены угла.

**Действие:** Незамкнутая рамка с обычной подписью INTERPRETATION опускается над мотивами, не запечатывая их в окончательный вывод.

**Акцент:** STOIC CONTEXT · речевой маркер «Stoic context» · расчётное начало 14:30.6. Маска: Акцент появляется из-за верхней перекладины рамки интерпретации. Место: Верхнее правое поле, отдельно от имени свитка. Уход: Прячется за перекладину перед открытием карточки упоминания.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P46.B04 · оценочно 14:31.4–14:38.7

> In a preserved final column, they identify a reference to Aristocreon, associated with the Stoic philosopher Chrysippus.

**Кадр:** CU, справа к отдельной карточке упоминания, мотивы видны в глубине.

**Камера:** Плавный боковой проезд на 5 см.

**Действие:** Шторка открывает типографскую карточку ARISTOCREON — MENTIONED IN THE TEXT. На associated with раскрывается отдельная небольшая планка CHRYSIPPUS с нейтральной связью ASSOCIATED WITH. Это современная передача имён латиницей; авторская строка нигде не заполняется.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Карточка упоминания поворачивается на своём шарнире и заполняет кадр обратной кремовой стороной. Под перекрытием — переход к предметному каталогу SET-L; имя остаётся на отдельной вкладке MENTIONED, а не перемещается в поле AUTHOR.

**Музыкальный замысел:** M5 продолжается; вернуть лёгкую тёплую верхнюю гармонику на перечне человеческих тем, сохраняя тихий уровень на researchers interpret.

**Активы:** K46-THEMES — четыре собственных абстрактных мотива этики; K46-INTERPRETATION — незамкнутая рамка с подписью; K46-MENTION — современная карточка Aristocreon и отдельная связь с Chrysippus; K46-PARAPHRASE — постоянная маркировка иллюстрации.

**Граница достоверности:** ILLUSTRATION / PARAPHRASE, а не реконструкция авторской сцены или цитата. Стоический контекст — интерпретация исследователей. Aristocreon назван в тексте; это не установление авторства. Не вводить точную родственную связь, отсутствующую в VO.

**Источники:** S01, S02, S19.

### P47 · оценочно 14:39.1–14:57.4 · SET-L

**Реплика:** A person named inside a book is not automatically its author. The author and title remain unknown. Scholars can now examine the surviving argument, compare interpretations, and disagree about what the damaged passages allow. Access to the evidence makes that conversation possible.

**Цель и тип:** Зритель отделяет упомянутое имя от авторства и воспринимает открытое обсуждение как нормальное продолжение исследования. (fact model).

**Передний план:** Левая кромка каталожного лотка и нижняя горизонтальная рейка.

**Средний план:** В центре — современная каталожная карточка PHerc. 1667 с отдельными полями AUTHOR и TITLE, первоначально закрытыми узкими створками. Слева лежит самостоятельная вкладка ARISTOCREON — MENTIONED. Справа два условных листа сравнения интерпретаций.

**Задний план:** Закрытая модель 1667 в отдельной нише; над листами постоянная подпись SCHEMATIC REVIEW, NO TRANSCRIPTION.

**Перекрытия и опоры:** Вкладка MENTIONED имеет свой паз и физически не входит в поля автора и заглавия. Створки закрывают только статусные поля. Листы интерпретаций стоят в раздельных направляющих, их можно сопоставить, не подменяя один другим.

#### P47.B01 · оценочно 14:39.1–14:43.8

> A person named inside a book is not automatically its author.

**Кадр:** CU, сверху под углом к вкладке MENTIONED и закрытым полям.

**Камера:** Медленный боковой проезд на 4 см.

**Действие:** Вкладка упомянутого имени поворачивается к своему отдельному пазу и остаётся там. Закрытые поля автора и заглавия не получают эту вкладку.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P47.B02 · оценочно 14:43.8–14:46.4

> The author and title remain unknown.

**Кадр:** CU, тот же непрерывный план.

**Камера:** Статично.

**Действие:** Две узкие створки открывают AUTHOR: UNKNOWN и TITLE: UNKNOWN. Поля напечатаны собственной нейтральной типографикой, не копируют внешний вид научного каталога.

**Акцент:** UNKNOWN · речевой маркер «unknown» · расчётное начало 14:45.9. Маска: Акцент выходит из-за правой створки поля TITLE. Место: Нижнее правое свободное поле вне обоих полей. Уход: Уходит за створку, когда внимание смещается к листам обсуждения.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P47.B03 · оценочно 14:46.4–14:53.6

> Scholars can now examine the surviving argument, compare interpretations, and disagree about what the damaged passages allow.

**Кадр:** MS, фронтально к двум листам сравнения с каталогом слева.

**Камера:** Плавный проезд вправо на 7 см.

**Действие:** Два условных листа INTERPRETATION A и INTERPRETATION B наклоняются друг к другу; у одного и того же пустого участка стоят разные незамкнутые рамки. Текста вымышленных мнений и вымышленных цитат специалистов нет.

**Акцент:** OPEN TO DEBATE · речевой маркер «compare interpretations, and disagree» · расчётное начало 14:49.4. Маска: Планка выдвигается из-за бокового края правого листа. Место: Верхнее правое поле над сравнением, без перекрытия повреждённого участка. Уход: Возвращается за лист на последней фразе абзаца.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P47.B04 · оценочно 14:53.6–14:57.1

> Access to the evidence makes that conversation possible.

**Кадр:** MS, тот же ракурс.

**Камера:** Небольшое отдаление на 4 см.

**Действие:** Оба листа остаются одновременно видны; третья пустая рамка наблюдения ставится рядом как возможность нового рассмотрения. Каталог с UNKNOWN и закрытый предмет сохраняются в одном пространстве.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Боковая стенка каталожного лотка проходит перед камерой и полностью закрывает кадр. Под ней — переход к более крупной современной карточке статуса препринта на столе SET-J; цвет бумаги тот же, объект и ракурс явно другие.

**Музыкальный замысел:** M5 непрерывен; сохранить подвижную гармонию очень тихой, не ставить музыкальную точку на UNKNOWN или на несогласии.

**Активы:** L47-CATALOGUE — собственная статусная карточка 1667; K46-MENTION — отдельная вкладка упомянутого имени; L47-INTERPRETATIONS — два условных листа и пустая рамка следующего рассмотрения; CORE-1667 — закрытый объект в отдельной нише.

**Граница достоверности:** UNKNOWN относится к автору и названию именно 1667. Листы A и B обозначают возможность сравнения, не документируют реальные разногласия конкретных исследователей. Открытость обсуждения не означает свободную коммерческую лицензию на все данные.

**Источники:** S01, S02.

### P48 · оценочно 14:57.4–15:16.2 · SET-J

**Реплика:** At the end of October twenty twenty-six, the work remains available as a preprint; publication in a peer-reviewed journal has not been confirmed. The specialists’ examination of the text is a different process. The published methods and readings remain open to further scrutiny.

**Цель и тип:** Зритель различает экспертное прочтение текста и подтверждённую публикацию в рецензируемом журнале, понимая временную границу публичного статуса работы. (fact model).

**Передний план:** Ближний бортик современного стола; слева узкая непрозрачная стойка карточки даты.

**Средний план:** Слева — собственная карточка PHerc. 1667 / PREPRINT / STATUS CHECK: 31 OCT 2026. Справа — два отдельных горизонтальных лотка TEXT EXAMINATION и JOURNAL PUBLICATION. На дальнем краю лежат собственные схемы методов и чтений без страниц статьи.

**Задний план:** Нейтральная стена и маленький объектный ярлык; постоянное обозначение EDITORIAL STATUS GRAPHIC. Никаких печатей принятия, логотипа журнала или выдуманного письма рецензента.

**Перекрытия и опоры:** Стойка закрывает начало акцентной планки. Лотки отделены зазором и имеют самостоятельные кромки. Карточка NOT CONFIRMED входит только в лоток JOURNAL PUBLICATION; она не касается лотка TEXT EXAMINATION.

#### P48.B01 · оценочно 14:57.4–15:03.4

> At the end of October twenty twenty-six, the work remains available as a preprint;

**Кадр:** MS, фронтально к статусной карточке и двум лоткам.

**Камера:** Медленный въезд на 5 см.

**Действие:** Открывается фактическая дата среза 31 OCT 2026. Карточка работы разворачивается на вертикальной оси и останавливается лицом к зрителю; на ней только собственная типографика и обозначение PREPRINT.

**Акцент:** PREPRINT · речевой маркер «preprint» · расчётное начало 15:03.0. Маска: Акцент выходит из-за левой непрозрачной стойки даты. Место: Верхнее левое свободное поле. Уход: Скрывается за стойкой перед выделением журнального статуса.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P48.B02 · оценочно 15:03.4–15:07.3

> publication in a peer-reviewed journal has not been confirmed.

**Кадр:** MS, тот же план.

**Камера:** Статично.

**Действие:** В правом лотке JOURNAL PUBLICATION становится видна простая карточка NOT CONFIRMED. Она относится к публично подтверждённой публикации в рецензируемом журнале; нет отрицательной печати, красного креста или вывода о ходе непубличных процедур.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P48.B03 · оценочно 15:07.3–15:11.6

> The specialists’ examination of the text is a different process.

**Кадр:** CU, сверху на два отдельных лотка.

**Камера:** Статично после смены ракурса и масштаба.

**Действие:** Левая рамка TEXT EXAMINATION слегка поднимается над своим лотком; JOURNAL PUBLICATION остаётся справа с отдельным статусом. Между рамками сохраняется видимый зазор без общего штампа.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P48.B04 · оценочно 15:11.6–15:15.9

> The published methods and readings remain open to further scrutiny.

**Кадр:** MS, под углом к собственным схемам методов и чтения.

**Камера:** Удержать план схем до полного прочтения FURTHER SCRUTINY, при необходимости в начале P49.B01; затем передний бортик полностью закрывает кадр.

**Действие:** Рамка рассмотрения проходит над условными схемами и останавливается у незамкнутой области; дата и два разных статуса сохраняются различимыми.

**Акцент:** FURTHER SCRUTINY · речевой маркер «further scrutiny» · расчётное начало 15:15.0. Маска: Акцент появляется из-за дальнего бортика лотка схем. Место: Верхнее правое поле, отдельно от статуса журнала. Уход: После читаемой остановки опустить буквы за дальний бортик; затем бортик заполняет кадр для перехода в начале P49.B01.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Сцена P48 продолжается в начале P49.B01 до читаемого ухода FURTHER SCRUTINY. Только затем передний бортик полностью перекрывает кадр и открывает стеллаж P49; переход выполняется один раз.

**Музыкальный замысел:** M5 остаётся редким; под not been confirmed оставить только мягкую основу. Последние секунды готовят переход к тёплой теме M6, не завершая трек отдельной каденцией.

**Активы:** J48-STATUS — собственная карточка статуса на 31 OCT 2026; J48-TWO-REVIEWS — раздельные лотки экспертного чтения и статуса журнальной публикации; J48-NOT-CONFIRMED — нейтральная статусная карточка; J48-METHODS — собственные схемы без воспроизведения статьи.

**Граница достоверности:** Графика привязана к 31 октября 2026 года; перед релизом позже этой даты статус нужно обновить после проверки источников. NOT CONFIRMED относится к публично подтверждённой публикации в рецензируемом журнале и не означает отсутствия экспертного чтения, непроведения непубличного рецензирования или журнального отказа. Скриншоты arXiv и защищённые figures не нужны.

**Источники:** S19, S21, S22, S31.

### P49 · оценочно 15:16.2–15:35.4 · SET-A

**Реплика:** A larger library waits behind this result. Reaching it means repeating the hard parts: measuring, tracing, checking, and reading. Some rolls will be harder. Some passages may stay lost. The achievement is a way to investigate writing while preserving the fragile object carrying it.

**Цель и тип:** Зритель понимает масштаб будущей работы и ценность чтения, которое сохраняет физический предмет. (fact model).

**Передний план:** Вертикальная стойка стеллажа слева и ближний край основного стола; колыбель 1667 остаётся на устойчивой центральной опоре.

**Средний план:** Закрытая модель 1667 и несколько иных, явно обобщённых рулонов в самостоятельных колыбелях без вымышленных инвентарных номеров. Позади них четыре собственные карточки операций.

**Задний план:** Мягко освещённые бумажные полки с маркировкой COLLECTION SCHEMATIC. Дальние модели различаются силуэтом, но не изображают конкретные ещё не прочитанные музейные объекты.

**Перекрытия и опоры:** Стойка реально перекрывает край полки. Каждая колыбель имеет контакт с поверхностью; движутся только отдельные карточки операций. Общая полка, модели и опоры не дрейфуют относительно друг друга.

#### P49.B01 · оценочно 15:16.2–15:19.2

> A larger library waits behind this result.

**Кадр:** Начало фразы: продолжающийся MS схем P48; после ухода акцента и перекрытия — широкий план архивного стеллажа P49.

**Камера:** Удержать P48 до ухода текста, затем открыть более широкий архивный план под полным перекрытием бортиком; речь не прерывается.

**Действие:** Сначала открыты статусные карточки и незамкнутая рамка исследования; затем показаны отдельные объекты стеллажа P49.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P49.B02 · оценочно 15:19.2–15:24.4

> Reaching it means repeating the hard parts: measuring, tracing, checking, and reading.

**Кадр:** WS, тот же непрерывный план.

**Камера:** Плавный въезд на 5 см.

**Действие:** На measuring, tracing, checking, reading по очереди наклоняются четыре небольшие карточки собственных пиктограмм: пучок, контур, рамка проверки, читательская зона. Это один непрерывный жест, без четырёх коротких склеек.

**Акцент:** HARD PARTS · речевой маркер «hard parts» · расчётное начало 15:21.3. Маска: Акцент выходит из-за передней кромки полки с карточками операций. Место: Верхнее левое свободное поле. Уход: Уходит под кромку полки перед взглядом на отдельные сложные модели.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P49.B03 · оценочно 15:24.4–15:26.5

> Some rolls will be harder.

**Кадр:** MS, под углом к двум дальним обобщённым моделям.

**Камера:** Статично после расширения угла относительно предыдущего кадра.

**Действие:** Боковой свет делает видимым неодинаковый неровный рельеф двух закрытых рулонов. Модели не разрушаются и не демонстрируют конкретную предсказанную неудачу.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P49.B04 · оценочно 15:26.5–15:28.6

> Some passages may stay lost.

**Кадр:** MS, тот же план.

**Камера:** Статично, короткая намеренная выдержка.

**Действие:** Перед одним закрытым предметом остаётся пустая карточка без текста. Ничего не заполняет её автоматически.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P49.B05 · оценочно 15:28.6–15:35.1

> The achievement is a way to investigate writing while preserving the fragile object carrying it.

**Кадр:** MS, возвращение к основному столу с 1667, видны отдельная цифровая схема и физический предмет.

**Камера:** Плавный отъезд на 6 см.

**Действие:** Физическая модель остаётся в колыбели. Отдельная небольшая цифровая схема на подставке наклоняется к зрителю, сохраняя расстояние от предмета; доступность схемы не требует движения древнего оригинала.

**Акцент:** PRESERVE THE OBJECT · речевой маркер «preserving the fragile object» · расчётное начало 15:32.5. Маска: Буквы выходят из-за переднего основания колыбели, не касаясь самой модели. Место: Нижнее правое свободное поле рядом с колыбелью. Уход: Опускаются обратно за основание перед переходом.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Стойка стеллажа проходит слева направо перед камерой и закрывает кадр; под перекрытием — переход к музейной галерее отдельных этапов труда SET-L. Появляется новая общая подпись ILLUSTRATED WORKFLOW THROUGH TIME.

**Музыкальный замысел:** Перевести M5 в M6 кроссфейдом примерно за 3 секунды от начала P49. Тёплая тема возвращается тихо; на Some passages may stay lost сохранить разреженность.

**Активы:** A49-COLLECTION — собственные обобщённые рулоны и отдельные колыбели; A49-WORKFLOW — четыре собственные пиктограммы этапов; A49-BLANK — пустая карточка неопределённого результата; CORE-1667 — неизменная закрытая модель; A49-DIGITAL — отдельная маленькая схема поверхности.

**Граница достоверности:** COLLECTION SCHEMATIC, не фотографически точная архивная комната и не указание точного количества доступных рулонов. Не обещать, что все свитки или все фрагменты будут прочитаны.

**Источники:** S01, S18, S20.

### P50 · оценочно 15:35.4–15:53.3 · SET-L

**Реплика:** Generations of work brought the project here. Early scholars copied exposed writing. Conservators preserved objects and fragments. Imaging researchers made measurements. Programmers made surfaces and signals accessible. Papyrologists produced readings that others could examine. Each contribution made the next one possible.

**Цель и тип:** Зритель воспринимает результат как последовательность взаимозависимых вкладов многих поколений. (explanatory metaphor).

**Передний план:** Непрерывная нижняя музейная рейка и вертикальные перегородки между пятью отдельными миниатюрными станциями.

**Средний план:** Слева направо пять станций: EARLY COPIES, CONSERVATION, IMAGING, COMPUTATION, PAPYROLOGY. У каждой собственная закреплённая подставка и маленький предметный символ работы; старый стол отделён перегородкой от современных приборов.

**Задний план:** Тёплый единый задник ILLUSTRATED WORKFLOW THROUGH TIME. У исторической станции отдельная подпись HISTORICAL RECONSTRUCTION; у современных технических станций — SCHEMATIC. Это галерея, не одна лаборатория.

**Перекрытия и опоры:** Перегородки реально заслоняют соседние станции при боковом проезде. Все столы и фигуры закреплены на своих основаниях. Нижняя связующая рейка находится перед станциями и не выглядит физической передачей одного древнего предмета между эпохами.

#### P50.B01 · оценочно 15:35.4–15:38.4

> Generations of work brought the project here.

**Кадр:** MS, три четверти к началу галереи; одна постоянная оптика на весь абзац.

**Камера:** Начать единый боковой проезд вправо; за этот beat пройти 6 см.

**Действие:** Входная перегородка открывает первую станцию и видимый ряд последующих. Общая маркировка галереи уже читается.

**Акцент:** GENERATIONS · речевой маркер «Generations» · расчётное начало 15:35.4. Маска: Акцент поднимается из-за первой музейной перегородки. Место: Верхнее левое свободное поле. Уход: Остаётся у входа и естественно скрывается за следующей перегородкой при движении камеры.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P50.B02 · оценочно 15:38.4–15:40.6

> Early scholars copied exposed writing.

**Кадр:** MS, тот же непрерывный боковой ракурс и масштаб.

**Камера:** Продолжить тот же проезд ещё на 6 см, без склейки.

**Действие:** На станции EARLY COPIES нейтральная рука опирается на старый стол, а простой пишущий инструмент делает одно короткое движение над условной копией. Открытый фрагмент лежит отдельно; никаких читаемых вымышленных греческих букв нет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P50.B03 · оценочно 15:40.6–15:42.7

> Conservators preserved objects and fragments.

**Кадр:** MS, тот же непрерывный ракурс.

**Камера:** Продолжить проезд ещё на 6 см.

**Действие:** На станции CONSERVATION видна закреплённая колыбель и отдельная рамка фрагмента. Небольшая поддерживающая боковая створка поднимается к рамке, не сжимая и не перенося предмет.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P50.B04 · оценочно 15:42.7–15:44.4

> Imaging researchers made measurements.

**Кадр:** MS, тот же непрерывный ракурс.

**Камера:** Продолжить проезд ещё на 6 см.

**Действие:** На станции IMAGING поворачивается собственная миниатюрная модель держателя между источником и детектором. Этот современный прибор находится за отдельной перегородкой, вдали от исторического стола.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P50.B05 · оценочно 15:44.4–15:47.0

> Programmers made surfaces and signals accessible.

**Кадр:** MS, тот же непрерывный ракурс.

**Камера:** Продолжить проезд ещё на 6 см.

**Действие:** На станции COMPUTATION неровная цветная цифровая лента расправляется только на своей отдельной подставке; перед ней открывается карта условных точек без текста.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P50.B06 · оценочно 15:47.0–15:50.0

> Papyrologists produced readings that others could examine.

**Кадр:** MS, тот же непрерывный ракурс.

**Камера:** Продолжить проезд ещё на 6 см.

**Действие:** На станции PAPYROLOGY две разные рамки рассмотрения одновременно открывают условную карту и отдельную область транскрипции. Область транскрипции помечена SCHEMATIC и не содержит фиктивного древнего текста.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P50.B07 · оценочно 15:50.0–15:53.0

> Each contribution made the next one possible.

**Кадр:** MS, тот же непрерывный ракурс; последняя станция и уходящие в глубину предыдущие.

**Камера:** Пройти последние 6 см и мягко остановить единый проезд.

**Действие:** Нижняя общая рейка открывает пять последовательных соединений между станциями. Последний короткий соединитель ложится в паз: показана зависимость вкладов, а не передача одного папируса из рук в руки.

**Акцент:** MADE POSSIBLE · речевой маркер «made the next one possible» · расчётное начало 15:50.8. Маска: Акцент выходит из-за последней вертикальной перегородки и останавливается перед её тенью. Место: Верхнее правое свободное поле. Уход: При переходе перегородка закрывает планку целиком.

**Звуковой замысел:** Один мягкий контакт последнего соединителя с пазом в конце видимого движения. (нового звука пока нет).

**Переход:** Последняя вертикальная перегородка занимает весь кадр. Под ней — переход к двум самостоятельным философским окнам SET-K; продолжение движения открывает уже другой масштаб и подпись ILLUSTRATION / PARAPHRASE.

**Музыкальный замысел:** M6 идёт одной непрерывной тёплой фразой; не ставить новый музыкальный удар на каждую профессию и не ускорять пульс вслед за короткими предложениями.

**Активы:** L50-GALLERY — пять раздельных музейных станций и перегородки; L50-EARLY — общий исторический стол копирования без конкретного героя; L50-CONSERVATION — поддерживаемая рамка и колыбель; L50-IMAGING — собственная миниатюра CT; L50-COMPUTATION — отдельная цифровая лента и точки; L50-PAPYROLOGY — две рамки рассмотрения; L50-RELAY — общая нижняя рейка зависимостей.

**Граница достоверности:** Один непрерывный проезд исключает дробление коротких предложений на случайные двухсекундные склейки. Галерея — метафора истории труда, не документально существовавшая комната. Историческое копирование не относится автоматически к 1667; современные устройства не появляются на старом столе.

**Источники:** S05, S06, S08, S01.

**Камера — ограничение:** Один непрерывный мастер с пятью закреплёнными станциями и фоном с запасом; 42 см исходного макета не являются координатами Palmier. Координаты задать и проверить в отдельной беззвучной пробе.

### P51 · оценочно 15:53.3–16:12.5 · SET-K

**Реплика:** The reward is unexpectedly intimate. In Paris Four, someone argues about pleasure. In sixteen sixty-seven, someone considers human conduct. Their names are uncertain; their pages are damaged. Parts of their thinking can enter a conversation again because enough physical traces survive to be questioned.

**Цель и тип:** Зритель чувствует человеческий масштаб найденных тем, сохраняя различие между двумя свитками и неизвестность имён. (explanatory metaphor).

**Передний план:** Нижняя кромка площадки и две узкие кулисы, каждая относится к своему окну.

**Средний план:** Слева охристое окно PARIS 4 с нейтральным мотивом слуха и простыми бумажными волнами; справа ржаво-оранжевое окно PHerc. 1667 с двумя анонимными силуэтами и условной протянутой ладонью. Между окнами пространственный промежуток с отдельной кулисой для NAMES UNCERTAIN.

**Задний план:** Задник ILLUSTRATION — ENGLISH PARAPHRASE. Над каждым окном отдельное пустое поле имени; ниже — условный повреждённый край поверхности, не страницы кодекса.

**Перекрытия и опоры:** Кулисы ограничивают темы по объектам и скрывают акцентные планки отдельно. Профили и ладонь закреплены на собственной сцене; центральная кулиса находится в зазоре между окнами. Ни один древний персонаж не получает речевой пузырь или авторскую подпись. Дополнение v1.3: Между окнами отдельная непрозрачная центральная кулиса; она скрывает NAMES UNCERTAIN, не прикрывая ни бирки, ни предметы. Каждое окно и каждая из двух боковых кулис на отдельных опорах.

#### P51.B01 · оценочно 15:53.3–15:55.5

> The reward is unexpectedly intimate.

**Кадр:** MS, фронтально к двум закрытым боковыми кулисами окнам.

**Камера:** Медленный въезд на 3 см.

**Действие:** После предыдущей перегородки появляется небольшая, камерная площадка. Кулисы расходятся только настолько, чтобы открыть два самостоятельных ярлыка объектов.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P51.B02 · оценочно 15:55.5–15:58.5

> In Paris Four, someone argues about pleasure.

**Кадр:** MS, непрерывный общий план обоих окон; внимание слева.

**Камера:** Держать один ракурс B01–B04, не теряя бирки и не закрывая второе окно.

**Действие:** В окне PARIS 4 поднимаются две волнистые бумажные линии у нейтрального мотива слуха.

**Акцент:** PLEASURE · речевой маркер «pleasure» · расчётное начало 15:58.1. Маска: Акцент выходит из-за левой кулисы окна PARIS 4. Место: Верхнее левое поле над соответствующим окном. Уход: После читаемой остановки убрать за левую кулису; возможное пересечение по времени с правым акцентом допускается только при полной раздельности и читаемости.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P51.B03 · оценочно 15:58.5–16:01.5

> In sixteen sixty-seven, someone considers human conduct.

**Кадр:** MS, продолжение общего плана двух окон; внимание справа.

**Камера:** Удержать непрерывную композицию B01–B04, не меняя опор и бирок.

**Действие:** В окне PHerc. 1667 условная ладонь поворачивается к анонимному силуэту, оставаясь на собственной опоре.

**Акцент:** HUMAN CONDUCT · речевой маркер «human conduct» · расчётное начало 16:00.6. Маска: Акцент выходит из-за правой кулисы окна PHerc. 1667. Место: Верхнее правое свободное поле. Уход: После читаемой остановки убрать за правую кулису до входа NAMES UNCERTAIN.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P51.B04 · оценочно 16:01.5–16:04.9

> Their names are uncertain; their pages are damaged.

**Кадр:** MS, продолжение общего плана двух окон; раздельные поля имён и повреждённые края видимы.

**Камера:** Удержать ракурс B01–B04 без короткой смены крупности; при необходимости продолжить в начало B05.

**Действие:** Подписи NAME UNCERTAIN остаются у своих полей; свет затем отдельно выделяет неровные края, имена не дорисовываются.

**Акцент:** NAMES UNCERTAIN · речевой маркер «names are uncertain» · расчётное начало 16:01.9. Маска: Общая отдельная непрозрачная центральная кулиса скрывает буквы; они выходят из-за её верхнего края. Место: Свободная центральная зона между окнами, вне предметов и обеих бирок. Уход: После читаемой остановки опустить за ту же кулису, при необходимости в начале B05, затем переход к широкому виду.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P51.B05 · оценочно 16:04.9–16:12.2

> Parts of their thinking can enter a conversation again because enough physical traces survive to be questioned.

**Кадр:** Начало фразы: продолжение MS двух окон B04; после ухода акцента — WS всей площадки с отдельной современной рамкой рассмотрения.

**Камера:** Удержать MS до читаемого ухода NAMES UNCERTAIN, затем перейти к широкому виду без прерывания речи.

**Действие:** Сначала имена остаются неопределёнными; затем рамка рассмотрения поднимается на собственной опоре перед двумя раздельными окнами. Фигуры молчат.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Нижняя кромка площадки поднимается перед объективом и закрывает кадр. Под перекрытием — возвращение к реальному масштабу постоянной модели 1667 на столе SET-A, с её знакомой инвентарной биркой.

**Музыкальный замысел:** M6 сохраняет тёплую тему, но становится камернее: мягкое фортепиано и тонкая струнная опора. Никаких голосов, древней музыки или звуков вымышленного разговора.

**Активы:** K51-TWO-THEMES — два самостоятельных тематических окна; K51-PLEASURE — нейтральный мотив слуха и волны; K51-CONDUCT — анонимные силуэты и условная ладонь; K51-NAMES — отдельные поля неопределённых имён; K51-READER — современная рамка рассмотрения; REV13_P51_CURTAIN — Между окнами отдельная непрозрачная центральная кулиса; она скрывает NAMES UNCERTAIN, не прикрывая ни бирки, ни предметы. Каждое окно и каждая из двух боковых кулис на отдельных опорах..

**Граница достоверности:** ILLUSTRATION / PARAPHRASE. Удовольствие относится к Paris 4, человеческое поведение — к 1667. Это не идентифицированные авторы и не буквально описанные эпизоды. Слово pages в VO передаётся поверхностью папируса, не переплетённой книгой.

**Источники:** S14, S18, S01, S02.

### P52 · оценочно 16:12.5–16:30.5 · SET-A

**Реплика:** Look again at the black core. It has not become fresh papyrus. Its lost edges are still lost. The digital surface preserves that damage while making room for recoverable words. Reading has changed what we can know without undoing what happened.

**Цель и тип:** Зритель возвращается к неизменённому хрупкому предмету и понимает, что изменилось знание, а не его материальная история. (fact model).

**Передний план:** Знакомая передняя стенка колыбели и нижний край инвентарной бирки PHerc. 1667.

**Средний план:** В центре слева — постоянная закрытая угольная модель в поддерживающей колыбели. Справа на отдельном основании — кремовая цифровая поверхность с теми же условно обозначенными утратами, без подлинной транскрипции.

**Задний план:** Мягко освещённые архивные полки в расфокусе. Подписи STYLIZED OBJECT MODEL и DIGITAL MODEL размещены рядом со своими объектами, без пересечения зон.

**Перекрытия и опоры:** Передняя стенка колыбели скрывает только нижнюю опору ядра; его оборванный край остаётся открытым. Цифровая поверхность стоит отдельно с собственным зазором и тенью. Ни одна её часть не выходит из реального рулона. Дополнение v1.3: Та же модель 1667, что в P53: повреждения, ориентация, опора и бирка сохраняются; цифровая поверхность остаётся отдельной.

#### P52.B01 · оценочно 16:12.5–16:15.1

> Look again at the black core.

**Кадр:** CU, низкий ракурс три четверти к знакомому чёрному ядру.

**Камера:** Очень медленный въезд на 2 см.

**Действие:** Кромка предыдущей сцены открывает тот же предмет и его бирку. Модель не меняет цвет, форму или размер.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P52.B02 · оценочно 16:15.1–16:17.7

> It has not become fresh papyrus.

**Кадр:** MS, общий план знакомого ядра слева и отдельной цифровой поверхности справа; начало непрерывного плана B02–B04.

**Камера:** После перехода от B01 удержать единый ракурс, сохраняя раздельные опоры и бирку.

**Действие:** На чёрной поверхности остаются прежние повреждения, без свежей основы или реставрационного блеска.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P52.B03 · оценочно 16:17.7–16:20.3

> Its lost edges are still lost.

**Кадр:** MS, продолжение плана B02 с неровным краем и цифровой поверхностью.

**Камера:** Без склейки перевести световое внимание на край ядра.

**Действие:** Тёплый боковой свет выделяет пустоту у оборванного края; частицы не возвращаются и контур не замыкается.

**Акцент:** STILL LOST · речевой маркер «still lost» · расчётное начало 16:19.4. Маска: Передняя непрозрачная стенка колыбели скрывает буквы; они выходят позади её нижнего края. Место: Нижнее левое свободное поле под объектом, не поверх утраты. Уход: После читаемой остановки в продолжающемся B04 опустить буквы за ту же стенку; до входа WHAT WE KNOW.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P52.B04 · оценочно 16:20.3–16:25.4

> The digital surface preserves that damage while making room for recoverable words.

**Кадр:** MS, продолжение B02–B03: физическое ядро слева, отдельная цифровая поверхность справа.

**Камера:** Удержать единый ракурс без склейки.

**Действие:** Свет выделяет неровный край цифровой поверхности; условная область чтения появляется только на сохранившемся участке, вырезы не заполняются.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P52.B05 · оценочно 16:25.4–16:30.1

> Reading has changed what we can know without undoing what happened.

**Кадр:** MS, тот же непрерывный план.

**Камера:** Продолжить боковой проезд ещё на 3 см и остановиться.

**Действие:** Свет мягко выделяет отдельную цифровую поверхность, сохраняя прежнее освещение физического ядра. Оба предмета остаются вместе в кадре, с независимыми подписями и опорами.

**Акцент:** WHAT WE KNOW · речевой маркер «what we can know» · расчётное начало 16:26.7. Маска: Акцент появляется из-за левого ребра отдельного основания цифровой поверхности. Место: Нижнее правое свободное поле вне модели и рамки читаемости. Уход: Скрывается за основанием перед переходом к финальному общему плану.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** Передний край основания цифровой модели проходит по всему кадру. Под полным перекрытием — смена на отчётливый верхний общий план того же стола в P53, без переноса или преобразования самого ядра.

**Музыкальный замысел:** M6 становится ещё тише и реже; фортепиано сохраняет тему в нескольких нотах, струнная опора почти неподвижна. Повреждение не сопровождается трагическим ударом.

**Активы:** CORE-1667 — тот же закрытый предмет без изменения повреждений; CRADLE-1667 — прежняя колыбель и бирка; A52-DIGITAL — собственная отдельная цифровая поверхность с открытыми вырезами; A52-LABELS — физическая и цифровая зоны различимы; REV13_P52_CONTINUITY — Та же модель 1667, что в P53: повреждения, ориентация, опора и бирка сохраняются; цифровая поверхность остаётся отдельной..

**Граница достоверности:** STYLIZED OBJECT MODEL / DIGITAL MODEL. Повреждения собственной диорамы не выдаются за точную документальную карту 1667. Свет улучшает видимость модели, но не обозначает реальную реставрацию материала. Никаких вновь созданных древних букв.

**Источники:** S01, S02.

### P53 · оценочно 16:30.5–16:50.0 · SET-A

**Реплика:** For this surviving core, the successful new act of reading required a different kind of touch: a beam, a measured surface, and a careful decision about each mark. The roll stayed closed. Its surviving words no longer had to remain silent.

**Цель и тип:** Зритель уходит с ясным парадоксом: сохранившиеся слова стали доступны, хотя рулон остался закрытым. (fact model).

**Передний план:** Передняя стенка постоянной колыбели и низкая рамка финального стола.

**Средний план:** Закрытая модель 1667 в центре. Позади неё на отдельных собственных подставках три маленькие поясняющие карточки: условный пучок, измеренная поверхность, рамка решения о следе. Цифровая поверхность P52 остаётся справа и не касается предмета.

**Задний план:** Тёплый спокойный бумажный задник; полки уходят в мягкую нерезкость. На карточках постоянная малая маркировка SCHEMATIC, у предмета — STYLIZED OBJECT MODEL.

**Перекрытия и опоры:** Карточки открываются только за предметом и не посылают настоящий световой луч на консервационный стол. Их основания скрыты задним бортиком. Передняя стенка колыбели маскирует акцент; ядро сохраняет контакт с опорами и не поворачивается. Дополнение v1.3: Та же модель и те же повреждения, что в P52; зерно движется даже во время смысловой неподвижности.

#### P53.B01 · оценочно 16:30.5–16:37.3

> For this surviving core, the successful new act of reading required a different kind of touch:

**Кадр:** WS, высокий угол около 75 градусов к знакомому столу.

**Камера:** Медленный въезд на 6 см.

**Действие:** После перекрытия становится виден весь стол: физический предмет и отдельная цифровая поверхность. За ними три поясняющие карточки пока стоят ребром. Ничья рука не прикасается к оригиналу.

**Акцент:** A DIFFERENT TOUCH · речевой маркер «a different kind of touch» · расчётное начало 16:35.2. Маска: Буквы поднимаются из-за низкого заднего бортика стола, впереди трёх закрытых карточек. Место: Верхний левый свободный сектор, не над ядром. Уход: Акцент опускается за бортик перед перечислением трёх операций.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P53.B02 · оценочно 16:37.3–16:42.5

> a beam, a measured surface, and a careful decision about each mark.

**Кадр:** WS, тот же непрерывный план.

**Камера:** Продолжить въезд ещё на 3 см и мягко остановиться.

**Действие:** На a beam открывается карточка условного пучка; на a measured surface — карточка сетки; на a careful decision — карточка рамки проверки. В последней есть один абстрактный след и незамкнутая рамка, но нет восстановленной буквы или автоматически завершённого слова.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P53.B03 · оценочно 16:42.5–16:44.2

> The roll stayed closed.

**Кадр:** CU, низкий боковой ракурс к одному закрытому ядру; карточки вне фокуса позади.

**Камера:** Статично после отчётливой смены угла и масштаба.

**Действие:** Камера удерживает закрытый рулон в поддерживающей колыбели. Ничего не раскрывается и не выходит из его края.

**Акцент:** STAYED CLOSED · речевой маркер «stayed closed» · расчётное начало 16:43.3. Маска: Акцент выходит из-за передней стенки колыбели. Место: Нижнее правое поле, отдельно от ядра и бирки. Уход: После читаемой остановки в том же плане B04 опустить буквы за переднюю стенку колыбели; затем оставить ядро и бирку до конца финальной выдержки.

**Звуковой замысел:** NONE (нового звука пока нет).

#### P53.B04 · оценочно 16:44.2–16:48.0

> Its surviving words no longer had to remain silent.

**Кадр:** CU, тот же финальный план.

**Камера:** Удержать тот же финальный план после ухода STAYED CLOSED; зерно продолжает движение.

**Действие:** После полного ухода акцента остаются закрытое ядро, его бирка и мягкий свет; новые буквы и целый свиток не появляются.

**Бумажный акцент:** отдельного нового нет.

**Звуковой замысел:** NONE (нового звука пока нет).

**Переход:** После последнего слова сохранить финальный предмет в течение двухсекундной смысловой выдержки. Закрытие занимает 0,5 с, количество кадров пересчитать по фактическому FPS. Зерно продолжается; затем четыре титровые карточки общей длительностью 20 с.

**Музыкальный замысел:** M6 к последней строке почти неподвижен: мягкая удержанная гармония без нового мотива. После последнего слова сохранить двухсекундную выдержку, затем продолжить тихую коду титров T01–T04; окончательное затухание на T04. Финального удара и SFX нет.

**Активы:** CORE-1667 — неизменный финальный закрытый предмет; CRADLE-1667 — прежняя опора и инвентарная бирка; A53-THREE-CARDS — три собственные схемы пучка, поверхности и проверки; A52-DIGITAL — отдельная поверхность на собственной подставке; A53-END — чистый финальный кадр без нового текста; REV13_P53_CONTINUITY — Та же модель и те же повреждения, что в P52; зерно движется даже во время смысловой неподвижности..

**Граница достоверности:** Все три карточки — объясняющие схемы. Beam здесь показан внутри карточки, не как реальное облучение архивного стола. Новый успешный акт чтения не требует физического разматывания сохранившегося ядра; исторические повреждения не отменяются. Последняя строка — образ доступа к словам, не обещание голоса или полной книги.

**Источники:** S01, S20.

## Заключительные титры

- T01 · оценочно 16:50.0–16:55.0: A PAPER DETOUR FILM — Бумажная марка PAPER DETOUR поднимается из-за нижнего бортика; рядом остаётся маленький силуэт закрытого рулона, подписанный MODEL.
- T02 · оценочно 16:55.0–17:00.0: RESEARCH / Seales et al. · 2016 / Parker et al. · 2019 / Vesuvius Challenge · 2023–2026 — Передняя карточка проходит слева направо и закрывает кадр; за ней открывается этот фиксированный список.
- T03 · оценочно 17:00.0–17:05.0: 2026 FINDINGS / Angelotti et al. · arXiv:2606.29085 / PREPRINT / Research cutoff: 31 OCT 2026 — Та же непрозрачная карточка открывает следующий лист; PREPRINT занимает отдельную строку.
- T04 · оценочно 17:05.0–17:10.0: Full sources and method notes in the description. / Original paper reconstructions and explanatory models. / PAPER DETOUR — Последняя карточка входит справа и открывает заключительный текст. В последние две секунды свет мягко снижается.

## Реестр запланированных активов

Это производственное задание; файлы не считаются созданными.

- **A_CORE1667** (P01, P02, P03, P10, P11): самостоятельная модель сердцевины 8 × 2 см — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A_CRADLE1667** (P01, P02, P10, P11): ложемент с двумя опорами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A_TAG1667** (P01, P02, P10, P11): небольшая инвентарная бирка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A_HAND_SCALE** (P01): плоская карточка масштаба с безличным силуэтом ладони — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A_LAYER_RISK** (P01): отдельный учебный разрез со следом и указателем — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A_ARCHIVE_DEPTH** (P01): три плоскости полок — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_CABINET1667** (P02, P10): шкаф с отдельными отсеками истории объекта — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_FRAGMENT_FRAME** (P02, P10): рама с десятью условными сохранившимися кусками — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_LOSS_OUTLINE** (P02): отдельный условный контур утраченной массы рулона — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_PREVIEW_STAGE** (P03): четыре учебные карточки в последовательных пазах — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_PHYSICAL_BAY** (P03, P12, P14, P16): отдельная ячейка исходного предмета — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_PREVIEW_BEAM** (P03): условный луч — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_PREVIEW_MESH** (P03): искривлённая бумажная сетка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_PREVIEW_PHONE** (P03): безымянная карточка общего условного профиля и отдельного телефона с пустым экраном; перегородка отделяет её от ячейки 1667 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_REVIEW_FRAMES** (P03): пара рамок сравнения без букв — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_VESUVIUS_PROFILE** (P04): многослойный профиль вулкана — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_COAST_RELIEF** (P04): передние береговые слои — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_ROMAN_BLOCKS** (P04): условная городская застройка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_VILLA_CUTAWAY** (P04): условный разрез виллы с отдельной передней стенкой — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_ROLL_TRAYS** (P04): подносы с учебными рулонами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_ASH_PLANES** (P04): мягкие пепельные и осадочные плоскости — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_DATE79** (P04): небольшая бирка AD 79 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_PAPYRUS_STRIP** (P05): учебная светлая полоса с соединениями листов — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_ROLL_SUPPORTS** (P05): две неподвижные опоры для учебных скруток — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_COLUMN_MARKS** (P05): заведомо неалфавитные штрихи для схемы колонок — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_BURNT_COMPARISON** (P05): отдельная обугленная модель без инвентарного номера — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_LAYER_WINDOW** (P05): увеличивающая учебная рамка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_EXCAVATION_SECTION** (P06): условный разрез грунта и галереи — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_EXCAVATOR_SILHOUETTES** (P06): два безликих силуэта без детализации одежды — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_DISCOVERY_ROLLS** (P06): самостоятельные закрытые модели рулонов — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **B_CENTURY_CARD** (P06): бирка 18TH CENTURY — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_COLLECTION_TRAY** (P06): архивный лоток с направляющей — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_EMPTY_READING_FRAME** (P06): пустая учебная рамка чтения — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_PADERNI_SAMPLE** (P07): условный рулон для общего метода, без номера 1667 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_METHOD_HANDS** (P07): безличные кисти рук на одной плоскости рабочего пространства — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_CUTTING_PLATE** (P07): условная режущая пластина — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_SCRAPER** (P07): условный скребок — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_REMOVAL_TRAY** (P07): лоток снятого материала — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_COPY_SHEET** (P07): отдельный лист с неалфавитными учебными штрихами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_PADERNI_LABEL** (P07): карточка имени и маркировок — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_PIAGGIO_SCHEME** (P08): собственная объясняющая рама с натянутыми нитями — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_PIAGGIO_SUPPORT** (P08): поддерживающая полоса и опора условного рулона — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_PIAGGIO_LABEL** (P08): карточка имени — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_NAPLES1753** (P08): историческая бирка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_MUSIC1754** (P08): отдельная полка результата 1754 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **C_WORK_MUSIC** (P08): фактическая карточка Philodemus / work on music — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_HISTORY_LINE** (P08): нейтральная линия времени — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_COLLECTION_CABINET** (P09): архивный шкаф с тремя раздельными ячейками — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_OPEN_FRAGMENT_MODEL** (P09): условный открытый фрагмент — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_DAMAGED_ROLL_MODEL** (P09): отдельная повреждённая модель без номера — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_INTERVENTION_CARDS** (P09): пустые учебные поля истории — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_TWO_HISTORY_LINES** (P09): две линии с фактическими заголовками — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_1667_TIMELINE** (P10): три документированные карточки 1800s/1969/1987 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_TIMELINE_SHUTTERS** (P10): три независимые заслонки — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_DIMENSION_BOARD** (P11): планшет с продольной и поперечной шкалами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_1782_HEIGHT** (P11): отдельная историческая карточка 1782 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **D_EARLIER_DIAMETER** (P11): условный сравнительный контур прежнего диаметра — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **H_SEALES_SILHOUETTE** (P12): стилизованная иллюстрация учёного с фактической карточкой роли — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **H_GENERIC_WORKSPACE** (P12): современный стол и бумажный монитор — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **H_COLLABORATOR_CARDS** (P12): нейтральные карточки сотрудничества — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_MEASURED_CONTOURS** (P12): три учебных контура сечения — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_DIGITAL_MESH** (P12, P16): светлая сетка с неровными границами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_DIGITAL_LABEL** (P12): постоянная подпись DIGITAL COPY — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **E_TOMO_STAGE** (P13): учебный томограф с неподвижными источником и детектором — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **E_ROTATION_CRADLE** (P13): защитная опора на одной оси вращения — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **E_GENERIC_ROLL** (P13): самостоятельная закрытая модель без инвентарного номера — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **E_BEAM_DIAGRAM** (P13): условный луч с явной маркировкой — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **E_PROJECTION_CARDS** (P13): отдельные карточки угловых проекций — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_DIGITAL_VOLUME** (P13, P14): кремовый объём данных — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_SECTION_PLANE** (P13, P14): независимая виртуальная плоскость сечения — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_SURFACE_TRACE** (P14): оранжевая линия одной поверхности с корректными масками — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_SURFACE_CARD** (P14): отдельная контурная карточка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_REFERENCE_GRID** (P14, P16): сетка координат на рамке — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_ROAD_METAPHOR** (P15): отдельная сложенная дорожная лента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_MODEL_DIVIDER** (P15): перегородка между метафорой и технической схемой — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_ADJACENT_WRAPS** (P15): схема тесных соседних витков — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_WRONG_PATH** (P15): линия с явно пунктирным неправильным переходом — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_ABSTRACT_MARKS** (P15): квадратные и круглые метки без букв — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_SCRAMBLED_OUTPUT** (P15): отдельная выходная карточка неверного порядка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_TASK_SURFACE** (P16): карточка задачи геометрии — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_TASK_INK** (P16): отдельная карточка задачи чернил — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F_GEOMETRY_RAILS** (P16): направляющие двух раздельных задач — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **G_INK_SAMPLE** (P17): самостоятельная схема углеродного следа — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **G_CARBONIZED_SUBSTRATE** (P17): отдельная схема обугленного основания — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **G_SIMULATED_DISPLAY** (P17): бумажный дисплей неоднозначного сигнала — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **G_CONTRAST_SLIDER** (P17): ползунок в реальной рамке — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **G_NO_SCAN_LABEL** (P17): постоянная маркировка учебного изображения — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L_ENGEDI_BAY** (P18): отдельная сине-серая ячейка Эн-Геди — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L_ENGEDI_MODEL** (P18): самостоятельная стилизованная модель обгоревшего рулона на отдельной опоре — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L_ENGEDI2016** (P18): фактическая карточка исследования 2016 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L_ANIMAL_SKIN_CARD** (P18): объясняющая карточка материала — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L_CONTRAST_COMPARISON** (P18): пара условных дисплеев с различным отделением сигнала от фона — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L_HERCULANEUM_BAY** (P18): отдельная тёплая ячейка Геркуланума — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L_WARM_DIVIDER** (P18): непрозрачная подвижная перегородка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P19-A01** (P19): шкаф с синей ячейкой EN-GEDI и отдельным отсеком HERCULANEUM — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P19-A02** (P19): собственные редакционные карточки исследований 2015 и 2019 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P19-A03** (P19): реечная рамка проверки и два набора бумажных акцентов — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P20-A01** (P20): собственный схематический фрагмент без букв с тремя штрихами и отверстиями — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P20-A02** (P20): парные держатели PHOTO и CT с регистрационной плёнкой — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P20-A03** (P20): лоток MODEL, ползунок и бумажные акценты — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P21-A01** (P21): собственная карта вероятного сигнала без букв — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P21-A02** (P21): три контрольных окна со стойками и регистрационным ползунком — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P21-A03** (P21): условная рука, лупа и пустая финальная графа — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P21-A04** (P21): два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P22-A01** (P22): три именные ниши основателей без реконструкции конкретной встречи — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P22-A02** (P22): пакеты SCANS / SOFTWARE / PRIZES и распределительная рейка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P22-A03** (P22): три собственные схематические панели геометрии, текстуры и сигнала — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P22-A04** (P22): карточка даты и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P23-A01** (P23): двухъячеечный шкаф с непрозрачным разделителем — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P23-A02** (P23): отдельный стилизованный Paris4 и его охристый комплект бирок — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P23-A03** (P23): отдельный короткий сердечник 1667 и рыжий комплект бирок — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P23-A04** (P23): общая полоса метода и две раздельные дорожки данных — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P23-A05** (P23): два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P24-A01** (P24): условный силуэт Handmer и современный стол без конкретных деталей одежды — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P24-A02** (P24): собственная схематическая текстура волокон и трещин без букв — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P24-A03** (P24): объёмная рамка, скоба направления и общая рейка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P24-A04** (P24): карточки этапов и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P25-A01** (P25): общий условный профиль и срезанный угол основания, отдельные фигура и рука; имя вводится на соответствующих словах — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P25-A02** (P25): разделённые лотки EXAMPLES / NEW SECTION и стилус — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P25-A03** (P25): собственные схематические штрихи и карты вероятного сигнала — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P25-A04** (P25): подписи реконструкции и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P26-A01** (P26): нейтральная комната с перегородкой и неназванными силуэтами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P26-A02** (P26): тот же условный силуэт, отдельные рука и телефон; пустой экран, ненадписанное уведомление, внешняя схема удалённого компьютера и поздние неписьменные штрихи — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P26-A03** (P26): отдельная нейтральная гаражная стойка и проход — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P26-A04** (P26): самостоятельная архивная ячейка Paris4 с подставкой — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P26-A05** (P26): подписи RECONSTRUCTION / SCHEMATIC и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P27-A01** (P27): собственная посимвольная векторная транскрипция ΠΟΡΦΥΡΑϹ / porphyras по официальному First Letters, без копирования скана — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P27-A02** (P27): бумажный держатель, окно даты OCTOBER 2023 и подпись источника — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P27-A03** (P27): отдельный закрытый макет Paris4 и цифровое контрольное окно — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P27-A04** (P27): цветовая карточка и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P28-A01** (P28): условный силуэт Nader и отдельный рабочий стол — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P28-A02** (P28): две собственные карты одной области с регистрационными вырезами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P28-A03** (P28): карточка EARLIER RESULT, линейка и пустой держатель READING — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P28-A04** (P28): подписи схемы и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P29-A01** (P29): собственная изогнутая цифровая поверхность и отдельная плоская развёртка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P29-A02** (P29): отдельный задний отсек с закрытым стилизованным Paris4 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P29-A03** (P29): три именные карточки и общая рейка вкладов — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P29-A04** (P29): панели GEOMETRY / INK DETECTION / CHECKED IMAGE — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P29-A05** (P29): большой смотровой портал и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P30-A01** (P30): конверты заявок с непрозрачными именными клапанами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P30-A02** (P30): раздельные панели воспроизведения и независимых чтений — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P30-A03** (P30): собственная схематическая контрольная карта без букв с настоящими прорезями — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P30-A04** (P30): держатель результата и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P31-A01** (P31): календарное окно и раздельные карточки даты объявления и года конкурса — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P31-A02** (P31): три именные карточки и одна общая плашка $700,000 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P31-A03** (P31): сохранённый держатель проверок с редакционной карточкой REVIEW COMPLETED — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P31-A04** (P31): отдельная папка и стилизованный закрытый Paris4 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P31-A05** (P31): два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P32-A01** (P32): сетка из двадцати одинаковых плиток, ровно одна выделенная — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P32-A02** (P32): три собственных схематических колоночных окна без древнего текста — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P32-A03** (P32): карточка ARGUMENT, рамки и постоянная дата FEBRUARY 2024 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P32-A04** (P32): два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P33-A01** (P33): собственный условный театр с двумя одинаковыми чашами и шестью одинаковыми бумажными кусочками — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P33-A02** (P33): два безымянных профиля и знаки FOOD / MUSIC / PERCEPTION — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P33-A03** (P33): вопросительная перегородка и незавершённая стрелка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P33-A04** (P33): редакционная карточка пересказа и отдельная неровная цифровая рамка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P33-A05** (P33): два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P34-A01** (P34): регистрационная карточка Paris4 с физическими пустыми полями AUTHOR / TITLE — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P34-A02** (P34): отдельная папка CONTENT и редакционная карточка темы — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P34-A03** (P34): жёсткая перегородка IDENTIFICATION NEEDED и отдельный закрытый макет Paris4 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P34-A04** (P34): два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P35-A01** (P35): собственный обобщённый макет рулонной геометрии с несколькими прослеженными участками — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P35-A02** (P35): три окна уже существующих дефектов и независимые указатели — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P35-A03** (P35): контрольная рамка, направляющие и матовая створка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P35-A04** (P35): два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P36-A01** (P36): существующий короткий стилизованный сердечник 1667 и поддерживающая подставка SET-A — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P36-A02** (P36): рыжая бирка PHerc.1667 и постоянный фактический идентификатор — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P36-A03** (P36): отдельное цифровое боковое окно с собственным контуром и настоящими прорезями — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **P36-A04** (P36): матовая переходная створка и два бумажных акцента — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **CORE-1667** (P37, P38, P42, P43, P44, P47, P49, P52, P53): постоянная стилизованная закрытая модель примерно 8 × 2 см; оригинал сохраняет отдельную нишу; неизменный закрытый предмет правой ниши; постоянное закрытое ядро; отдельная закрытая модель; закрытый объект в отдельной нише; неизменная закрытая модель; тот же закрытый предмет без изменения повреждений; неизменный финальный закрытый предмет — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **CRADLE-1667** (P37, P52, P53): колыбель и отдельная инвентарная бирка; прежняя колыбель и бирка; прежняя опора и инвентарная бирка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **E37-BEAMLINE** (P37): собственные источник, детектор и вращающийся держатель — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **E37-DATA-CUBE** (P37): модель объёма со сменной сеткой — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **E37-CREDITS** (P37): две именные бумажные планки — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F38-TRACE** (P38): собственная доска неровных контуров без письма — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F38-TABS31** (P38): веер ровно из 31 вкладки — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F38-TIME** (P38): фактическая табличка приблизительного времени на виток — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F38-PIN** (P38): механический указатель и контрольный штифт — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F39-WINDOW** (P39): малое исследующее окно и направляющая — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F39-PATCHES** (P39): три собственных условных образца поверхности — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F39-PREDICTION** (P39): прозрачная карта точек без текста — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F39-REVIEW** (P39): большая рамка и незамкнутое кольцо проверки — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J40-NICOLARDI** (P40): именная карточка и нейтральная иллюстрация роли — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J40-TRAYS8** (P40): восемь самостоятельных лотков — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J40-RENDS** (P40): условные виды A и B без букв — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J40-REVIEW** (P40): рамки сопоставления и DISCUSSION — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L41-PARIS4** (P41, P42): отдельная обобщённая модель без заявленного масштаба и охристый постамент; отдельный охристый постамент — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L41-CUBE** (P41): прозрачный собственный куб условного сигнала — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L41-PROJECTION** (P41): собственные сетка и схема соответствий без букв — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L41-DIVIDER** (P41): глухая перегородка между объектами — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L41-OPTIONAL-EVIDENCE** (P41): необязательный проверенный asset именно Paris 4 после разрешения; fallback полностью задан собственными L41-CUBE и L41-PROJECTION — OPTIONAL / NOT CLEARED: не входит в базовый монтаж; требуется точный файл и разрешающее основание.
- **L42-TWO-CHAINS** (P42): два независимых набора GEOMETRY, IMAGES, READING — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L42-GAP** (P42): физический промежуток и перегородка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L43-DATES** (P43): собственные карточки 25 JUN и 27 JUN 2026 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L43-COLUMNS22** (P43): развёртка из 22 условных зон без букв — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L43-STUDY-FRAME** (P43): рамка рассмотрения с пазом — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L43-LABELS** (P43): SURVIVING MATERIAL и маркировка схемы — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F44-LOWER-PORTIONS** (P44): собственная схема нижних частей колонок — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F44-APPROX-FRAME** (P44): прерывистая рамка приблизительного прежнего объёма — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **F44-GAPS** (P44): реальные пустые пространства, не белая заливка поверх текста — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J45-READABILITY** (P45): собственная условная карта с вырезами и номерами 1–3 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J45-UNCERTAINTY** (P45): незамкнутая рамка неопределённости — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J45-BLANK** (P45): пустая непрозрачная подложка без текста — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J45-LABEL** (P45): постоянное обозначение схематичности и отсутствия масштаба — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K46-THEMES** (P46): четыре собственных абстрактных мотива этики — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K46-INTERPRETATION** (P46): незамкнутая рамка с подписью — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K46-MENTION** (P46, P47): современная карточка Aristocreon и отдельная связь с Chrysippus; отдельная вкладка упомянутого имени — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K46-PARAPHRASE** (P46): постоянная маркировка иллюстрации — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L47-CATALOGUE** (P47): собственная статусная карточка 1667 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L47-INTERPRETATIONS** (P47): два условных листа и пустая рамка следующего рассмотрения — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J48-STATUS** (P48): собственная карточка статуса на 31 OCT 2026 — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J48-TWO-REVIEWS** (P48): раздельные лотки экспертного чтения и статуса журнальной публикации — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J48-NOT-CONFIRMED** (P48): нейтральная статусная карточка — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **J48-METHODS** (P48): собственные схемы без воспроизведения статьи — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A49-COLLECTION** (P49): собственные обобщённые рулоны и отдельные колыбели — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A49-WORKFLOW** (P49): четыре собственные пиктограммы этапов — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A49-BLANK** (P49): пустая карточка неопределённого результата — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A49-DIGITAL** (P49): отдельная маленькая схема поверхности — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L50-GALLERY** (P50): пять раздельных музейных станций и перегородки — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L50-EARLY** (P50): общий исторический стол копирования без конкретного героя — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L50-CONSERVATION** (P50): поддерживаемая рамка и колыбель — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L50-IMAGING** (P50): собственная миниатюра CT — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L50-COMPUTATION** (P50): отдельная цифровая лента и точки — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L50-PAPYROLOGY** (P50): две рамки рассмотрения — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **L50-RELAY** (P50): общая нижняя рейка зависимостей — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K51-TWO-THEMES** (P51): два самостоятельных тематических окна — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K51-PLEASURE** (P51): нейтральный мотив слуха и волны — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K51-CONDUCT** (P51): анонимные силуэты и условная ладонь — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K51-NAMES** (P51): отдельные поля неопределённых имён — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **K51-READER** (P51): современная рамка рассмотрения — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A52-DIGITAL** (P52, P53): собственная отдельная цифровая поверхность с открытыми вырезами; отдельная поверхность на собственной подставке — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A52-LABELS** (P52): физическая и цифровая зоны различимы — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A53-THREE-CARDS** (P53): три собственные схемы пучка, поверхности и проверки — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **A53-END** (P53): чистый финальный кадр без нового текста — PLANNED ORIGINAL: создать самостоятельно; не импортировать чужую картинку/датасет.
- **REV13_P01_SHUTTER** (P01): Отдельная круглая непрозрачная заслонка должна закрыть весь экран до смены сцены; её видимая и скрытая геометрия подготовлены с запасом. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P02_FRAME** (P02): Две независимые ячейки и подвижная левая рама на направляющей; перекладина движется вместе с рамой и закрывает привязанный к ней текст. Ядро и бирка остаются на отдельной правой опоре. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P07_TRANSITION** (P07): Отдельная широкая непрозрачная плоскость закрывает весь экран после ухода A COPY SURVIVES; она не является листом, повёрнутым ребром. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P12_SCREEN_MASK** (P12): Крупная отдельная непрозрачная рамка полностью покрывает экран с запасом, прежде чем открывается томограф P13. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P14_MASK** (P14): Наружная непрозрачная кромка рамки на отдельном переднем слое скрывает TRACE THE SURFACE; начальное и конечное положение текста и кромки связаны. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P21_VERIFIED** (P21): Пустая графа VERIFIED и её непрозрачная стойка с маской для NOT A VERDICT отдельно от контрольных окон; кадр удерживается до начала P22. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P24_RAIL** (P24): Единая рейка и отдельные карточки OBSERVATION, SCANNED и SEGMENTED; стойка OBSERVATION перекрывает SHARED CLUE. Текст привязан к этой движущейся карточке. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P34_FRAME** (P34): Отдельная регистрационная рамка и её вертикальная стойка перекрывают NO SUBSTITUTE; поля AUTHOR и TITLE не заполняются. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P44_SEPARATE** (P44): Физическое ядро на отдельном ложементе и цифровая схема на отдельной опоре видны одновременно; внешняя рейка является маской A BOUNDARY. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P51_CURTAIN** (P51): Между окнами отдельная непрозрачная центральная кулиса; она скрывает NAMES UNCERTAIN, не прикрывая ни бирки, ни предметы. Каждое окно и каждая из двух боковых кулис на отдельных опорах. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P52_CONTINUITY** (P52): Та же модель 1667, что в P53: повреждения, ориентация, опора и бирка сохраняются; цифровая поверхность остаётся отдельной. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.
- **REV13_P53_CONTINUITY** (P53): Та же модель и те же повреждения, что в P52; зерно движется даже во время смысловой неподвижности. — PLANNED ORIGINAL: изготовить; наличие и права ещё не подтверждены.

- **MASTER_LUKE_SILHOUETTE** (P03, P22, P25, P26): общий условный профиль, пропорции и срезанный угол отдельного основания; фигура и рука на раздельных слоях; не документальный портрет — PLANNED ORIGINAL: создать самостоятельно; наличие и совместимость ещё не подтверждены.
- **MASTER_LUKE_PHONE** (P03, P26): единая условная форма телефона с пустым экраном; отдельные телефон и рука с точками крепления; без восстановленных интерфейсов и факсимиле букв — PLANNED ORIGINAL: создать самостоятельно; наличие и совместимость ещё не подтверждены.
- **P22_COMMUNITY_WINDOW** (P22): отдельное малое окно с безымянной фигурой; появляется после фразы о запуске на словах расширения сообщества, не часть ниш основателей — PLANNED ORIGINAL: создать самостоятельно; наличие и совместимость ещё не подтверждены.

## Реестр акцентов

- P01.B01: **WHAT REMAINS**, маркер «what remains», маска: Ближний бортик ложемента скрывает нижнюю часть букв; буквы поднимаются из-за него. Уход: На последнем слове предложения буквы опускаются обратно за бортик.
- P01.B05: **FRAGILE EVIDENCE**, маркер «evidence may break away», маска: Дуга увеличенного слоя скрывает буквы; они выходят из-за её нижнего края. Уход: После читаемой остановки акцент остаётся на своей опоре; круглая непрозрачная заслонка закрывает разрез и буквы, затем весь кадр до склейки на P02.
- P02.B03: **PRESERVED FRAGMENTS**, маркер «Some fragments», маска: Верхняя непрозрачная перекладина левой рамы скрывает буквы; они поднимаются позади неё. Уход: После читаемой остановки опускаются за ту же перекладину в продолжающемся плане B04 до входа INNER CORE.
- P02.B04: **INNER CORE**, маркер «tight inner core», маска: Нижняя кромка инвентарной бирки скрывает буквы; они поднимаются за ней. Уход: После читаемой остановки опустить за ту же кромку до следующей склейки.
- P03.B01: **READ WITHOUT OPENING**, маркер «without pulling», маска: Передняя стенка ячейки PHYSICAL ORIGINAL скрывает буквы; они поднимаются наружу с отдельной задней направляющей. Уход: Буквы уходят за первую перегородку при начале следующего проезда.
- P03.B04: **HUMAN JUDGEMENT**, маркер «people who can tell», маска: Ближняя рамка сравнения скрывает буквы, которые выдвигаются из-за её правого ребра. Уход: Все буквы закрывает вертикальная боковая стенка театра, проходящая перед объективом.
- P04.B02: **HERCULANEUM**, маркер «Herculaneum», маска: Передняя гряда берега скрывает буквы; они поднимаются за грядой в небо слева от вулкана. Уход: Пепельная передняя плоскость проходит перед буквами и закрывает их.
- P04.B04: **CARBONIZED**, маркер «carbonized objects», маска: Передняя стенка подноса скрывает буквы; они появляются за её правым краем. Уход: Буквы и поднос закрываются охристой горизонтальной плоскостью осадка.
- P05.B01: **COLUMNS**, маркер «columns», маска: Правая вертикальная скрутка полосы скрывает буквы; они выходят из-за её внешнего края. Уход: Буквы скользят обратно за вертикальную скрутку.
- P05.B03: **FRAGILE SURFACE**, маркер «dangerous», маска: Ближний тёмный бортик правой ячейки скрывает буквы до своего опускания. Уход: Буквы закрывает возвращающийся бортик в конце абзаца.
- P06.B02: **A LIBRARY**, маркер «a library», маска: Верхняя каменная перемычка тоннеля скрывает буквы; они опускаются из-за неё. Уход: Буквы закрывает затемняющая передняя стенка галереи перед следующей склейкой.
- P06.B03: **STILL CLOSED**, маркер «possession did not provide access», маска: Передний борт лотка закрывает буквы; они поднимаются сзади него. Уход: Буквы опускаются за борт, оставляя пустую рамку.
- P07.B01: **EXPOSE THE NEXT**, маркер «expose the next», маска: Передний край условного слоя закрывает буквы; они выходят за его правый торец. Уход: Буквы опускаются за переднюю кромку подставки до следующей склейки.
- P07.B03: **A COPY SURVIVES**, маркер «rescued in a drawing», маска: Поднимаемый лист скрывает буквы за своим нижним краем; буквы становятся видны, когда лист занимает подставку. Уход: Буквы прячутся за нижний край листа. Затем отдельная широкая непрозрачная плоскость проходит перед объективом и полностью закрывает кадр.
- P08.B01: **CONTROLLED TENSION**, маркер «more controlled», маска: Ближняя вертикальная стойка механизма скрывает буквы; они выходят за её правый край. Уход: Буквы возвращаются за стойку на следующей фразе.
- P08.B04: **ABOUT MUSIC**, маркер «about music», маска: Край полки и задняя карточка 1754 образуют реальную маску; буквы поднимаются из-за полки. Уход: Буквы опускаются за полку перед расширением кадра.
- P09.B01: **ANCIENT TEXTS**, маркер «real ancient texts», маска: Верхняя перекладина левой рамки скрывает буквы; они поднимаются над ней. Уход: Буквы закрывает следующая стойка по ходу проезда.
- P09.B02: **ALTERED OBJECTS**, маркер «damaged rolls», маска: Передний край центральной подложки скрывает буквы; они выходят вперёд и вверх из-за него. Уход: Буквы опускаются за подложку при переходе к двум линиям.
- P10.B02: **OPENING ATTEMPTS**, маркер «opening attempt», маска: Первая вертикальная заслонка скрывает буквы; они выдвигаются из-за её бокового края. Уход: Буквы закрывает вторая заслонка по ходу проезда.
- P10.B05: **PRESERVED PIECES**, маркер «Ten separated pieces», маска: Верхняя кромка выдвигаемой рамы скрывает буквы; они поднимаются из-за неё после остановки. Уход: Буквы опускаются за раму на следующей короткой фразе.
- P11.B02: **ALREADY REDUCED**, маркер «already recorded», маска: Передняя заслонка карточки 1782 скрывает буквы; они выходят из-за её верхнего края. Уход: Буквы опускаются за карточку после следующей фразы.
- P11.B05: **WHAT REMAINS**, маркер «material that remains», маска: Ближний край измерительного планшета скрывает буквы; они поднимаются за ним. Уход: Буквы уходят за переднюю планку; та заполняет нижнюю половину кадра и задаёт переход.
- P12.B01: **ANOTHER ROUTE**, маркер «another route», маска: Левая вертикальная стойка монитора скрывает буквы; они выходят за её внешнее ребро. Уход: Буквы опускаются за верхнюю рамку монитора на следующей фразе.
- P12.B04: **DIGITAL COPY**, маркер «copy was opened», маска: Нижняя отдельная непрозрачная передняя кромка рамки монитора скрывает буквы; они поднимаются позади кромки, оставаясь вне изображения сетки. Уход: Буквы опускаются позади той же передней кромки; затем отдельная непрозрачная рамка полностью перекрывает кадр для перехода.
- P13.B02: **3D VOLUME**, маркер «three-dimensional volume», маска: Ближняя стойка детектора скрывает буквы; они выходят из-за её наружного края. Уход: Буквы уходят за заднюю стенку объёма при переходе к сечениям.
- P13.B03: **VIRTUAL SLICES**, маркер «virtual slices», маска: Верхняя грань объёма данных скрывает буквы; они поднимаются над ней. Уход: Буквы скрывает продвигающаяся непрозрачная рамка плоскости сечения.
- P14.B01: **MEASURED DATA**, маркер «only a measurement», маска: Левая непрозрачная рамка объёма скрывает буквы; они выходят из-за её внутреннего ребра. Уход: Буквы закрываются рамкой при следующем боковом движении.
- P14.B03: **TRACE THE SURFACE**, маркер «follow it through the volume», маска: Наружная непрозрачная кромка рамки скрывает буквы; они выдвигаются из-за неё. Уход: После читаемой остановки скрыть за той же кромкой в начале продолжающего смысл плана B04, до входа ONE SURFACE.
- P14.B04: **ONE SURFACE**, маркер «same piece of papyrus», маска: Правая карточка ONE SURFACE скрывает буквы за нижним краем; они выдвигаются вверх из-за неё. Уход: Карточка закрывает буквы своим поворотом на 90° и становится маской перехода.
- P15.B02: **NEIGHBOURING LAYERS**, маркер «Neighbouring layers», маска: Центральная перегородка скрывает буквы; они появляются из-за её правого края после открытия схемы. Уход: Буквы закрываются нижним бортиком учебного стола перед показом ошибки.
- P15.B03: **WRONG ROUTE**, маркер «wrong route», маска: Ближняя дуга папируса скрывает буквы; они выходят за её нижний край. Уход: Буквы остаются на продолжении действия и исчезают за входящей рамкой выходной карточки.
- P16.B01: **DIGITAL GEOMETRY**, маркер «digital geometry», маска: Передняя направляющая сетки скрывает буквы; они поднимаются за ней. Уход: Буквы уходят за направляющую перед расширением кадра.
- P16.B05: **FIND THE INK**, маркер «finding the ink», маска: Передняя кромка второй карточки скрывает буквы; они поднимаются над ней. Уход: Буквы опускаются за карточку; карточка поднимается до заполнения кадра.
- P17.B02: **CARBON ON CARBON**, маркер «So is the papyrus», маска: Передний край нижней подложки скрывает буквы; они поднимаются из-за него. Уход: После читаемой остановки буквы опускаются за передний край своей подложки в продолжающемся плане.
- P17.B04: **AMBIGUOUS SIGNALS**, маркер «ambiguous texture», маска: Правая стойка условного дисплея скрывает буквы; они выдвигаются за её внешнее ребро. Уход: Стойка дисплея проходит перед буквами и закрывает кадр для перехода.
- P18.B02: **EN-GEDI**, маркер «En-Gedi», маска: Сине-серая передняя стойка ячейки скрывает буквы; они выходят за её правый край. Уход: Буквы уходят за стойку перед открытием учебного материала.
- P18.B03: **STRONGER CONTRAST**, маркер «stood out more clearly», маска: Нижняя кромка карточки материала скрывает буквы; они поднимаются из-за неё. Уход: Буквы опускаются за карточку до перехода к правой ячейке.
- P19.B01: **EARLIER CLAIMS**, маркер «earlier claims», маска: Буквы выходят справа из-за вертикального разделителя шкафа. Уход: Уходят обратно за разделитель до появления карточки 2019.
- P19.B04: **NOT YET CONFIRMED**, маркер «not yet been confirmed», маска: Оранжевая подложка поднимается из-за нижнего борта лотка 2019. Уход: Опускается за борт перед финальным планом.
- P20.B02: **VISIBLE INK**, маркер «photograph the ink», маска: Буквы выдвигаются из-за верхней планки держателя PHOTO. Уход: Буквы уходят за ту же планку после совмещения.
- P20.B03: **LINKED VIEWS**, маркер «linking visible writing», маска: Акцент раскрывается из-за стойки регистрационной линейки, как короткая боковая вкладка. Уход: Вкладка задвигается за линейку к следующему предложению.
- P21.B01: **INK?**, маркер «where ink might be present», маска: Буква и знак вопроса появляются из-за переднего борта лотка. Уход: Карточка акцента опускается за борт перед проверкой.
- P21.B03: **CHECK THE EVIDENCE**, маркер «checking against the scan», маска: Акцент выходит из-за левой вертикальной стойки окна SURFACE. Уход: Уходит за правую стойку при завершении проезда.
- P21.B05: **NOT A VERDICT**, маркер «not a verdict», маска: Непрозрачная стойка пустой графы VERIFIED скрывает буквы; они выходят из-за её внешнего края. Уход: После читаемой остановки в начале P22.B01 буквы уходят обратно за стойку; графа VERIFIED остаётся незаполненной.
- P22.B02: **WIDER COMMUNITY**, маркер «a wider community», маска: Буквы разворачиваются из-за торца общей доски слева. Уход: Закрываются назад за торец, когда вид переходит к ролям.
- P22.B04: **MANY WAYS IN**, маркер «a better way to detect ink», маска: Акцент появляется из-за нижней опоры третьей панели. Уход: Уходит за опору вместе с закрывающейся крышкой панели.
- P23.B01: **PARIS FOUR**, маркер «Paris Four», маска: Акцент поднимается из-за нижнего охристого борта ячейки. Уход: Складывается за борт, когда открывается вторая ячейка.
- P23.B04: **THAT PARTICULAR ROLL**, маркер «that particular roll», маска: Буквы выходят из-за центрального разделителя влево. Уход: Уходят обратно за разделитель перед переходом в рабочую область Paris4.
- P24.B01: **CRACKED TEXTURE**, маркер «a distinctive cracked texture», маска: Акцент выдвигается из-за правой толстой грани увеличительной рамки. Уход: Убирается под грань рамки до следующего крупного плана.
- P24.B03: **SHARED CLUE**, маркер «shared the observation», маска: Передняя непрозрачная стойка карточки OBSERVATION скрывает буквы; они выходят позади её края. Уход: После читаемой остановки буквы уходят за ту же стойку в продолжающемся плане B04; не перекрывать SCANNED и SEGMENTED.
- P25.B02: **FIND THE PATTERN**, маркер «seek the pattern elsewhere», маска: Акцент выходит из-за бортика между EXAMPLES и NEW SECTION. Уход: Опускается за разделительный бортик перед заменой результата.
- P25.B04: **TEST AGAIN**, маркер «test whether the clue held up», маска: Буквы появляются из-за правой боковой стенки подающего лотка. Уход: Задвигаются за стенку; лоток остаётся пустым до следующего эпизода.
- P26.B02: **REMOTE RUN**, маркер «a remote run», маска: Буквы выдвигаются из-за правого торца объёмного телефона. Уход: Скрываются за его торцом перед монтажной сменой места.
- P26.B04: **MORE LETTERS**, маркер «more recognizable letters», маска: Буквы поднимаются из-за нижнего края корпуса телефона. Уход: Возвращаются за корпус до последнего предложения.
- P27.B01: **PURPLE**, маркер «purple», маска: Акцент выходит слева из-за нижнего бортика держателя. Уход: Уходит под бортик перед календарным планом.
- P27.B04: **READABLE WRITING**, маркер «readable writing», маска: Акцент выдвигается из-за рамки цифрового контрольного окна. Уход: Скрывается за рамкой, которая остаётся открытой для сравнения в P28.
- P28.B01: **SAME REGION**, маркер «the same region», маска: Акцент выходит из-за переднего бортика сравнительного лотка. Уход: Уходит вниз за бортик до смены угла.
- P28.B03: **COMPARE METHODS**, маркер «Different methods», маска: Буквы выезжают из-за правой стойки переднего держателя. Уход: Карточка акцента скрывается за стойкой при переходе к последнему плану.
- P29.B02: **MORE SURFACE**, маркер «larger digital regions», маска: Акцент поднимается из-за нижней кромки большого цифрового окна. Уход: Уходит за кромку к началу следующей фразы.
- P29.B03: **COMBINED WORK**, маркер «combined their work», маска: Буквы выходят из-за переднего борта общей рейки. Уход: Уходят под направляющую после стыковки.
- P30.B02: **REPRODUCE**, маркер «reproduced methods», маска: Акцент выдвигается из-за передней стенки лотка CODE RE-RUN. Уход: После полной читаемой остановки опустить за стенку CODE RE-RUN; лишь затем перейти на макроплан.
- P30.B04: **NO FILLING GAPS**, маркер «without filling the gaps», маска: Буквы поднимаются из-за нижнего внешнего борта контрольной рамки. Уход: Складываются за борт, оставляя пустой промежуток видимым.
- P31.B01: **WINNERS**, маркер «the winners», маска: Акцент выходит из-за левой боковины календарного окна. Уход: Скрывается за боковиной к переходу на сумму.
- P31.B02: **SHARED AWARD**, маркер «shared the seven-hundred-thousand-dollar award», маска: Буквы поднимаются из-за переднего борта общей плашки. Уход: Уходят под борт перед возвращением к проверке.
- P32.B01: **ABOUT FIVE PERCENT**, маркер «about five percent», маска: Акцент выдвигается из-за нижнего охристого борта лотка. Уход: Уходит за борт до смены изображения.
- P32.B03: **ANCIENT ARGUMENT**, маркер «an ancient argument», маска: Буквы появляются из-за правой толстой стойки цифрового окна. Уход: Скрываются за стойкой, пока карточка ARGUMENT поворачивается к следующей сцене.
- P33.B01: **PLEASURE**, маркер «pleasure», маска: Акцент появляется из-за левой боковой кулисы. Уход: Уходит за кулису до сравнения количества.
- P33.B03: **NOT AUTOMATICALLY**, маркер «automatically provide greater pleasure», маска: Буквы выезжают из-за правой кулисы. Уход: Уходят за кулису перед возвращением к повреждённой поверхности.
- P34.B01: **AUTHOR UNKNOWN**, маркер «no secure author», маска: Акцент поднимается из-за нижнего борта карточного ящика. Уход: Уходит вниз перед планом содержания.
- P34.B03: **NO SUBSTITUTE**, маркер «cannot substitute», маска: Наружная вертикальная стойка регистрационной рамки скрывает буквы; они выходят из-за неё. Уход: После читаемой остановки скрыть буквы за той же стойкой в продолжающемся B04; поле остаётся пустым до перехода.
- P35.B01: **SCALE**, маркер «scale», маска: Акцент выдвигается из-за левого переднего обреза макета. Уход: Уходит за обрез при открытии окон дефектов.
- P35.B03: **BROKEN PATH**, маркер «interrupt the path», маска: Буквы поднимаются из-за переднего борта центрального окна разрыва. Уход: Опускаются за борт к финальному предложению.
- P36.B01: **SIXTEEN SIXTY-SEVEN**, маркер «sixteen sixty-seven», маска: Акцент поднимается из-за передней кромки консервационного стола. Уход: Уходит за кромку перед вопросом о поверхности.
- P36.B03: **KEEP THE GAPS**, маркер «leaving the real losses and damage visible», маска: Акцент появляется из-за внешней стойки бокового светового окна. Уход: Уходит за стойку; прорези сохраняются видимыми до закрытия створки.
- P37.B02: **GRENOBLE**, маркер «Grenoble», маска: Буквы на оранжевой подложке поднимаются из-за непрозрачного правого края детектора. Уход: Планка скользит обратно за детектор при переходе к отдельному плану объёма.
- P37.B03: **MORE DETAIL**, маркер «a more detailed volume», маска: Нижний непрозрачный бортик постамента находится перед буквами по глубине; буквы поднимаются из-за бортика в свободное поле справа от куба. Уход: Уходит за нижний бортик постамента на последнем слове предложения.
- P38.B01: **PATIENT WORK**, маркер «patient work», маска: Планка выходит из-за нижнего неподвижного зажима и ложится параллельно краю доски. Уход: Зажим остаётся маской, за которую планка возвращается при открытии веера.
- P38.B02: **THIRTY-ONE WINDINGS**, маркер «thirty-one windings», маска: Акцент поднимается из-за непрозрачной крайней вкладки веера; её край действительно перекрывает буквы. Уход: Планка складывается за крайнюю вкладку перед переходом к крупному месту проверки.
- P39.B01: **LOCAL SIGNALS**, маркер «local physical signals», маска: Планка вытягивается вправо из-за непрозрачной ручки окна. Уход: Возвращается под ручку, когда окно останавливается.
- P39.B04: **NEEDS EXAMINATION**, маркер «needs to be examined», маска: Буквы выходят из-за нижней перекладины большой рамки. Уход: На переходе большая рамка опускается перед планкой и закрывает её.
- P40.B02: **EIGHT SPECIALISTS**, маркер «Eight specialists», маска: Буквы поднимаются из-за дальней стенки восьмого лотка. Уход: Планка опускается за ту же стенку при переходе к результатам сопоставления.
- P40.B04: **PEOPLE READ**, маркер «people remained responsible», маска: Акцент выходит из-за передней кромки рабочего лотка фигуры. Уход: Кромка нового предметного постамента перекрывает планку на переходе.
- P41.B01: **PARIS FOUR**, маркер «Paris Four», маска: Акцент появляется из-за охристой заслонки, одновременно с открытием постамента. Уход: После полной читаемой остановки вернуть буквы за ту же охристую заслонку; после этого перейти на куб.
- P41.B05: **PHYSICAL EVIDENCE**, маркер «physical evidence», маска: Акцент выдвигается из-за нижней перекладины рамки сравнения. Уход: Уходит за перекладину во время дальнейшего отъезда к двум постаментам.
- P42.B01: **THIS ROLL**, маркер «Paris Four», маска: Акцент выходит из-за передней охристой заслонки. Уход: Возвращается за охристую заслонку до смещения внимания к 1667.
- P42.B03: **EACH OBJECT**, маркер «Each object», маска: Буквы выходят из-за передней ржаво-оранжевой заслонки 1667. Уход: Планка уходит вниз за заслонку перед финальным общим взглядом.
- P43.B02: **SURVIVING CORE**, маркер «surviving core», маска: Акцент поднимается из-за передней рейки постамента 1667. Уход: Уходит обратно за рейку при появлении второй даты.
- P43.B04: **TWENTY-TWO COLUMNS**, маркер «twenty-two columns», маска: Акцент появляется из-за поднятой верхней планки, затем останавливается над ней. Уход: Планка акцента прячется за верхнюю рейку до перехода к локальному рассмотрению.
- P44.B01: **A BOUNDARY**, маркер «a boundary», маска: Акцент выходит из-за левой стойки внешней рамки. Уход: После читаемой остановки скрыть акцент за той же стойкой в продолжающемся плане B02.
- P44.B04: **WHAT SURVIVES**, маркер «what survives», маска: Буквы поднимаются из-за нижней несущей рейки цифровой поверхности. Уход: Уходят за рейку, когда передний край рамки приближается к камере на переходе.
- P45.B02: **NO TRANSCRIPTION**, маркер «without transcription», маска: Планка выходит из-за верхней стенки лотка трёх колонок. Уход: Опускается за стенку на переходе внимания к остальным зонам.
- P45.B05: **RECOVERY AND INVENTION**, маркер «recovery and invention», маска: Буквы появляются из-за ближнего бортика стола, когда пустая подложка уже убрана. Уход: Возвращаются за бортик в конце паузы, прежде чем карта покинет сцену.
- P46.B01: **ETHICS**, маркер «ethics», маска: Буквы выходят из-за левой кулисы и останавливаются на собственном небольшом основании. Уход: Уходят обратно за кулису после последовательного выделения мотивов.
- P46.B03: **STOIC CONTEXT**, маркер «Stoic context», маска: Акцент появляется из-за верхней перекладины рамки интерпретации. Уход: Прячется за перекладину перед открытием карточки упоминания.
- P47.B02: **UNKNOWN**, маркер «unknown», маска: Акцент выходит из-за правой створки поля TITLE. Уход: Уходит за створку, когда внимание смещается к листам обсуждения.
- P47.B03: **OPEN TO DEBATE**, маркер «compare interpretations, and disagree», маска: Планка выдвигается из-за бокового края правого листа. Уход: Возвращается за лист на последней фразе абзаца.
- P48.B01: **PREPRINT**, маркер «preprint», маска: Акцент выходит из-за левой непрозрачной стойки даты. Уход: Скрывается за стойкой перед выделением журнального статуса.
- P48.B04: **FURTHER SCRUTINY**, маркер «further scrutiny», маска: Акцент появляется из-за дальнего бортика лотка схем. Уход: После читаемой остановки опустить буквы за дальний бортик; затем бортик заполняет кадр для перехода в начале P49.B01.
- P49.B02: **HARD PARTS**, маркер «hard parts», маска: Акцент выходит из-за передней кромки полки с карточками операций. Уход: Уходит под кромку полки перед взглядом на отдельные сложные модели.
- P49.B05: **PRESERVE THE OBJECT**, маркер «preserving the fragile object», маска: Буквы выходят из-за переднего основания колыбели, не касаясь самой модели. Уход: Опускаются обратно за основание перед переходом.
- P50.B01: **GENERATIONS**, маркер «Generations», маска: Акцент поднимается из-за первой музейной перегородки. Уход: Остаётся у входа и естественно скрывается за следующей перегородкой при движении камеры.
- P50.B07: **MADE POSSIBLE**, маркер «made the next one possible», маска: Акцент выходит из-за последней вертикальной перегородки и останавливается перед её тенью. Уход: При переходе перегородка закрывает планку целиком.
- P51.B02: **PLEASURE**, маркер «pleasure», маска: Акцент выходит из-за левой кулисы окна PARIS 4. Уход: После читаемой остановки убрать за левую кулису; возможное пересечение по времени с правым акцентом допускается только при полной раздельности и читаемости.
- P51.B03: **HUMAN CONDUCT**, маркер «human conduct», маска: Акцент выходит из-за правой кулисы окна PHerc. 1667. Уход: После читаемой остановки убрать за правую кулису до входа NAMES UNCERTAIN.
- P51.B04: **NAMES UNCERTAIN**, маркер «names are uncertain», маска: Общая отдельная непрозрачная центральная кулиса скрывает буквы; они выходят из-за её верхнего края. Уход: После читаемой остановки опустить за ту же кулису, при необходимости в начале B05, затем переход к широкому виду.
- P52.B03: **STILL LOST**, маркер «still lost», маска: Передняя непрозрачная стенка колыбели скрывает буквы; они выходят позади её нижнего края. Уход: После читаемой остановки в продолжающемся B04 опустить буквы за ту же стенку; до входа WHAT WE KNOW.
- P52.B05: **WHAT WE KNOW**, маркер «what we can know», маска: Акцент появляется из-за левого ребра отдельного основания цифровой поверхности. Уход: Скрывается за основанием перед переходом к финальному общему плану.
- P53.B01: **A DIFFERENT TOUCH**, маркер «a different kind of touch», маска: Буквы поднимаются из-за низкого заднего бортика стола, впереди трёх закрытых карточек. Уход: Акцент опускается за бортик перед перечислением трёх операций.
- P53.B03: **STAYED CLOSED**, маркер «stayed closed», маска: Акцент выходит из-за передней стенки колыбели. Уход: После читаемой остановки в том же плане B04 опустить буквы за переднюю стенку колыбели; затем оставить ядро и бирку до конца финальной выдержки.

## Реестр запланированных звуковых жестов

Эти позиции являются замыслом и не подтверждают создание звука.

- P04.B02 · оценочно 00:57.8–01:03.0: На появлении первого пепельного слоя — один тихий дальний низкий гул, плавно затихающий к концу следующей фразы.
- P06.B03 · оценочно 01:42.7–01:47.4: В момент остановки лотка — один тихий деревянный стук направляющей.
- P07.B02 · оценочно 01:55.9–02:04.5: На движении скребка — один очень тихий сухой скребущий звук, без повторов.
- P08.B01 · оценочно 02:11.7–02:16.4: В момент натяжения нитей — один тихий короткий звук натянутой нити, без скрипа механизма.
- P10.B05 · оценочно 03:04.2–03:07.7: При достижении рамой упора — один мягкий стук дерева.
- P13.B02 · оценочно 03:49.4–03:54.1: С началом поворота опоры — один тихий ровный механический гул, плавно затихающий после остановки.
- P18.B02 · оценочно 05:26.1–05:33.0: Когда карточка 2016 достигает паза — один тихий бумажно-деревянный контакт.
- P19.B02 · оценочно 05:44.5–05:49.6: Один тихий деревянный контакт на момент остановки карточки в направляющей.
- P22.B02 · оценочно 06:44.6–06:49.4: Один мягкий щелчок фиксатора на остановке центрального пакета данных.
- P26.B02 · оценочно 08:04.9–08:08.8: Один очень тихий короткий электронный щелчок, синхронный видимому касанию пустого экрана; звук пока не создан.
- P29.B03 · оценочно 09:07.5–09:12.2: Один тихий деревянный щелчок на стыковке центрального фиксатора общей рейки.
- P30.B02 · оценочно 09:21.5–09:25.8: Один мягкий контакт бумажной карты с упором лотка на завершении повторного вывода.
- P31.B02 · оценочно 09:44.2–09:47.6: Один тихий глухой контакт при остановке наградной плашки на держателе.
- P35.B03 · оценочно 10:59.5–11:04.2: Один тихий сухой щелчок на остановке центрального указателя перед разрывом.
- P37.B02 · оценочно 11:30.4–11:35.6: На начале видимого вращения — один тихий ровный звук мотора; затихает вместе с остановкой диска в конце beat.
- P38.B03 · оценочно 11:58.2–12:01.2: Один тихий контакт штифта с пазом точно в момент его фиксации.
- P40.B03 · оценочно 12:33.6–12:37.0: Один негромкий контакт связующей рамки с пазом при её остановке.
- P43.B05 · оценочно 13:39.0–13:42.4: Один тихий контакт рамки рассмотрения с её пазом.
- P50.B07 · оценочно 15:50.0–15:53.0: Один мягкий контакт последнего соединителя с пазом в конце видимого движения.

## Права и пределы исследования — исходные сведения Pro для дополнительной проверки

Предположение: публичный англоязычный YouTube-фильм, допускающий монетизацию, обложку и промо. Ниже сохранены предварительные сведения Pro об опубликованных условиях и подписях; каждый фактический файл и способ использования проверяются отдельно до импорта. Индивидуальные разрешения не запрашивались; авторство будущих заказных иллюстраций, музыки и фоли оформляется при их производстве.

| Материал | Что подтверждено | Решение |
|---|---|---|
| Собственные бумажные декорации и объясняющие схемы | План не требует копирования чужого изображения или переработки чужого массива КТ | Базовый вариант всех сцен. Это новые иллюстрации по фактам, не обводка научных figures |
| Новые данные / изображения PHerc. 1667 | Карточка S23 выделяет CC BY-NC 4.0 для данных, кроме старых DLS-серий | Не включать автоматически в коммерческий мастер; для точного файла нужно разрешающее основание. Базовый собственный рисунок уже предусмотрен |
| Старые DLS-данные 3.24 / 7.91 µm | В S23 указана отдельная EduceLab Data License; S24 содержит ограничения на перераспространение | Не делать из них рендер для выпуска по предположению об общей CC-лицензии |
| Figures препринта 2026 | S21 связан с arXiv non-exclusive distribution license, S25 | Эта лицензия разрешает распространение arXiv; она не заменяет разрешение на использование figure в фильме |
| Фото и B-roll UK media kit | S26 содержит разные кредиты, в том числе сторонних фотографов/организаций | Выбрать точный файл, проверить его предмет и условия. Надпись «media kit» не очищает весь набор. В основном монтаже файлов из набора нет |
| PLOS 2019, Figure 5 A–C | S08 / S27: CC BY 4.0; объект Paris 2 Fragment 96 | Допустимый кандидат на дополнительное объяснение метода после инспекции загруженной версии. Подпись и лицензия обязательны; D нельзя выдать за фотографию |
| Met 53.514.8, 1746 | S29 помечен Public Domain | Необязательный архивный контекст, не доказательство сцены открытия свитков или машины Piaggio |
| Source Sans 3 | S30: SIL Open Font License 1.1 | Не является эталоном фирменных акцентов. Если используется отдельно для служебного паспорта, проверить условия и сохранить лицензию при передаче |
| Современные переводы и транскрипции | Древний текст, современная редакция, перевод, фотография и рендер — разные материалы | VO пересказывает аргументы. Длинные современные переводы не копируются; единственное греческое слово набрано с маркировкой транскрипции |
| Музыка, голос, фоли | Готовые записи не предоставлены и права на них ещё не приобретены | Произвести по партитуре либо лицензировать точную запись с нужными территориями/платформами; сохранить документы. Не брать звук из чужого YouTube-ролика |

Для необязательной PLOS-вставки рекомендуемая кредитная строка:  
**Parker et al. (2019), PLOS ONE, Figure 5 A–C. PHerc. Paris 2, Fragment 96. CC BY 4.0. Cropped and annotated.**  
Указывать *Cropped and annotated* только если именно эти изменения действительно сделаны; DOI и лицензию разместить в описании. Панели и соответствующие подписи сверить перед импортом.

**Выбранное решение:** базовая версия фильма содержит только самостоятельные бумажные сцены и редакционные фактические карточки. Опциональные подлинные изображения не являются незавершёнными местами сценария: для каждой такой позиции уже существует полный основной вариант. Монтажер не заменяет их самостоятельно картинкой из поиска.

## 9. Неопределённости, спорные места и исключённые сенсации

| Вопрос | Что можно сказать | Чего доказательства не дают |
|---|---|---|
| Как именно открывали 1667 в XIX веке? | Рукопись фиксирует неудачную попытку | Точный год, исполнитель, химический рецепт, конкретное движение инструмента |
| Когда утрачена верхняя часть? | Высота около 8 см уже описана в записи 1782 года, согласно Nicolardi | Нельзя приписывать утрату верха целиком Fackelmann или опыту 1987 |
| Все ли отделённые части уничтожены? | Некоторые фрагменты сохранились отдельно; каталог говорит о десяти частях в раме | Неверна формула «всё, к чему прикоснулись, исчезло» |
| Что значит complete? | Прослежена сохранившаяся поверхность по критериям авторов работы 2026 | Это не весь исходный свиток и не уверенное чтение каждой буквы |
| Сколько колонок? | Рукопись: 22 колонки или их эквивалента; пресс-релизы иногда округляют | Нельзя превращать число в 22 полностью сохранившиеся страницы |
| Кто написал 1667? | Автор/заглавие неизвестны; вероятен стоический контекст | Упоминание Aristocreon не устанавливает Chrysippus автором |
| Кто написал Paris 4? | Автор и заглавие не установлены в проверенных текущих источниках | Преобладание Philodemus в коллекции не атрибуция конкретного объекта |
| Были ли чтения до 2023? | Да: физические чтения, En-Gedi и более ранние заявления о геркуланумских буквах | Vesuvius Challenge не начало всей папирологии и не первое чтение любого древнего свитка |
| Что с заявлениями 2015? | Они опубликованы; авторы работы 2019 описали недостаток подтверждения/расширения | Нет основания обвинять авторов в выдумке или объявлять каждую предложенную букву ложной |
| Проверка Paris 4 в 2026 | Более прямой физический сигнал согласуется с прежним чтением этого предмета | Она не удостоверяет каждую букву 1667 и не является внешней репликацией всей программы |
| Препринт или статья? | На 31 октября 2026 подтверждены препринт v1 и отсутствие найденной журнальной публикации; октябрьское интервью тоже называет работу препринтом | Неизвестны возможные закрытые процедуры рецензирования. DOI arXiv не журнальное принятие |
| Возможно ли всё прочитать? | Есть метод и материал для дальнейших исследований | Утраченная физическая информация не восстановится от более уверенного текста модели |

Дополнительные числа оставлены в справке, а не перегружают VO: около 860 см² сохранившейся поверхности письма и около 1231 см² геометрически развёрнутой поверхности в рукописи относятся к разным величинам. Нельзя заменять одно другим. Из диаметра или массы остатка нельзя вычислять процент потерянного текста. Площадь первых нетранскрибированных областей — не процент полной древней книги.

Фраза *journal publication has not been confirmed* — сознательная граница знания. Её, актуальный статус Paris 4 и новые чтения 1667 нужно перепроверить в S18/S21 непосредственно перед публикацией. Остальной фильм не привязан к выдуманному сроку, обещанию открыть всю библиотеку или гипотезе о «секретном учении».

## Утверждения и ограничения

- **C01 (P01–P03):** Перед нами сохранившаяся небольшая обугленная сердцевина 1667; новый способ чтения должен сохранить её физически. Граница: Не вся первоначальная книга; в руке её не показываем и намеренно не разрушаем. Источники: S01, S02, S03.
- **C02 (P04):** Извержение 79 года погребло Геркуланум; папирусы виллы карбонизировались. Граница: Не назначены точная температура, день извержения, место каждого свитка или владелец виллы. Лава не заливает библиотеку. Источники: S05, S06.
- **C03 (P05):** Свитки состоят из папирусных листов, письмо расположено колонками; физическое разворачивание обугленного материала опасно. Граница: Механика показана на условной свежей модели, без вымышленного античного читателя с известной биографией. Источники: S05, S06.
- **C04 (P06):** В XVIII веке нашли папирусы виллы. Граница: VO намеренно не объединяет несколько сезонов раскопок в один выдуманный день открытия. Источники: S05, S06.
- **C05 (P07):** Paderni разрезал рулоны продольно; раскрытое письмо копировалось, а материал снимался для доступа к следующему слою. Граница: Источники не устанавливают, что Падерни лично выполнял каждое копирование и соскабливание; не доказано применение к 1667. Реконструкция условная. Источники: S05.
- **C06 (P08):** Piaggio прибыл в Неаполь в 1753; PHerc.1497 с трудом о музыке был успешно открыт в 1754. Граница: Название/автор относятся к PHerc.1497, не Paris 4 и не 1667. Подлинная конструкция машины не воспроизведена по полному чертежу. Источники: S06, S05.
- **C07 (P09):** Ранее физически открытые свитки уже давали читаемые тексты. Граница: Нельзя говорить, что до 2023 не прочитали ни слова из всей коллекции. Источники: S05, S06.
- **C08 (P10):** У 1667 был неудачный опыт физического открытия в XIX веке. Граница: Точная дата, исполнитель и инструменты этой попытки не установлены просмотренными источниками. Источники: S01.
- **C09 (P10):** Fackelmann работал с 1667 в 1969; новый опыт 1987 связан с Oslo method, Caprino и Fosse; десять частей в раме. Граница: Не утверждать полного физического раскрытия сохранившейся сердцевины или уничтожения всех отделённых фрагментов. Источники: S03, S01.
- **C10 (P11):** Нынешний остаток около 8 × 2 см; высота около 8 см записана ещё в 1782. Граница: Запись 1782 пересказана через Nicolardi, не непосредственно прочитана нами. Нельзя показывать утрату верхней половины как доказанное событие 1969/1987. Источники: S02, S01.
- **C11 (P12–P13):** КТ измеряет объект под разными углами и позволяет реконструировать трёхмерный объём. Граница: Луч рисуется как схема; КТ не выдаёт сразу готовый перевод или обычную фотографию страницы. Источники: S07, S08, S09.
- **C12 (P14–P15):** Сегментация прослеживает одну поверхность в объёме; перескок между слоями искажает взаимное положение знаков. Граница: Раздавленный город — помеченная метафора, не археологическая карта виллы. Источники: S09, S01.
- **C13 (P16):** Плоской становится цифровая геометрия; физический оригинал остаётся свёрнутым. Граница: Оригинал и цифровая копия имеют разные материалы/цвета, отдельные подписи и опоры. Источники: S07, S08, S09.
- **C14 (P17):** Углеродные чернила на карбонизированном папирусе часто дают слабый контраст. Граница: Не утверждать одинаковый состав всех чернил или абсолютную невозможность прямой видимости; Paris 4 позже даёт контрпример. Источники: S08, S09.
- **C15 (P18):** Работа 2016 об En-Gedi — предшествующий успех виртуального чтения, на животной коже и с более заметным сигналом. Граница: Не называть En-Gedi геркуланумским папирусом, не назначать точный элемент чернил без анализа. Источники: S07.
- **C16 (P19):** Mocella et al. заявили о буквах в 2015; Parker/Seales et al. в 2019 критически оценили неподтверждённость расширенного чтения. Граница: Это атрибутированный спор, а не решение о недобросовестности исследователей. Источники: S10, S08.
- **C17 (P20):** Пары фотографии открытых фрагментов и соответствующего КТ служат обучающими примерами. Граница: Пример Paris 2 Fragment 96 нельзя подписать как Paris 4 или 1667. Источники: S08, S09.
- **C18 (P21,P39):** Модель чернил ищет физический сигнал, а язык читают специалисты; ошибочные изображения всё равно возможны. Граница: Отсутствие языкового дополнения не равно невозможности ошибок. Не заявлять, что LLM нигде не использовалась в подготовке научной рукописи. Источники: S08, S09, S01.
- **C19 (P22):** Vesuvius Challenge запущен в марте 2023 Seales, Friedman и Gross. Граница: Коллективная инфраструктура предшествует отдельным участникам; нет выдуманной сцены основания за одним столом. Источники: S11, S12.
- **C20 (P23):** Paris 4 / Scroll 1 и PHerc.1667 / Scroll 4 — разные предметы. Граница: Число 4 в Paris 4 не означает Scroll 4. Это главный запрет на подмену в монтаже. Источники: S11, S23, S01.
- **C21 (P24):** Handmer заметил crackle в участке, который уже был отсканирован и сегментирован другими. Граница: Не приписывать ему создание исходного КТ или всей геометрии. Источники: S13, S12.
- **C22 (P25):** Farritor размечал примеры и обучал модель искать соответствующий рисунок. Граница: Не изображать нейросеть как переводчик греческого или современный чат-бот. Источники: S04, S12.
- **C23 (P26):** Сообщение на дне рождения в Омахе, удалённый запуск с телефона, проверка у парковки после развоза друзей описаны Farritor. Граница: Мебель, одежда, композиция и мимика условны; диалогов, точного времени и внутреннего монолога нет. Источники: S04.
- **C24 (P27):** В 2023 прочитали последовательность, связанную со словом purple; First Letters объявлены 12 октября. Граница: Перевод сформулирован осторожно; грамматическая форма и контекст не превращаются в рассказ о конкретной пурпурной одежде. Источники: S12.
- **C25 (P28):** Nader получил свой результат в том же регионе, зная о предшествующих находках. Граница: Не слепая репликация без общего исходного знания. Источники: S12, S15.
- **C26 (P29):** Schilliger внёс вклад в геометрию; три участника объединили работу для главного приза. Граница: Нет сцены одновременной совместной работы в одной комнате как документального факта. Источники: S11, S16.
- **C27 (P30):** Эксперты оценивали анонимизированные результаты; техническая команда воспроизводила методы. Граница: Не спутать конкурсную проверку с журнальным рецензированием 2026. Источники: S11, S17.
- **C28 (P31):** 2023 Grand Prize объявлен 5 февраля 2024; $700,000 получили Nader, Farritor, Schilliger. Граница: Не отдельный новый приз 2024 и не сумма всех призов 2023. Источники: S11.
- **C29 (P32):** Около 5% Paris 4 было оценкой на момент объявления приза. Граница: Не сегодняшняя доля и не точное число процентов всей утраченной первоначальной книги. Источники: S11.
- **C30 (P33):** Текст Paris 4 обсуждает восприятие и удовольствие, еду, музыку и ценность редкости. Граница: Английский VO — пересказ аргумента; не длинная цитата современного перевода и не вымышленный античный диалог. Источники: S14, S11.
- **C31 (P34):** Надёжно установленного имени автора и заглавия Paris 4 нет в проверенных текущих источниках. Граница: Не приписывать ему Philodemus только по типичному составу библиотеки. Источники: S18, S14.
- **C32 (P35–P36):** Следующая задача — непрерывное прослеживание сохранившейся поверхности 1667. Граница: Непрерывность геометрии не восполняет утраченные части книги. Источники: S01, S20.
- **C33 (P37):** Для результата 2026 использованы улучшенные ESRF-сканы; Tafforeau и Mirone участвовали в получении и реконструкции данных. Граница: Основные сканы сделаны ранее, в 2025; фраза work released in 2026 не означает, что весь эксперимент выполнен за один день 2026. Источники: S01, S19.
- **C34 (P38):** Рукопись сообщает 31 виток и приблизительно 25 часов ручной аннотации на виток. Граница: Не превращать произведение этих чисел в полную длительность проекта. Это ручная работа внутри более широкого процесса. Источники: S01.
- **C35 (P40):** Nicolardi возглавила папирологическую работу; восемь специалистов сверяли чтения. Граница: Независимость отдельных чтений внутри команды не равна внешней репликации всего исследования. Источники: S01, S02.
- **C36 (P41):** На Paris 4 улучшенная КТ позволила прямо увидеть чернильные отложения и сопоставить проекцию с прежним чтением. Граница: Другой тип физического свидетельства в той же программе, а не независимая внешняя команда. Источники: S01, S19.
- **C37 (P42):** Проверка на Paris 4 не удостоверяет автоматически каждый знак 1667. Граница: Каждому объекту нужны собственные изображения, геометрия и чтение. Источники: S01.
- **C38 (P43):** Объявление 25 июня 2026; препринт загружен 27 июня; 22 колонки или эквивалента колонок. Граница: Пресс-релизы округляют до примерно 20; сценарий использует точное определение рукописи. Источники: S20, S21, S01.
- **C39 (P44):** Сердцевина сохраняет нижние части заключительных колонок более крупного свитка. Граница: Complete surviving core не означает entire original book. Источники: S01, S02, S20.
- **C40 (P45):** Первые три небольшие области колонок не транскрибированы; остаются лакуны и сомнительные буквы. Граница: Нельзя заполнять экран гладкой непрерывной греческой строкой как будто всё уверенно прочитано. Источники: S01.
- **C41 (P46):** Исследователи видят этическую аргументацию и вероятный стоический контекст; прочитано имя Aristocreon. Граница: Вероятность школы не доказывает автора. Имя Chrysippus упомянуто только как связь, не подпись под книгой. Источники: S01, S02, S19.
- **C42 (P47):** Автор и заглавие 1667 не установлены. Граница: On Gods Book 8 относится к PHerc.139; On Vices Book 1 — к другому свитку. Эти названия не вставлять. Источники: S01, S02.
- **C43 (P48):** На срез 31 октября 2026 доступна v1 препринта; журнальная публикация не подтверждена. Граница: Не утверждать осведомлённость о закрытом рецензировании. Перепроверить непосредственно перед выпуском. Источники: S21, S19, S22, S31.
- **C44 (P49):** Работа создаёт возможность дальнейшего исследования многих ещё закрытых рулонов. Граница: Вся библиотека не прочитана. Нет обещания одинакового результата для любого свитка. Источники: S01, S18, S20.
- **C45 (P50):** Исторические, консервационные, измерительные, вычислительные и филологические вклады связаны последовательно. Граница: Не приписывает всё одной модели, одному студенту или одному институту. Источники: S05, S06, S07, S08, S01.
- **C46 (P51–P53):** В финале сравниваются два конкретных текста и сохраняется видимость их утрат. Граница: Метафора возвращения голоса не означает воссоздания настоящего голоса автора или восстановления отсутствующих слов. Источники: S14, S18, S01, S02.
- **C47 (Все схемы / SET-G):** Учебная графика не выдаётся за подлинные данные. Граница: Наборные буквы подпишем TRANSCRIPTION, NOT FACSIMILE; собственный томографический рисунок — SCHEMATIC. Источники: S08, S09.
- **C48 (Права):** Новые данные 1667 имеют NC-условия, старые DLS — отдельную лицензию; медиакит не имеет найденного общего разрешения на всё. Граница: Исследование страниц не равно полученному разрешению на выбранный файл. Источники: S23, S24, S25, S26, S28.
- **C49 (Права / optional evidence):** PLOS 2019 Figure 5 — возможная CC BY 4.0 вставка, но показывает Paris 2 Fragment 96. Граница: Панель D не исходная фотография; конкретный скачанный файл ещё не инспектировался. Источники: S08, S27.
- **C50 (Права / типографика):** Лицензия Source Sans допускает использование по SIL OFL 1.1; эта гарнитура не подтверждена как фирменная типографика Paper Detour. Met 53.514.8 отмечен Public Domain. Граница: Met-книга 1746 — контекст раскопок, не момент обнаружения свитков; font license сохраняется при передаче шрифтов. Источники: S29, S30.

## Источники

- **S01** [Angelotti et al. — Complete virtual unwrapping and reading of a rolled Herculaneum papyrus](https://arxiv.org/html/2606.29085v1) — Метод, покрытие 1667, количественные критерии, экспертная проверка, отдельный опыт Paris 4. Ограничения: Не подтверждена журнальная публикация. Complete относится к сохранившемуся остатку; не каждый знак прочитан.
- **S02** [Lindsey Piercy / University of Kentucky — The day the Herculaneum scrolls began speaking again](https://research.uky.edu/news/day-herculaneum-scrolls-began-speaking-again) — Размеры, запись 1782 года, утраты, вероятная философская принадлежность, неизвестное авторство. Ограничения: Пресс-релиз участника проекта. Архивную запись 1782 года непосредственно не сверяли; осторожные цитаты надёжнее рекламного заголовка.
- **S03** [CISPE / Chartes — Papiro 1667](https://www.chartes.it/index.php?r=document/view&id=1691) — Fackelmann / 1969; Caprino и Fosse / 1987; десять частей в одной раме; ссылки на отчёты. Ограничения: Не позволяет назначить точный день, инструмент или автора вмешательства XIX века. Каталог не заменяет непрочитанные исторические отчёты.
- **S04** [Scott Schrage / University of Nebraska–Lincoln — Husker is first to decode word on ancient scroll](https://news.unl.edu/article/husker-is-first-to-decode-word-on-ancient-scroll) — Документированные действия Farritor, обучение модели, связь с наблюдением Handmer. Ограничения: В фильме нет дословных реплик, приватных мыслей, точного времени или доказанного интерьера. Снимок с обугленным рулоном в статье показывает современную реплику.
- **S05** [J. Paul Getty Museum — Buried by Vesuvius: Treasures from the Villa dei Papiri / Inner Workings](https://www.getty.edu/art/exhibitions/villa_papiri/inner.html) — Вилла, карбонизация, Paderni и Piaggio; ранее прочитанные тексты. Ограничения: Общие методы коллекции не приписываются 1667. Возможное использование свитков как топлива не превращено в установленный эпизод.
- **S06** [Biblioteca Nazionale di Napoli — I papiri ercolanesi: libri antiquiores in biblioteca](https://www.bnnonline.it/it/165/i-papiri-ercolanesi-libri-antiquiores-in-biblioteca) — Прибытие Piaggio в 1753; PHerc. 1497, книга IV труда Philodemus о музыке, успешное открытие в 1754. Ограничения: Не доказательство того, что именно 1667 проходил машину Piaggio. Техническая доступность страницы нестабильна.
- **S07** [Seales et al. — From damage to discovery via virtual unwrapping: Reading the scroll from En-Gedi](https://pmc.ncbi.nlm.nih.gov/articles/PMC5031465/) — Предшествующий успех виртуального разворачивания; животная кожа, более заметный сигнал чернил, этапы метода. Ограничения: 2016 — год статьи, не обязательно первого публичного объявления. En-Gedi не папирус из Геркуланума; состав чернил не объявляется химически установленным.
- **S08** [Parker et al. — From invisibility to readability: Recovering the ink of Herculaneum](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0215775) — Трудности контраста, обучение по открытым фрагментам; оценка более ранних заявлений; технические различия изображений. Ограничения: Критика предыдущих чтений — позиция авторов, а не доказательство, что каждое раннее наблюдение было ложным.
- **S09** [Parsons et al. — EduceLab-Scrolls: Verifiable Recovery of Text from Herculaneum Papyri using X-ray CT](https://arxiv.org/abs/2304.02084) — Совмещение фотографий и КТ, обучающие метки, геометрия, проверяемые результаты. Ограничения: Версия v4 включает события после исходной публикации; не переносить её содержание целиком в апрель 2023.
- **S10** [Mocella et al. — Revealing letters in rolled Herculaneum papyri by X-ray phase-contrast imaging](https://www.nature.com/articles/ncomms6895) — Факт заявления о буквах до Vesuvius Challenge. Ограничения: Статья не доказывает чтение целой книги; позднейшая критика представлена отдельно, через S08.
- **S11** [Vesuvius Challenge — 2023 Grand Prize: Winners](https://scrollprize.org/grandprize) — Nader / Farritor / Schilliger; $700,000; около 5% Paris 4 на момент объявления; содержание об удовольствии. Ограничения: Приз называется 2023 Grand Prize, объявлен в 2024. Оценка 5% не выдаётся за текущий прогресс.
- **S12** [Vesuvius Challenge — First Letters](https://scrollprize.org/firstletters) — Первые буквы/слово в конкурсе 2023; роли участников. Ограничения: Не утверждать, что это вообще первое чтение какого-либо геркуланумского папируса.
- **S13** [Casey Handmer — Reading ancient scrolls](https://caseyhandmer.wordpress.com/2023/08/05/reading-ancient-scrolls/) — Наблюдение crackle; данные и геометрия подготовлены до него; работа Farritor связана с этим сигналом. Ограничения: Дата записи не равна дню первого наблюдения. Общие исторические утверждения блога не принимаются без музейных источников.
- **S14** [Nicolardi, Delattre, Del Mastro, Janko, Fowler — The final columns of PHerc.Paris. 4 revealed through virtual unwrapping](https://www.iris.unina.it/handle/11588/985203) — Части шестнадцати заключительных колонок, эпикурейская аргументация, восприятие, еда и музыка, уточнение чтений. Ограничения: Открытая доступность PDF не равна свободной лицензии: карточка указывает copyright издателя. Шестнадцать колонок в этой статье не подменяют более раннюю оценку релиза.
- **S15** [Youssef Nader — Vesuvius-First-Letters](https://github.com/younader/Vesuvius-First-Letters) — Собственный метод Nader и воспроизводимость технической части. Ограничения: Не объявлять его работу слепой независимой репликацией без знания прежних находок.
- **S16** [Julian Schilliger — ThaumatoAnakalyptor](https://github.com/schillij95/ThaumatoAnakalyptor) — Вклад в выделение поверхности и масштабирование. Ограничения: Современный README может описывать более позднюю функциональность; в VO не назначена точная дата каждой функции.
- **S17** [Vesuvius Challenge — 2023 Grand Prize rules](https://scrollprize.org/grand_prize) — Техническая воспроизводимость и отдельная папирологическая оценка. Ограничения: Регламент — не независимое внешнее рецензирование научной статьи 2026.
- **S18** [Vesuvius Challenge — Prizes](https://scrollprize.org/prizes) — Автор и название Paris 4 не считаются установленными. Ограничения: Состояние может измениться; проверить перед публикацией фильма.
- **S19** [ESRF — The day the Herculaneum scrolls began speaking again](https://www.esrf.fr/cms/live/live/fr/sites/www/home/news/general/content-news/general/the-day-the-herculaneum-scrolls-began-speaking-again.html) — Новые измерения, этическое содержание, статус рукописи на момент сообщения. Ограничения: Не независимая внешняя репликация; июньское сообщение само по себе не исключает позднейшего принятия в журнал.
- **S20** [Vesuvius Challenge — The first scroll](https://scrollprize.org/firstscroll) — Объявление результата 1667; непрерывность сохранившейся поверхности. Ограничения: Заголовок сильнее подробных оговорок: в фильме complete всегда ограничено surviving core.
- **S21** [arXiv — 2606.29085, metadata and version history](https://arxiv.org/abs/2606.29085) — Дата препринта и публично подтверждённый статус. Ограничения: Отсутствие journal reference не раскрывает закрытый процесс рецензирования. Формула: журнальная публикация не подтверждена.
- **S22** [Chris Simms / Nature News — Watch scientists decipher burned scrolls without unrolling them](https://www.nature.com/articles/d41586-026-02920-8) — Независимый позднейший источник продолжает ссылаться на препринт. Ограничения: Это новость о другом эксперименте с репликами; не новая рецензированная версия статьи Angelotti и не проверка каждой буквы 1667.
- **S23** [Vesuvius Challenge — PHerc. 1667 data browser](https://scrollprize.org/data_browser/PHerc1667) — Scroll 4 = PHerc. 1667; различение старых DLS и новых ESRF данных; отдельные лицензии. Ограничения: Краткий статус Full scroll read не заменяет критерии покрытия статьи.
- **S24** [EduceLab / Vesuvius Challenge — Data License](https://dl.ash2txt.org/LICENSE.txt) — Ограничения на перераспространение и новые текстовые раскрытия из соответствующих данных. Ограничения: Не переносить договорные ограничения на запрет пересказывать уже опубликованные факты.
- **S25** [arXiv — Non-exclusive license to distribute](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html) — Разрешение arXiv распространять работу не является общей CC-лицензией на figures. Ограничения: Нужны отдельное разрешение или иное применимое основание для использования конкретного изображения.
- **S26** [University of Kentucky — Herculaneum Media Kit](https://engr.uky.edu/herculaneum) — Кандидаты на доказательные кадры, разные авторы и кредиты. Ограничения: Не найдено универсального разрешения на всё. Подписи/alt-текст местами требуют дополнительной проверки идентичности объекта.
- **S27** [Creative Commons — Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) — Условия повторного использования PLOS 2019 при отсутствии исключения у фигуры. Ограничения: Сохранить кредит, ссылку лицензии и обозначить изменения; отдельно проверить точный файл.
- **S28** [Creative Commons — Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/) — Публичная доступность новых данных не разрешает любое коммерческое использование. Ограничения: Один кредит или отключение рекламы не являются автоматической заменой проверки назначения использования.
- **S29** [The Metropolitan Museum — Disegni intagliati in rame di pitture antiche ritrovate nelle scavazioni di Resina, 53.514.8](https://www.metmuseum.org/art/collection/search/628956) — Необязательный архивный материал об эпохе раскопок. Ограничения: Не изображение открытия папирусов 1750-х и не чертёж машины Piaggio.
- **S30** [Adobe Fonts — Source Sans, LICENSE.md](https://github.com/adobe-fonts/source-sans/blob/release/LICENSE.md) — Условия лицензии, если Source Sans будет отдельно выбран для служебного музейного паспорта; не является эталоном бумажных акцентов. Ограничения: При передаче файла шрифта сохранить лицензию; условия modified font не подменять условиями готового видео.
- **S31** [Julie Duruflé / Biblissima — Lire un rouleau sans l’ouvrir : de nouveaux papyrus d’Herculanum déchiffrés](https://odysseum-biblissima.ens.psl.eu/article/papyrus-herculanum-deroule-virtuellement/) — Более позднее октябрьское подтверждение того, что результат опубликован как препринт; интервью о сканировании и ограничениях. Ограничения: Некоторые популярные формулировки упрощают историю повреждений и роль алгоритмов; для точных критериев 1667 используем S01, не переносим все обобщения интервью в VO.

- **S32** [TIME — Farritor and the Vesuvius Challenge](https://time.com/6326563/vesuvius-challenge-herculaneum-papyri-ai/) — Дополнительная публикация о рассказе Фарритора; последовательность также подтверждается доступным S04. Ограничения: Это тот же рассказ участника, не независимое наблюдение очевидца; не подтверждает внешний вид, точный интерфейс, интерьер или маршрут.

## Что ещё не проверено

- Полный аудит всех реальных границ планов и считываемости в монтаже.
- Фактическое время и произношение без озвучки.
- Существование и композит всех графических активов, прослушивание звука и проверка прав каждого заимствования.
- Техническая возможность и параметры проекта Palmier 006.
- Независимая проверка интеграции v1.3.
- Дополнительные активы v1.3 перечислены как составные требования к планам, не как полная покадровая нарезка отдельных файлов.

- Непрерывность условного силуэта, его опор и телефона, а также окно P22 не проверены в кадрах и беззвучной пробе.

Права исходных материалов проверять по конкретному файлу и способу использования. Ограничение CC BY-NC у отдельных данных Vesuvius Challenge не считать разрешением на коммерческий монтаж. Подробнее: [исходное исследование](../../../research/2026-10-31-next-long-film/HERCULANEUM_SOURCE_RESEARCH.md).
