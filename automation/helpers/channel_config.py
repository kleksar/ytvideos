"""Read channel-owned production settings for legacy CLI adapters.

The application enforces active/frozen status. This reader also supports pinned
legacy deliveries, including their historical paper/nuviko aliases.
"""
import json
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
LEGACY_ALIASES = {'paper': 'paper_detour', 'nuviko': 'nuviko_history'}
PINNED = None


def configure_pinned_profile(path, expected_sha256):
    """Use explicitly bound canonical profile bytes for this helper process."""
    global PINNED
    if not isinstance(expected_sha256, str) or not re.fullmatch(r'[0-9a-f]{64}', expected_sha256):
        raise ValueError('Invalid pinned profile SHA-256')
    source = Path(path).resolve(strict=True)
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError('Pinned channel profile bytes changed')
    value = json.loads(raw)
    if not isinstance(value, dict) or value.get('schema_version') != 1:
        raise ValueError('Invalid pinned channel profile')
    PINNED = (value, source, expected_sha256)


def channel_profile(channel, *, root=None):
    if not isinstance(channel, str) or not re.fullmatch(r'[a-z][a-z0-9_]{1,63}', channel):
        raise ValueError('A registered channel slug is required')
    channel = LEGACY_ALIASES.get(channel, channel)
    if root is None and PINNED is not None:
        value, path, expected = PINNED
        if value.get('id') != channel or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned channel profile identity or bytes changed')
        return value, path
    path = Path(root or ROOT) / 'channels' / channel / 'channel.json'
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict) or value.get('id') != channel or value.get('schema_version') != 1:
        raise ValueError('Invalid channel profile identity or schema')
    return value, path


def configured_channels(*, root=None):
    channels = []
    for path in sorted((Path(root or ROOT) / 'channels').glob('*/channel.json')):
        channel_profile(path.parent.name, root=root)
        channels.append(path.parent.name)
    return tuple(channels)


def visual_profile(channel, *, root=None):
    value, _ = channel_profile(channel, root=root)
    name = value.get('visual_profile')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', name):
        raise ValueError('Channel requires an explicit visual_profile')
    return name


def voice_id(channel, *, root=None):
    value, _ = channel_profile(channel, root=root)
    voice = value.get('voice')
    if not isinstance(voice, dict) or voice.get('provider') != 'elevenlabs':
        raise ValueError('Channel has no configured ElevenLabs voice')
    identity = voice.get('id')
    if not isinstance(identity, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', identity):
        raise ValueError('Channel has no valid voice ID')
    return identity
