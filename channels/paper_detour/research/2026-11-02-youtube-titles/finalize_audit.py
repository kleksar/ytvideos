"""Reconcile this specific title audit's observed evidence; no external writes."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
load = lambda p: json.loads(p.read_text())
save = lambda p, data: p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
audit = load(HERE / 'AUDIT.json')
before = load(HERE / 'BEFORE.json')
after = load(HERE / 'AFTER.json')
old = {v['id']: v for v in before['videos']}
new = {v['id']: v for v in after['videos']}
locations = {
    'orQiLIvOL-8': ('009_knorozov_asya', 'Source/Voice/roger_v2_20261101/narration_en.txt', 'SHE CAME LATER'),
    'xYS2XBeR_Jc': ('003_iq_gallery', 'Published IQ gallery v24; current release metadata and accepted reported-estimates caveat', 'THINK YOU’RE SMARTER THAN THEM?'),
    'sA-PYrDl5H8': ('008_boyfriend_brought_friend', 'Script/narration_en.txt; published v06', 'EVERY DATE?'),
    'r71aCn4p88A': ('027_doomscrolling_short', 'Source/Script/script_en_minnie_candidate_v03.txt', 'FROM ONE BOY'),
    '-KW8jgSoEz0': ('004_last_video', 'Script/narration_en.txt; published scrolling Short', 'STILL SCROLLING?'),
    'WQw7ny9svrk': ('007_joshua_jessica', 'Script/narration_en.txt; current published 45-second Short', 'HE STILL CRIED / 55% REMAINING'),
    'pdSgHe6ScTI': ('002_margorie_mccall', 'Source/Voice/script_en.txt; accepted folklore narration', 'SHE CAME HOME'),
    '7DygREwtxfY': ('001_radio_game', 'Shorts/02_decoder: current release metadata, prior title decision, supporting narration_pro_v2.txt (not assumed to be the exact final 37-second narration)', 'GAME IN THE STATIC?'),
    '85dwIXy_lZs': ('001_radio_game', 'Shorts/01_radio_signal: current release metadata and supporting narration_pro_v2.txt (not assumed to be the exact final 30-second narration)', 'A PROGRAM ON TAPE?'),
    '0RaC4t7yn5o': ('001_radio_game', 'Published 001_en_long_paper_world_20261031_audio256.mp4; accepted release/chapters evidence', 'Active three-thumbnail experiment'),
}
radio = next(r for r in audit['videos'] if r['id'] == '0RaC4t7yn5o')
radio.update(content_status='grounded', selected_title=radio['before'],
             prepared_title='How People Got Computer Programs From the Radio',
             consultation='CONSULT_0RaC4t7yn5o.md',
             reason='All three existing variants reviewed. Variant 3 has the clearest editorial promise; active test retained, no winner inferred and no automatic replacement authorized.')
assert len(audit['videos']) == 10 and len(new) == 11
assert set(new) == set(old)
assert {v['snippet']['channelId'] for v in new.values()} == {audit['channel_id']}
checks = []
for row in audit['videos']:
    vid = row['id']
    b, a = old[vid], new[vid]
    assert row['decision'] in ('keep', 'revise', 'defer')
    assert (HERE / row['consultation']).is_file()
    assert a['snippet']['title'] == row['selected_title']
    assert len(row['selected_title']) <= 100 and not re.search('[<>]', row['selected_title'])
    assert re.findall(r'#[^\s#]+', row['before']) == re.findall(r'#[^\s#]+', row['selected_title'])
    stable_fields = sorted((set(b['snippet']) | set(a['snippet'])) - {'title', 'localized'})
    assert all(b['snippet'].get(k) == a['snippet'].get(k) for k in stable_fields)
    assert b['status'] == a['status'] and b['contentDetails'] == a['contentDetails']
    assert a['status']['privacyStatus'] == 'public'
    row.update(canonical_path='new_channel/videos/' + locations[vid][0],
               accepted_material=locations[vid][1], cover_text=locations[vid][2],
               display_status='desktop_checked',
               display_evidence='LONG_DESKTOP_AFTER.png' if vid == '0RaC4t7yn5o' else 'SHORTS_DESKTOP_AFTER.png',
               desktop_viewport={'width': 2056, 'height': 1147},
               responsive_phone_status='open: no valid final phone-size proof; see DISPLAY_CHECK.md',
               current_title=a['snippet']['title'])
    if row['decision'] == 'revise':
        receipt = load(HERE / ('TITLE_' + vid + '_RECEIPT.json'))
        assert receipt['state'] == 'saved_verified'
        assert receipt['after']['snippet']['title'] == row['selected_title']
        row.update(application_status='applied_and_read_back_verified', receipt='TITLE_' + vid + '_RECEIPT.json')
        lb, la = receipt['before'].get('localizations', {}), receipt['after'].get('localizations', {})
        row['localization_changes_observed_outside_requested_part'] = sorted(k for k in set(lb) | set(la) if lb.get(k) != la.get(k))
    elif row['decision'] == 'keep':
        row['application_status'] = 'unchanged_and_verified'
    else:
        row['application_status'] = 'deferred_for_active_experiment'
    checks.append({'id': vid, 'title_matches_decision': True,
                   'other_snippet_fields_preserved': stable_fields,
                   'status_and_content_details_unchanged': True,
                   'title_hashtags_preserved_exactly': True})

def memberships(s):
    return {pid: [(r['contentDetails']['videoId'], r['snippet']['position'], r['id']) for r in rows]
            for pid, rows in s['members'].items()}

assert memberships(before) == memberships(after)
assert {p['id']: {k: p[k] for k in ('snippet', 'status', 'contentDetails')} for p in before['playlists']} == {p['id']: {k: p[k] for k in ('snippet', 'status', 'contentDetails')} for p in after['playlists']}
assert old['QqMudxBNZgo']['snippet'] == new['QqMudxBNZgo']['snippet']
audit.update(version=2, checked_at=after['checked_at'],
             counts={'reviewed': 10, 'revised_and_verified': 8, 'kept': 1, 'deferred_active_test': 1, 'technical_excluded': 1},
             review_scope='Default English titles; no multilingual editorial audit, new full-film AV review, independent review, or performance claim.',
             checks=checks)
save(HERE / 'AUDIT.json', audit)
save(HERE / 'VALIDATION.json', {'checked_at': after['checked_at'], 'rows': checks,
     'all_11_video_ids_accounted_for': True, 'playlist_membership_order_ids_and_metadata_preserved': True,
     'technical_stream_unchanged': True, 'descriptions_and_seven_radio_chapters_preserved': True,
     'active_test': 'Studio still testing, three original title variants unchanged; RADIO_AB_AFTER_DOM.txt and PNG',
     'limits': ['Final responsive phone fit remains unverified', 'English-default title audit, not a multilingual audit', 'Separate localizations changed in receipts; only snippet was written. English mirror changes expected, Arabic changes also observed on five videos; source of Arabic changes not established. No rollback attempted.']})

report_path = 'new_channel/research/2026-11-02-youtube-titles/REPORT.md'
groups = {}
for row in audit['videos']:
    groups.setdefault(row['canonical_path'], []).append(row)
for canonical, rows in groups.items():
    target = ROOT / canonical / 'Packaging/Metadata/TITLE_CURRENT_20261102.md'
    target.parent.mkdir(parents=True, exist_ok=True)
    sections = ['# Current YouTube title decision — 2026-11-02', '',
                'This is a title/packaging state note, not a new production approval. Default English titles audited; other languages were not editorially reviewed.', '',
                f'Catalog evidence: [report]({Path(__import__("os").path.relpath(ROOT / report_path, target.parent)).as_posix()}). Read current live state before a later mutation.', '']
    for r in rows:
        sections += [f"## {r['id']}", '', f"Video: https://www.youtube.com/watch?v={r['id']}", '',
                     f"Current saved default title: **{r['current_title']}**", '',
                     f"Decision: `{r['decision']}`; external state: `{r['application_status']}`.", '',
                     'Material: ' + r['accepted_material'] + '.', '',
                     'Reason: ' + r['reason'], '',
                     'Display: all meaningful title words visible in the actual desktop card at 2056×1147; trailing hashtags may truncate. Final phone-size fit is still open; do not call it mobile approved.', '']
        if r.get('prepared_title'):
            sections += ['Prepared editorial preference only: **' + r['prepared_title'] + '**. Already variant 3 of the active test. Do not replace the test or infer its winner.', '']
    if canonical.endswith('009_knorozov_asya'):
        sections += ['The published v04 narration, not the unmade v09 proposal in PRODUCTION_DRAFT.md, grounds this title. Asya arrived after the breakthrough.', '']
    target.write_text('\n'.join(sections))
    readme = ROOT / canonical / 'README.md'
    if readme.exists():
        text = readme.read_text()
        note = '**Названия YouTube, проверка 2 ноября 2026:** актуальные решения и ограничения — [TITLE_CURRENT_20261102.md](Packaging/Metadata/TITLE_CURRENT_20261102.md). Данные и квитанции ниже сохраняют историю; текущий title брать из этой записи и свежего YouTube read-back.'
        if note not in text:
            first, sep, rest = text.partition('\n')
            text = first + '\n\n' + note + '\n' + rest
        old_sentence = 'Обрезание смыслового названия на карточках ПК/390 px остаётся отдельной задачей titles; исправление меток не является приёмкой всего названия.'
        text = text.replace(old_sentence, 'Смысловое название исправлено в проходе titles 2 ноября и проверено на реальной карточке ПК; финальная проверка телефонного отображения остаётся открытой — см. актуальную запись выше.')
        readme.write_text(text)

registry_path = ROOT / '.agent/episode-registry.json'
registry = load(registry_path)
for entry in registry['entries']:
    canonical = entry.get('canonical_path')
    if canonical not in groups:
        continue
    pointer = canonical + '/Packaging/Metadata/TITLE_CURRENT_20261102.md'
    for field in ('current_context', 'state_sources', 'records'):
        entry[field] = [pointer] + [x for x in entry.get(field, []) if x != pointer]
registry['updated'] = '2026-11-02'
save(registry_path, registry)
md_path = ROOT / '.agent/episode-registry.md'
lines = md_path.read_text().splitlines()
for i, line in enumerate(lines):
    if not line.startswith('| ['):
        continue
    fields = line.split(' | ')
    if len(fields) != 4:
        continue
    for canonical in groups:
        if fields[2] == f'[{canonical}](../{canonical})':
            link = f'[TITLE_CURRENT_20261102.md](../{canonical}/Packaging/Metadata/TITLE_CURRENT_20261102.md)'
            current = fields[3].removesuffix(' |')
            if link not in current:
                fields[3] = link + ('' if current == '—' else '; ' + current) + ' |'
                lines[i] = ' | '.join(fields)
            break
md_path.write_text('\n'.join(lines) + '\n')
print(json.dumps(audit['counts']))
