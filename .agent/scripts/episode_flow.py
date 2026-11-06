#!/usr/bin/env python3
"""Read-only flow validator and exclusive initializer; never executes a production step."""
import argparse
import fcntl
import hashlib
import json
import os
import tempfile
from pathlib import Path

INPUTS = ('collaborative', 'accepted_story', 'ready_text')
STATES = ('PENDING', 'DONE', 'STALE', 'BLOCKED')
CHECKS = ('PASS', 'FAIL', 'UNVERIFIED', 'N_A')
BASE = [
    ('script', []),
    ('storyboard', ['ytv-video-production']),
    ('audio', ['ytv-audio-delivery']),
    ('images', ['ytv-scene-images', 'ytv-image-motion']),
    ('subtitles', ['ytv-paper-subtitles', 'ytv-srt']),
    ('render', ['ytv-video-production', 'ytv-video-export', 'ytv-video-qa']),
    ('review', []),
    ('packaging', ['ytv-youtube-video-titles', 'ytv-youtube-thumbnails', 'ytv-youtube-descriptions', 'ytv-youtube-hashtags', 'ytv-youtube-playlists']),
    ('unlisted', ['ytv-youtube-release']),
    ('release', ['ytv-youtube-release', 'ytv-media-lifecycle']),
]
DECISIONS = {'packaging': 'mp4_accepted', 'unlisted': 'packaging_accepted', 'release': 'unlisted_accepted_and_release_choice'}

def new_state(episode, channel, kind, source):
    if kind not in INPUTS or channel not in ('paper', 'nuviko') or source not in ('long', 'short') or not episode.strip():
        raise ValueError('invalid episode, channel, format or input')
    stages = []
    if kind == 'collaborative':
        story_skills = ['ytv-storycraft']
        if channel == 'nuviko': story_skills.append('ytv-history-verification')
        if source == 'short': story_skills += ['ytv-shorts-story', 'ytv-shorts-loop']
        stages.append({'id': 'develop_story', 'skills': story_skills, 'status': 'PENDING', 'artifacts': [], 'checks': [], 'dependencies': [], 'skill_runs': []})
    for name, skills in BASE:
        skills = skills.copy()
        if name == 'script' and kind != 'ready_text':
            skills.append('ytv-storycraft')
        if name == 'script' and source == 'short' and kind != 'collaborative':
            if kind == 'accepted_story': skills.append('ytv-shorts-story')
            skills.append('ytv-shorts-loop')
        if name == 'packaging' and source == 'long':
            skills += ['ytv-youtube-ab-testing', 'ytv-youtube-chapters']
        stages.append({'id': name, 'skills': skills, 'status': 'PENDING', 'artifacts': [], 'checks': [], 'dependencies': [], 'skill_runs': []})
    return {'schema_version': 2, 'music_workflow': 1, 'episode': episode, 'channel': channel, 'format': source, 'input': kind,
            'input_evidence': '', 'scope': '', 'stages': stages, 'decisions': {}, 'next_step': ''}

