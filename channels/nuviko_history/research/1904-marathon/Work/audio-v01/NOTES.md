# Черновой микс v01

Статус: DRAFT / UNVERIFIED, не принят. Фактического прослушивания нет.

- Речь `../../Source/Voice/voice_en.mp3`, SHA-256 `423f3ead3931ddb74fcb7d63311d9f06b0a01610f1913dce77604c9c032f4115`, ElevenLabs channel voice в request receipt. `atempo=1.10` применён однократно; результат `voice_en_110_v01.wav`, SHA-256 `742603315e4459e8e985184855a6f3b07d5dd46375e5476895fa336f41d0e550`, 30,474521 с. В черновом миксе речь с 0,300 с.
- Музыка `../../Source/Music/thinking_music.mp3`, SHA-256 `891d3ea47e443e590a6562a1e2bff37c8830817b3cdf604091f92bfe87e5cc4f`, Thinking Music, Kevin MacLeod, ISRC USUAN1600060; [страница автора и CC BY 4.0](https://www.incompetech.com/music/royalty-free/index.html?isrc=USUAN1600060). Загружена с сайта автора; атрибуция в будущем описании обязательна, указать обрезку и сведение. Проверить выбранный отрезок на слух и соответствие истории.
- `mix_draft.wav`, SHA-256 `4463bb5c7c2130de065f42250d23f11739070477945bd60eb938377fe6fea4c4`: тестовый общий микс, музыкальный gain 0,07, fade in 0–0,3, fade out 30,5–31,5 с; речь delay 0,3 с. Баланс, произношение, вход и выход не проверены на слух. Это не приёмка микса.
- Provider word map находится в `../../Source/Voice/word_times_source_v01.json`; конформ должен быть `0.3 + source / 1.10`, затем проверка соответствия измеренной записи, порядка и границ слов и привязка к hash точного принимаемого микса. Provider timing — оценка, не прослушивание.
