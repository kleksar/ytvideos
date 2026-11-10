#!/usr/bin/env python3
"""Prepare paper cue rasters and static scene composites; never approve style/sync."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import shutil
import os
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, __version__ as PIL_VERSION

VERSION = "1.1.0"
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value, name, minimum=0):
    require(isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value > minimum, f"Invalid {name}")
    return value


def integer(value, name, minimum=1):
    require(type(value) is int and value >= minimum, f"Invalid {name}")
    return value


def unique(items, name):
    require(isinstance(items, list) and items, f"{name} must be a nonempty list")
    result = {}
    folded_ids = set()
    for item in items:
        require(isinstance(item, dict) and isinstance(item.get("id"), str) and ID.fullmatch(item["id"]), f"Invalid {name} ID")
        folded = item["id"].casefold()
        require(folded not in folded_ids, f"Duplicate {name} ID (case-insensitive): {item['id']}")
        folded_ids.add(folded)
        result[item["id"]] = item
    return result


class Inputs:
    def __init__(self, base):
        self.base = base
        self.files = {}

    def read(self, value):
        require(isinstance(value, str) and value, "An explicit input path is required")
        path = (self.base / value).resolve()
        if path not in self.files:
            self.files[path] = path.read_bytes()
        return self.files[path]

    def image(self, value):
        with Image.open(io.BytesIO(self.read(value))) as image:
            require(image.format == "PNG", f"Expected PNG input: {value}")
            return image.convert("RGBA")

    def hashes(self):
        return [{"path": str(path), "sha256": hashlib.sha256(data).hexdigest()}
                for path, data in sorted(self.files.items(), key=lambda pair: str(pair[0]))]


def face_bbox(mask):
    """Pillow bounds are half-open: right/bottom are exclusive, including one pixel."""
    box = mask.getbbox()
    require(box is not None, "Face mask is empty")
    return list(box)


def line_boxes(mask, count, authored=None):
    if authored is not None:
        require(isinstance(authored, list) and len(authored) == count, "face.line_boxes must match authored lines")
        covered = Image.new("L", mask.size)
        boxes = []
        previous_bottom = 0
        for box in authored:
            require(isinstance(box, list) and len(box) == 4 and all(type(n) is int for n in box), "Invalid face line box")
            x0, y0, x1, y1 = box
            require(0 <= x0 < x1 <= mask.width and previous_bottom <= y0 < y1 <= mask.height,
                    "Face line boxes must be ordered, nonoverlapping, inside the PNG")
            local = face_bbox(mask.crop(tuple(box)))
            boxes.append([local[0] + x0, local[1] + y0, local[2] + x0, local[3] + y0])
            covered.paste(mask.crop(tuple(box)), (x0, y0))
            previous_bottom = y1
        require(ImageChops.difference(mask, covered).getbbox() is None, "Face line boxes omit face pixels")
        return boxes
    rows = [y for y in range(mask.height) if mask.crop((0, y, mask.width, y + 1)).getbbox()]
    require(rows, "Face mask is empty")
    groups = [[rows[0], rows[0] + 1]]
    for y in rows[1:]:
        if y == groups[-1][1]:
            groups[-1][1] = y + 1
        else:
            groups.append([y, y + 1])
    require(len(groups) == count, "Face row bands do not match authored lines; supply explicit face.line_boxes")
    return [[0, y0, mask.width, y1] for y0, y1 in groups]


def cue_metrics(image, mask, boxes):
    alpha = image.getchannel("A").getbbox()
    require(alpha is not None, "Cue has no alpha pixels")
    face = face_bbox(mask)
    require(ImageChops.multiply(mask, image.getchannel("A").point(lambda v: 255 if v == 0 else 0)).getbbox() is None,
            "Face mask extends outside cue alpha")
    heights = [box[3] - box[1] for box in boxes]
    return {"size_px": list(image.size), "alpha_bbox": list(alpha), "face_bbox": face,
            "face_line_boxes": boxes, "face_line_heights_px": heights,
            "face_height_px": max(heights), "alpha_width_px": alpha[2] - alpha[0],
            "alpha_height_px": alpha[3] - alpha[1]}


def existing_png(spec, lines, inputs):
    image = inputs.image(spec["path"])
    require(image.getchannel("A").getextrema()[0] < 255, "Cue PNG must have actual transparency")
    face = spec["face"]
    if face.get("mode") == "mask":
        # Mask alpha is not the face mask: a grayscale PNG's luminance is explicit.
        raw = inputs.image(face["path"])
        require(raw.size == image.size, "Face mask dimensions differ from cue PNG")
        mask = raw.convert("L").point(lambda value: 255 if value > 0 else 0)
    elif face.get("mode") == "creamOrange":
        mask = Image.new("L", image.size)
        mask.putdata([255 if a > 30 and r > 160 and g > 110 and b > 70
                      and g > .58 * r and b > .50 * g else 0 for r, g, b, a in image.getdata()])
    else:
        raise ValueError("existingPNG requires explicit face.mode: mask or creamOrange")
    return image, mask, line_boxes(mask, len(lines), face.get("line_boxes"))


def color(value, name):
    require(isinstance(value, list) and len(value) == 4 and all(type(n) is int and 0 <= n <= 255 for n in value),
            f"{name} must be explicit RGBA")
    return tuple(value)


def render_text_mask(spec, lines, inputs):
    require("variation" in spec, "fontTexture requires explicit variation (null for a static font)")
    font = ImageFont.truetype(io.BytesIO(inputs.read(spec["font"])), integer(spec["font_px"], "font_px"))
    if spec["variation"] is not None:
        require(isinstance(spec["variation"], str) and spec["variation"], "Invalid variation")
        font.set_variation_by_name(spec["variation"].encode())
    texture = inputs.image(spec["texture"])
    require(texture.getchannel("A").getextrema() == (255, 255), "Texture must be an opaque PNG patch")
    gap = integer(spec["line_gap_px"], "line_gap_px", 0)
    text_boxes = [font.getbbox(line) for line in lines]
    require(all(box and box[2] > box[0] and box[3] > box[1] for box in text_boxes), "A line has no visible glyphs")
    edge = spec.get("edge")
    shadow = spec.get("shadow")
    edge_px = integer(edge["px"], "edge.px", 0) if edge else 0
    offset = shadow["offset_px"] if shadow else [0, 0]
    require(isinstance(offset, list) and len(offset) == 2 and all(type(n) is int for n in offset), "Invalid shadow offset")
    blur = number(shadow["blur_px"], "shadow.blur_px", -1) if shadow else 0
    require(blur >= 0, "shadow.blur_px must be nonnegative")
    pad = edge_px + math.ceil(blur * 4) + max(abs(n) for n in offset) + 4
    width = max(box[2] - box[0] for box in text_boxes) + 2 * pad
    height = sum(box[3] - box[1] for box in text_boxes) + gap * (len(lines) - 1) + 2 * pad
    mask = Image.new("L", (width, height))
    draw = ImageDraw.Draw(mask)
    y = pad
    boxes = []
    for text, box in zip(lines, text_boxes):
        w, h = box[2] - box[0], box[3] - box[1]
        x = (width - w) // 2
        draw.text((x - box[0], y - box[1]), text, font=font, fill=255)
        boxes.append([x, y, x + w, y + h])
        y += h + gap
    out = Image.new("RGBA", mask.size)
    if shadow:
        moved = Image.new("L", mask.size)
        moved.paste(mask, tuple(offset))
        layer = Image.new("RGBA", mask.size, color(shadow["color"], "shadow.color"))
        layer.putalpha(moved.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: round(v * shadow["color"][3] / 255)))
        out = Image.alpha_composite(out, layer)
    if edge:
        layer = Image.new("RGBA", mask.size, color(edge["color"], "edge.color"))
        outline = mask.filter(ImageFilter.MaxFilter(2 * edge_px + 1))
        layer.putalpha(outline.point(lambda v: round(v * edge["color"][3] / 255)))
        out = Image.alpha_composite(out, layer)
    face = Image.new("RGBA", mask.size)
    for y in range(0, height, texture.height):
        for x in range(0, width, texture.width):
            face.paste(texture, (x, y))
    face.putalpha(mask)
    return Image.alpha_composite(out, face), mask, line_boxes(mask, len(lines), boxes)


def normalize_face_height(image, mask, boxes, target):
    source = cue_metrics(image, mask, boxes)
    factor = target / source["face_height_px"]
    # One affine scale for both axes; integer output dimensions never squeeze width.
    size = (math.ceil(image.width * factor), math.ceil(image.height * factor))
    transform = (1 / factor, 0, 0, 0, 1 / factor, 0)
    out = image.transform(size, Image.Transform.AFFINE, transform, Image.Resampling.BICUBIC)
    scaled_mask = mask.transform(size, Image.Transform.AFFINE, transform, Image.Resampling.NEAREST)
    scaled_boxes = [[max(0, math.floor(x0 * factor)), max(0, math.floor(y0 * factor)),
                     min(size[0], math.ceil(x1 * factor)), min(size[1], math.ceil(y1 * factor))]
                    for x0, y0, x1, y1 in boxes]
    measured_boxes = []
    for x0, y0, x1, y1 in scaled_boxes:
        local = face_bbox(scaled_mask.crop((x0, y0, x1, y1)))
        measured_boxes.append([local[0] + x0, local[1] + y0, local[2] + x0, local[3] + y0])
    return out, scaled_mask, measured_boxes, factor


def composite_at_anchor(scene, cue, center, metrics):
    box = metrics["face_bbox"]
    left = round(center[0] * scene.width - (box[0] + box[2]) / 2)
    top = round(center[1] * scene.height - (box[1] + box[3]) / 2)
    layer = Image.new("RGBA", scene.size)
    layer.alpha_composite(cue, (left, top))
    return Image.alpha_composite(scene, layer), [left, top]


def geometry(metrics, position, anchor, canvas):
    x, y = position
    b = metrics["alpha_bbox"]
    box = [b[0] + x, b[1] + y, b[2] + x, b[3] + y]
    passed = (0 <= box[0] < box[2] <= canvas[0] and 0 <= box[1] < box[3] <= canvas[1]
              and metrics["alpha_width_px"] <= anchor["max_width_px"]
              and metrics["alpha_height_px"] <= anchor["max_height_px"])
    return {"technical": "PASS" if passed else "FAIL", "alpha_bbox_on_canvas": box,
            "visual": "UNVERIFIED", "sync": "UNVERIFIED", "motion": "UNVERIFIED"}


def prepare(manifest_path):
    inputs = Inputs(manifest_path.parent)
    raw = inputs.read(str(manifest_path))
    manifest = json.loads(raw)
    require(manifest.get("version") == 1, "Manifest version must be 1")
    canvas = manifest["canvas"]
    require(isinstance(canvas, list) and len(canvas) == 2, "canvas must be [width, height]")
    for n in canvas:
        integer(n, "canvas dimension")
    requested = integer(manifest["face_height_px"], "face_height_px")
    minimum = integer(manifest.get("min_face_height_px", 1), "min_face_height_px")
    require(minimum <= requested, "Minimum face height exceeds requested height")
    anchors = manifest["anchors"]
    require(isinstance(anchors, dict) and "primary" in anchors and set(anchors) <= {"primary", "alternate"},
            "Use primary and at most one alternate anchor")
    for name, anchor in anchors.items():
        center = anchor["center"]
        require(isinstance(center, list) and len(center) == 2 and all(
            isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n) and 0 < n < 1 for n in center),
            f"Invalid {name} center")
        number(anchor["max_width_px"], "max_width_px")
        number(anchor["max_height_px"], "max_height_px")
    scenes = unique(manifest["scenes"], "scene")
    cues = unique(manifest["cues"], "cue")
    pairs = manifest["pairs"]
    require(isinstance(pairs, list) and pairs, "Explicit scene/cue pairs are required")
    seen = set()
    for pair in pairs:
        key = (pair["scene"], pair["cue"])
        require(key not in seen, f"Duplicate assigned pair: {key}")
        require(pair["scene"] in scenes and pair["cue"] in cues and pair["anchor"] in anchors, "Unknown pair scene/cue/anchor")
        seen.add(key)
    require({p["cue"] for p in pairs} == set(cues), "Every cue needs an assigned scene")
    for scene in scenes.values():
        scene["image"] = inputs.image(scene["path"])
        require(scene["image"].size == tuple(canvas), f"Scene {scene['id']} dimensions differ from canvas")
        require(scene["image"].getchannel("A").getextrema() == (255, 255), "Scene must be full-frame opaque")
    base = {}
    for cue_id, cue in cues.items():
        lines = cue["lines"]
        require(isinstance(lines, list) and lines and all(isinstance(s, str) and s.strip() and "\n" not in s and "\r" not in s for s in lines),
                "Provide exact nonempty authored lines")
        backend = cue["backend"]
        require(isinstance(backend.get("status"), str) and backend["status"].strip(), "Explicit backend status is required")
        require(isinstance(cue.get("provenance"), dict), "Cue provenance must be explicit (an empty object is permitted)")
        inputs.image(backend["reference"])
        if backend["type"] == "existingPNG":
            image, mask, boxes = existing_png(backend, lines, inputs)
        elif backend["type"] == "fontTexture":
            image, mask, boxes = render_text_mask(backend, lines, inputs)
        else:
            raise ValueError("Unknown backend; use existingPNG or fontTexture")
        base[cue_id] = (image, mask, boxes)
    # Fit every cue at its assigned anchor(s); alternative comparisons keep this same size.
    target = float(requested)
    for pair in pairs:
        m = cue_metrics(*base[pair["cue"]])
        a = anchors[pair["anchor"]]
        h = m["face_height_px"]
        b, f = m["alpha_bbox"], m["face_bbox"]
        cx, cy = (f[0] + f[2]) / 2, (f[1] + f[3]) / 2
        limits = [a["max_width_px"] / m["alpha_width_px"], a["max_height_px"] / m["alpha_height_px"]]
        for space, extent in ((a["center"][0] * canvas[0], cx - b[0]),
                              ((1 - a["center"][0]) * canvas[0], b[2] - cx),
                              (a["center"][1] * canvas[1], cy - b[1]),
                              ((1 - a["center"][1]) * canvas[1], b[3] - cy)):
            if extent > 0:
                limits.append(space / extent)
        target = min(target, h * min(limits))
    target = math.floor(target)
    while target >= minimum:
        rendered = {key: normalize_face_height(*value, target) for key, value in base.items()}
        metrics = {key: cue_metrics(*value[:3]) for key, value in rendered.items()}
        if all(geometry(metrics[p["cue"]], composite_at_anchor(scenes[p["scene"]]["image"], rendered[p["cue"]][0],
                   anchors[p["anchor"]]["center"], metrics[p["cue"]])[1], anchors[p["anchor"]], canvas)["technical"] == "PASS" for p in pairs):
            break
        target -= 1
    else:
        raise ValueError("Cues cannot fit at the declared minimum face height; revise the authored layout")
    report = {"version": 1, "helper_version": VERSION, "helper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "pillow_version": PIL_VERSION, "manifest_sha256": hashlib.sha256(raw).hexdigest(),
              "source_manifest": json.loads(raw), "inputs": inputs.hashes(), "canvas": canvas,
              "shared_face_height_px": target, "checks": {"scope": "assigned pairs at their selected anchors; static geometry only",
                  "technical": "PASS", "visual": "UNVERIFIED", "sync": "UNVERIFIED", "motion": "UNVERIFIED"},
              "cues": [], "pairs": []}
    outputs = {}
    for cue_id, cue in cues.items():
        outputs[f"cues/{cue_id}/cue.png"] = rendered[cue_id][0]
        outputs[f"cues/{cue_id}/face.png"] = rendered[cue_id][1]
        report["cues"].append({"id": cue_id, "lines": cue["lines"], "backend": cue["backend"],
                              "provenance": cue["provenance"], "timing": cue.get("timing"),
                              "metrics": metrics[cue_id], "uniform_scale": rendered[cue_id][3], "png": f"cues/{cue_id}/cue.png",
                              "face_mask": f"cues/{cue_id}/face.png"})
    for pair in pairs:
        comparisons = []
        for name, anchor in anchors.items():
            preview, position = composite_at_anchor(scenes[pair["scene"]]["image"], rendered[pair["cue"]][0], anchor["center"], metrics[pair["cue"]])
            prefix = f"previews/{pair['scene']}/{pair['cue']}/{name}"
            outputs[prefix + ".png"] = preview
            phone = preview.copy()
            phone.thumbnail((360, 640), Image.Resampling.LANCZOS)
            outputs[prefix + "__phone.png"] = phone
            comparisons.append({"anchor": name, "center": anchor["center"], "layer_top_left_px": position,
                                "preview": prefix + ".png", "phone_preview": prefix + "__phone.png",
                                "checks": geometry(metrics[pair["cue"]], position, anchor, canvas)})
        report["pairs"].append({**pair, "comparisons": comparisons})
    return outputs, report


def run(manifest_path, output, previews_output=None):
    manifest_path, output = Path(manifest_path).resolve(), Path(output).resolve()
    require(not output.exists(), "Output directory already exists; choose a new version")
    require(output.parent.is_dir(), "Output parent must already exist")
    if previews_output is not None:
        previews_output = Path(previews_output).absolute()
        require(previews_output.is_dir() and not list(previews_output.iterdir()), "Preview directory must be empty")
        require(not previews_output.is_relative_to(output), "Previews must be stored separately")
    outputs, report = prepare(manifest_path)
    # Reserve only after every input, raster and selected geometry has been validated.
    output.mkdir()
    try:
        for relative, image in outputs.items():
            dest = previews_output / Path(relative).relative_to('previews') if previews_output and relative.startswith('previews/') else output / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            image.save(dest, format="PNG")
        for cue in report["cues"]:
            cue["png_sha256"] = hashlib.sha256((output / cue["png"]).read_bytes()).hexdigest()
            cue["face_mask_sha256"] = hashlib.sha256((output / cue["face_mask"]).read_bytes()).hexdigest()
        if previews_output:
            for pair in report['pairs']:
                for comparison in pair['comparisons']:
                    for key in ('preview', 'phone_preview'):
                        actual = previews_output / Path(comparison[key]).relative_to('previews')
                        comparison[key] = os.path.relpath(actual, output)
            report['storage'] = {'dependencies': str(output), 'previews': str(previews_output)}
        (output / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except BaseException:
        shutil.rmtree(output)
        raise
    return report


def run_managed(manifest, episode, run_id):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'media-lifecycle/scripts'))
    import workspace as storage
    episode = storage.initialize(episode)
    owner = 'captions-' + str(os.getpid())
    with storage.locked(episode):
        directory = storage.start(episode, run_id, owner)
        target = episode / 'Assets/Generated' / run_id
        try:
            storage.inventory.no_symlinks(target)
            report = run(manifest, target, directory / 'previews')
            for cue in report['cues']:
                for field in ('png', 'face_mask'):
                    rel = str((target / cue[field]).relative_to(episode))
                    storage.register(episode, run_id, owner, rel, 'dependency')
            for path in sorted((directory / 'previews').rglob('*.png')):
                storage.register(episode, run_id, owner, str(path.relative_to(episode)), 'preview')
            storage.finish(episode, run_id, owner, 'complete', True)
            return report
        except BaseException:
            storage.finish(episode, run_id, owner, 'failed', True)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, help="Legacy explicit single output directory")
    parser.add_argument('--episode', type=Path, help='Managed episode: separate dependencies/previews')
    parser.add_argument('--run-id', help='New unique caption run id')
    args = parser.parse_args()
    try:
        if args.episode and args.run_id and not args.output:
            report = run_managed(args.manifest, args.episode, args.run_id)
        elif args.output and not args.episode and not args.run_id:
            report = run(args.manifest, args.output)
        else:
            raise ValueError('Use --episode with --run-id, or legacy --output')
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.exit(2, f"Caption preparation failed: {error}\n")
    print(f"Prepared {len(report['cues'])} cues, {len(report['pairs'])} assigned pairs; shared face height {report['shared_face_height_px']}px. Visual/sync/motion UNVERIFIED.")


if __name__ == "__main__":
    main()
