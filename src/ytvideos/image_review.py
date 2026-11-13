"""Bind thumbnail review to actual artwork and inspection derivatives.

These checks establish identities, coverage and an independent review record.
They cannot judge composition, authenticate a person's perception or predict CTR.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re

from .errors import WorkflowError
from .util import file_digest, require_text


SCHEMA = "ytv-thumbnail-review-v1"
OBSERVATIONS = {"focal_point", "story_relation", "title_pair", "phone_size", "crop"}
PREVIEW_HELPER = "automation/helpers/youtube-thumbnails/scripts/thumbnail_previews.py"


def thumbnail_references(brief, artifacts):
    """Reuse the registered references understood by the native image host."""
    require_text(brief.get("title"), "thumbnail exact title")
    references = brief.get("references", [])
    if not isinstance(references, list):
        raise WorkflowError("thumbnail references must be registered artifact IDs")
    selected = []
    for reference in references:
        key = reference.get("artifact_id") if isinstance(reference, dict) else reference
        if not isinstance(key, str) or key not in artifacts:
            raise WorkflowError("register every selected thumbnail reference before generation")
        if key in selected:
            raise WorkflowError("duplicate thumbnail reference")
        selected.append(key)
    if not selected:
        require_text(brief.get("reference_na_reason"), "thumbnail reference_na_reason")
    return [artifacts[key] for key in selected]


def _record(value):
    if (not isinstance(value, dict) or set(value) != {"path", "sha256"}
            or not isinstance(value["path"], str) or not value["path"].strip()
            or not isinstance(value["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", value["sha256"])):
        raise WorkflowError("thumbnail evidence requires an exact path and SHA-256")
    return value


def validate_observation(observed, *, artifact_sha256, worker, brief, artifacts):
    """Cheap receipt checks; actual file inspection happens outside the transaction."""
    if not isinstance(observed, dict) or observed.get("schema") != SCHEMA:
        raise WorkflowError("thumbnail review requires the current structured observation")
    if observed.get("artifact_sha256") != artifact_sha256:
        raise WorkflowError("thumbnail review identifies different artwork")
    reviewer = require_text(observed.get("reviewer"), "thumbnail independent reviewer")
    if reviewer.strip() == worker.strip():
        raise WorkflowError("thumbnail review requires a reviewer distinct from the image generator")
    selected = thumbnail_references(brief, artifacts)
    if observed.get("title") != brief["title"]:
        raise WorkflowError("thumbnail review title differs from the exact brief title")
    notes = observed.get("observations")
    if not isinstance(notes, dict) or set(notes) != OBSERVATIONS:
        raise WorkflowError("thumbnail review needs separate composition, title, phone-size and crop observations")
    for name in OBSERVATIONS:
        require_text(notes[name], "thumbnail observation " + name)
    for name in ("preview_manifest", "phone_preview", "crop_preview", "evidence"):
        _record(observed.get(name))
    comparisons = observed.get("references")
    if not isinstance(comparisons, list):
        raise WorkflowError("thumbnail review must compare the selected references")
    expected = {artifact["id"]: artifact["sha256"] for artifact in selected}
    seen = set()
    for comparison in comparisons:
        if not isinstance(comparison, dict):
            raise WorkflowError("thumbnail reference comparison must be an object")
        key = comparison.get("artifact_id")
        if (not isinstance(key, str) or key in seen or key not in expected
                or comparison.get("sha256") != expected[key]):
            raise WorkflowError("thumbnail reference comparison differs from selected exact artifacts")
        require_text(comparison.get("comparison"), "thumbnail reference comparison")
        seen.add(key)
    if seen != set(expected):
        raise WorkflowError("thumbnail review omits selected reference comparisons")
    if not expected and observed.get("reference_na_reason") != brief["reference_na_reason"]:
        raise WorkflowError("thumbnail review must retain the brief's explicit reason for no references")
    return observed


def validate_files(observed, *, image_path, format, channel_name, project_root):
    """Verify helper outputs, actual dimensions/crops, title and evidence bytes.

    The existing helper owns crop/render math. Reusing its byte renderer verifies
    derivatives without creating another preview generator or a semantic score.
    """
    from PIL import Image, ImageOps

    records = []

    def checked(value):
        record = _record(value)
        path = Path(record["path"]).resolve()
        if not path.is_file() or path.stat().st_size == 0 or file_digest(path) != record["sha256"]:
            raise WorkflowError("thumbnail evidence is missing, corrupt or stale: " + str(path))
        normalized = {"path": str(path), "sha256": record["sha256"]}
        if normalized not in records:
            records.append(normalized)
        return path

    manifest_path = checked(observed["preview_manifest"])
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise WorkflowError("thumbnail preview manifest must be readable JSON") from exc
    helper_path = Path(project_root) / PREVIEW_HELPER
    spec = importlib.util.spec_from_file_location("ytv_thumbnail_previews", helper_path)
    if spec is None or spec.loader is None or not helper_path.is_file():
        raise WorkflowError("canonical thumbnail preview helper is unavailable")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    if (not isinstance(manifest, dict) or manifest.get("schema") != helper.SCHEMA
            or manifest.get("sha256") != observed["artifact_sha256"]):
        raise WorkflowError("thumbnail preview manifest does not bind the exact artwork")
    source = checked({"path": manifest.get("source"), "sha256": manifest["sha256"]})
    if file_digest(image_path) != manifest["sha256"]:
        raise WorkflowError("thumbnail preview source differs from the completed image")
    with Image.open(image_path) as raw:
        image = ImageOps.exif_transpose(raw).convert("RGB")
    if manifest.get("source_pixels") != list(image.size):
        raise WorkflowError("thumbnail preview source dimensions are incorrect")
    previews = manifest.get("previews")
    if not isinstance(previews, list) or not previews:
        raise WorkflowError("thumbnail review requires actual small previews")
    by_path = {}
    for preview in previews:
        if not isinstance(preview, dict):
            raise WorkflowError("thumbnail preview must contain dimensions and a crop")
        path = checked({"path": preview.get("path"), "sha256": preview.get("sha256")})
        if str(path) in by_path:
            raise WorkflowError("duplicate thumbnail preview path")
        pixels, box = preview.get("pixels"), preview.get("crop_box_source_px")
        if (not isinstance(pixels, list) or len(pixels) != 2
                or any(type(value) is not int or value < 1 or value > 4096 for value in pixels)
                or not isinstance(box, list) or len(box) != 4
                or any(type(value) not in (int, float) or not math.isfinite(value) for value in box)
                or not (0 <= box[0] < box[2] <= image.width and 0 <= box[1] < box[3] <= image.height)):
            raise WorkflowError("thumbnail preview geometry is invalid")
        if pixels[1] != round(pixels[0] * (box[3] - box[1]) / (box[2] - box[0])):
            raise WorkflowError("thumbnail preview stretches its crop")
        with Image.open(path) as raw:
            raw.load()
            if raw.size != tuple(pixels):
                raise WorkflowError("thumbnail preview dimensions differ from actual bytes")
        expected = hashlib.sha256(helper.preview_bytes(image, pixels, box)).hexdigest()
        if expected != preview["sha256"]:
            raise WorkflowError("thumbnail preview is not the canonical derivative of the completed image")
        by_path[str(path)] = preview
    full_box = [0, 0, image.width, image.height]
    for name in ("phone_preview", "crop_preview"):
        path = checked(observed[name])
        preview = by_path.get(str(path))
        if (preview is None or preview["sha256"] != observed[name]["sha256"]
                or not 180 <= preview["pixels"][0] <= 360):
            raise WorkflowError("thumbnail review must identify actual phone-size previews between 180 and 360px width")
        expected_box = (list(helper.center_box(image.size, 2 / 3))
                        if name == "crop_preview" and format == "short" else full_box)
        if any(abs(actual - expected) > .001
               for actual, expected in zip(preview["crop_box_source_px"], expected_box)):
            raise WorkflowError("thumbnail review omits the full image or required displayed crop")
    card = manifest.get("card_mock")
    if not isinstance(card, dict):
        raise WorkflowError("thumbnail review requires the exact title/image card mock")
    page = checked({"path": card.get("path"), "sha256": card.get("sha256")})
    card_json = checked({"path": card.get("json_path"), "sha256": card.get("json_sha256")})
    try:
        cards = helper.load_cards(card_json, source)
    except (ValueError, OSError) as exc:
        raise WorkflowError("thumbnail card inputs are invalid") from exc
    if not cards or cards[0]["title"] != observed["title"] or cards[0]["channel"] != channel_name:
        raise WorkflowError("thumbnail card title/channel differs from the accepted brief")
    assets = [{"path": str(card["src"]), "sha256": card["sha256"], "title": card["title"],
               "channel": card["channel"], "duration": card["duration"]} for card in cards]
    if card.get("assets") != assets:
        raise WorkflowError("thumbnail card asset list differs from actual inputs")
    for asset in assets:
        checked({key: asset[key] for key in ("path", "sha256")})
    if (card.get("theme") not in {"light", "dark", "both"} or type(card.get("grayscale")) is not bool
            or page.read_text(encoding="utf-8") != helper.build_card_html(cards, card["theme"], card["grayscale"])):
        raise WorkflowError("thumbnail card mock differs from the canonical title/image rendering")
    checked(observed["evidence"])
    return records
