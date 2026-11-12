# YouTube API: новый Nuviko History

Статус: **CONNECTED_VERIFIED**, 2 ноября 2026.

- Назначение: `UCbyLx6Rf3iWww4bPZJ2oo2A`, Nuviko History, `@Nuviko_History`.
- Профиль назначения: `nuviko_history` в `automation/channels.json`.
- Cloud-проект: `YT Videos` / `yt-videos-513009`; его владелец `google@kleksar.me` проверен в IAM. Существующий OAuth-клиент сохранён.
- Владелец канала: `glavred.journalist@gmail.com`; добавлен в Test users, прежние две записи сохранены.
- Пользователь явно подтвердил выдачу трёх YouTube scopes. На том же экране согласия нажато «Продолжить».
- Получены `youtube.upload`, `youtube.readonly`, `youtube.force-ssl`. Последний scope технически включает удаление; текущая задача не поручала удаление.
- `channels.list(mine=true)` вернул ровно канал назначения. Отдельно проверен refresh token: обновление без повторного входа успешно; затем повторно проверен точный channel ID.
- Credential сохранён вне проекта: `~/.local/share/story-youtube/nuviko-history/token.json`, права `0600`, каталог `0700`. Один токен содержит scope загрузки и управления, поэтому оба поля профиля указывают на него.
- Старый профиль `history` продолжает указывать на источник `UCqct_dth0WSCwiDZx1WMfgg`; его значения и Paper сохранены без изменений.

[Результат проверки API](API_VERIFIED.json). [Состояние до добавления профиля](channels_before.json). Изменения YouTube-видео, загрузка и публикация не выполнялись. Доступ и refresh проверены; сам upload, обработка, субтитры и будущий финальный файл ещё не проверены.

Приложение остаётся External/Testing. Для YouTube scopes Google ограничивает срок refresh token в этом режиме семью днями; это отдельное ограничение будущей постоянной автоматизации. Перевод приложения в Production и верификация сейчас не поручены и не выполнялись.

Процедура: project release → API adapter README → global youtube-upload. При будущей загрузке использовать явный ID назначения и новый профиль, начинать с Private; доступ на публикацию требует отдельного поручения.

Sources: [Desktop OAuth](https://developers.google.com/youtube/data/guides/auth/installed-apps), [OAuth token expiration](https://developers.google.com/identity/protocols/oauth2#expiration).
