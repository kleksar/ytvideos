# Задания и промпты для изображений v01 — выпуск 035

2026-11-02 · Nuviko History · English film · 16:9.

**Основа:** [STORYBOARD_v01.md](STORYBOARD_v01.md) и проверенная [спецификация референсов v01](VISUAL_REFERENCES_v01.md). Три выбранных задания выполнены отдельно через встроенный `image_gen`: натюрморт IT-01, Tudor-фон IT-02, викторианская стройплощадка IT-03. Их локальные черновые выходы и осмотр: [IMAGE_QA_v01.md](IMAGE_QA_v01.md). IT-04 и native-графика не генерировались. Нет разрешения на новый звук в рамках этой работы.

## Общая рамка для генератора

- Кадр 16:9 landscape. Фотореалистичная постановочная реконструкция мира; ведущий остаётся слегка мультяшным каноническим персонажем и добавляется отдельно только там, где он указан.
- Никаких надписей, подписей, цифр, графиков, букв, эмблем, водяных знаков, рамок интерфейса или псевдотекста внутри изображения. Подписи и диаграммы собираются отдельно.
- Никакой имитации старой фотографии для средневековья/Tudor. Для изображений XIX века не копировать лицо человека с архивной фотографии.
- Историческую неопределённость решать уменьшением детализации/заменой на абстрактный силуэт, а не придуманной точностью. Не создавать сцены с конкретным работником, семьёй, арестом или очевидцем.

## IT-01 — Общий натюрморт «основные нужды»

**Размещение:** S01, S05, S24. Один мастер-кадр пригоден для открытия и финала с разными кропами.

**Prompt (English):**

> Create an original photorealistic cinematic still life, 16:9 landscape, for a historical explainer film. A sturdy plain wooden tabletop seen from a low three-quarter angle, with four separate everyday necessities spaced clearly apart: a simple loaf of bread, a modest source of household fuel, an unbranded piece of washing soap beside a small amount of water, and one plain candle. Quiet neutral room, soft natural side light, realistic restrained materials, muted warm earth palette, generous uncluttered negative space on the right for graphics to be added later. Make the objects legible as categories, not a shopping basket or a complete annual budget. No people, no visible prices, no packaging, no basket, no coins, no readable marks, no modern branding, no text, no logos, no watermark.

**Контроль:** предметы не должны выглядеть как четыре явно конкретных товара с современной упаковкой. Не выдавать форму или количество вещей за историческую спецификацию корзины. Для S24 сохранить тот же порядок предметов и направление света.

## IT-02 — Городской фон Tudor London, 1540-е

**Размещение:** опционально в S13 после основных графических планов.

**Prompt (English):**

> Create an original, restrained photorealistic environmental reconstruction of mid-Tudor London, 16:9 landscape, based only on the broad city silhouette visible in the 1540s London panorama: a dense low-rise riverside city, layered rooflines and church spires, the Thames as a broad horizontal depth cue, pale overcast daylight. View from across the river at a moderate distance; the city is an atmospheric backdrop, not a precise map or a replica of named landmarks. If people are included, use only two or three very small anonymous silhouettes in the near foreground with indistinct period clothing; do not depict a specific building job or identifiable tools. Naturalistic stone, timber and roof textures without heroic grandeur. No presenter, no text, no labels, no modern skyline, no modern bridges, no precise recognizable landmarks, no fantasy towers, no invented flags, no watermark.

