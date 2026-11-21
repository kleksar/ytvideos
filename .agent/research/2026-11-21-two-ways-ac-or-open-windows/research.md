# Research · Two Ways Lab · AC versus open car windows

Дата наблюдения: **2026-11-21 UTC**. Public web sources only; public video cards != playback, transcripts or actual viewer comments. Общие источники для трёх EN/RU редакций; никакого реального собственного теста автомобиля. Не использовать закрытые repository identifiers во внешних поисковых запросах.

## 1. Очередь и реальная причина смотреть

На момент отбора фактический последний сюжетный Draft PR — #319 (Nuviko); предыдущие #318 (Paper), #317 (Two Ways). Поэтому новая история для Two Ways Lab. Проверен поиск PR по `AC vs windows`, `air conditioning`, `fuel efficiency`, `window` и ближайшим темам; явный дубль не найден на дату отбора. Близкий по ценности #307 — цена двух АЗС с дополнительным пробегом, но это **другой** выбор. #157 — idling vs restart, также иной расход. В бэклоге темы с очередями, носками и packing; не объявлять их свободными после одного поиска.

Универсальный вопрос: «В жаркой машине открывать окна или включать кондиционер, чтобы меньше потратить?» Два честных способа A/B. Единый автомобиль, одна скорость, одно расстояние, два состояния. **Metric до результата** — fuel per unit distance, не тепловой комфорт или субъективное ощущение. Ставка для зрителя — не только расход, но и опровержение привычного простого порога скорости на настоящих данных. Повороты: ожидаемое аэродинамическое правило → обе машины против него на 40–70 mph при max AC → Corolla сравнялась 75 и поменяла лидера 80, Explorer нет → действительная нагрузка AC и другие параметры, невозможность универсального порога. Зритель получает границы практического вывода, а не фиктивную гарантию экономии.

## 2. Фактическая воронка — 11 разных направлений

| Направление | Первичное решение/причина |
|---|---|
| **Окна против кондиционера автомобиля** | **FINALIST**: универсальный выбор; независимые исследования и реальный скоростной crossover; недостаток — известный миф, напряжение 10m |
| OLED: dark mode или light mode | **FINALIST**: знакомо почти всем владельцам телефонов, подтверждено Purdue; сильная альтернатива, но эффект зависит от яркости/панели и тема широко пересказана |
| Готовить стейк замороженным или предварительно разморозить | **FINALIST**: реальный split-steak A/B с результатом, сильная наглядная развязка; узкая пищевая аудитория и 10m без добавочных экспериментов |
| Беспроводная против проводной зарядки | Предварительно отклонено: вывод о счёте/потерях без подтверждённого same-device test |
| Лимит заряда 80% против 100% | Не смешивать предсказания lifetime с единичным измерением |
| Солнцезащитный экран против предварительного проветривания | Разные функции и погодные условия; невозможно честно назначить победителя по одной метрике |
| Электрочайник против кастрюли | Стандартный ожидаемый результат, слабо обоснованный 5/10m |
| Одна сумка покупок против нескольких | Определение победителя зависит от произвольной метрики переноски/хранения; много похожих тем в backlog |
| Промытый против непромытого риса | Сорт, вкус и показатели здоровья разнородны; без честного равного результата |
| Бумажные полотенца против сушилки для рук | Время, гигиена, LCA зависят от разных входов; не делать универсальное обещание |
| Хранить хлеб в холодильнике против при комнатной температуре | Свежесть/плесень/сорт и срок требуют дополнительной достоверной базы |

Исследованы три финалиста содержательно, остальные — быстрый screening, не десять «полностью прочитанных исследований».

## 3. Три конкурирующие заявки до полного сценария

### A. AC versus windows — выбран
- **Первое произнесённое действие/реплика:** `I'm about to switch on the air conditioning. But would opening my car windows use less fuel?`
- **Почему остановится:** сам узнаёт собственный выбор в летней машине и ожидает известный ответ «окна только на малой скорости».
- **Почему останется:** ORNL ломает ожидаемый порог; разная машина ведёт себя по-разному; max AC как скрытый параметр.
- **Payoff:** честный ответ с measured Corolla 80mph crossover и отсутствием универсального порога, плюс применимая DOE рекомендация.
- **Сильное возражение:** тема и MythBusters уже существовали, новый 2026 англоязычный ролик может быть просто повтором мифа; реальный comparable Short demand/retention неизвестен. Если начинается с сухих чисел, потеряем любого зрителя.

