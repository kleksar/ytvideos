# Озвучка Paper Detour 049 — скорость

- Принятый текст: `Source/Script/narration_en_v26.md` (431 слова).
- Канальный голос: Lawrence, `ktkP7Nsj67dw2zcplQYt`; ElevenLabs `eleven_v4`; исходный файл MP3 44.1 kHz mono; скорость генерации не задана.
- Исходник: `Source/Voice/en_v26/voice_en.mp3`; character alignment: `Source/Voice/en_v26/voice_en.alignment.json`.
- Применена одна операция FFmpeg `atempo=1.10`; финальный speech mix: `Source/Audio/narration_en_v26_110.wav`, PCM S16LE, 44.1 kHz mono.
- Тайминги character alignment преобразованы делением на 1.10 и собраны в word map `Edit/Timebase/word_times_en_v26_110.json`. Это преобразование сохраняет временную привязку как машинную оценку, но не подтверждает слышимую синхронизацию.
