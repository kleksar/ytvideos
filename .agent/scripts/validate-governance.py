#!/usr/bin/env python3.11
"""Read-only validation of current ytvideos instructions, routes and discovery."""
from pathlib import Path
import hashlib
import json
import re
import sys
import tomllib
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
errors = []
checks = {}


def check(ok, message):
    if not ok:
        errors.append(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


skills = sorted((ROOT / '.agents/skills').glob('*/SKILL.md'))
names = []
for path in skills:
    text = path.read_text()
    check(any(link in text for link in ('../../../.agent/CHANNEL_BOOTSTRAP.md', str(ROOT / '.agent/CHANNEL_BOOTSTRAP.md'))),
          f'Missing mandatory channel bootstrap: {path}')
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    check(match is not None, f'Missing frontmatter: {path}')
    if match:
        name = re.search(r'^name: (.+)$', match[1], re.M)
        desc = re.search(r'^description: (.+)$', match[1], re.M)
        check(bool(name and desc), f'Missing metadata: {path}')
        if name:
            names.append(name[1])
            check(name[1] == path.parent.name, f'Name/path mismatch: {path}')
check(len(names) == len(skills) and len(set(names)) == len(skills), 'Expected unique local skill names')
catalog = (ROOT / '.agent/skill-catalog.md').read_text()
registered_skills = set(re.findall(r'\]\(\.\./\.agents/skills/([^/]+)/SKILL\.md(?:#[^)]*)?\)', catalog))
check(set(names) == registered_skills, 'Local skill inventory differs from canonical catalog')
global_names = set()
for path in (Path.home() / '.codex/skills').glob('*/SKILL.md'):
    match = re.search(r'^name: (.+)$', path.read_text(), re.M)
    if match:
        global_names.add(match[1].strip('"\''))
check(not set(names) & global_names, 'Local/global skill name collision')
checks['skills_unique'] = len(skills)

roles = sorted((ROOT / '.codex/agents').glob('*.toml'))
for path in roles:
    data = tomllib.loads(path.read_text())
    check(all(data.get(k) for k in ('name', 'description', 'developer_instructions')), f'Incomplete role: {path}')
    check(data.get('name') == path.stem, f'Role name mismatch: {path}')
    check(not set(data) - {'name', 'description', 'developer_instructions'}, f'Unexpected runtime override: {path}')
checks['roles_parsed'] = len(roles)
check(len(roles) == 14, 'Expected fourteen current production roles')

manifest = json.loads((ROOT / '.agent/archive/before-skills-20261101/manifest.json').read_text())
for entry in manifest:
    check(digest(ROOT / entry['archive']) == entry['sha256'], f'Archive checksum: {entry["archive"]}')
checks['archive_checksums'] = len(manifest)
cleanup_manifest = json.loads((ROOT / '.agent/archive/before-current-docs-20261101/manifest.json').read_text())
for entry in cleanup_manifest:
    check(digest(ROOT / entry['archive']) == entry['sha256'], f'Cleanup archive checksum: {entry["archive"]}')
checks['cleanup_archive_checksums'] = len(cleanup_manifest)

migration = json.loads((ROOT / '.agent/migration-map.json').read_text())
source = ROOT / migration['source']
check(digest(source) == migration['source_sha256'], 'Original AGENTS checksum')
lines = source.read_text().splitlines(keepends=True)
covered = list(range(migration['preamble_lines'][0], migration['preamble_lines'][1] + 1))
snapshots = 0


for entry in migration['sections']:
    covered.extend(range(entry['start_line'], entry['end_line'] + 1))
    if 'block_sha256' in entry:
        block = ''.join(lines[entry['start_line'] - 1:entry['end_line']])
        check(hashlib.sha256(block.encode()).hexdigest() == entry['block_sha256'], f'Block checksum: {entry["heading"]}')
        destination = ROOT / entry['destination']
        check(destination.exists(), f'Missing migrated status: {destination}')
        if destination.exists():
            text = destination.read_text()
            marker = '## ' + entry['heading']
            check(marker in text, f'Missing snapshot heading: {destination}')
            if marker in text:
                # Current episode records may evolve; original bytes are verified
                # in the immutable source and block hashes above.
                snapshots += 1
check(sorted(covered) == list(range(1, len(lines) + 1)), 'Original line coverage has gaps/overlap')
checks['original_lines_accounted'] = len(lines)
checks['episode_status_destinations'] = snapshots
for entry in migration.get('embedded_episode_records', []):
    original = lines[entry['source_line'] - 1].strip()
    relocated = original.replace('new_channel/', 'channels/paper_detour/')
    text = (ROOT / entry['destination']).read_text()
    check(original in text or relocated in text, 'Lost embedded episode record')
generic = Path.home() / '.codex/skills/youtube-upload/SKILL.md'
generic_archive = ROOT / '.agent/archive/before-skills-20261101/user-skills/youtube-upload/SKILL.md'
check(generic.read_bytes() == generic_archive.read_bytes(), 'Generic youtube-upload changed during migration')
registry = json.loads((ROOT / '.agent/episode-registry.json').read_text())
entries = registry.get('episodes', registry.get('entries'))
for entry in entries:
    check((ROOT / entry['path']).exists(), f'Missing registered directory: {entry["path"]}')
    check((ROOT / entry['canonical_path']).exists(), f'Missing canonical directory: {entry["canonical_path"]}')
    for record in entry['records']:
        check((ROOT / record).is_file(), f'Missing episode record: {record}')
    for field in ('current_context', 'state_sources', 'history'):
        check(field in entry, f'Missing scoped context {field}: {entry["path"]}')
        for record in entry.get(field, []):
            check((ROOT / record).is_file(), f'Missing {field} record: {record}')
    check(not any('AGENTS_STATUS_' in p for p in entry['current_context']), f'Historical snapshot in mandatory context: {entry["path"]}')
    check(set(entry['records']) <= set(entry['current_context'] + entry['state_sources']), f'Lost state source: {entry["path"]}')
checks['episodes_indexed'] = len(entries)
checks['channels_unverified'] = sum(e['channel'] == 'UNVERIFIED' for e in entries)

entrypoints = json.loads((ROOT / '.agent/entrypoints.json').read_text())
entry_agents = []
for relative in entrypoints['managed_entrypoints']:
    base = ROOT / relative
    path = base / 'AGENTS.md'
    check(path.is_file(), f'Missing instruction entry point: {relative}')
    check((base / '.agents/skills').resolve() == ROOT / '.agents/skills', f'Wrong skill entry point: {relative}')
    if path.exists():
        text = path.read_text()
        check('CHANNEL_BOOTSTRAP.md' in text, f'Entry point omits channel bootstrap: {relative}')
        entry_agents.append(path)
for entry in entries:
    router = ROOT / entry['path'] / 'AGENTS.md'
    if not router.is_file():
        continue  # The missing registered directory is reported above.
    text = router.read_text()
    layout = json.loads((ROOT / '.agent/channel-layout.json').read_text())
    expected_channel = next((c['path'] + '/AGENTS.md' for c in layout['channels'] if c['registry_label'] == entry['channel']), '')
    if entry['channel'] == 'UNVERIFIED':
        check('UNVERIFIED' in text, f'Unknown channel silently assigned: {entry["path"]}')
    else:
        check(expected_channel in text and entry['channel'] in text, f'Wrong channel router: {entry["path"]}')
checks['entrypoints_bootstrapped'] = len(entry_agents)
native = json.loads((ROOT / '.agent/channel-layout-discovery.json').read_text())
check(native['pass'] and native['no_thread_or_turn_started'], 'Native discovery probe failed or used model turns')
check({row['cwd'] for row in native['cwds']} == {str(ROOT / p) for p in entrypoints['managed_entrypoints']}, 'Native probe does not cover managed entry points')
native_hashes = native.get('skill_file_sha256', {})
check(set(native_hashes) == {str(path.relative_to(ROOT)) for path in skills}, 'Native probe skill inventory differs from current skills')
for path in skills:
    relative = str(path.relative_to(ROOT))
    if relative in native_hashes:
        check(digest(path) == native_hashes[relative], f'Skill changed since native probe: {relative}')
checks['native_discovery_cwds_passed'] = sum(row['pass'] for row in native['cwds'])

files = [ROOT / p for p in ('AGENTS.md', 'channels/paper_detour/AGENTS.md', 'channels/nuviko_history/AGENTS.md', 'channels/nuviko_stories/AGENTS.md', '.codex/agents/README.md',
         'channels/paper_detour/RAROVISTA_PRODUCTION_GUIDE.md', 'channels/paper_detour/RAROVISTA_EDITING_STANDARD.md',
         'channels/paper_detour/docs/PAPER_DETOUR_CREW_WORKFLOW.md')]
files += skills + list((ROOT / '.agents/skills').glob('*/references/*.md'))
files += [p for p in (ROOT / '.agent').glob('*.md') if p.name != 'migration-ledger.md']
files += list((ROOT / '.agent/templates').glob('*.md'))
files += entry_agents + [ROOT / '.agent/discovery-checks-20261101/REPORT.md', ROOT / '.agent/consultations/20261101-discovery/README.md']
current_references = [ROOT / p for p in (
    'channels/paper_detour/RAROVISTA_INDEX.md', 'channels/paper_detour/brand/TYPOGRAPHY_STANDARD.md',
    'channels/paper_detour/brand/THUMBNAIL_PLAYBOOK.md', 'channels/paper_detour/docs/YOUTUBE_POSTS_PLAYBOOK.md',
    'channels/paper_detour/docs/SHORTS_RELEASE_STRATEGY.md', 'channels/paper_detour/docs/YOUTUBE_PLAYLISTS.md',
    'channels/nuviko_history/docs/HISTORY_STORY_PIPELINE.md', 'channels/nuviko_history/docs/STORYTELLING_STANDARD.md',
    'channels/nuviko_stories/docs/story-shorts-v1/WORKFLOW.md', 'channels/nuviko_stories/docs/story-shorts-v1/CAPTIONS.md',
    'channels/nuviko_stories/docs/story-shorts-v1/VPN_ADVERTISING.md')]
current_references += [ROOT / 'channels/paper_detour/automation/README.md', ROOT / 'automation/palmier/README.md']
files += current_references
files = list(dict.fromkeys(files))
active_rules = [p for p in files if p not in list((ROOT / '.agent').glob('*.md'))]
active_rules += [ROOT / '.agent' / p for p in ('README.md', 'CHANNEL_BOOTSTRAP.md', 'skill-catalog.md', 'documentation-index.md')]
active_rules = [p for p in active_rules if '/discovery-checks-' not in str(p) and '/consultations/' not in str(p)]
retired = re.compile(r'parallax|параллакс|BG/MG/FG|paper_layer_storyboarder', re.I)
for path in active_rules + roles:
    check(not retired.search(path.read_text()), f'Retired production workflow in active rules: {path}')
checks['current_rules_checked'] = len(set(active_rules + roles))
link_count = 0
for path in files:
    for target in re.findall(r'\]\(([^\n]+?)\)', path.read_text()):
        target = target.strip('<>').split('#')[0]
        if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        target = unquote(target)
        resolved = Path(target) if target.startswith('/') else path.parent / target
        check(resolved.exists(), f'Broken link in {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {target}')
        link_count += 1
checks['local_links_checked'] = link_count
checks['root_bytes'] = (ROOT / 'AGENTS.md').stat().st_size
check(checks['root_bytes'] <= 8 * 1024, 'Root AGENTS exceeds instruction budget')
for channel in ('channels/paper_detour/AGENTS.md', 'channels/nuviko_history/AGENTS.md', 'channels/nuviko_stories/AGENTS.md'):
    check(checks['root_bytes'] + (ROOT / channel).stat().st_size < 32 * 1024, f'Root+channel exceeds default instruction budget: {channel}')

print(json.dumps({'status': 'PASS' if not errors else 'FAIL', 'checks': checks, 'errors': errors}, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
