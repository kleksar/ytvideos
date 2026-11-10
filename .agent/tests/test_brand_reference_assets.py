"""Verify reusable Paper reference assets from a source-only checkout."""
from pathlib import Path
import hashlib
import json
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "channels/paper_detour/brand"
PACKS = BRAND / "References"


class BrandReferenceTests(unittest.TestCase):
    def test_accepted_assets_match_manifest(self):
        for name, key in [
            ("meaningful_staging_20261105_v01", "assets"),
            ("bold_visual_hooks_20261105_v01", "items"),
        ]:
            root = PACKS / name
            manifest = json.loads((root / "manifest.json").read_text())
            self.assertEqual(len(manifest[key]), 6)
            for item in manifest[key]:
                with self.subTest(pack=name, asset=item["id"]):
                    path = root / item.get("file", item.get("path"))
                    data = path.read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
                    self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                    self.assertEqual(list(struct.unpack(">II", data[16:24])), item["native_size"])
            if "contact_sheet" in manifest:
                contact = manifest["contact_sheet"]
                self.assertEqual(hashlib.sha256((root / contact["file"]).read_bytes()).hexdigest(),
                                 contact["sha256"])

    def test_input_references_resolve_from_clone(self):
        root = PACKS / "meaningful_staging_20261105_v01"
        references = json.loads((PACKS / "bold_visual_hooks_20261105_v01" / "REFERENCES.json").read_text())
        for item in references:
            # Historical absolute paths are provenance; source assets live in the sibling pack.
            data = (root / Path(item["path"]).name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])

    def test_reusable_document_links_exist(self):
        docs = [BRAND / name for name in (
            "FILM_REFERENCE_030.md", "REFERENCE_STATUS.md", "SCENE_IMAGE_REFERENCES.md")]
        docs += [PACKS / name / "REFERENCE.md" for name in (
            "meaningful_staging_20261105_v01", "bold_visual_hooks_20261105_v01")]
        for doc in docs:
            for target in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
                if target.startswith(("https://", "http://", "#")):
                    continue
                with self.subTest(doc=doc.name, target=target):
                    self.assertTrue((doc.parent / target.split("#", 1)[0]).is_file())


if __name__ == "__main__":
    unittest.main()
