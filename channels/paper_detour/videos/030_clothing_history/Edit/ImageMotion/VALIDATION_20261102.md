# Проверка общего image-motion pipeline — 2026-11-02

Поручение: общий CLI, пресеты, skill и место в production flow. Звук не генерировался. Механическая реализация ранее принятого движения030; разрешение пропустить Extra High сохранено в CURRENT_CONTEXT выпуска.

## Реальный Palmier smoke test

- Source: project `B1BA2D18`, baseline `A7C273C5` с39still scenes,190с,1920×1080,30fps.
- Config: [motion.json](motion.json), оригинальные PNG/framing и привязки: [sources.json](sources.json). Полный `plan` успешно разрешил все39сцен, включая повторяющийся исходник.
- Проверенная команда: `python3 automation/image_motion/run.py apply --config channels/paper_detour/videos/030_clothing_history/Edit/ImageMotion/motion.json --limit 2`.
- Проверенный target: **1229EF38**. Первые2сцены заменены на depth video; остальные37сцен сохранены. Исходник не менялся.
- Структурная сверка: PASS, включая порядок tracks, все интервалы, camera keys и все остальные дорожки/их clip properties. Duration190с не сокращался ради теста.
- [run.json](e6a4a326836a85a86028/run.json) содержит snapshots, source/result fingerprint, hashes, параметры и отдельные QA; [receipts](e6a4a326836a85a86028/receipts.jsonl) — реальные API-ответы.
- Два реальных1080pMP4 полностью декодированы:134кадра каждый,132различных видимых кадра и2резервных. Видимые интервалы132кадра сохранены; дополнительных звуковых streams нет.
- Визуально просмотрены кадры0/66/131 каждого scene render: [контактный лист](e6a4a326836a85a86028/render_samples.png). Это проверка исходных scene videos; составной timeline/export не просматривался целиком. **Full AV/playback: UNVERIFIED.**
- Повтор той же команды вернул `unchanged`, тот же1229EF38, без рендера/клона/повторного0.75. Изменение скрипта, не меняющее plan/renderer/version, не создаёт новый run.
- Подготовка глубины повторно подтвердила2cache hits. Точное содержимое было вычислено в постоянном runtime сDepthFlow1.0.1; временный старый env не используется.

## Исправленные особенности API

Первый диагностический clone `E0DBD349` остановился до перезаписи сцен: clone меняет также `trackId`, что теперь исключено из сравнения идентичности. Второй `A1F53C08` остановился на финальной проверке: API опускает `mediaType` для default video. Это учтено в валидаторе. Оба диагностических timeline сохранены, актуальный проверенный результат — только1229EF38. Повтор неизвестных мутаций не выполнялся.

## Автоматические проверки

Реальный synthetic9:16render180×320,30fps прошёл ffprobe:12видимых+2резервных кадра; второй вариант15+2. Направление sign−1 отрендерено; изменение только camera_factor переиспользовало тот же MP4, изменение duration создало другой MP4 с той же глубиной. [Квитанция](portrait_cache_validation.json). Reverse-cache для противоположного направления также прошёл:12видимых кадров развернуты до добавления2резервных, около0.22с в этом маленьком тесте. Это проверка renderer/cache, не художественная приёмка портретного фильма.

Семь unit tests: сохранение midpoint при0.75, различение zoom и pan, все направления, отказ на сложном пути, текущие duration с media binding, детектирование изменения чужого track и clone identity. Новый skill прошёл quick_validate. Все новые ссылки проверены; root/channel/episode discovery paths разрешаются к одному canonical skill. Native future auto-selection не заявляется проверенным.

Production flow обновлён: намерение движения при storyboard; depth cache после приёмки PNG; один apply после окончательного timing/cues/микса, перед экспортом и финальным QA. Framing030не превращён в универсальный crop preset. Все39сцен фактически не рендерились в этом smoke test.

После пользовательской очистки служебных слоёв прежние source/result fingerprints исторические. Текущие основной монтаж, акценты и звук проверены отдельно в общей квитанции `.agent/OVERLAY_CLEANUP_20261102.json`. Новый render требует нового полного playback; автоматические проверки и skill validation повторно пройдены.
