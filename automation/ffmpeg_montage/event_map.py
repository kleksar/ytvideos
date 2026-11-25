"""Resolve an explicit, sample-clock graph for local speech-led edits.

This helper does not choose a channel/style or retime source pictures. Resolved
times are derived outputs: edit the authored map, never both independently.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


class MapError(ValueError):
    pass


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def integer(value, name):
    if type(value) is not int:
        raise MapError(f"{name}: expected integer samples, got {value!r}")
    return value


def compile_map(plan):
    """Resolve refs recursively, rejecting cycles, orphans and invalid bounds.

    A time is integer samples, or {ref, point, offset_samples?, quantize?}.
    A phrase has start + duration_samples + relative word intervals. An sfx has
    attack + attack_offset_samples + duration_samples. Other nodes have start
    and either end or duration_samples. Supported points: start/end,
    speech_start/speech_end (phrases), attack (sfx).
    """
    if plan.get("schema_version") != 1:
        raise MapError("Unsupported event-map schema")
    clock = plan["clock"]
    fps = integer(clock["fps"], "fps")
    sr = integer(clock["sample_rate"], "sample_rate")
    frames = integer(clock["total_frames"], "total_frames")
    if min(fps, sr, frames) <= 0 or sr % fps:
        raise MapError("Clock must have positive integral samples per frame")
    spf = sr // fps
    total = frames * spf
    authored = {}
    for node in plan["nodes"]:
        ident = node.get("id")
        if not isinstance(ident, str) or not ident or ident in authored:
            raise MapError(f"Missing/duplicate node id: {ident!r}")
        authored[ident] = node
    resolved, visiting = {}, set()

    def time(binding):
        if type(binding) is int:
            return binding
        if not isinstance(binding, dict) or set(binding) - {
                "ref", "point", "offset_samples", "quantize"}:
            raise MapError(f"Invalid time binding: {binding!r}")
        ref, point = binding.get("ref"), binding.get("point")
        other = resolve(ref)
        if point not in other["points"]:
            raise MapError(f"Unknown point {ref}.{point}")
        value = other["points"][point]
        quantize = binding.get("quantize")
        if quantize == "ceil_frame":
            value = -(-value // spf) * spf
        elif quantize is not None:
            raise MapError(f"Unknown quantization: {quantize}")
        return value + integer(binding.get("offset_samples", 0), "offset_samples")

    def resolve(ident):
        if ident in resolved:
            return resolved[ident]
        if ident not in authored:
            raise MapError(f"Unknown reference: {ident}")
        if ident in visiting:
            raise MapError(f"Cyclic event reference: {ident}")
        visiting.add(ident)
        node = authored[ident]
        kind = node.get("kind")
        if kind not in {"phrase", "sfx", "flash", "caption", "event"}:
            raise MapError(f"{ident}: unsupported kind {kind!r}")
        out = copy.deepcopy(node)
        if kind == "sfx":
            attack = time(node["attack"])
            lead = integer(node["attack_offset_samples"], "attack_offset_samples")
            duration = integer(node["duration_samples"], "duration_samples")
            if not 0 <= lead < duration:
                raise MapError(f"{ident}: attack outside sample")
            start, end = attack - lead, attack - lead + duration
            points = {"start": start, "end": end, "attack": attack}
        else:
            start = time(node["start"])
            if ("end" in node) == ("duration_samples" in node):
                raise MapError(f"{ident}: exactly one of end/duration_samples required")
            end = time(node["end"]) if "end" in node else start + integer(
                node["duration_samples"], "duration_samples")
            points = {"start": start, "end": end}
        if not 0 <= start < end <= total:
            raise MapError(f"{ident}: interval [{start},{end}) outside [0,{total})")
        if kind == "phrase":
            words, previous = [], 0
            for word in node["words"]:
                a = integer(word["start_sample"], "word.start_sample")
                b = integer(word["end_sample"], "word.end_sample")
                if not word.get("text") or not previous <= a < b <= end - start:
                    raise MapError(f"{ident}: invalid/overlapping word {word!r}")
                words.append({**word, "start_sample": start + a, "end_sample": start + b})
                previous = b
            if not words:
                raise MapError(f"{ident}: missing word map")
            out["resolved_words"] = words
            points.update(speech_start=words[0]["start_sample"],
                          speech_end=words[-1]["end_sample"])
        if kind == "caption":
            words = [token for row in node["rows"] for token in row["tokens"]]
            for token in words:
                if token.get("colour") not in plan["palette"]:
                    raise MapError(f"{ident}: unknown semantic colour")
            if node.get("phrase"):
                phrase = resolve(node["phrase"])
                normal = lambda s: "".join(c for c in s.casefold() if c.isalnum())
                if [normal(t["text"]) for t in words] != [
                        normal(w["text"]) for w in phrase["words"]]:
                    raise MapError(f"{ident}: caption tokens differ from spoken word map")
        out.update(points=points, start_sample=start, end_sample=end,
                   start_seconds=start / sr, end_seconds=end / sr,
                   first_frame=-(-start // spf), end_frame=-(-end // spf))
        visiting.remove(ident)
        resolved[ident] = out
        return out

    nodes = [resolve(ident) for ident in authored]
    audio = [{k: n[k] for k in ("id", "kind", "asset", "start_sample", "end_sample",
                               "gain_db", "music_duck") if k in n}
             for n in nodes if n["kind"] in {"phrase", "sfx"}]
    # Point bindings matter for duck recovery even when sample onset is unchanged.
    for n, a in zip([n for n in nodes if n["kind"] in {"phrase", "sfx"}], audio):
        a["points"] = n["points"]
    audio_assets = {a["asset"] for a in audio}
    audio_assets.update(b["asset"] for b in plan.get("beds", {}).values())
    identities = {a: plan.get("assets", {}).get(a, {}).get("sha256") for a in sorted(audio_assets)}
    return {"schema_version": 1, "clock": copy.deepcopy(clock), "nodes": nodes,
            "palette": copy.deepcopy(plan.get("palette", {})),
            "map_sha256": fingerprint(plan),
            "audio_sha256": fingerprint({"clock": clock, "nodes": audio,
                                         "beds": plan.get("beds", {}),
                                         "assets": identities, "mix": plan.get("mix"),
                                         "duck_mode": "deepest_envelope"}),
            "source_picture_retimed": False}


def shift_node(plan, ident, delta_samples):
    """Return a new map; references keep their relative offsets automatically."""
    delta_samples = integer(delta_samples, "delta_samples")
    shifted = copy.deepcopy(plan)
    node = next((n for n in shifted["nodes"] if n["id"] == ident), None)
    if node is None:
        raise MapError(f"Unknown node to shift: {ident}")
    key = "attack" if node["kind"] == "sfx" else "start"
    if type(node[key]) is int:
        node[key] += delta_samples
    else:
        node[key]["offset_samples"] = node[key].get("offset_samples", 0) + delta_samples
    # A literal end is also absolute authored timing, not a dependent reference.
    if key == "start" and type(node.get("end")) is int:
        node["end"] += delta_samples
    compile_map(shifted)
    return shifted


def verify_assets(plan, root):
    """Hash all explicit media inputs; no fallback to a similarly named asset."""
    checked = []
    for ident, asset in plan.get("assets", {}).items():
        p = Path(asset["path"])
        if not p.is_absolute():
            p = Path(root) / p
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        actual = h.hexdigest()
        if actual != asset["sha256"]:
            raise MapError(f"Asset hash mismatch: {ident}")
        checked.append({"id": ident, "path": str(p.resolve()), "sha256": actual})
    for node in plan["nodes"]:
        if node["kind"] in {"phrase", "sfx"} and node.get("asset") not in plan["assets"]:
            raise MapError(f"{node['id']}: missing asset binding")
    for bed in plan.get("beds", {}).values():
        if bed["asset"] not in plan["assets"]:
            raise MapError("Missing bed asset binding")
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--shift-samples", nargs=2, action="append", metavar=("ID", "DELTA"))
    parser.add_argument("--save-map", type=Path)
    parser.add_argument("--verify-assets", action="store_true")
    args = parser.parse_args()
    plan = json.loads(args.map.read_text(encoding="utf-8"))
    for ident, delta in args.shift_samples or []:
        plan = shift_node(plan, ident, int(delta))
    out = compile_map(plan)
    if args.verify_assets:
        out["verified_assets"] = verify_assets(plan, args.map.parent)
    if args.save_map:
        args.save_map.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
