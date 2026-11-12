# Analytics skill consultation — 2026-11-02

Coordinator personally used Google Chrome. URL: https://chatgpt.com/c/6ae7e9a2-2714-83eb-adeb-868baffd06d3

Immediately before request: model GPT-6 checked; visible mode “Extra High, 4 из 5.” Completed substantive answer fully read.

## Exact prompt
Ты — консультант в уже открытом ChatGPT Extra High; требование обращения выполнено, не открывай другой ChatGPT. Предыдущая процедура A/B сохранена. Новая одна узкая задача: минимальный переносимый навык ytv-youtube-analytics для первого разбора YouTube-канала после релиза. Нужен контракт получения и интерпретации данных, а не A/B, новые названия или монтаж. Входы: channel/video IDs, формат Shorts/long, источник и точный период/часовой пояс, дата снимка, изменения упаковки. Data API даёт lifetime view/like/comment counters, существующие OAuth Paper не имеют yt-analytics.readonly; Studio доступна read-only. Доступ не расширять автоматически. Надо различать просмотры Shorts и engaged views, CTR только по учтённым thumbnail impressions, просмотр/свайп в Shorts feed, retention, average view duration/percentage, источники трафика. Дай короткую практическую процедуру: какие минимальные поля сохранять, как выбирать сопоставимые окна/когорты, что делать с realtime/лагом/скрытыми и отсутствующими данными, какие решения допустимы при крошечной выборке; наблюдение/гипотеза/причинность отдельно. Как вернуть одну проверяемую следующую гипотезу, не придумывая универсальные пороги CTR/retention и не приписывая рост новой обложке IQ без теста. Канальные цели/проверки вынести в профиль. До 600 слов. Не исследуй сам канал и не исполняй эксперимент.

## Visible answer and prompt
Ты — консультант в уже открытом ChatGPT Extra High; требование обращения выполнено, не открывай другой ChatGPT. Предыдущая процедура A/B сохранена. Новая одна узкая задача: минимальный переносимый навык ytv-youtube-analytics для первого разбора YouTube-канала после релиза. Нужен контракт получения и интерпретации данных, а не A/B, новые названия или монтаж. Входы: channel/video IDs, формат Shorts/long, источник и точный период/часовой пояс, дата снимка, изменения упаковки. Data API даёт lifetime view/like/comment counters, существующие OAuth Paper не имеют yt-analytics.readonly; Studio доступна read-only. Доступ не расширять автоматически. Надо различать просмотры Shorts и engaged views, CTR только по учтённым thumbnail impressions, просмотр/свайп в Shorts feed, retention, average view duration/percentage, источники трафика. Дай короткую практическую процедуру: какие минимальные поля сохранять, как выбирать сопоставимые окна/когорты, что делать с realtime/лагом/скрытыми и отсутствующими данными, какие решения допустимы при крошечной выборке; наблюдение/гипотеза/причинность отдельно. Как вернуть одну проверяемую следующую гипотезу, не придумывая универсальные пороги CTR/retention и не приписывая рост новой обложке IQ без теста. Канальные цели/проверки вынести в профиль. До 600 слов. Не исследуй сам канал и не исполняй эксперимент.
…
Показать ещё
ChatGPT сказал:
ytv-youtube-analytics — минимальный skill

Назначение: первый анализ YouTube-канала после релиза, фиксация наблюдений и формирование одной проверяемой гипотезы. Без A/B-тестирования, изменения публикаций и самостоятельного расширения доступа.

1. Входной контракт
YAML
channel_id: string
video_ids: [string]
format: shorts | long
published_at: datetime
period:
  start: datetime
  end: datetime
  timezone: string
snapshot_at: datetime
sources: [data_api, studio_readonly]
packaging_changes:
  - timestamp: datetime
    element: title | thumbnail
    revision: string

Цели канала, целевые показатели и специальные проверки определяются внешним channel_profile.

2. Collect — получение данных

Data API: lifetime viewCount, likeCount, commentCount, время публикации, формат и идентификаторы.

