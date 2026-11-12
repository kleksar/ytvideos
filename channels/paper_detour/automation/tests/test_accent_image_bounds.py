"""Image-bound parity without Palmier access or episode assets."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "normalize_paper_accent_cues.py"
SPEC = importlib.util.spec_from_file_location("accent_bounds_under_test", SCRIPT)
accent = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(accent)


class AccentImageBoundsTest(unittest.TestCase):
    def assert_bounds(self, pixels, expected_alpha, expected_face):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.png"
            image = Image.new("RGBA", (8, 7), (0, 0, 0, 0))
            for xy, rgba in pixels.items():
                image.putpixel(xy, rgba)
            image.save(path)
            results = []
            for backend in (np, None):
                accent.image_bounds.cache_clear()
                with patch.object(accent, "np", backend):
                    results.append(accent.image_bounds(str(path)))
            accent.image_bounds.cache_clear()
        self.assertEqual(results[0], results[1], "NumPy and Pillow must return identical half-open bounds")
        self.assertEqual(results[0], (8, 7, expected_alpha, expected_face))

    def test_single_pixel_has_one_pixel_extent(self):
        self.assert_bounds({(4, 3): (240, 220, 190, 255)},
                           (4, 3, 5, 4), (4, 3, 5, 4))

    def test_multiple_disconnected_pixels_share_half_open_box(self):
        self.assert_bounds({(1, 2): (240, 220, 190, 255),
                            (6, 4): (240, 220, 190, 255),
                            (2, 3): (240, 220, 190, 255)},
                           (1, 2, 7, 5), (1, 2, 7, 5))

    def test_alpha_shadow_and_orange_outline_do_not_enlarge_cream_face(self):
        self.assert_bounds({(0, 0): (20, 10, 0, 25),
                            (7, 6): (20, 10, 0, 25),
                            (1, 1): (255, 100, 40, 255),
                            (6, 5): (255, 100, 40, 255),
                            (2, 2): (240, 220, 190, 255),
                            (3, 3): (240, 220, 190, 255)},
                           (0, 0, 8, 7), (2, 2, 4, 4))

    def test_cream_face_on_canvas_edge_does_not_extend_outside_image(self):
        self.assert_bounds({(0, 0): (240, 220, 190, 30),
                            (7, 6): (240, 220, 190, 255)},
                           (0, 0, 8, 7), (7, 6, 8, 7))


if __name__ == "__main__":
    unittest.main()