### B. OLED dark/light — сильнейший конкурент по широкой аудитории
- **Первая реплика:** `I turn on dark mode to save battery. But how much does my phone really gain?`
- **После hook:** Purdue измерил разные OLED-модели и обычную/максимальную яркость; 30–50% brightness даёт скромную экономию, на 100% — значительно выше.
- **Payoff:** привычка полезна при одном освещении и менее заметна при другом; не универсальный процент для всех телефонов.
- **Сильное возражение:** визуально на 2m отличная, но 5/10m рискуют стать перечислением OLED-устройств; 2019 известные видео уже объяснили механизм.
- **Evidence:** Purdue University News 2021-07-28: https://www.purdue.edu/newsroom/archive/releases/2021/Q3/dark-mode-may-not-save-your-phones-battery-life-as-much-as-you-think,-but-there-are-a-few-silver-linings.html . Exact configurations from university study; не объявлять влияние на общую батарею равным энергопотреблению экрана. Community August 2026: https://www.reddit.com/r/iPhoneBatteryParanoia/comments/1vvipn0/dark_mode_isnt_the_batterysaving_hack_you_think/ . Evergreen videos: https://www.youtube.com/watch?v=qbxdHpD5jWw (PhoneBuff, 2019) and https://www.youtube.com/watch?v=dkLHJgZfVfE (Engadget, 2019); это не свежий сопоставимый спрос.

### C. Frozen steak vs thawed — сильнейший конкурент по видимому тесту
- **Первая реплика:** `I forgot to thaw dinner. Could the frozen steak actually come out better?`
- **После hook:** America's Test Kitchen режет 8 strip loin steaks пополам, замораживает; половина оттаивает ночь в холодильнике, обе стороны жарятся 90s, духовка 275°F до 125°F. Frozen требует 18–22 мин против 10–15, но теряет в среднем на 9% меньше влаги и имеет меньше серую полосу пережаривания.
- **Payoff:** не безоговорочный shortcut, а конкретный метод с ценой в дополнительных минутах. Не приравнивать 9% *relative moisture-loss difference* к 9 процентным пунктам веса.
- **Сильное возражение:** ограниченная кулинарная аудитория; материал после одного сравнения быстро исчерпан, 10m потребовал бы новых контролируемых данных; риск подменить измерение сочинённым собственным опытом.
- **Evidence:** https://www.americastestkitchen.com/how-tos/8741-the-science-of-cooking-frozen-steaks (открыт, раздел HOW WE TESTED and RESULTS). YouTube: https://www.youtube.com/watch?v=uru7heY8Iog (2025-02-02, карточка ~7k views), https://www.youtube.com/watch?v=tNYoY1j5DsY (2025-02-01, ~13.7k), оба только внешний indexing.

**Сравнение:** OLED потенциально ещё шире, steak ещё нагляднее; AC побеждает *развитием* на реально изменяющихся контролируемых условиях и независимыми разными исходами, а не «легко нарисовать». Остаётся риск старого мифа и недостатка доказанного спроса; это экспериментальная редакционная гипотеза.

## 4. Evidence register — только подтверждённые заявления

