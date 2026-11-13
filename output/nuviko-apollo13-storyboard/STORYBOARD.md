# Apollo 13 — раскадровка Nuviko History

Версия preproduction. 14 планов покрывают английский мастер без пропуска слов. Точные секунды, длительность и координаты камеры появятся после озвучки и просмотра готовых кадров. Изображения планируются в 9:16. Ведущий открывает и замыкает историю в современной музейной демонстрации. Исторические сцены показывают экипаж и инженеров.

Сценарий SHA-256 `d720fc90d9b726c2f064c4f18da13feccfbb1fb0b0e2c5e9b41a7b340d099f02`.

| План | Реплика | Кадр и действие | Крупность / камера |
|---|---|---|---|
| S001 · Форма фильтра | Apollo 13's spare air filters were square. | Современный музейный стенд. Рисованный ведущий в три четверти раскрывает правую ладонь рядом с квадратным серебристым картриджем. | medium / zoom_in |
| S002 · Круглое гнездо | The filter openings in the lunar lander were round. | Предметный вид под углом на музейные модели квадратного картриджа и круглого посадочного места, расстояние между ними видимо. Ведущий вне кадра. | close / zoom_out |
| S003 · Авария | An oxygen tank had exploded on the way to the Moon, | Взгляд через плечо астронавта на тесную панель командного модуля. Рука опирается на край консоли. Без огня внутри кабины, без киношного взрыва. | medium / static |
| S004 · Убежище | so all three astronauts took shelter in the lander. | Ракурс из глубины лунного модуля к переходному люку. Три человека в белой полётной одежде без шлемов распределены по тесному объёму. Видны спины и профиль. | wide / zoom_in |
| S005 · Рассчитано на двоих | Its life support was designed for two people. | Низкая камера сбоку кабины, два рабочих места у передних окон и третий человек позади. Система кабины сохраняет расположение ориентиров из S004. | wide / zoom_out |
| S006 · Предупреждение | Now three were breathing in there, and a warning light came on. Carbon dioxide had reached a dangerous level. | Крупный взгляд астронавта на светящийся индикатор штатной панели. Лицо частично видно в профиль, главная деталь — лампа и окружающая реальная панель. | close / zoom_in |
| S007 · Запас | The crew had spare filters back in the command module. | Внутри командного модуля квадратный картридж удерживается двумя руками над открытым отсеком. Боковой ракурс показывает толщину и решётку. | close / zoom_out |
| S008 · Воздух через фильтр | They needed to pull cabin air through one of those filters. | Макро на открытые решётки квадратного фильтра, пальцы держат его по краям и не закрывают отверстия. Никаких видимых цветных газов или стрелок. | macro / zoom_in |
| S009 · Наземная проверка | Engineers in Houston built and tested an adapter using supplies the crew had on board. | Фотореалистичная лабораторная установка по NASA S70-35395. Картридж, мешок, серая лента и белые шланги уже соединены на тестовом стенде. Инженер виден со спины. | medium / zoom_out |
| S010 · По радио | Mission Control talked the astronauts through the build over the radio. | Диспетчер со спины и в профиль за серо-зелёной консолью 1970 года с гарнитурой. Бумажная инструкция перед ним, свет CRT и ламп, фон по NASA S70-35136. | medium / zoom_in |
| S011 · Материалы | With cardboard, a plastic bag and duct tape, | Крупная предметная композиция внутри лунного модуля. Руки экипажа придерживают картонную карточку, пластиковый пакет и полоску серой ленты рядом с тем же квадратным фильтром. | close / zoom_out |
| S012 · Соединение | the crew sealed a hose to the square filter. | Крупный боковой вид рук, завершающих герметичное соединение мешка со шлангом лентой. За лентой читается квадратный фильтр, белая тканевая оплётка шланга соответствует NASA. | close / zoom_in |
| S013 · Система заработала | The lander's ventilation fan pulled cabin air through the filter and into the hose.

Within minutes, the carbon dioxide level began to fall. | Более широкий вид установленного адаптера и белого шланга, который непрерывно уходит к штатной системе LM. Край корпуса приборной панели в фоне. Фильтр и шланг сохраняют размер и расположение из S012. | medium / zoom_out |
| S014 · Возврат к вопросу | Why did a working filter need that detour? | Возврат к точному музейному кадру S001. Ведущий смотрит на две формы, глаза открыты, ладонь спокойно раскрыта. Последний кадр равен первому по положению объектов. | medium / static |

## Непрерывность

