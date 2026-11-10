"""Explicit synthetic test font. This never changes a production profile.

Linux CI can use its packaged DejaVu font. Native-font appearance still requires
the approved font on a production worker; these tests verify engine behavior.
"""
import os
from pathlib import Path
import unittest

from PIL import ImageFont


def configure():
    configured = os.environ.get('YTV_TEST_FONT')
    linux_fixture = Path('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf')
    if configured or linux_fixture.is_file():
        path = Path(configured) if configured else linux_fixture
        if not path.is_file():
            raise RuntimeError('YTV_TEST_FONT must point to an existing fixture font')
        for profile in ('PAPER', 'NUVIKO'):
            os.environ.setdefault('YTV_FONT_OVERRIDE_' + profile, str(path))
            os.environ.setdefault('YTV_FONT_INDEX_' + profile, '0')


def font(channel, size):
    configure()
    fallback = {'paper': ('/System/Library/Fonts/Supplemental/ChalkboardSE.ttc', 2),
                'nuviko': ('/System/Library/Fonts/Supplemental/Georgia Bold.ttf', 0)}[channel]
    path = os.environ.get('YTV_FONT_OVERRIDE_' + channel.upper(), fallback[0])
    index = int(os.environ.get('YTV_FONT_INDEX_' + channel.upper(), str(fallback[1])))
    if not Path(path).is_file():
        raise unittest.SkipTest('Install an explicit YTV_TEST_FONT fixture or the approved channel font')
    return ImageFont.truetype(path, size, index=index)
