"""Build this catalog's local review bundle. No network or YouTube writes."""
import importlib.util
import json
import os
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
load = lambda p: json.loads(p.read_text())
save = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n')
validator_path = ROOT / '.agents/skills/ytv-youtube-descriptions/scripts/validate_description.py'
spec = importlib.util.spec_from_file_location('description_validator', validator_path)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
audit, bodies = load(HERE / 'AUDIT.json'), load(HERE / 'BODIES.json')
if any(row.get('external_status') in ('applied_verified', 'unchanged_verified')
       for row in audit['videos']):
    raise SystemExit('Review bundle already reconciled with YouTube. Preserve current state; create a new versioned review instead.')
snapshot = load(HERE / 'BEFORE.json')
videos = {v['id']: v for v in snapshot['videos']}
assert len(audit['videos']) == 10 and len(videos) == 11
assert all(v['snippet']['channelId'] == audit['channel_id'] for v in videos.values())
assert len({r['id'] for r in audit['videos']}) == 10
preview = ['# Paper Detour — полные описания для просмотра', '',
           'Подготовленные основные английские тексты, 2 ноября 2026. Это локальный review bundle; записи в YouTube из этого прохода нет. Три описания сохранены полностью, семь предложено исправить. Все исходные хэштеги, семь глав и реальные URL сохранены.', '']
labels = {
    'orQiLIvOL-8': 'Кнорозов и Ася', 'xYS2XBeR_Jc': 'IQ-галерея',
    'sA-PYrDl5H8': 'Matt — третий на каждом свидании', 'r71aCn4p88A': 'Минни Фримен',
    '-KW8jgSoEz0': 'Последнее видео / скроллинг', 'WQw7ny9svrk': 'Joshua и Jessica',
    'pdSgHe6ScTI': 'Margorie McCall', '7DygREwtxfY': 'Декодирование радиозаписи',
    '85dwIXy_lZs': 'Передача программ по радио — Short', '0RaC4t7yn5o': 'Радио-фильм',
}
groups, validations = {}, []
for n, row in enumerate(audit['videos'], 1):
    vid = row['id']
    assert row['decision'] in ('keep', 'revise')
    assert (HERE / row['consultation']).is_file()
    assert videos[vid]['status']['privacyStatus'] == 'public'
    baseline_path = HERE / 'texts' / f'{vid}.before.txt'
    before = baseline_path.read_bytes().decode('utf-8')
    assert before == videos[vid]['snippet']['description']
    manifest_path = HERE / 'texts' / f'{vid}.protected.json'
    manifest = load(manifest_path)
    by_label = {b['label']: b['text'] for b in manifest['blocks']}
    assert 'hashtags' in by_label
    if row['decision'] == 'keep':
        text = before
    else:
        body = bodies[vid].strip()
        assert not re.search(r'(?m)^#|^\d{1,2}:\d{2}\s|https?://', body)
        parts = [body]
        if vid in ('7DygREwtxfY', '85dwIXy_lZs'):
            parts.append('Watch the full film: ' + by_label['link_1'])
        if 'recreation_disclosure' in by_label:
            parts.append(by_label['recreation_disclosure'])
        if 'chapters' in by_label:
            parts.append(by_label['chapters'])
        parts.append(by_label['hashtags'])
        text = '\n\n'.join(parts)
    # The scoped audit preserves every hashtag, not merely one protected substring.
    assert re.findall(r'(?<!\w)#\w+', text) == re.findall(r'(?<!\w)#\w+', before)
    assert re.findall(r'https?://\S+', text) == re.findall(r'https?://\S+', before)
    result = validator.validate(text, manifest, before)
    assert result['valid'], (vid, result)
    assert result['changed'] == (row['decision'] == 'revise')
    out = HERE / 'texts' / f'{vid}.proposed.txt'
    out.write_bytes(text.encode('utf-8'))
    save(HERE / 'texts' / f'{vid}.validation.json', result)
    episode_dir = ROOT / row['canonical_path']
    if vid == '7DygREwtxfY':
        episode_dir = episode_dir / 'Shorts/02_decoder'
    elif vid == '85dwIXy_lZs':
        episode_dir = episode_dir / 'Shorts/01_radio_signal'
    proposed = episode_dir / 'Packaging/Metadata' / f'DESCRIPTION_EN_PREVIEW_20261102_{vid}.txt'
    proposed.parent.mkdir(parents=True, exist_ok=True)
    proposed.write_bytes(text.encode('utf-8'))
    row.update(label=labels[vid], editorial_status=row['decision'], editorial_reviewer='coordinator; not independent review or user acceptance',
               assembly_status='validated', external_status='not_requested',
               baseline_file=baseline_path.relative_to(ROOT).as_posix(),
               proposed_file=proposed.relative_to(ROOT).as_posix(),
               validator_result=(HERE / 'texts' / f'{vid}.validation.json').relative_to(ROOT).as_posix(),
               characters=result['characters'], utf8_bytes=result['utf8_bytes'],
               live_display_status='not_checked_for_proposal', protected_blocks=result['protected_blocks'])
    groups.setdefault(row['canonical_path'], []).append(row)
    validations.append({'id': vid, 'valid': result['valid'], 'changed': result['changed'],
                        'characters': result['characters'], 'utf8_bytes': result['utf8_bytes'],
                        'protected_blocks': result['protected_blocks']})
    preview += [f"## {n}. {labels[vid]} — {'оставлено' if row['decision'] == 'keep' else 'предлагаемая правка'}", '',
                f"https://www.youtube.com/watch?v={vid}", '', row['reason'], '', '```text', text, '```', '']
