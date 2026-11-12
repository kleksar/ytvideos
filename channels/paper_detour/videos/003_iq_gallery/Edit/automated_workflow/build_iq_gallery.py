#!/usr/bin/env python3
"""Run the repeatable IQ Gallery pipeline: labels, manifest, preflight, render."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys


HERE = pathlib.Path(__file__).resolve().parent


def resolve(value: pathlib.Path) -> pathlib.Path:
    value = value.expanduser()
    return value.resolve() if value.is_absolute() else (HERE / value).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cast", type=pathlib.Path, default=HERE / "cast_v6.json")
    parser.add_argument("--manifest", type=pathlib.Path, default=HERE / "iq_gallery_v6_manifest.json")
    parser.add_argument("--prepared-dir", type=pathlib.Path, default=HERE / "prepared_labels_v6")
    parser.add_argument("--force-manifest", action="store_true",
                        help="replace the derived manifest; never replaces a rendered video")
    parser.add_argument("--probe-only", action="store_true",
                        help="build and validate the manifest without rendering a video")
    args = parser.parse_args()

    cast_path = resolve(args.cast)
    manifest_path = resolve(args.manifest)
    prepared_dir = resolve(args.prepared_dir)
    try:
        cast = json.loads(cast_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read cast file {cast_path}: {exc}") from exc
    output_value = cast.get("output")
    if not isinstance(output_value, str) or not output_value.strip():
        raise SystemExit("cast file must declare an output MP4")
    video = (HERE / output_value).resolve()
    report = pathlib.Path(str(video) + ".report.json")
    if video.exists() or report.exists():
        raise SystemExit(f"refusing to overwrite rendered output or report: {video}")

    builder = HERE / "build_manifest.py"
    renderer = HERE / "render_iq_gallery.py"
    build_command = [sys.executable, str(builder), "--cast", str(cast_path),
                     "--output", str(manifest_path), "--prepared-dir", str(prepared_dir)]
    if args.force_manifest:
        build_command.append("--force")
    subprocess.run(build_command, check=True)
    preflight = subprocess.run(
        [sys.executable, str(renderer), str(manifest_path), "--probe"],
        capture_output=True, text=True,
    )
    if preflight.returncode:
        sys.stderr.write(preflight.stderr or preflight.stdout)
        return preflight.returncode
    try:
        plan = json.loads(preflight.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"renderer returned invalid preflight JSON: {exc}") from exc
    print(
        f"Preflight OK: {len(plan['scenes'])} scenes, {plan['frames']} frames, "
        f"{plan['format']}; output {plan['output']}"
    )
    if args.probe_only:
        return 0
    subprocess.run([sys.executable, str(renderer), str(manifest_path)], check=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode or 1)
