#!/usr/bin/env python3
"""Prepare a film for editorial selection or render every selected plan in parallel."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


PIPELINE = Path(__file__).resolve().parent
TEASER_FIELDS = ("open_question", "mini_payoff", "cut_reason")


def write_json(path, value):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def digest(path):
    with path.open("rb") as source:
        sha = hashlib.sha256()
        for chunk in iter(lambda: source.read(4 * 1024 * 1024), b""):
            sha.update(chunk)
        return sha.hexdigest()


def read_plan(path, source, discovery):
    plan = json.loads(path.read_text(encoding="utf-8"))
    clip_id = plan.get("id")
    if not isinstance(clip_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", clip_id):
        raise ValueError(f"{path.name}: expected a safe clip id")
    if plan.get("source") and (path.parent / plan["source"]).resolve() != source:
        raise ValueError(f"{path.name}: plan identifies a different film")
    if discovery and plan.get("audio_stream") != discovery["audio_stream"]:
        raise ValueError(f"{path.name}: audio stream differs from discovery")
    if type(plan.get("audio_stream")) is not int or plan["audio_stream"] < 0:
        raise ValueError(f"{path.name}: missing absolute audio stream index")
    if not all(isinstance(plan.get(k), str) and plan[k].strip() for k in ("title", "hook", "poster")):
        raise ValueError(f"{path.name}: title, hook and official poster are required")
    if not isinstance(plan.get("shots"), list) or not plan["shots"] or not isinstance(plan.get("cues"), list):
        raise ValueError(f"{path.name}: expected shots and cues lists")
    intent = plan.get("edit_intent", "scene")
    if intent not in ("scene", "teaser"):
        raise ValueError(f"{path.name}: edit_intent must be scene or teaser")
    if intent == "teaser" and not all(isinstance(plan.get(key), str) and plan[key].strip()
                                       for key in TEASER_FIELDS):
        raise ValueError(f"{path.name}: teaser requires {', '.join(TEASER_FIELDS)}")
    poster = (path.parent / plan["poster"]).resolve(strict=True)
    if not poster.is_file():
        raise ValueError(f"{path.name}: invalid poster path")
    plan["poster"] = str(poster)
    plan["source"] = str(source)
    plan["edit_intent"] = intent
    return plan, poster


def render_one(source, plan, out, clip_id, language):
    start = time.time()
    argv = [sys.executable, str(PIPELINE / "render_clip.py"), str(source), str(plan), str(out)]
    media = out / f"{clip_id}.mp4"
    qa = out / f"{clip_id}.qa.json"
    result = {"started_unix": start, "log": str(out / "render.log"), "argv": argv}
    try:
        with (out / "render.log").open("w", encoding="utf-8") as log:
            proc = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT)
        if proc.returncode or not media.is_file() or not qa.is_file():
            raise ValueError(f"Renderer exit {proc.returncode}; MP4 or QA receipt missing or render failed")
        receipt = json.loads(qa.read_text(encoding="utf-8"))
        media_hash = digest(media)
        if receipt.get("sha256") != media_hash or receipt.get("full_decode") != "pass":
            raise ValueError("MP4 does not match the renderer's technical QA receipt")
        result.update(status="rendered", mp4=str(media), qa=str(qa), sha256=media_hash)
        sidecar = out / f"{clip_id}.{language}.srt"
        if sidecar.is_file():
            result["srt"] = str(sidecar)
    except (OSError, ValueError) as exc:
        result.update(status="failed", error=str(exc))
    result["finished_unix"] = time.time()
    return result


def render_batch(args, source):
    discovery = None
    source_stat = source.stat()
    if args.discovery:
        discovery_path = args.discovery.resolve(strict=True)
        discovery = json.loads(discovery_path.read_text(encoding="utf-8"))
        if Path(discovery["source"]).resolve() != source:
            raise ValueError("Discovery report identifies a different film")
        if (discovery.get("source_size_bytes") != source_stat.st_size or
                discovery.get("source_mtime_ns") != source_stat.st_mtime_ns):
            raise ValueError("Film changed since discovery; run discovery again")
    if args.jobs < 1:
        raise ValueError("--jobs must be at least 1")
    plans = {}
    poster_hashes = {}
    for path in sorted(args.plans.resolve(strict=True).glob("*.json")):
        plan, poster = read_plan(path, source, discovery)
        if plan["id"] in plans:
            raise ValueError(f"Duplicate clip id: {plan['id']}")
        if poster not in poster_hashes:
            poster_hashes[poster] = digest(poster)
        plans[plan["id"]] = (plan, path, poster_hashes[poster])
    if not plans:
        raise ValueError("No selected JSON plans found")

    output = args.output.resolve()
    source_hash = digest(source)
    current = source.stat()
    if (current.st_size, current.st_mtime_ns) != (source_stat.st_size, source_stat.st_mtime_ns):
        raise ValueError("Film changed while verifying its identity")
    scripts = [PIPELINE / "render_clip.py", PIPELINE.parent / "add_film_poster.py"]
    script_hashes = {script.name: digest(script) for script in scripts}
    output.mkdir(parents=True, exist_ok=False)
    workers = min(args.jobs, len(plans))
    manifest = {
        "format": "film-shorts-v1", "source": str(source), "source_sha256": source_hash,
        "source_bytes": source_stat.st_size, "output": str(output), "scripts_sha256": script_hashes,
        "discovery": str(discovery_path) if discovery is not None else None,
        "discovery_sha256": digest(discovery_path) if discovery is not None else None,
        "parallel_jobs": workers,
        "delivery": {
            "container": "mp4", "video": "H.264", "width": 1080, "height": 1920,
            "fps": "24/1", "color": "BT.709", "audio": "AAC stereo, 48000 Hz",
            "purpose": "local review",
        },
        "clips": {},
    }
    jobs = []
    for clip_id, (plan, original, poster_hash) in plans.items():
        clip_dir = output / clip_id
        clip_dir.mkdir()
        frozen = clip_dir / "plan.json"
        write_json(frozen, plan)
        manifest["clips"][clip_id] = {
            "status": "queued", "title": plan["title"], "hook": plan["hook"],
            "edit_intent": plan["edit_intent"],
            "original_plan": str(original), "frozen_plan": str(frozen),
            "plan_sha256": digest(frozen), "poster_sha256": poster_hash,
            "source_range": [plan["shots"][0]["in"], plan["shots"][-1]["out"]],
        }
        if plan["edit_intent"] == "teaser":
            manifest["clips"][clip_id].update({key: plan[key] for key in TEASER_FIELDS})
        jobs.append((source, frozen, clip_dir, clip_id, plan.get("language", "en")))
    manifest_path = output / "batch.json"
    write_json(manifest_path, manifest)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        active = {executor.submit(render_one, *job): job[3] for job in jobs}
        for future in as_completed(active):
            clip_id = active[future]
            result = future.result()
            manifest["clips"][clip_id].update(result)
            write_json(manifest_path, manifest)
            print(f"{clip_id}: {result['status']}", flush=True)
    print(manifest_path)
    return int(any(c["status"] != "rendered" for c in manifest["clips"].values()))


def render_many(args):
    """Render selected clips from several films through one bounded worker pool."""

    if args.jobs < 1:
        raise ValueError("--jobs must be at least 1")
    queue_path = args.manifest.resolve(strict=True)
    queue_data = queue_path.read_bytes()
    queue = json.loads(queue_data)
    films = queue.get("films") if isinstance(queue, dict) else None
    if not isinstance(films, list) or not films:
        raise ValueError("Manifest must contain a nonempty films list")
    prepared = {}
    for film in films:
        if not isinstance(film, dict) or not all(isinstance(film.get(key), str) and film[key]
                                               for key in ("source", "plans")):
            raise ValueError("Every film requires source and plans paths")
        film_id = film.get("id")
        if not isinstance(film_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", film_id):
            raise ValueError("Every film requires a safe id")
        if film_id in prepared:
            raise ValueError(f"Duplicate film id: {film_id}")
        source = (queue_path.parent / film["source"]).resolve(strict=True)
        if not source.is_file():
            raise ValueError(f"{film_id}: source must be a film file")
        stat = source.stat()
        source_hash = digest(source)
        plans_dir = (queue_path.parent / film["plans"]).resolve(strict=True)
        plans = {}
        for path in sorted(plans_dir.glob("*.json")):
            plan, poster = read_plan(path, source, None)
            if plan["id"] in plans:
                raise ValueError(f"{film_id}: duplicate clip id {plan['id']}")
            plans[plan["id"]] = (plan, path, poster)
        if not plans:
            raise ValueError(f"{film_id}: no selected JSON plans found")
        current = source.stat()
        if (current.st_size, current.st_mtime_ns) != (stat.st_size, stat.st_mtime_ns):
            raise ValueError(f"{film_id}: film changed during preflight")
        prepared[film_id] = (source, source_hash, stat, plans)

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    workers = min(args.jobs, sum(len(item[3]) for item in prepared.values()))
    receipt = {
        "format": "film-shorts-multi-v1", "input_manifest": str(queue_path),
        "input_manifest_sha256": hashlib.sha256(queue_data).hexdigest(), "parallel_jobs": workers,
        "purpose": "local review", "films": {},
        "scripts_sha256": {p.name: digest(p) for p in
                           (PIPELINE / "render_clip.py", PIPELINE.parent / "add_film_poster.py")},
    }
    jobs = []
    for film_id, (source, source_hash, stat, plans) in prepared.items():
        film_dir = output / film_id
        film_dir.mkdir()
        record = {"source": str(source), "source_sha256": source_hash,
                  "source_bytes": stat.st_size, "source_mtime_ns": stat.st_mtime_ns, "clips": {}}
        receipt["films"][film_id] = record
        for clip_id, (plan, original, poster) in plans.items():
            clip_dir = film_dir / clip_id
            clip_dir.mkdir()
            poster_data = poster.read_bytes()
            frozen_poster = clip_dir / ("poster" + poster.suffix)
            frozen_poster.write_bytes(poster_data)
            plan["poster"] = str(frozen_poster)
            frozen_plan = clip_dir / "plan.json"
            write_json(frozen_plan, plan)
            record["clips"][clip_id] = {
                "status": "queued", "title": plan["title"], "hook": plan["hook"],
                "original_plan": str(original), "frozen_plan": str(frozen_plan),
                "plan_sha256": digest(frozen_plan),
                "poster_sha256": hashlib.sha256(poster_data).hexdigest(),
            }
            jobs.append((film_id, clip_id, (source, frozen_plan, clip_dir, clip_id, plan.get("language", "en"))))
    receipt_path = output / "batch.json"
    write_json(receipt_path, receipt)

    def execute(film_id, clip_id, argv):
        source, _, stat, _ = prepared[film_id]
        try:
            current = source.stat()
            if (current.st_size, current.st_mtime_ns) != (stat.st_size, stat.st_mtime_ns):
                raise ValueError("Film changed after preflight")
            result = render_one(*argv)
            current = source.stat()
            if (current.st_size, current.st_mtime_ns) != (stat.st_size, stat.st_mtime_ns):
                raise ValueError("Film changed during rendering; output is not ready")
            return result
        except Exception as exc:
            return {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}

    with ThreadPoolExecutor(max_workers=workers) as executor:
        active = {executor.submit(execute, *job): job[:2] for job in jobs}
        for future in as_completed(active):
            film_id, clip_id = active[future]
            result = future.result()
            receipt["films"][film_id]["clips"][clip_id].update(result)
            write_json(receipt_path, receipt)
            print(f"{film_id}/{clip_id}: {result['status']}", flush=True)
    print(receipt_path)
    return int(any(clip["status"] != "rendered" for film in receipt["films"].values()
                   for clip in film["clips"].values()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    stages = parser.add_subparsers(dest="stage", required=True)
    scan = stages.add_parser("discover")
    scan.add_argument("source", type=Path)
    scan.add_argument("output", type=Path)
    scan.add_argument("--audio-stream", type=int)
    scan.add_argument("--language", default="ru")
    render = stages.add_parser("render")
    render.add_argument("source", type=Path)
    render.add_argument("plans", type=Path, help="Directory containing only selected clip plans")
    render.add_argument("output", type=Path, help="New directory for this render revision")
    render.add_argument("--discovery", type=Path)
    render.add_argument("--jobs", type=int, default=3)
    many = stages.add_parser("render-many", help="Render plans from multiple films with one global queue")
    many.add_argument("manifest", type=Path, help="JSON films list with id, source and plans directory")
    many.add_argument("output", type=Path, help="New directory for this render revision")
    many.add_argument("--jobs", type=int, default=3, help="Maximum simultaneous clip renders across all films")
    args = parser.parse_args()
    try:
        if args.stage == "render-many":
            return render_many(args)
        source = args.source.resolve(strict=True)
        if not source.is_file():
            raise ValueError("Source must be a film file")
        if args.stage == "discover":
            argv = [sys.executable, str(PIPELINE / "discover.py"), str(source),
                    str(args.output.resolve()), "--language", args.language]
            if args.audio_stream is not None:
                argv += ["--audio-stream", str(args.audio_stream)]
            return subprocess.call(argv)
        return render_batch(args, source)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"{exc}\n")


if __name__ == "__main__":
    sys.exit(main())