def previous_skill_routes(stage, skills, channel):
    """Previously recorded routes, for validating evidence only."""
    if stage == 'storyboard':
        if channel == 'paper':
            return [('ytv-paper-storyboard',), ('ytv-video-production', 'ytv-paper-storyboard')]
        return [('ytv-history-story',)]
    if stage not in ('develop_story', 'script'):
        return []
    short_skills = tuple(skill for skill in skills if skill in ('ytv-shorts-story', 'ytv-shorts-loop'))
    routes = []
    if short_skills:
        routes.append(tuple(skill for skill in skills if skill not in short_skills))
    if 'ytv-storycraft' in skills:
        former_owner = 'ytv-paper-production' if channel == 'paper' else 'ytv-history-story'
        routes.append((former_owner,))
        if short_skills:
            routes.append((former_owner, *short_skills))
    return routes

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def assess(state):
    """Return diagnostic snapshot; no writes and no assertions about editorial quality."""
    errors, stale, warnings = [], set(), []
    if not isinstance(state, dict):
        return {'errors': ['state must be an object'], 'stale': [], 'ready': []}
    try:
        expected = new_state(state['episode'], state['channel'], state['input'], state['format'])
        stages = state['stages']
        if state.get('schema_version') not in (1, 2) or not isinstance(stages, list):
            raise ValueError('schema or stages')
        if state.get('schema_version') == 2 and state.get('music_workflow') != 1:
            raise ValueError('new route requires music_workflow 1')
        if not all(isinstance(s, dict) for s in stages): raise ValueError('stage must be object')
        if [s['id'] for s in stages] != [s['id'] for s in expected['stages']]:
            raise ValueError('stage sequence differs from applicable route')
    except (KeyError, TypeError, ValueError) as e:
        return {'errors': [f'invalid route: {e}'], 'stale': [], 'ready': []}
    if any(not isinstance(s.get(k), list) for s in stages for k in ('artifacts', 'checks', 'dependencies', 'skill_runs')):
        return {'errors': ['stage arrays must be lists'], 'stale': [], 'ready': []}
    for field in ('input_evidence', 'scope', 'next_step'):
        if not isinstance(state.get(field), str): errors.append(f'{field}: expected string')
    decisions = state.get('decisions')
    if not isinstance(decisions, dict):
        errors.append('decisions: expected object'); decisions = {}
    for key, d in decisions.items():
        if not isinstance(d, dict) or d.get('accepted') is not True or not all(isinstance(d.get(k), str) and d[k].strip() for k in ('evidence', 'target')):
            errors.append(f'decision {key}: evidence required')
    for stage, template in zip(stages, expected['stages']):
        name = stage['id']
        if stage.get('status') not in STATES: errors.append(f'{name}: invalid status')
        required_skills = set(template['skills'])
        previous_routes = previous_skill_routes(name, template['skills'], state['channel'])
        recorded_skills = stage.get('skills')
        if recorded_skills != template['skills']:
            if stage.get('status') == 'DONE' and isinstance(recorded_skills, list) and tuple(recorded_skills) in previous_routes:
                required_skills = set(recorded_skills)
                warnings.append(f'{name}: completed under previous routing; recorded evidence preserved')
            else:
                errors.append(f"{name}: reconcile route; current skills = {json.dumps(template['skills'])}")
        # A migrated stage can retain prior work. Only the current skills satisfy its completion checks.
        allowed_skills = required_skills.union(*previous_routes) if recorded_skills == template['skills'] else required_skills
        for key in ('artifacts', 'checks', 'dependencies', 'skill_runs'):
            if not isinstance(stage.get(key), list): errors.append(f'{name}.{key}: expected list')
        for run in stage.get('skill_runs', []):
            if not isinstance(run, dict) or not isinstance(run.get('skill'), str) or run['skill'] not in allowed_skills or run.get('status') not in ('APPLIED', 'N_A') or not isinstance(run.get('evidence'), str) or not run['evidence'].strip():
                errors.append(f'{name}: invalid skill run record')
        if stage.get('status') == 'DONE':
            completed_skills = {run['skill'] for run in stage['skill_runs'] if isinstance(run, dict) and isinstance(run.get('skill'), str) and run.get('status') in ('APPLIED', 'N_A') and run.get('evidence')}
            if not required_skills.issubset(completed_skills): errors.append(f'{name}: each applicable skill needs APPLIED or N_A evidence')
            if not state.get('input_evidence') or not state.get('scope'): errors.append(f'{name}: input evidence and scope required')
        for a in stage.get('artifacts', []):
            if not isinstance(a, dict) or not all(isinstance(a.get(k), str) and a[k].strip() for k in ('path', 'version', 'sha256')):
                errors.append(f'{name}: artifact path/version/sha256 required'); continue
            if len(a['sha256']) != 64 or any(c not in '0123456789abcdef' for c in a['sha256']): errors.append(f'{name}: invalid artifact hash')
            elif not Path(a['path']).is_absolute(): errors.append(f'{name}: artifact path must be absolute')
            else:
                try:
                    if digest(a['path']) != a['sha256']: stale.add(name)
                except OSError: stale.add(name)
        for c in stage.get('checks', []):
            if not isinstance(c, dict) or c.get('status') not in CHECKS or not isinstance(c.get('name'), str) or not c['name'].strip():
                errors.append(f'{name}: invalid check'); continue
            if c['status'] in ('PASS', 'FAIL', 'N_A') and not all(isinstance(c.get(k), str) and c[k].strip() for k in ('evidence', 'reviewer', 'method', 'coverage')):
                errors.append(f'{name}: {c["status"]} requires evidence/reviewer/method/coverage')
        for dep in stage.get('dependencies', []):
            if not isinstance(dep, dict) or not all(isinstance(dep.get(k), str) and dep[k].strip() for k in ('path', 'sha256')):
                errors.append(f'{name}: dependency path/sha256 required'); continue
            if not Path(dep['path']).is_absolute() or len(dep['sha256']) != 64 or any(c not in '0123456789abcdef' for c in dep['sha256']):
                errors.append(f'{name}: invalid dependency identity'); continue
            try:
                if digest(dep['path']) != dep['sha256']: stale.add(name)
            except OSError: stale.add(name)
        if stage.get('status') == 'DONE' and not stage.get('artifacts') and name != 'review':
            errors.append(f'{name}: DONE requires recorded artifact')
        if stage.get('status') == 'DONE' and any(c.get('status') in ('FAIL', 'UNVERIFIED') for c in stage.get('checks', []) if isinstance(c, dict)):
            errors.append(f'{name}: DONE with open check')
        if name == 'audio' and stage.get('status') == 'DONE' and state.get('schema_version') == 2:
            music = stage.get('music_handoff')
            if not isinstance(music, dict):
                errors.append('audio: music_handoff required')
            else:
                if music.get('mode') not in ('music', 'exception'):
                    errors.append('audio: music mode must be music or exception')
                for key in ('mix_path', 'handoff_path', 'edit_revision', 'reason'):
                    if not isinstance(music.get(key), str) or not music[key].strip():
                        errors.append(f'audio: music_handoff {key} required')
                paths = {a.get('path') for a in stage['artifacts'] if isinstance(a, dict)}
                if music.get('mix_path') not in paths or music.get('handoff_path') not in paths:
                    errors.append('audio: mix and handoff must be hashed artifacts')
            for check in ('music_decision', 'mix_listening'):
                if not any(isinstance(c, dict) and c.get('name') == check and c.get('status') == 'PASS' for c in stage['checks']):
                    errors.append(f'audio: {check} PASS evidence required')
    # Follow recorded artifact edges only. Results are flagged, never overwritten.
    stale.update(s['id'] for s in stages if s.get('status') == 'STALE')
    changed = True
    while changed:
        changed = False
        paths = {a.get('path') for s in stages if s['id'] in stale for a in s.get('artifacts', []) if isinstance(a, dict)}
        for s in stages:
            if s['id'] not in stale and any(isinstance(d, dict) and d.get('path') in paths for d in s.get('dependencies', [])):
                stale.add(s['id']); changed = True
    ready = []
    predecessor_done = True
    for s in stages:
        name = s['id']; done = s.get('status') == 'DONE' and name not in stale
        needed = ('story_accepted' if name == 'script' and state['input'] == 'collaborative' else DECISIONS.get(name))
        decision_ok = not needed or (isinstance(decisions.get(needed), dict) and decisions[needed].get('accepted') is True and bool(decisions[needed].get('evidence')) and bool(decisions[needed].get('target')))
        if done and (not predecessor_done or not decision_ok): errors.append(f'{name}: DONE without preceding stage or decision {needed or ""}')
        if not done and predecessor_done and decision_ok and (s.get('status') in ('PENDING', 'STALE') or name in stale):
            ready.append(name)
        predecessor_done = predecessor_done and done and decision_ok
    return {'errors': errors, 'stale': sorted(stale), 'ready': ready, 'warnings': warnings,
            'note': 'Structural checks only; consult stage skills and preserve real user decisions and existing upload receipt.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('init'); p.add_argument('state'); p.add_argument('--episode', required=True); p.add_argument('--channel', choices=('paper','nuviko'), required=True); p.add_argument('--format', choices=('long','short'), required=True); p.add_argument('--input', choices=INPUTS, required=True)
    p = sub.add_parser('check'); p.add_argument('state')
    p = sub.add_parser('update'); p.add_argument('state'); p.add_argument('candidate'); p.add_argument('--expected-sha256', required=True)
    args = parser.parse_args()
    if args.command == 'init':
        data = new_state(args.episode, args.channel, args.input, args.format)
        # Exclusive creation prevents accidental overwrite of a concurrent or existing record.
        fd = os.open(args.state, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')
        print('Created; populate input evidence, scope and real results. No work has been executed.')
    elif args.command == 'update':
        state_path = Path(args.state)
        if state_path.is_symlink() or not state_path.is_file(): raise ValueError('state must be an existing regular non-symlink file')
        with open(args.candidate) as f: candidate = json.load(f)
        report = assess(candidate)
        if report['errors']: raise ValueError('invalid candidate: ' + '; '.join(report['errors']))
        # Cooperating updates serialize on this lock; hash check prevents stale snapshots overwriting newer ones.
        with open(str(state_path) + '.lock', 'a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if digest(state_path) != args.expected_sha256: raise ValueError('state changed; reread and reconcile')
            fd, tmp = tempfile.mkstemp(prefix='.episode-flow-', dir=str(state_path.parent))
            try:
                with os.fdopen(fd, 'w') as out:
                    json.dump(candidate, out, ensure_ascii=False, indent=2); out.write('\n'); out.flush(); os.fsync(out.fileno())
                os.replace(tmp, state_path)
            finally:
                if os.path.exists(tmp): os.unlink(tmp)
        print('Updated; recheck evidence and current dependencies on resume.')
    else:
        with open(args.state) as f: report = assess(json.load(f))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if report['errors'] or report['stale'] else 0
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
