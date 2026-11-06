#!/usr/bin/env python3.11
"""Install skill links and maintain generated AGENTS routers; preserve user-owned files."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
registry = json.loads((ROOT / '.agent/episode-registry.json').read_text())
entries = registry.get('episodes', registry.get('entries'))
layout = json.loads((ROOT / '.agent/channel-layout.json').read_text())
channel_rules = {c['registry_label']: c['path'] + '/AGENTS.md' for c in layout['channels']}
targets = {ROOT: None}
for channel in layout['channels']:
    for suffix in ('', '/videos'):
        path = ROOT / (channel['path'] + suffix)
        if path.is_dir():
            targets[path] = channel['registry_label']
for relative in (layout['unclassified'], layout['legacy_router']):
    targets[ROOT / relative] = 'UNVERIFIED' if relative == layout['unclassified'] else None
missing = []
for entry in entries:
    for key in ('path', 'canonical_path'):
        path = ROOT / entry[key]
        assert path.is_relative_to(ROOT), path
        if not path.is_dir():
            missing.append(entry[key])
            continue
        previous = targets.get(path)
        assert previous in (None, entry['channel']), f'Conflicting channel: {path}'
        targets[path] = entry['channel']

archive = ROOT / '.agent/entrypoints.json'
previous = json.loads(archive.read_text()) if archive.exists() else {'created_links': [], 'created_routers': []}
new_links = new_routers = 0
for path, channel in sorted(targets.items()):
    if path != ROOT:
        link = path / '.agents/skills'
        canonical = ROOT / '.agents/skills'
        if link.is_symlink():
            assert link.resolve() == canonical, f'Unexpected existing symlink: {link}'
        elif link.exists():
            assert link.resolve() == canonical, f'Existing separate skill directory: {link}'
        else:
            link.parent.mkdir(exist_ok=True)
            link.symlink_to(os.path.relpath(canonical, link.parent), target_is_directory=True)
            previous['created_links'].append(str(link.relative_to(ROOT)))
            new_links += 1
    agents = path / 'AGENTS.md'
    if agents.exists() and '<!-- ytvideos-entrypoint-router:v1 -->' not in agents.read_text():
        continue
    channel_line = ''
    if channel in channel_rules:
        channel_line = f'Канал: {channel}. Обязательно прочитать [правила канала]({ROOT}/{channel_rules[channel]}).\n'
    elif channel == 'UNVERIFIED':
        channel_line = 'Канал не установлен (UNVERIFIED). Не назначать стиль/голос по slug; установить канал по фактическим материалам до зависящих от него действий.\n'
    else:
        channel_line = 'Здесь несколько выпусков/каналов: определить конкретный через реестр, не переносить общий стиль на весь каталог.\n'
    text = (f'# Точка входа ytvideos\n\n'
            '<!-- ytvideos-entrypoint-router:v1 -->\n\n'
            f'Сначала прочитать [корневой AGENTS.md]({ROOT}/AGENTS.md), затем [обязательный bootstrap]({ROOT}/.agent/CHANNEL_BOOTSTRAP.md).\n\n'
            f'Рабочий путь: `{path.relative_to(ROOT)}`. Найти его в [реестре]({ROOT}/.agent/episode-registry.md), перейти к canonical-каталогу. Читать current_context и только нужные действию сведения из state_sources по bootstrap.\n\n'
            + channel_line + '\n'
            f'Процедуру выбрать в [каталоге skills]({ROOT}/.agent/skill-catalog.md). `.agents/skills` здесь — ссылка на единственный канонический набор, а не отдельная версия. Этот файл не даёт новых разрешений и не меняет состояние выпуска.\n')
    if not agents.exists():
        previous['created_routers'].append(str(agents.relative_to(ROOT)))
        new_routers += 1
    agents.write_text(text)
previous['managed_entrypoints'] = [str(p.relative_to(ROOT)) for p in sorted(targets)]
previous['missing_registered_directories'] = sorted(set(missing))
archive.parent.mkdir(parents=True, exist_ok=True)
archive.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'entrypoints': len(targets), 'new_links': new_links, 'new_routers': new_routers, 'missing_registered_directories': sorted(set(missing))}))