**Опора и граница:** общий силуэт опирается на [панораму Tudor London 1540-х](https://artcollection.dcms.gov.uk/artwork/0-108/). Изображение не является точным видом улицы или стройплощадки. Если генератор добавит узнаваемый монумент или неверный мост, отклонить кадр и заменить его графической картой-силуэтом.

**Запасной native-design brief:** вместо генерации — простая двухцветная панорамная полоска города и Thames, вручную собранная по проверенному силуэту; никаких меток зданий. Рабочих показать несколькими абстрактными фигурами только если зрительно необходимы.

## IT-03 — Лондонская стройплощадка позднего XIX века

**Размещение:** опциональный установочный кадр S20 перед диаграммой `1850–1899 · ≈116 days’ pay`.

**Prompt (English):**

> Create an original photorealistic historical reconstruction of a London construction site in the later nineteenth century, 16:9 landscape, viewed from human eye level. A broad work area with timber staging, stacked beams and masonry, a few small anonymous workers engaged in ordinary manual tasks, and a distant hazy urban riverfront atmosphere. Use a sober documentary composition and natural grey daylight, realistic scale, subdued workwear, and no single heroic worker. Keep faces unidentifiable. The setting is generic and must not reproduce Crystal Palace, Victoria Embankment, or a named landmark; it evokes the material scale of a London building site without claiming these workers belong to a particular wage record. Avoid showing the site as a cause of changing purchasing power. No presenter, no text, no signage, no modern safety equipment, no hard hats, no cranes unless clearly supported by the supplied period reference, no steam spectacle, no factory smokestacks, no recognizable monument, no watermark.

**Опора и граница:** предварительная фактура стройки сопоставлена с архивными материалами середины/второй половины XIX века: [London Museum, Victoria Embankment, 1865](https://www.londonmuseum.org.uk/collections/v/object-101242/construction-of-the-victoria-embankment/), [Historic England, Victoria Embankment workmen](https://historicengland.org.uk/images-books/photos/item/OP04628), [Wellcome, Crystal Palace workers, 1854](https://wellcomecollection.org/works/mjka5kg2). Ни один из объектов не привязывает wage series к этой площадке; prompt специально не воссоздаёт конкретную из них.

**Контроль:** прежде чем принять выход, отдельно сверить одежду, леса, материалы и инструмент с одной выбранной датированной визуальной опорой. Если генератор домысливает технику или смешивает 1850-е и 1890-е, кадр отклонить либо упростить до общего плана с минимумом читаемых деталей.

## IT-04 — До чумы: безопасная замена без недоказанной реконструкции

**Размещение:** S04/S09 только если переходу нужен визуальный мост. Не генерировать реалистичный реконструированный рабочий костюм по текущему комплекту источников.

**Native-design brief (English):**

> Design a minimal editorial map card for a historical explainer: a simple outline of London and the Thames, with three small neutral human silhouettes near a plain building outline. No facial, clothing, tool, or architectural detail. Clean matte graphics, high contrast, plain background, ample whitespace, no labels; the word “London” will be typeset separately. The symbols stand for a broad labour market, not specific people or a documented scene.

**Причина ограничения:** имеющиеся London Museum shoe/textile fragments относятся к позднему XIV веку, то есть не дают полного образа лондонского работника до Чёрной смерти. Если позже найдутся надёжные предметные опоры до 1348 года, сцену можно пересмотреть отдельной версией.

## IT-05 — Обязательные экраны, которые не генерируются

- **Четыре доли, 333/250, 176/216/116, рост x2.22/x2.78, формулы и вопрос зрителю:** рисовать векторно/композитно по раскадровке. Не просить image model рисовать текст или числа.
- **Статут 1351 года:** набирать карточку только из текста, проверенного по рабочему источнику. Не делать псевдорукопись, королевскую печать, орнаментированный свиток, сцену суда или наказания.
- **Ведущий:** использовать существующий принятый reference 004 для композиции/персонажа. Эти задания не меняют его дизайн и не требуют нового полного character sheet.
- **Средневековая рабочая группа:** пока закрыта графической заменой IT-04; никаких реалистичных лиц/костюмов до дополнительной проверки.

## Порядок возможного производства

1. IT-01, IT-02 и IT-03 уже сгенерированы и проходят как черновые кандидаты; качество и ограничения описаны в [IMAGE_QA_v01.md](IMAGE_QA_v01.md).
2. До использования IMG-07 в монтаже отдельно сверить одежду, леса/подъёмный механизм и материалы с выбранной архивной опорой.
3. Решить при монтаже, оправдана ли короткая Tudor-врезка; при сомнении оставить native-карту/панораму и графику.
4. До правки сценария, расширения набора или создания любых новых изображений зафиксировать новые требования в следующей версии storyboard/задач. Никакой из текущих кадров не заявлен как финально принятый пользователем.