| Сущность | Состояния и ограничения |
|---|---|
| Музейная экспозиция | S001, S002, S014 существуют вне хронологии полёта. S014 повторяет S001. Ведущий не взаимодействует с астронавтами. |
| Картридж на борту | S007–S008 целый и без адаптера. S011 материалы подготовлены. S012 стык закрывается. S013 он подключён. |
| Наземный образец | S009 — отдельная испытательная копия, его нельзя незаметно превратить в бортовой предмет. |
| Экипаж | Три человека. Белая полётная одежда, открытые головы. Положение в невесомости задаётся удержанием за поручни. Перед финальной генерацией закрепить лица/одежду на референсном листе. |
| Шланг | Белая тканевая оплётка, непрерывное соединение фильтр → шланг → штатная система. Гофрированный чёрный пылесосный шланг не соответствует просмотренным фото. |
| Предупреждение | S006 нужен отдельный проверенный вид панели. Не придумывать маркировку и таймер смерти. Снижение CO₂ в S013 подтверждается рассказом. |

## Листы для генерации

- **REF-HOST**. Потребители S001, S014. Use both approved traveler PNGs. Identity sheet for museum explanation. Front, three-quarter body and side profile; right palm open beside exhibit at waist height, relaxed left hand, both eyes open. Preserve jacket, backpack, hair, beard and 2D line shading. Neutral curious expression. Only required poses, no action inside historical spacecraft.
- **REF-FILTER**. Потребители S001, S002, S007, S008, S009, S011, S012, S013, S014. Photographic object reference sheet using NASA AS13-62-9004 and S70-35395. Same square Apollo CM lithium hydroxide cartridge in front, side and three-quarter views. Distinguish plain cartridge, cardboard/plastic bag/tape sleeve, and final sealed white cloth-wrapped hose assembly. Preserve metal mesh face, proportions and tube connection. State labels outside image may be added only for QA contact sheet.
- **REF-LM**. Потребители S004, S005, S006, S011, S012, S013. Photoreal LM Aquarius cabin reference sheet from NASA photographs. Fix cramped ivory equipment panels, fabric bags, white wrapped hoses, mesh storage and handholds. Show toward docking hatch, opposite corner, and equipment close-up. Three white-clothed crew members without helmets, filmed from backs and partial side views. Do not use movie actors. Exact panel labels require a separate verified close-up.
- **REF-MCC**. Потребители S009, S010. Two separate photoreal environment reference compositions based on supplied NASA photos. A ground CO2 adapter test rig and the 1970 Mission Control room with gray-green console rows, blue CRTs, paper, headset operators. Keep the lab and control room distinct, consistent fluorescent practical lighting.
- **REF-CM**. Потребители S003, S007, S008. Photoreal Apollo command module interior reference sheet. Obtain and open dedicated NASA cockpit/storage photos before generation. Preserve real CM geometry, seats, instrument panels and storage. No modern ISS walls or large standing room.

## Проверки перед анимацией

Для каждого будущего клипа проверить первый, средний и последний кадры, затем весь клип. Сверять руки, лица, положение реквизита и шлангов. В кадрах с ведущим сверять оба эталона. В конце — спокойная читаемая поза с открытыми глазами. Оценить фактический переход S014 → S001. Субтитры Nuviko остаются отдельным слоем по профилю.

14 композиций — исходная редакционная разбивка. S006 и S013 проверяются по фактической озвучке и будущему рецепту анимации. Выбор клипов 3–10 секунд требует измеренной карты слов и параметров провайдера. Начальные и конечные состояния для анимации описаны в JSON как замысел; они не являются разрешением внешней видеогенерации.

Визуальные источники и пределы проверки сохранены в REFERENCES.md.

## Подход Ingredients

Изучены последние 20 сообщений из чата `01a1d4f3-fb16-7e41-8203-4878ef5fde4b`. Для каждой сцены готовится один опорный кадр. Начальное и конечное состояния описывают возможное действие внутри будущего клипа. Сначала закрепляются нужные виды сущностей, затем создаются изображения сцен. Каждый поворот и наклон на листе должен иметь сцену-потребителя. Подробный промпт анимации уточняется по фактическому перечню видимых объектов принятого кадра и измеренным словам озвучки.

Состав кадра сохраняется на протяжении клипа. У появления, исчезновения или изменения реквизита есть видимое действие. Число людей, соединения шлангов, положение креплений и детали помещения проверяются во всей последовательности. Общий стиль сверяется по утверждённым листам, включая цвет волос, форму лица, материалы и свет. Текущие camera intents служат постановке. Параметры будущего видео пока не назначены.

## Подробные задания сцен

Состав объектов, позы, камера, действие и звук каждого плана уточнены в [DETAILED_SCENE_SPECS.md](DETAILED_SCENE_SPECS.md) и [detailed-scene-specs.json](detailed-scene-specs.json). Exact привязки принятых изображений заполняются после их просмотра.
