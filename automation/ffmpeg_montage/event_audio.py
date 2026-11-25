"""Render mapped speech/SFX placements while keeping explicit background stems."""
from pathlib import Path

import numpy as np
import soundfile as sf


def render_stems(plan, compiled, root):
    sr = compiled["clock"]["sample_rate"]
    n = compiled["clock"]["total_frames"] * sr // compiled["clock"]["fps"]

    def audio(ident):
        asset = plan["assets"][ident]
        p = Path(asset["path"])
        a, rate = sf.read(p if p.is_absolute() else Path(root) / p, always_2d=True,
                          dtype="float64")
        if rate != sr or a.shape[1] not in {1, 2}:
            raise ValueError(f"{ident}: unexpected sample rate or channels")
        return np.repeat(a, 2, axis=1) if a.shape[1] == 1 else a

    stems = {name: np.zeros((n, 2), np.float64) for name in ["voice", "sfx"]}
    for name in ["music", "original"]:
        bed = plan["beds"][name]
        a = audio(bed["asset"]) * 10 ** (bed["gain_db"] / 20)
        if len(a) != n:
            raise ValueError(f"{name}: background stem duration mismatch")
        stems[name] = a
    duck = np.ones(n, np.float64)
    samples = np.arange(n)
    for node in compiled["nodes"]:
        if node["kind"] not in {"phrase", "sfx"}:
            continue
        a = audio(node["asset"]) * 10 ** (node["gain_db"] / 20)
        first, end = node["start_sample"], node["end_sample"]
        if len(a) != end - first:
            raise ValueError(f"{node['id']}: asset length differs from mapped duration")
        stems["voice" if node["kind"] == "phrase" else "sfx"][first:end] += a
        shape = node.get("music_duck")
        if shape:
            attack = node["points"]["attack"]
            knots = [0, max(0, first - shape["lead_samples"]),
                     first + shape["attack_samples"], attack + shape["hold_samples"],
                     attack + shape["release_samples"], n]
            if knots != sorted(knots):
                raise ValueError(f"{node['id']}: unordered duck envelope")
            db = np.interp(samples, knots, [0, 0, shape["depth_db"],
                                           shape["depth_db"], 0, 0])
            # Overlaps use the deepest requested dip, never multiply dips.
            duck = np.minimum(duck, 10 ** (db / 20))
    stems["music"] *= duck[:, None]
    mix = sum(stems.values())
    peak = float(np.abs(mix).max())
    cap = 10 ** (plan["mix"]["peak_cap_dbfs"] / 20)
    gain = min(1.0, cap / max(peak, 1e-12))
    return {k: a * gain for k, a in stems.items()}, mix * gain, {
        "sample_rate": sr, "frames": n, "master_gain": gain,
        "music_duck_mode": "deepest_envelope", "listening": "UNVERIFIED",
        "original_bed": "Explicit preserved source mix stem; no source separation",
        "picture_review_required": [node["id"] for node in compiled["nodes"]
                                    if node["kind"] == "phrase" and
                                    node["start_sample"] != node.get("picture_bound_start_sample",
                                                                   node["start_sample"])]}
