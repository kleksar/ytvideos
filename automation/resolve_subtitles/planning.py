"""Offline Resolve subtitle conformance. No session access, media writes or alignment.

Source in/out and word times are seconds; timelines use absolute, half-open
record frames. Required observed anchors are evidence, not trusted playback QA.
"""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
_SHA = re.compile(r"[0-9a-f]{64}")
_SLUG = re.compile(r"[a-z][a-z0-9_]{1,63}")


def _tool(root):
    spec = importlib.util.spec_from_file_location(
        "ytv_resolve_srt", root / "automation/helpers/srt/scripts/srt_tool.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _text(value, name):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError(f"{name} must be nonempty single-line text")
    return value.strip()


def _id(value, name):
    result = _text(value, name)
    if result != value or result.lower() in {"current", "active", "default", "unknown"}:
        raise ValueError(f"{name} must be an exact stable identity")
    return result


def _num(value, name):
    if type(value) not in (int, float, str):
        raise ValueError(f"{name} must be a finite rational number")
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a finite rational number") from exc


def _frame(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer record frame")
    return value


def _round(value):
    # Half up with exact arithmetic; frame products are nonnegative.
    return int(value + Fraction(1, 2))


def _hash(value):
    return hashlib.sha256(value).hexdigest()


def _target(request):
    raw = request.get("target")
    if not isinstance(raw, dict):
        raise ValueError("exact target is required")
    keys = {"project_id", "timeline_id", "fps", "raster", "origin_frame", "end_frame"}
    if set(raw) != keys:
        raise ValueError("target requires exact project, timeline, fps, raster, origin and end")
    project = _id(raw.get("project_id"), "project_id")
    timeline = _id(raw.get("timeline_id"), "timeline_id")
    fps = _num(raw.get("fps"), "fps")
    # 23.976/29.97 display values are not an exact rational read-back.
    if fps <= 1 or (fps.denominator != 1
                    and not (isinstance(raw["fps"], str) and "/" in raw["fps"])):
        raise ValueError("fps requires an exact integer or explicit rational timebase")
    raster = raw.get("raster")
    if not isinstance(raster, list) or len(raster) != 2 or any(type(x) is not int or x <= 0 for x in raster):
        raise ValueError("raster must contain two positive integer dimensions")
    origin, end = (_frame(raw.get(k), k) for k in ("origin_frame", "end_frame"))
    if end <= origin:
        raise ValueError("target interval must be nonempty")
    return dict(project_id=project, timeline_id=timeline, fps=str(fps), raster=list(raster),
                origin_frame=origin, end_frame=end), fps


def _placements(records, target, fps):
    if not isinstance(records, list) or not records:
        raise ValueError("read-back voice placements are required")
    result, previous = {}, target["origin_frame"]
    allowed = {"id", "source_sha256", "source_in", "source_out", "timeline_start",
               "timeline_end", "speed", "retime"}
    for raw in records:
        if not isinstance(raw, dict) or set(raw) - allowed or raw.get("retime", "linear") != "linear":
            raise ValueError("only unambiguous constant-speed voice placements are supported")
        identity = _id(raw.get("id"), "placement id")
        sha = raw.get("source_sha256")
        if identity in result or not isinstance(sha, str) or not _SHA.fullmatch(sha):
            raise ValueError("voice placements require unique IDs and exact SHA-256")
        source_in, source_out, speed = (_num(raw.get(key), key)
                                        for key in ("source_in", "source_out", "speed"))
        start, end = (_frame(raw.get(key), key) for key in ("timeline_start", "timeline_end"))
        if not (0 <= source_in < source_out and speed > 0):
            raise ValueError("voice source interval and constant positive speed are required")
        if not previous <= start < end <= target["end_frame"]:
            raise ValueError("voice placements overlap, are out of order, or exceed target interval")
        if _round((source_out - source_in) * fps / speed) != end - start:
            raise ValueError("voice placement length disagrees with trims, speed and timeline timebase")
        result[identity] = (sha, source_in, source_out, start, end, speed)
        previous = end
    return result


def _words(records, placements, fps):
    if not isinstance(records, list) or not records:
        raise ValueError("source word alignment is required for a speech edit")
    result, previous = [], None
    for index, rec in enumerate(records):
        if not isinstance(rec, dict):
            raise ValueError("word alignment entries must be objects")
        identity = _id(rec.get("placement_id"), "word placement id")
        if identity not in placements:
            raise ValueError("word placement is absent or ambiguous")
        sha, source_in, source_out, start, end, speed = placements[identity]
        if rec.get("source_sha256") != sha:
            raise ValueError("word-map audio hash differs from its read-back placement")
        if not Fraction(4, 5) <= _num(rec.get("confidence"), "word confidence") <= 1:
            raise ValueError("word confidence below 0.80 or invalid; check source alignment")
        a, b = (_num(rec.get(key), "word " + key) for key in ("start", "end"))
        if not source_in <= a < b <= source_out:
            raise ValueError("word intersects a trim or falls outside its actual source placement")
        exact_a, exact_b = (start + (x - source_in) * fps / speed for x in (a, b))
        fa, fb = _round(exact_a), _round(exact_b)
        if not start <= fa < fb <= end or previous is not None and exact_a < previous:
            raise ValueError("word intervals overlap, are out of order, or collapse after frame quantization")
        previous = exact_b
        text = _text(rec.get("text"), "word text")
        if len(text.split()) != 1:
            raise ValueError("highlightable word timings must identify individual tokens")
        result.append(dict(index=index, placement_id=identity, text=text, start_frame=fa, end_frame=fb))
    return result


def _style(request, target, fps, root):
    channel = request.get("channel")
    form = request.get("format")
    if not isinstance(channel, str) or not _SLUG.fullmatch(channel) or form not in {"short", "long"}:
        raise ValueError("explicit supported channel and format required")
    profile_file = root / "channels" / channel / "channel.json"
    data = profile_file.read_bytes()
    profile = json.loads(data)
    if profile.get("id") != channel:
        raise ValueError("channel identity differs from the profile")
    production = profile.get("production", {})
    fmt = production.get("formats", {}).get(form)
    if not isinstance(fmt, dict):
        raise ValueError("channel format has no committed production profile")
    variants = fmt.get("variants", {})
    variant = request.get("variant")
    if variants and (not isinstance(variant, str) or variant not in variants) or not variants and variant is not None:
        raise ValueError("explicit matching caption production variant required")
    selected = variants.get(variant, {})
    video = {**production.get("video", {}), **fmt.get("video", {}), **selected.get("video", {})}
    if video.get("canvas") != target["raster"] or _num(video.get("fps"), "profile fps") != fps:
        raise ValueError("observed timeline raster/fps differ from channel format")
    cfg = {**production.get("captions", {}), **fmt.get("captions", {}), **selected.get("captions", {})}
    mode = cfg.get("mode")
    if mode not in {"word_highlight", "when_speech"}:
        raise ValueError("this format has no supported ordinary speech subtitle recipe")
    result = dict(mode=mode, channel=channel, format=form, profile_sha256=_hash(data),
                  font_face=cfg.get("font"), text_plus_supported=mode == "word_highlight")
    if mode == "word_highlight":
        visual = profile.get("visual_profile")
        if (not isinstance(cfg.get("font"), dict) or not all(cfg["font"].get(k) for k in ("family", "style"))
                or not isinstance(visual, str) or not _SLUG.fullmatch(visual)):
            # Canonical montage profiles include the short name "paper"/"nuviko";
            # the same slug safety check applies to filesystem paths.
            raise ValueError("channel Text+ font and visual profile are not configured")
        profiles = root / "automation/ffmpeg_montage/profiles"
        style = (profiles / (visual + ".json")).read_bytes()
        geom = profiles / (visual + "_" + form + ".json")
        if not geom.is_file():
            geom = profiles / (form + ".json")
        geometry = geom.read_bytes()
        result.update(style=json.loads(style), geometry=json.loads(geometry),
                      style_sha256=_hash(style), geometry_sha256=_hash(geometry))
    return result


def _sync(evidence, placements, words, tool):
    if (not isinstance(evidence, dict) or evidence.get("kind") != "timeline_observed"
            or not isinstance(evidence.get("anchors"), list)):
        raise ValueError("observed timeline anchor evidence is required")
    provenance = _text(evidence.get("source"), "timeline anchor evidence source")
    support = {identity: [] for identity in placements}
    for word in words:
        support[word["placement_id"]].append(word["index"])
    seen, measures = set(), []
    for anchor in evidence["anchors"]:
        if not isinstance(anchor, dict):
            raise ValueError("anchor must be an object")
        index, edge = anchor.get("word_index"), anchor.get("edge", "start")
        if type(index) is not int or not 0 <= index < len(words) or edge not in ("start", "end"):
            raise ValueError("anchor must identify a supported word and edge")
        word = words[index]
        identity = word["placement_id"]
        if anchor.get("placement_id") != identity or (index, edge) in seen:
            raise ValueError("anchor identity is ambiguous or duplicated")
        seen.add((index, edge))
        at = _frame(anchor.get("timeline_frame"), "observed anchor")
        _, _, _, start, end, _ = placements[identity]
        if not start <= at <= end:
            raise ValueError("anchor outside actual placement")
        measures.append(dict(label=f"{identity}:word {index} {edge}", voice_frame=at,
                             caption_frame=word[edge + "_frame"]))
    for indexes in support.values():
        if not indexes:
            raise ValueError("voice placement missing aligned words")
        required = {indexes[0], indexes[len(indexes)//2], indexes[-1]}
        if not required <= {index for index, edge in seen if edge == "start"}:
            raise ValueError("observed word-start anchors must cover first/middle/last of each placement")
    report = tool.compare_sync_anchors(sorted(measures, key=lambda row: row["voice_frame"]))
    if report["result"] != "WITHIN_ONE_FRAME":
        raise ValueError(f"timeline anchor mismatch: {report['result']}; do not guess a global shift")
    return {**report, "source": provenance}


def _groups(request, words):
    groups = request.get("groups")
    if not isinstance(groups, list) or not groups:
        raise ValueError("explicit reviewed semantic cue grouping is required")
    grouped, order, owners = [], [], {}
    for number, indexes in enumerate(groups):
        if (not isinstance(indexes, list) or not indexes
                or any(type(x) is not int or not 0 <= x < len(words) for x in indexes)):
            raise ValueError("group requires nonempty word indexes")
        group = [words[index] for index in indexes]
        if len({word["placement_id"] for word in group}) != 1:
            raise ValueError("a cue cannot cross a speech cut; review its grouping")
        order.extend(indexes)
        owners.update((index, number) for index in indexes)
        grouped.append(group)
    if order != list(range(len(words))):
        raise ValueError("cue groups must preserve every word exactly once in timeline order")
    spans = request.get("keep_together", [])
    if not isinstance(spans, list):
        raise ValueError("keep_together must contain reviewed entity/number spans")
    for span in spans:
        if (not isinstance(span, list) or len(span) < 2
                or any(type(x) is not int or x not in owners for x in span)
                or span != list(range(span[0], span[-1] + 1))
                or len({owners[x] for x in span}) != 1):
            raise ValueError("a protected entity or number span was split or is invalid")
    return grouped


def plan_subtitles(request, *, root=None):
    """Map an explicitly observed speech edit and grouping to editable captions."""
    if not isinstance(request, dict):
        raise ValueError("subtitle request must be an object")
    root = Path(root) if root is not None else ROOT
    target, fps = _target(request)
    placements = _placements(request.get("placements"), target, fps)
    words = _words(request.get("words"), placements, fps)
    groups = _groups(request, words)
    style = _style(request, target, fps, root)
    if style.get("style", {}).get("name") == "paper" and request["format"] == "short" and any(len(group) > 3 for group in groups):
        raise ValueError("Paper Short captions permit at most three words per cue")
    tool = _tool(root)
    alignment = _sync(request.get("evidence"), placements, words, tool)
    default_hold = style.get("style", {}).get("name") == "nuviko" and request["format"] == "long"
    hold = request.get("hold_gaps", default_hold)
    if type(hold) is not bool:
        raise ValueError("hold_gaps must be a boolean channel decision")
    origin = target["origin_frame"]

    cues, srt_cues = [], []
    for i, group in enumerate(groups):
        start, spoken_end = group[0]["start_frame"], group[-1]["end_frame"]
        end = groups[i+1][0]["start_frame"] if hold and i+1 < len(groups) else spoken_end
        value = " ".join(word["text"] for word in group)
        cues.append(dict(id=f"C{i+1:04d}", text=value, start_frame=start, end_frame=end,
                         spoken_start_frame=start, spoken_end_frame=spoken_end, words=group))
        # The accessibility track follows real speech, not the visual phrase hold.
        sa, sb = (_round(Fraction(frame - origin) * 1000 / fps) for frame in (start, spoken_end))
        srt_cues.append(f"{i+1}\n{tool.stamp(sa)} --> {tool.stamp(sb)}\n{value}")
    srt = "\n\n".join(srt_cues) + "\n"
    duration = Decimal(_round(Fraction(target["end_frame"] - origin) * 1000 / fps)) / 1000
    supplied = request.get("transcript", " ".join(word["text"] for word in words))
    if not isinstance(supplied, str):
        raise ValueError("expected transcript must be text")
    _, report = tool.check(tool.parse_srt(srt), supplied, duration, {"max_lines": 1})
    if report["structure"] != "PASS" or report["text_coverage"] != "PASS":
        raise ValueError("SRT structure or exact transcript coverage failed")
    # Fraction strings canonicalize equivalent input spellings; provenance is
    # distinct from PASS at the named anchor frames and from native read-back.
    binding = dict(target=target, placements=[dict(id=identity, sha256=values[0],
        source_in=str(values[1]), source_out=str(values[2]), start=values[3], end=values[4],
        speed=str(values[5])) for identity, values in placements.items()])
    conform = _hash(json.dumps(binding, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())
    if request["evidence"].get("conform_sha256", conform) != conform:
        raise ValueError("anchor evidence fingerprint is stale for this voice conformance")
    return dict(schema="ytv-resolve-subtitles-plan-v1", target=target, style=style, cues=cues, srt=srt,
                alignment=alignment, conformance=binding, conform_sha256=conform,
                srt_check=report, playback="UNVERIFIED")
