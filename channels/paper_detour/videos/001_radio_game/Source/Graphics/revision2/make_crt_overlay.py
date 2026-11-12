#!/usr/bin/env python3
"""Produce a subtle, static, transparent CRT texture for an editor layer."""
from pathlib import Path
import numpy as np
from PIL import Image

w, h = 1920, 1080
y, x = np.mgrid[0:h, 0:w]
radius = np.sqrt(((x - (w - 1) / 2) / (w / 2)) ** 2 + ((y - (h - 1) / 2) / (h / 2)) ** 2)
edge = np.clip((radius - 0.46) / (1.40 - 0.46), 0, 1) ** 2 * 42
lines = np.where(y % 4 == 0, 12, 0)
alpha = np.rint(np.clip(edge + lines, 0, 54)).astype(np.uint8)
rgba = np.zeros((h, w, 4), dtype=np.uint8)
rgba[:, :, 3] = alpha
Image.fromarray(rgba).save(Path(__file__).with_name('crt_scanlines_vignette.png'), optimize=True)