Studio read-only, если показатели доступны:

views и engaged_views — отдельно. Для Shorts обычные просмотры не эквивалентны engaged views.

shown_in_feed, stayed_to_watch, swiped_away — воронка Shorts feed.

impressions, impressions_ctr — CTR только для учитываемых YouTube показов обложки, не всех просмотров и не всей Shorts feed-дистрибуции.

average_view_duration, average_percentage_viewed, audience_retention — с указанием формата, определения и базы расчёта.

traffic_sources, watch time, доступные разбивки.

Для каждой метрики сохранять value, unit, source, period, snapshot_at, status и числитель/знаменатель, когда применимо.

Отсутствующие, скрытые и задержанные показатели обозначать null с причиной. Никогда не заменять нулём.

Не использовать отсутствующий OAuth scope yt-analytics.readonly. Не расширять разрешения автоматически.

3. Normalize — сопоставимость

Сравнивать ролики одинакового формата и возраста относительно публикации: например, первые 24 часа с первыми 24 часами, а не lifetime одного с первым днём другого.

Учитывать источник трафика, географию, время публикации, изменения упаковки и определения метрик. При возможности формировать когорты по сопоставимым условиям.

Lifetime-счётчики Data API не считать готовой исторической аналитикой. Разницы между снимками обозначать как приблизительные изменения счётчиков, учитывая возможные корректировки платформы.

4. Validate — качество данных

Realtime считать предварительным.

Учитывать задержку обработки и последующие корректировки.

Не сравнивать показатели с разными знаменателями.

Не смешивать Shorts feed и thumbnail impressions.

Не интерпретировать скрытые или отсутствующие данные.

При недостаточной выборке снижать уверенность, а не придумывать универсальные пороги CTR и retention.

Если сопоставимых данных нет, вернуть insufficient_data с точным перечнем пробелов.

5. Interpret — вывод

Строго разделять:

Observation: измеренное значение или различие.

Hypothesis: проверяемое предположение о возможном объяснении.

Causality: причинный эффект, который нельзя устанавливать из простого сравнения до/после.

Исправление обложки IQ Short фиксировать как изменение упаковки. Рост после него, если он наблюдается, не доказывает эффект обложки.

При крошечной выборке допустимы проверка качества данных, описание сигналов и выбор следующей проверки. Недопустимы уверенное ранжирование и объявление победителей.

6. Recommend — одна следующая гипотеза

Вернуть максимум одну гипотезу, выбранную из наиболее существенного наблюдения, которое допускает проверку.

YAML
observation: string
hypothesis: string
expected_signal: string
comparison_cohort: string
measurement_window: string
verification_method: string
falsification_condition: string
confidence: low | medium | high
limitations: [string]

Гипотеза должна иметь конкретный ожидаемый сигнал и условие опровержения. Если данных недостаточно даже для её постановки, вернуть hypothesis: null, не выдумывая объяснение.

7. Persist — сохранение

Сохранять исходные значения, источники, периоды, snapshots, определения метрик, изменения упаковки, сопоставимые когорты, наблюдения, ограничения и единственную следующую гипотезу.

Историю не перезаписывать. Повторный запуск создаёт новый snapshot и сравнивает его с предыдущим.

Критерий готовности: skill возвращает воспроизводимый отчёт observations → limitations → one hypothesis, не смешивает разные метрики и не приписывает наблюдаемым изменениям недоказанную причинность.

ChatGPT может допускать ошибки. Проверяйте важную информацию.
Последний ответ




Уровень усилий рассуждения
Extra High

## Coordinator decision
Use source/period/denominator-aware collection and separate observations, hypotheses and causality. Verify metric definitions from official primary sources. Data API does not reliably identify Shorts by duration alone: use observed format/catalog evidence. Snapshot counters are not dated Analytics reports; do not reconstruct unobserved first-24h values. Existing Paper OAuth lacks analytics scope, so use available Studio read-only reports without expanding access.
