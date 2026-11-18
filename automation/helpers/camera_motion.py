"""Canonical whole-shot editorial camera clock (not event/character animation).

Python frames are zero based. FFmpeg perspective's output counter `on` is one
based during eval=frame; callers of other filters must specify their own index.
Spatial cubic interpolation is independent from this linear temporal clock.
"""
import math


def _frames(frames):
    if type(frames) is not int or frames < 2:
        raise ValueError('editorial camera needs at least two rendered frames')
    return frames


def progress(frame, frames):
    _frames(frames)
    if type(frame) is not int or not 0 <= frame < frames:
        raise ValueError('camera frame must be in the rendered shot')
    return frame / (frames - 1)


def expression(frames, index='on-1'):
    """No clipping/hold/ease: exact first and last rendered-frame endpoints."""
    return f'(({index})/{_frames(frames)-1})'


def lerp_expression(start, end, frames, index='on-1'):
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)
           for x in (start, end)):
        raise ValueError('finite numeric camera endpoints required')
    return f'({start:.12f}+({end-start:.12f})*{expression(frames, index)})'