audit['counts'] = dict(Counter(r['decision'] for r in audit['videos']))
audit['review_scope'] = 'Narrative/source and assembly review; not new full-film AV QA, independent fact-check, multilingual rewrite or live-display proof.'
audit['public_link_checks'] = [{'url': 'https://www.youtube.com/watch?v=0RaC4t7yn5o',
                               'target_channel_id': videos['0RaC4t7yn5o']['snippet']['channelId'],
                               'privacy_status': videos['0RaC4t7yn5o']['status']['privacyStatus'],
                               'method': 'Current owner-authorized API read; not proof of a clickable Shorts link or Related Video UI.'}]
save(HERE / 'AUDIT.json', audit)
save(HERE / 'VALIDATION.json', {'videos': validations, 'coverage': 10,
                               'hashtag_and_chapter_blocks_exact': True,
                               'same_two_URL_occurrences': True,
                               'external_writes': 0, 'limits': 'Mechanical assembly checks only; source and display limits are per row.'})
(HERE / 'PREVIEW.md').write_text('\n'.join(preview))

for canonical, rows in groups.items():
    target = ROOT / canonical / 'Packaging/Metadata/DESCRIPTION_REVIEW_20261102.md'
    lines = ['# Description review — 2026-11-02', '',
             'Local review/proposals only. No YouTube description writes were requested or performed in this pass. Existing published descriptions remain separate from these candidates. Not user acceptance.', '',
             '[Complete catalog preview](' + Path(os.path.relpath(HERE / 'PREVIEW.md', target.parent)).as_posix() + ').', '']
    for r in rows:
        lines += [f"## {r['id']} — {r['decision']}", '',
                  '[Exact full review text](' + Path(os.path.relpath(ROOT / r['proposed_file'], target.parent)).as_posix() + ').', '',
                  'Reason: ' + r['reason'], '',
                  f"Source: `{r['source_status']}`; assembly: validated exact blocks; external: not requested; live destination display: not checked for proposal.", '',
                  r['method'], '']
        if r.get('source_limit'):
            lines += [r['source_limit'], '']
    lines += ['Before an authorized write re-read live metadata, preserve concurrent changes and the current experiment, and use release/global uploader. No translation, title, thumbnail, privacy or playlist mutation is implied.', '']
    target.write_text('\n'.join(lines))
    readme = ROOT / canonical / 'README.md'
    if readme.exists():
        s = readme.read_text()
        note = '**Описания, review 2 ноября 2026:** [решения и полные локальные тексты](Packaging/Metadata/DESCRIPTION_REVIEW_20261102.md). Это версии для просмотра, не подтверждение новой записи в YouTube; текущие опубликованные поля сверять через API.'
        if note not in s:
            first, sep, rest = s.partition('\n')
            readme.write_text(first + '\n\n' + note + '\n' + rest)

registry_file = ROOT / '.agent/episode-registry.json'
registry = load(registry_file)
for entry in registry['entries']:
    if entry.get('canonical_path') not in groups:
        continue
    pointer = entry['canonical_path'] + '/Packaging/Metadata/DESCRIPTION_REVIEW_20261102.md'
    for field in ('current_context', 'state_sources', 'records'):
        entry[field] = [pointer] + [x for x in entry.get(field, []) if x != pointer]
registry['updated'] = '2026-11-02'
save(registry_file, registry)
md_file = ROOT / '.agent/episode-registry.md'
lines = md_file.read_text().splitlines()
for i, line in enumerate(lines):
    if not line.startswith('| ['):
        continue
    fields = line.split(' | ')
    if len(fields) != 4:
        continue
    for canonical in groups:
        if fields[2] == f'[{canonical}](../{canonical})':
            link = f'[DESCRIPTION_REVIEW_20261102.md](../{canonical}/Packaging/Metadata/DESCRIPTION_REVIEW_20261102.md)'
            current = fields[3].removesuffix(' |')
            if link not in current:
                fields[3] = link + ('' if current == '—' else '; ' + current) + ' |'
                lines[i] = ' | '.join(fields)
            break
md_file.write_text('\n'.join(lines) + '\n')
print(json.dumps({'counts': audit['counts'], 'validated': len(validations), 'external_writes': 0}))
