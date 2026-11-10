"""Read channel-owned production settings for legacy CLI adapters.

The application enforces active/frozen status. This reader also supports pinned
legacy deliveries, including their historical paper/nuviko aliases.
"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
LEGACY_ALIASES = {'paper': 'paper_detour', 'nuviko': 'nuviko_history'}


def channel_profile(channel, *, root=None):
    if not isinstance(channel, str) or not re.fullmatch(r'[a-z][a-z0-9_]{1,63}', channel):
        raise ValueError('A registered channel slug is required')
    channel = LEGACY_ALIASES.get(channel, channel)
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