1. **ORNL 2013 / US DOE OSTI** — Shean P. Huff, Brian H. West, John F. Thomas, `Effects of Air Conditioner Use on Real-World Fuel Economy`, SAE conference paper 2013-01-0551 (2013-04-08). Полный текст paywalled; **авторский abstract прочитан**, не подменяется полным paper. Открытые abstract copies: https://www.ornl.gov/publication/effects-air-conditioner-use-real-world-fuel-economy , https://www.osti.gov/biblio/1092236 , https://saemobilus.sae.org/papers/effects-air-conditioner-use-real-world-fuel-economy-2013-01-0551 . Установлено: Ford Explorer 2009, Toyota Corolla 2009; on-road/chassis dyno; 40–70 mph обе расходуют больше с AC на max cooling (compressor 100% duty), чем с окнами вниз; Corolla equality 75 mph и AC better 80; Explorer не пересёк порог в указанном tested range. **Не установлено**: точные суммы долларов на одну поездку, абсолютный универсальный расход, современное EV поведение.
2. **DOE/EPA FuelEconomy.gov, `Fuel Economy in Hot Weather`**, https://www.fueleconomy.gov/feg/hotweather.shtml — опубликованный advice и подпункт references; accessed 2026-11-21. AC cost зависит от температуры/влажности/солнечного света; окна увеличивают drag (особенно high speed); практическая рекомендация lower speeds windows, highway AC; предварительное краткое проветривание, не чрезмерное охлаждение; hybrid/EV effects особые. **Это практический совет**, не новый эксперимент и не противоречие измеренному max AC.
3. **ORNL 2014, `Oak Ridge study pegs fuel economy costs of common practices`**, https://www.ornl.gov/news/ornl-study-pegs-fuel-economy-costs-common-practices — отдельное исследование о windows/drag, не подменять им 2013 AC comparison.
4. **1982 SAE abstract**, https://saemobilus.sae.org/papers/detecting-small-differences-fuel-economy-air-conditioning-versus-open-windows-820075 — indexed abstract only, эффект AC в тесте двух авто значительно больше open windows. Это доп. контекст 10m, **full paper NOT READ**.
5. **Consumer Reports by Jake Fisher, 2017-06-18**, собственный текст в syndication https://www.yahoo.com/news/fuel-economy-face-off-driving-windows-open-c-110020310.html : CR сообщает AC reduction 1–4 mpg at 85°F, windows open 65 mph no measurable reduction in its tests; не переносить эту оценку на Corolla/Explorer 2013 и не считать «нулевым сопротивлением».
6. **Consumer Reports secondary 2018**, https://www.yahoo.com/news/best-fuel-economy-now-191948352.html — согласуется с 2017, но не дополнительное независимое исследование.

**Слепые зоны:** точный тип/позиция окон 2013 доступен только в полном paper; claims не требуют этого. Не выдавать метод 1982/CR за одну и ту же тестовую машину. Обещание «универсальный crossover 45mph» не доказано.

## 5. YouTube / community demand (публичные карточки, 2026-11-21 observation)

| Реальная публичная ссылка | Автор/язык/тип | Публикация и известный результат карточки | Baseline/ограничение |
|---|---|---|---|
| https://www.youtube.com/watch?v=O9r77Dpu8Xc | MythBusters, EN, clip/entertainment | 2025-07-05, ~92,085 views, 1,800 likes | Автор крупный (~770k); другие full episodes другого формата **не baseline**, views не CTR |
| https://www.youtube.com/watch?v=j95XD9N3o74 | Garagem 360, PT, car explanation | 2025-11-24, indexed ~500,156 views | Другой язык/формат; нет сопоставимой same-author медианы |
| https://www.youtube.com/watch?v=fRA94XznG6I | Info Station, EN, short | 2026-05-20, ~14,512 views, 42 likes | Даты и публичный count, baseline по соседним роликам не установлен |
| https://www.youtube.com/watch?v=wvyvop5Zdl0 | Demand Detroit, EN, corporate clip | 2026-07-27, ~111 views, 5 likes | Соседние корпоративные ролики в публичной выдаче ~57–114, но их длина и возраст могут отличаться; очень слабый сигнал |
| https://www.youtube.com/watch?v=t7Je_995cdI | 9000police, EN, MythBusters excerpt | 2010-07-26, ~157,498 views | Evergreen, не новый спрос |

**Свежие 30–90 дней:** найдено 2026-09 отраслевое изложение https://daxstreet.com/guide/414630/running-the-ac-in-car-costs-less-than-open-windows-at-highway-speed/ (примерно 2 мес до 21 Nov), но это article, **не** сопоставимое новое видео и не доказательство текущего роста. 2026 May reddit https://www.reddit.com/r/theydidthemath/comments/1tc8llm/request_in_a_car_using_the_ac_use_more_gas_but/ показывает реальный вопрос, но это 6 месяцев, не 30–90 days. Комментарии под роликами, транскрипты, exact video playback и paid vidIQ не доступны/не использовались: **UNVERIFIED**. Своей аналитики нет.

**Конкурентный вывод:** зрители уже знают тему, но *реальная пара машин с 75/80 mph crossover и точная MAX-cooling оговорка* даёт новую проверяемую последовательность. Ни просмотры крупнейшего MythBusters, ни views/subscribers ratio, ни просмотры/возраст не доказывают спрос или удержание нашего Short.

## 6. Ограничения и права

Использовать собственный текст и оригинальную будущую иллюстрацию, **не копировать кадры MythBusters, Consumer Reports, графики SAE и визуальные активы каналов**. Научные числа пересказываются как public documented facts. Настоящие permissions/hero reference bytes/voice rights/actual MP4 не проверены и до media stages не требуются. Никакого собственного эксперимента нет. Production selection/registration/independent review остаются отдельными этапами.
