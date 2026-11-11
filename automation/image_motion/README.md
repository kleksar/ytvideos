# Дополнительный image-motion runtime

Средства в этом каталоге имеют отдельные зависимости `pyproject.toml`/`uv.lock` и используются только в явно поддержанном recipe. Общие Paper/Nuviko scenes применяют цельный pan/zoom в [FFmpeg montage](../ffmpeg_montage/README.md); segmentation/parallax не включаются ради доступности другого инструмента.

```bash
uv run --project automation/image_motion python automation/image_motion/run.py --help
```

Перед реальным запуском проверить установленные зависимости, models, media, место и scope. Загрузка больших моделей и наличие runtime сами по себе не доказывают подходящий художественный результат или разрешение на платное действие.
