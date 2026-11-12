# CLI/API 4K — готовые команды

2026-11-02 пользователь явно выбрал CLI с явными параметрами. Scope: те же три Paper Detour сцены из `prompts.json`; без новых творческих решений. Режим CLI `edit` используется для передачи двух файлов стилевых эталонов, а не для создания независимого SDK runner.

Параметры: `gpt-image-2`, `3840x2160`, `high`, `png`, один результат на prompt, без resize/augmentation. Prompts вынесены в отдельные текстовые файлы без изменения текста.

Проверка окружения: `OPENAI_API_KEY` отсутствует, uv доступен; Python-пакет openai в системном Python не установлен, поэтому команды используют `uv run --with openai` для штатного временного окружения зависимостей. Ключи не выводились. Dry run первой команды через bundled CLI прошёл и показал size=3840x2160, quality=high, model=gpt-image-2 и оба референса. Это проверка сборки запроса, не подтверждение доступности модели/размера в API. Реальных API-запросов не было; новые 4K PNG пока отсутствуют.

Для реального запуска сначала локально задать `OPENAI_API_KEY` в окружении процесса либо в локальном конфигурационном файле, путь к которому можно передать координатору без раскрытия ключа в чате. Затем выполнить:

```bash
uv run --with openai python /Users/diplomat/.codex/skills/.system/imagegen/scripts/image_gen.py edit \
  --model gpt-image-2 \
  --prompt-file /Users/diplomat/ytvideos/new_channel/Experiments/20261102_4k_scene_test/01_harbor_prompt.txt \
  --image /Users/diplomat/ytvideos/new_channel/Shared/References/Paper/paper004_user_38.png \
  --image /Users/diplomat/ytvideos/new_channel/videos/033_time_stop/Source/Images/paper_v01/S01_v01.png \
  --size 3840x2160 --quality high --output-format png --no-augment \
  --out /Users/diplomat/ytvideos/new_channel/Experiments/20261102_4k_scene_test/cli_4k/01_harbor.png
```

```bash
uv run --with openai python /Users/diplomat/.codex/skills/.system/imagegen/scripts/image_gen.py edit \
  --model gpt-image-2 \
  --prompt-file /Users/diplomat/ytvideos/new_channel/Experiments/20261102_4k_scene_test/02_fox_prompt.txt \
  --image /Users/diplomat/ytvideos/new_channel/Shared/References/Paper/paper004_user_38.png \
  --image /Users/diplomat/ytvideos/new_channel/videos/033_time_stop/Source/Images/paper_v01/S01_v01.png \
  --size 3840x2160 --quality high --output-format png --no-augment \
  --out /Users/diplomat/ytvideos/new_channel/Experiments/20261102_4k_scene_test/cli_4k/02_fox.png
```

```bash
uv run --with openai python /Users/diplomat/.codex/skills/.system/imagegen/scripts/image_gen.py edit \
  --model gpt-image-2 \
  --prompt-file /Users/diplomat/ytvideos/new_channel/Experiments/20261102_4k_scene_test/03_watchmaker_prompt.txt \
  --image /Users/diplomat/ytvideos/new_channel/Shared/References/Paper/paper004_user_38.png \
  --image /Users/diplomat/ytvideos/new_channel/videos/033_time_stop/Source/Images/paper_v01/S01_v01.png \
  --size 3840x2160 --quality high --output-format png --no-augment \
  --out /Users/diplomat/ytvideos/new_channel/Experiments/20261102_4k_scene_test/cli_4k/03_watchmaker.png
```

После ответа API измерить реальные размеры PNG, открыть каждый файл, проверить детали относительно эталонов и зафиксировать SHA-256. Нативный 4K пока не подтверждён. Стандарты проекта не изменялись.

