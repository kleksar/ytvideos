# Image motion runtime

Этот отдельный runtime использует Python 3.12.x и зависимости, закреплённые в `pyproject.toml` и `uv.lock`.

Из корня репозитория:

```sh
uv sync --project automation/image_motion --python 3.12
uv run --project automation/image_motion python automation/image_motion/run.py --help
```

Первый запуск `uv sync` скачивает пакеты из Python package registry. Реальный рендер также может потребовать сетевую загрузку больших моделей и значительное место на диске; сам source-only клон не содержит этих моделей, media и release bundles. Не запускайте рендер до передачи входных файлов, проверки требований канала и свободного места.
