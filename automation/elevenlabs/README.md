# ElevenLabs adapter

Голос берётся из проверенного `channels/<id>/channel.json`, `voice.provider/id`. Список каналов не зашит в CLI. Не менять голос на default другого канала; перед платным запросом проверить доступность exact ID, бюджет и task scope. [Audio standard](../../docs/standards/audio.md) задаёт скорость, полный mix и проверки.

```bash
python3 automation/elevenlabs/tts.py --help
```

`--channel` обязателен; необязательный `--voice-id` проверяет совпадение. Без `--generate` helper выполняет локальную подготовку без сетевой генерации. Для новой run запускать через guarded media adapter, а не считать `--generate` пользовательским approval.

Сохранить exact input/hash, provider/model/settings, request/history handle, аудио и alignment. Existing results/receipts не перезаписывать. Неизвестный outcome после отправки требует reconcile истории провайдера; новый платный запрос не является восстановлением старого.

Текущий helper использует свой явно заявленный output format; возможности provider account могут отличаться. Native alignment/MP3 response не доказывают произношение, скорость, слуховой sync или качество final mix. Одну корректировку производить минимально и обновлять зависимые timings/checks.

Проверки: `python3 -m unittest discover -s automation/elevenlabs -p 'test_*.py'`. Unit tests не подтверждают доступ живого аккаунта.
