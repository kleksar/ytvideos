"""Convert timed SRT to a frame-exact neutral display plan without editing input."""
from fractions import Fraction
import hashlib
from planning import _tool, _round, ROOT


def plan_srt(text, target):
    if not isinstance(text, str):
        raise ValueError('SRT must be UTF-8 text')
    fps = Fraction(target['fps'])
    if fps <= 1:
        raise ValueError('Invalid frame rate')
    origin, limit = target['origin_frame'], target['end_frame']
    raw = _tool(ROOT).parse_srt(text)
    cues = []
    previous_end = Fraction(0)
    for i, row in enumerate(raw):
        a, b = Fraction(row['start_seconds']), Fraction(row['end_seconds'])
        phrase = ' '.join(row['text'].split())
        if not phrase or a < previous_end or b <= a:
            raise ValueError('SRT cues must contain text and be ordered, positive and non-overlapping')
        start, end = (origin + _round(t * fps) for t in (a, b))
        if not origin <= start < end <= limit:
            raise ValueError('SRT cue outside timeline or collapsed after frame quantization')
        if cues and start <= cues[-1]['start_frame']:
            raise ValueError('SRT cue starts collapse on the same frame')
        cues.append(dict(id=f'C{i+1:04d}', text=phrase, start_frame=start,
                         end_frame=end, spoken_start_frame=start, spoken_end_frame=end,
                         words=[dict(index=i, text=phrase, start_frame=start, end_frame=end)]))
        previous_end = b
    for current, following in zip(cues, cues[1:]):
        current['end_frame'] = following['start_frame']
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return dict(schema='ytv-resolve-srt-plan-v1', target=target, cues=cues,
                conform_sha256=digest, source_srt_sha256=digest, playback='UNVERIFIED')


def choose_carriers(snapshot, cues):
    """Find one complete, enabled video lane covering the display interval."""
    first, last = cues[0]['start_frame'], cues[-1]['end_frame']
    states = snapshot['video_track_state']
    for number, track in enumerate(snapshot['picture'], 1):
        if not states.get(str(number)):
            continue
        cursor, chosen = first, []
        for row in sorted(track, key=lambda r: r[1]):
            identity, start, end, _, _, enabled, _, media = row
            if end <= cursor:
                continue
            if start > cursor or not enabled or not media:
                break
            stop = min(end, last)
            chosen.append(dict(id=f'section-{len(chosen)+1:04d}', carrier_id=identity,
                               start_frame=cursor, end_frame=stop))
            cursor = stop
            if cursor == last:
                return chosen
    raise ValueError('No enabled source video lane covers all caption frames')


def format_srt(plan):
    """Separate display SRT for inspection; never changes the timed source."""
    fps=Fraction(plan['target']['fps']); origin=plan['target']['origin_frame']
    tool=_tool(ROOT)
    rows=[]
    for index, cue in enumerate(plan['cues'], 1):
        a,b=(_round(Fraction(cue[k]-origin)*1000/fps) for k in ('start_frame','end_frame'))
        rows.append(f"{index}\n{tool.stamp(a)} --> {tool.stamp(b)}\n{cue['text']}")
    return '\n\n'.join(rows)+'\n'
