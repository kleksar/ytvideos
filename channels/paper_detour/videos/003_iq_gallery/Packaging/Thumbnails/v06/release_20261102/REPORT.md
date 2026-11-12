# IQ v06 — применённая обложка, 2 ноября 2026

Пользователь принял вариант v06 и прямо поручил заменить обложку `xYS2XBeR_Jc` канала Paper Detour (`UCMVfdfaNxV3ZkI3_J3Eejzw`). Точный JPG: `../iq_cover_v06_2160x3840.jpg`, SHA-256 `29f1aa9a9f538caee10247577ad449e357b231cb7b8f1b2f9adb0ee17dabd889`.

**Статус: applied_verified — API и осмотренная публичная desktop-карточка.** [Видео](https://youtube.com/shorts/xYS2XBeR_Jc).

Одна команда `upload.py set-thumbnail`, без повторной mutation и без UI-записи. Предварительно проверены фактический владелец, `youtube.upload` + `youtube.readonly`, принадлежность видео и хэш принятого файла. [API квитанция](api_set_receipt.json): `api_set_accepted=true`, `readback=matched`. [До](api_before.json), [после](api_after.json), [проверка сохранности](preservation_check.json): различий вне thumbnails нет; public, название, описание, Tags, языки и остальные прочитанные snippet/status/contentDetails сохранены. Членства плейлистов этим чтением не перепроверялись и не менялись.

Координатор лично увидел WHICH IQ / ESTIMATE / SURPRISES YOU? после reload [Studio](studio_after_reload.jpg) и в [публичной ленте Shorts](public_shorts_desktop.jpg). [Карточка с названием](public_iq_card.jpg): примерно 209×313 CSS px, полученный портрет 405×608; вся надпись и все 13 портретов видны. Это фактическое отображение YouTube, а не локальный HTML.

Запрошенная эмуляция viewport 390×844 не применилась: фактический viewport остался 2056×1147, DPR 2 — [измерение](viewport_attempt.json). Override сброшен. Поэтому физический телефон и live mobile-layout не объявляются проверенными; ранее выполнены [локальные уменьшения и crop QA](../REPORT.md). Открытые source PNG и исходное видео не изменялись, нового звука или монтажа не было. Независимый review не выполнялся.

Для этого IQ отдельная Shorts selection через Studio не потребовалась: API-результат подтверждён фактической целевой карточкой. Известный capability gap другого выпуска не является основанием повторно менять уже правильную обложку. Общее правило остаётся у youtube-upload/API adapter; навыку обложек передаётся ссылка на проверенную поверхность и её границы. Рост CTR/просмотров этой заменой ещё не доказан.
