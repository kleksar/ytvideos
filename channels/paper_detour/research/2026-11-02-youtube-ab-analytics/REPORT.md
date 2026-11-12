# Paper Detour — A/B и аналитика, 2 ноября 2026

Созданы переносимые [ytv-youtube-ab-testing](../../../.agents/skills/ytv-youtube-ab-testing/SKILL.md) и [ytv-youtube-analytics](../../../.agents/skills/ytv-youtube-analytics/SKILL.md), у каждого отдельный профиль Paper. Подключены каталог, bootstrap, карта владельцев, production, release и владельцы упаковки. Личные последовательные консультации Extra High: [контракт A/B](../../../.agent/consultations/paper_ab_skill_20261102.md), [контракт аналитики](../../../.agent/consultations/paper_analytics_skill_20261102.md), [интерпретация baseline](../../../.agent/consultations/paper_analytics_baseline_20261102.md). Первый A/B ответ не загрузился; один короткий повтор дал полный результат. Консультации не заменяют первичные источники или независимый review.

## Применение IQ закрыто

Пользователь принял v06; одна API mutation проверена в reload Studio и публичной Shorts-карточке — [квитанция](../../videos/003_iq_gallery/Packaging/Thumbnails/v06/release_20261102/REPORT.md). Остальные прочитанные поля сохранены. Live mobile viewport не применился, физическое устройство не проверено; desktop-показ подтверждён. Правило фактической Shorts-поверхности уточнено у canonical thumbnail owner.

## Действующий A/B

[Радио 0RaC4t7yn5o](../../videos/001_radio_game/Packaging/Experiments/AB_CURRENT_20261102.md): active / pending, три пары названий и обложек. Доли времени просмотра «—», ожидаемый остаток на снимке 12 дней 11 часов. Победитель не установлен, тест не менялся. [Скриншот](radio_test.jpg) и [URL фактических превью](radio_variant_assets.json) сохранены. Хэши локальных мастеров заново не установлены.

[Официальная функция](https://support.google.com/youtube/answer/16391400?hl=en) не поддерживает Shorts; native результат основан на watch time/share. Замена IQ — редакционная правка, не A/B-доказательство. В [публичной Data API discovery](api_ab_coverage.json) не найден endpoint эксперимента; native операция имеет документированную границу Studio. Новых тестов или расписаний не запускалось.

## Первый baseline

[Data API snapshot](api_catalog_baseline.json): **14 uploads, 11 public**. В реально осмотренной публичной вкладке — 10 Shorts, плюс один радио-фильм. Три непубличных upload исключены из public-инвентаря. Новый Taj Mahal уже входит в актуальные 11; прежний аудит десяти видео не подменяет текущий каталог. Формат не выводился из одной длительности.

Накопленные Data API counters: ирландская история — 303, радио-сигнал — 192, MSX — 83, IQ — 3, радио-фильм — 13. Полный инвентарь с capture time и остальными значениями сохранён в JSON. Это разные возраста публикации, **не рейтинг эффективности**.

Оба действующих Paper OAuth файла не содержат `yt-analytics.readonly`; доступ не расширялся. Data API baseline не выдаётся за полную Analytics API выгрузку. Прочитаны Studio reports: [обзор](channel_overview.txt), [Shorts](shorts_content.txt), [Video-on-demand](long_content.txt); значения и missing statuses в [studio_baseline.json](studio_baseline.json), скриншоты рядом.

**Studio, выбранный период 4–31 октября 2026:**

| Scope | Наблюдение |
|---|---|
| Channel overview, без privacy-фильтра | 59 просмотров, 0,4 ч, +1 подписчик |
| Realtime отдельно | 709 просмотров за последние 48 ч, предварительно |
| Shorts | 50 просмотров; 23 engaged views; 72% трафика из Shorts feed и 4% из поиска |
| Shorts reaction | 57,9% продолжили / 42,1% не стали смотреть; absolute feed denominator не показан |
| Video-on-demand channel | 9 просмотров, 17 thumbnail impressions, CTR «—», AVD 1:02 |
| Radio row in overview | 5 просмотров, AVD 0:50 / 19,2% в данном периоде |

Часовой пояс интерфейс в этих экранах не показал. Realtime, lifetime counters и dated report не сравниваются как одинаковые окна. Все VOD totals не приписываются одному public-фильму; «—» не заменён нулём. Retention curves не просматривались, first-24h cohort не выгружена. Метрики слишком малочисленны для уверенного выбора лучшего сюжета или причинного вывода. Эффект новой IQ-обложки не установлен — [эпизодный baseline](../../videos/003_iq_gallery/Analytics/BASELINE_20261102.md).

## Следующая измеримая проверка

Одна наблюдательная гипотеза: сохранятся ли различия lifetime-счётчиков Shorts при сравнении реально доступных первых 24 часов после публикации с одинаковыми определениями/часовым поясом и отдельными engaged views/источниками трафика? Сигнал против гипотезы — различия/порядок не воспроизводятся в сопоставимых окнах. При крошечной выборке это всё равно не причинный тест и не доказанный рейтинг. Если Studio не предоставляет нужную выгрузку или ролику ещё нет 24 часов — `insufficient_data`, а не восстановление из lifetime counters. Это сохранённая контрольная точка, **не обещание автоматического будущего запуска**.

Новый эксперимент не нужен для продолжения производства. Следующий производственный этап плана — переносимость сценовых изображений и полный пилот с текущего принятого состояния своего выпуска; длинный радио-тест остаётся отдельным состоянием.

## Источники и проверка

[Native A/B](https://support.google.com/youtube/answer/16391400?hl=en), [thumbnail impressions](https://support.google.com/youtube/answer/9314486?hl=en), [Reach](https://support.google.com/youtube/answer/9314355?hl=en), [Content by format](https://support.google.com/youtube/answer/12942217?hl=en), [Analytics metrics](https://developers.google.com/youtube/analytics/metrics), [reports.query](https://developers.google.com/youtube/analytics/reference/reports/query), [Data API video statistics](https://developers.google.com/youtube/data/reference/rest/v3/videos#statistics). Проверены 2 ноября 2026; определения API и конкретных Studio карточек не объявлялись идентичными автоматически.

Новые навыки проверены на inspect/baseline кейсах этого прохода; native start/stop/manual selection не выполнялись. Самопроверка не называется независимым review. Наличие навыков и symlink discovery не доказывает будущий выбор навыка моделью или автоматически созданную задачу мониторинга.

Проверки реализации: quick_validate прошли оба новых навыка и четыре затронутых владельца; проверены 240 локальных ссылок и актуальные registry paths. Installer подтвердил 49 общих точек входа без новых копий; канальный и IQ/radio входы разрешают оба навыка к canonical файлам. Проверены сохранность хэшей IQ и отсутствие отличий вне thumbnails, полный текст трёх консультаций, active/pending без mutation у радио, null CTR и раздельные периоды baseline. Native skills/list в текущих инструментах не доступен; filesystem discovery проверено, будущий автоматический выбор не тестировался.
