"""The small preserved YBW art-reference pack must remain auditable."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'docs/references/ybw-visual-style'
SPEC = importlib.util.spec_from_file_location('ybw_verify_pack', PACK / 'verify_pack.py')
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class ReferencePackTests(unittest.TestCase):
    def test_preserved_pack(self):
        VERIFY.verify(PACK)

    def test_changed_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'pack'
            shutil.copytree(PACK, copy)
            source = copy / 'originals/Mind_12s.png'
            source.write_bytes(source.read_bytes() + b'changed')
            with self.assertRaisesRegex(AssertionError, 'hash mismatch'):
                VERIFY.verify(copy)


if __name__ == '__main__':
    unittest.main()
