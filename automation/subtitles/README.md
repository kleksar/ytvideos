# Прозрачный subtitle layer

`nuviko_long_subtitles.py` создаёт слой по проверенной cue map. Semantic grouping находится в [helper](../helpers/paper-subtitles/scripts/semantic_grouping.py); общий стандарт — [audio](../../docs/standards/audio.md). Nuviko freeze сохраняется.

```bash
python3 automation/subtitles/nuviko_long_subtitles.py --help
```

`--plan-only` готовит план без полного video render. `--preserve-groups` сохраняет уже принятые группы после проверки width/sentence/boundary constraints. Обычный проход применяет sentence-first grouping; он не заменяет прочтение групп и sync по звуку.

Вход содержит actual FPS/canvas/audio hash/word times/style/cues. Генератор не создаёт alignment. Выход в новый owned directory: states, `segmented_cue_map.json`, concat, alpha video/receipt по выбранному режиму. Не менять imported dependencies. Обычный production montage использует общий renderer и его subtitle contract; альтернативный слой не создаёт вторую процедуру утверждения.
