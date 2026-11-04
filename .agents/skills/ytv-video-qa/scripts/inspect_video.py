#!/usr/bin/env python3
"""Read-only AV inspection and exact frame extraction; never an artistic QA PASS."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{name}: expected integer >= {minimum}')
    return value


def frame_plan(plan):
    """Half-open intervals; explicit extras must never be silently clamped."""
    if not isinstance(plan, dict):
        raise ValueError('plan must be an object')
    expected = plan.get('expected', {})
    if not isinstance(expected, dict) or set(expected) - {'video', 'audio'}:
        raise ValueError('expected supports video and audio objects')
    for kind, supported in (
            ('video', {'width', 'height', 'codec_name', 'pix_fmt', 'color_space'}),
            ('audio', {'required', 'codec_name', 'channels', 'sample_rate'})):
        value = expected.get(kind, {})
        if not isinstance(value, dict) or set(value) - supported:
            raise ValueError(f'unsupported expected.{kind} check')
    total = integer(plan['frame_count'], 'frame_count', 1)
    fps = Fraction(str(plan['fps']))
    if fps <= 0:
        raise ValueError('fps must be positive')
    frames = {0, total - 1}
    policy = plan.get('scene_seconds')
    if policy is not None and (len(policy) != 2 or
            not all(type(x) in (int, float) and math.isfinite(x) for x in policy) or
            not 0 < policy[0] <= policy[1]):
        raise ValueError('scene_seconds must be a positive [min, max]')
    violations = []
    for kind in ('scenes', 'cues'):
        if not isinstance(plan.get(kind, []), list):
            raise ValueError(f'{kind} must be a list')
        seen = set()
        intervals = []
        for item in plan.get(kind, []):
            ident = item['id']
            if not isinstance(ident, str) or not ident or ident in seen:
                raise ValueError(f'{kind}: missing or duplicate id')
            seen.add(ident)
            start = integer(item['start'], ident + '.start')
            end = integer(item['end'], ident + '.end', 1)
            if not start < end <= total:
                raise ValueError(f'{ident}: invalid half-open interval')
            intervals.append((start, end))
            frames.update((start, (start + end - 1) // 2, end - 1))
            if start:
                frames.add(start - 1)
            if end < total:
                frames.add(end)
            if kind == 'cues':
                for key in ('entry_end', 'exit_start'):
                    if key in item:
                        n = integer(item[key], ident + '.' + key)
                        if not start <= n < end:
                            raise ValueError(f'{ident}: {key} outside cue')
                        frames.add(n)
                if item.get('entry_end', start) > item.get('exit_start', end - 1):
                    raise ValueError(f'{ident}: negative hold interval')
            elif policy is not None:
                duration = float(Fraction(end - start, 1) / fps)
                if not policy[0] <= duration <= policy[1]:
                    violations.append({'scene': ident, 'duration_seconds': duration,
                                       'required_range_seconds': policy})
        if kind == 'scenes' and intervals:
            cursor = 0
            for start, end in sorted(intervals):
                if start != cursor:
                    raise ValueError('scenes must cover the timeline without gaps/overlap')
                cursor = end
            if cursor != total:
                raise ValueError('scenes do not cover the final frame')
    for n in plan.get('extra_frames', []):
        integer(n, 'extra_frames')
        if n >= total:
            raise ValueError('extra_frames outside visible range')
        frames.add(n)
    if not isinstance(plan.get('freshness', {}), dict):
        raise ValueError('freshness must be an object')
    if plan.get('freshness', {}).get('status', 'UNVERIFIED') not in (
            'CURRENT', 'STALE', 'UNVERIFIED'):
        raise ValueError('unknown freshness status')
    return sorted(frames), violations


def verdict(failures, policy_failures, freshness):
    if failures or policy_failures or freshness == 'STALE':
        return 'FAIL'
    # This helper cannot inspect pictures, hear audio or prove current edit binding.
    return 'UNVERIFIED'


def run(command, output, name):
    result = subprocess.run(command, capture_output=True, text=True)
    (output / (name + '.stdout')).write_text(result.stdout)
    (output / (name + '.stderr')).write_text(result.stderr)
    return result


def selection_expression(indices):
    """Keep FFmpeg's expression-parser depth logarithmic for long review plans."""
    terms = [f'eq(n\\,{n})' for n in indices]
    if not terms:
        raise ValueError('frame selection must not be empty')
    while len(terms) > 1:
        terms = ['(' + terms[i] + '+' + terms[i + 1] + ')'
                 if i + 1 < len(terms) else terms[i]
                 for i in range(0, len(terms), 2)]
    return 'select=' + terms[0]


def inspect(media, plan, output, extract=True, frames_output=None):
    indices, policy_failures = frame_plan(plan)
    if frames_output is not None:
        frames_output = Path(frames_output).absolute()
        if frames_output.exists() or any(p.is_symlink() for p in (frames_output, *frames_output.parents)):
            raise ValueError('Frame output must be a new path without symlink components')
        if frames_output == output.absolute():
            raise ValueError('Frames and evidence need separate directories')
    output.mkdir(parents=True, exist_ok=False)
    report = {'created_utc': datetime.now(timezone.utc).isoformat(),
              'media': str(media.resolve()), 'plan': plan,
              'policy_failures': policy_failures, 'failures': [],
              'reported_freshness': plan.get('freshness', {'status': 'UNVERIFIED'}),
              'checks': {k: 'UNVERIFIED' for k in (
                  'stream_metadata', 'full_decode', 'frame_extraction', 'frame_sampling',
                  'motion_framing', 'cue_timing', 'audio_signal',
                  'subjective_audio_listening', 'independent_review')},
              'inspected_frame_indices': [], 'requested_frame_indices': indices}
    try:
        digest = hashlib.sha256()
        with media.open('rb') as source:
            for block in iter(lambda: source.read(1024 * 1024), b''):
                digest.update(block)
        report['sha256'] = digest.hexdigest()
        if plan.get('sha256') and plan['sha256'] != report['sha256']:
            raise ValueError('media SHA differs from planned target; stop before sampling')
        probe = run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                     '-of', 'json', str(media)], output, 'ffprobe')
        if probe.returncode:
            raise ValueError('ffprobe failed; see ffprobe.stderr')
        info = json.loads(probe.stdout)
        report['streams'] = info['streams']
        videos = [s for s in info['streams'] if s['codec_type'] == 'video']
        audios = [s for s in info['streams'] if s['codec_type'] == 'audio']
        if not videos:
            raise ValueError('no video stream')
        video = videos[0]
        expected = plan.get('expected', {})
        for key in ('width', 'height', 'codec_name', 'pix_fmt', 'color_space'):
            if key in expected.get('video', {}) and video.get(key) != expected['video'][key]:
                report['failures'].append('video.' + key + ' mismatch')
        if Fraction(video['avg_frame_rate']) != Fraction(str(plan['fps'])):
            report['failures'].append('video FPS mismatch; frame plan may be stale')
        ae = expected.get('audio', {})
        if ae.get('required') and not audios:
            report['failures'].append('required audio stream missing')
        if audios:
            for key in ('codec_name', 'channels', 'sample_rate'):
                if key in ae and str(audios[0].get(key)) != str(ae[key]):
                    report['failures'].append('audio.' + key + ' mismatch')
        report['checks']['stream_metadata'] = 'FAIL' if report['failures'] else 'PASS'
        decode = run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(media),
                      '-map', '0:v?', '-map', '0:a?', '-progress', 'pipe:1',
                      '-nostats', '-f', 'null', '-'], output, 'full_decode')
        report['checks']['full_decode'] = 'PASS' if decode.returncode == 0 else 'FAIL'
        if decode.returncode:
            raise ValueError('full decode failed; see full_decode.stderr')
        counts = re.findall(r'^frame=(\d+)$', decode.stdout, re.M)
        if len(videos) == 1 and counts:
            report['decoded_video_frames'] = int(counts[-1])
            if int(counts[-1]) != plan['frame_count']:
                report['failures'].append('decoded frame count differs from frame plan')
        else:
            report['failures'].append('single-video counted-frame check unavailable')
        if audios:
            signal = run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(media),
                          '-map', '0:a:0', '-vn', '-af',
                          'volumedetect,silencedetect=noise=-50dB:d=0.25',
                          '-f', 'null', '-'], output, 'audio_signal')
            report['audio_measurements'] = {
                'stream': '0:a:0', 'method': 'sample levels and silence candidates; not listening',
                'mean_dbfs': re.findall(r'mean_volume: ([\-\w.]+) dB', signal.stderr),
                'sample_peak_dbfs': re.findall(r'max_volume: ([\-\w.]+) dB', signal.stderr),
                'silence_candidate_threshold_dbfs': -50, 'minimum_silence_seconds': 0.25}
            report['checks']['audio_signal'] = 'UNVERIFIED'
            report['audio_analysis_execution'] = 'PASS' if signal.returncode == 0 else 'FAIL'
            if signal.returncode:
                report['failures'].append('audio signal analysis failed')
        else:
            report['checks']['audio_signal'] = 'N_A' if not ae.get('required') else 'FAIL'
        # Wrong geometry/timing must not silently produce a misleading review set.
        if extract and not report['failures']:
            frames = frames_output if frames_output is not None else output / 'frames'
            frames.mkdir(parents=True)
            expression = selection_expression(indices)
            command = ['ffmpeg', '-v', 'error', '-xerror', '-i', str(media),
                              '-map', '0:v:0', '-vf', expression, '-fps_mode', 'vfr',
                              '-start_number', '0', str(frames / '%06d.png')]
            tool = run(['ffmpeg', '-version'], output, 'ffmpeg_version')
            if tool.returncode:
                raise ValueError('Unable to record reconstruction tool version')
            report['frame_recipe'] = {'argv': command, 'ffmpeg_version': tool.stdout.splitlines()[0],
                                      'stream': '0:v:0', 'index_basis': 'zero-based decoded video frame',
                                      'fps': str(plan['fps'])}
            extraction = run(command, output, 'extract')
            actual = sorted(frames.glob('*.png'))
            if extraction.returncode or len(actual) != len(indices):
                raise ValueError('frame extraction failed or count mismatch')
            report['frame_map'] = [{'index': n, 'path': os.path.relpath(p, output)}
                                   for n, p in zip(indices, actual)]
            report['frames_directory'] = str(frames.absolute())
            report['checks']['frame_extraction'] = 'PASS'
    except (OSError, ValueError, KeyError, ZeroDivisionError) as error:
        report['failures'].append(str(error))
    report['technical_status'] = 'FAIL' if report['failures'] else 'PASS'
    report['verdict'] = verdict(report['failures'], policy_failures,
                                report['reported_freshness'].get('status', 'UNVERIFIED'))
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def inspect_managed(episode, name, owner, media, plan, output):
    """A dedicated synchronous QA writer; failed runs are retained for diagnosis."""
    scripts = Path(__file__).resolve().parents[2] / 'ytv-media-lifecycle/scripts'
    sys.path.insert(0, str(scripts))
    import workspace as storage
    from qa_lifecycle import register_qa
    if any('..' in Path(p).parts for p in (episode, media, output)):
        raise ValueError('Managed paths must not contain parent traversal')
    episode = storage.initialize(episode)
    output = output.absolute()
    media = media.absolute()
    storage.inventory.no_symlinks(output)
    storage.inventory.no_symlinks(media)
    output_rel = str(output.relative_to(episode))
    if not output_rel.startswith('Edit/QA/'):
        raise ValueError('Managed report output must be in Edit/QA')
    media.relative_to(episode)  # Retained exact reconstruction input, never an external guess.
    source_identity = storage.inventory.identity(media)
    required = plan.get('required_review_checks')
    if (not isinstance(required, list) or not all(isinstance(k, str) and k for k in required) or
            not {'stream_metadata', 'full_decode', 'frame_sampling'}.issubset(required)):
        raise ValueError('Managed QA plan must freeze applicable required_review_checks')
    with storage.locked(episode):
        directory = storage.start(episode, name, owner)
        try:
            result = inspect(media, plan, output, frames_output=directory / 'scratch/qa')
            if storage.inventory.identity(media) != source_identity:
                raise ValueError('QA source changed during inspection')
            if result['technical_status'] == 'PASS' and result['checks']['frame_extraction'] == 'PASS':
                register_qa(episode, name, owner, str((output / 'report.json').relative_to(episode)))
                storage.finish(episode, name, owner, 'complete', True)
            else:
                storage.finish(episode, name, owner, 'failed', True)
            return result
        except Exception:
            storage.finish(episode, name, owner, 'failed', True)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media', required=True, type=Path)
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--no-extract', action='store_true')
    parser.add_argument('--frames-dir', type=Path, help='New frame directory, normally Work/<run>/previews/qa; reports stay in output-dir')
    parser.add_argument('--episode', type=Path, help='Managed QA: automatically create and account a dedicated run')
    parser.add_argument('--run-id')
    parser.add_argument('--owner')
    args = parser.parse_args()
    try:
        if any((args.episode, args.run_id, args.owner)):
            if not all((args.episode, args.run_id, args.owner)) or args.no_extract or args.frames_dir:
                raise ValueError('Managed QA requires episode/run-id/owner and automatic frame extraction')
            result = inspect_managed(args.episode, args.run_id, args.owner, args.media,
                                     json.loads(args.plan.read_text()), args.output_dir)
        else:
            result = inspect(args.media, json.loads(args.plan.read_text()),
                             args.output_dir, not args.no_extract, args.frames_dir)
    except (OSError, ValueError, KeyError, ZeroDivisionError) as error:
        parser.exit(2, str(error) + '\n')
    print(json.dumps({'report': str(args.output_dir / 'report.json'),
                      'technical_status': result['technical_status'],
                      'verdict': result['verdict']}))
    return 1 if result['technical_status'] == 'FAIL' else 0


if __name__ == '__main__':
    raise SystemExit(main())
