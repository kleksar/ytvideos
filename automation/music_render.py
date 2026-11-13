#!/usr/bin/env python3
"""Canonical music-first picture, three-frame transitions and lyric-mask compositor."""
# ruff: noqa: E402 -- This standalone repository CLI resolves its pinned src tree first.
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "automation"))

from ytvideos.errors import WorkflowError
from ytvideos.media_checks import validate_video
from ytvideos.media_script import bind_requirements, read_script
from ytvideos.music_contract import (ENGINE, RECEIPT_SCHEMA, checked, document, file_record,
                                    helper, validate_lyric_plan, validate_plan)
from ytvideos.production_contract import production_requirements, validate_delivery_summary
from ytvideos.profiles import load_profile
from ytvideos.util import file_digest


def write(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def motion_filter(width, height, frames, scales):
    """Reserve source margin for 95%, then interpolate the whole picture each frame."""
    if frames < 2:
        raise WorkflowError("music motion needs at least two frames")
    sw, sh = (2 * math.ceil(value / .95 / 2) for value in (width, height))
    progress = f"(on/{frames-1})"
    ease = f"({progress}*{progress}*(3-2*{progress}))"
    zoom = f"({scales[0]}+({scales[1]-scales[0]:.12f})*{ease})"
    left, top = f"((W-W*{zoom})/2)", f"((H-H*{zoom})/2)"
    return (f"scale={sw}:{sh}:force_original_aspect_ratio=increase:flags=lanczos,crop={sw}:{sh},"
            f"perspective=sense=destination:x0='{left}':y0='{top}':x1='{left}+W*{zoom}':y1='{top}':"
            f"x2='{left}':y2='{top}+H*{zoom}':x3='{left}+W*{zoom}':y3='{top}+H*{zoom}':"
            f"interpolation=cubic:eval=frame,crop={width}:{height},setsar=1")


def lyric_command(plan, prepared, work, project):
    sub = plan["subtitles"]
    settings, font = sub["settings"], sub["font"]
    command = [sys.executable, str(Path(project) / "automation/captions/music_lyrics.py"), sub["words"]["path"],
            "--font", font["path"], "--font-index", str(font["index"]),
            "--font-size", str(settings["font_size_px"]), "--fps", "30", "--frames", str(prepared["frames"]),
            "--offset", "0", "--invert-masks", "--max-words", "1", "--tilt-every", str(settings["tilt_every"]),
            "--vocal-beat", "--cuts", str(work / "cuts.json"), "--motion-seed", "17",
            "--output", str(work / "lyrics.mov"), "--plan", str(work / "lyrics-plan.json")]
    if "beats" in sub:
        command += ["--beats", sub["beats"]["path"]]
    return command


def final_color_filter():
    # The composite is planar RGB. Merely tagging its default RGB→YUV conversion
    # as 709 would mislabel BT.601 samples; specify the conversion matrix itself.
    return ("setsar=1,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,"
            "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=limited")


def build_command(plan, prepared, requirements, work, output):
    """Build every picture operation; the stored argv is rechecked at completion."""
    width, height = requirements["video"]["canvas"]
    scenes = plan["scenes"]
    command = ["ffmpeg", "-nostdin", "-v", "error", "-n"]
    filters, pieces = [], []
    for index, (scene, (first, stop)) in enumerate(zip(scenes, prepared["visible_intervals"])):
        command += ["-protocol_whitelist", "file,pipe", "-i", scene["clip"]]
        labels = [f"normal{index}"]
        if index:
            labels.append(f"incoming{index}")
        if index + 1 < len(scenes):
            labels.append(f"outgoing{index}")
        color = plan["color"]
        filters.append(f"[{index}:v:0]fps=30,trim=end_frame={stop-first},setpts=PTS-STARTPTS,"
                       + motion_filter(width, height, stop-first, scene["scale"])
                       + f",eq=contrast={color['contrast']}:saturation={color['saturation']},format=yuv444p,"
                       + f"split={len(labels)}" + "".join(f"[{label}]" for label in labels))
        start = scene["start_frame"] + (2 if index else 0) - first
        end = scene["end_frame"] - (1 if index + 1 < len(scenes) else 0) - first
        filters.append(f"[normal{index}]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS[n{index}]")
        pieces.append(f"[n{index}]")
        if index + 1 < len(scenes):
            outgoing = scene["end_frame"] - 1 - first
            filters.append(f"[outgoing{index}]trim=start_frame={outgoing}:end_frame={outgoing+3},setpts=PTS-STARTPTS[o{index}]")
            # T is the local timestamp, avoiding ambiguity about FFmpeg's N base.
            opacity = "if(lt(T,0.0166666667),0,if(lt(T,0.05),0.7,0.85))"
            envelope = "if(lt(T,0.0166666667),0,if(lt(T,0.05),1,0.5))"
            filters.append(f"[o{index}][i{index+1}]blend=all_expr='A*(1-({opacity}))+B*({opacity})',split=2[c{index}][b{index}]")
            filters.append(f"[b{index}]gblur=sigma={plan['transition']['blur_sigma_px']}:steps=2[g{index}]")
            brightness = envelope.replace("T", "t")
            filters.append(f"[c{index}][g{index}]blend=all_expr='A*(1-({envelope}))+B*({envelope})',"
                           f"eq=brightness='{plan['transition']['brightness']}*({brightness})':eval=frame[t{index}]")
            pieces.append(f"[t{index}]")
        if index:
            filters.append(f"[incoming{index}]trim=end_frame=3,setpts=PTS-STARTPTS[i{index}]")
    filters.append("".join(pieces) + f"concat=n={len(pieces)}:v=1:a=0,format=gbrp[picture]")
    source = "picture"
    audio_index = len(scenes)
    if prepared["lyrics"] is not None:
        command += ["-protocol_whitelist", "file,pipe", "-i", str(work / "lyrics.mov")]
        sigma = plan["subtitles"]["settings"]["mask_sigma_px"]
        # The canonical helper encodes ordinary/active glyph alpha in R/G. Both
        # are one soft inversion mask for this one-word music recipe.
        filters.append(f"[{audio_index}:v:0]format=gbrp,"
                       "colorchannelmixer=rr=1:rg=1:rb=0:gr=1:gg=1:gb=0:br=1:bg=1:bb=0,"
                       f"gblur=sigma={sigma}:steps=2,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,format=gbrp[mask]")
        filters.append("[picture]split=2[base][inverse_source]")
        filters.append("[inverse_source]negate[inverse]")
        filters.append("[base][inverse][mask]maskedmerge[captioned]")
        source = "captioned"
        audio_index += 1
    command += ["-protocol_whitelist", "file,pipe", "-i", plan["audio"]]
    filters.append(f"[{source}]" + final_color_filter() + "[vout]")
    command += ["-filter_complex_threads", "1", "-filter_complex", ";".join(filters), "-map", "[vout]",
                "-map", f"{audio_index}:a:0", "-frames:v", str(prepared["frames"]), "-t", str(prepared["frames"] / 30),
                "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
                "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(output)]
    return command


def fragment_contract(plan, prepared):
    return {"fps": 30, "frames": prepared["frames"], "transition_centres": prepared["cuts"],
            "source": prepared["track"]["path"], "source_sha256": prepared["track"]["sha256"],
            "offset": prepared["track"]["source_in_seconds"],
            "ending": {"source_end_seconds": prepared["track"]["source_in_seconds"] + prepared["duration_seconds"],
                       "fade_out_seconds": prepared["fade_out_seconds"]},
            "clips": [{"path": scene["source"]["path"], "sha256": scene["source"]["sha256"],
                       "source_in": scene["source"]["start_seconds"], "source_page": scene["source"].get("source_page"),
                       "subject": chosen["subject"], "scale": chosen["scale"]}
                      for scene, chosen in zip(plan["scenes"], prepared["planned"]["clips"])],
            "motion": [{"first_frame": first, "frames": stop-first, "scale": scene["scale"], "easing": scene["easing"]}
                       for scene, (first, stop) in zip(plan["scenes"], prepared["visible_intervals"])]}


def render(manifest, output, work, requirements, *, project=ROOT):
    manifest, output, work, project = (Path(value).resolve() for value in (manifest, output, work, project))
    if output.exists() or work.exists():
        raise WorkflowError("music output/work already exists; preserve and reconcile it before retrying")
    plan = json.loads(manifest.read_text())
    profile = load_profile(project / "channels", plan["channel"])
    if profile["recipe"] != "music_first":
        raise WorkflowError("the music compositor needs a registered music-first profile")
    script = read_script(Path(plan["script"]), profile, plan["format"])
    script["artifact_sha256"] = file_digest(plan["script"])
    expected = bind_requirements(production_requirements(profile, plan["format"], variant=script["production_variant"]), script)
    if requirements != expected:
        raise WorkflowError("music renderer requirements differ from the pinned profile and accepted edit")
    prepared = validate_plan(plan, requirements, base=manifest.parent, project=project, script=script)
    inputs = [file_record(manifest), file_record(project / "channels" / profile["id"] / "channel.json"), *prepared["inputs"]]
    engine = [file_record(project / relative) for relative in ENGINE]
    work.mkdir(parents=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    write(work / "cuts.json", {"fps": 30, "cut_frames": prepared["cuts"]})
    lyrics = None
    if prepared["lyrics"] is not None:
        command = lyric_command(plan, prepared, work, project)
        subprocess.run(command, check=True, stdin=subprocess.DEVNULL, timeout=900)
        lyric_plan = json.loads((work / "lyrics-plan.json").read_text())
        validate_lyric_plan(lyric_plan, plan, prepared, project)
        lyrics = {"command": command, "plan": file_record(work / "lyrics-plan.json"),
                  "mask": file_record(work / "lyrics.mov"), "cuts": file_record(work / "cuts.json")}
    command = build_command(plan, prepared, requirements, work, output)
    write(work / "render-command.json", command)
    subprocess.run(command, check=True, stdin=subprocess.DEVNULL, timeout=1800)
    measured = validate_video(output)
    validate_delivery_summary(measured, requirements)
    if int(measured["video"][0]["nb_frames"]) != prepared["frames"]:
        raise WorkflowError("music compositor frame count differs from the exact beat timeline")
    for record in inputs + engine:
        checked(record)
    media = file_record(output)
    write(work / "export-qa.json", {"sha256": media["sha256"], "full_decode": "PASS", "probe": measured,
                                    "scope": "Technical decoding only; audiovisual/rights review remains unverified."})
    write(work / "export-contract.json", fragment_contract(plan, prepared))
    write(work / "review-index.json", [{"file": str(output), "sha256": media["sha256"], "qa": str(work / "export-qa.json")}])
    fragments = helper(project, "automation/music_fragments.py", "ytv_music_fragments")
    write(work / "fragments.json", fragments.collect(work / "review-index.json"))
    receipt = {"schema": RECEIPT_SCHEMA, "purpose": "production", "manifest": file_record(manifest), "media": media,
               "requirements_sha256": requirements["sha256"], "inputs": inputs, "engine": engine,
               "command": file_record(work / "render-command.json"), "lyrics": lyrics,
               "technical_review": file_record(work / "export-qa.json"),
               "fragment_contract": file_record(work / "export-contract.json"),
               "fragment_index": file_record(work / "review-index.json"), "fragments": file_record(work / "fragments.json"),
               "review_status": "UNVERIFIED"}
    write(str(output) + ".delivery.json", receipt)
    return receipt


def validate_receipt(receipt_path, plan, requirements, output, *, project=ROOT):
    """Recheck native command/input provenance; this never grants perceptual QA."""
    receipt = json.loads(Path(receipt_path).read_text())
    if (receipt.get("schema") != RECEIPT_SCHEMA or receipt.get("purpose") != "production"
            or receipt.get("media") != file_record(output) or receipt.get("requirements_sha256") != requirements["sha256"]):
        raise WorkflowError("music render receipt does not bind this exact production output")
    for record in receipt["inputs"] + receipt["engine"]:
        checked(record)
    expected_engine = [file_record(Path(project) / relative) for relative in ENGINE]
    if receipt["engine"] != expected_engine:
        raise WorkflowError("music render used another canonical implementation")
    if document(receipt["manifest"]) != plan:
        raise WorkflowError("music render receipt identifies another manifest")
    profile = load_profile(Path(project) / "channels", plan["channel"])
    script = read_script(Path(plan["script"]), profile, plan["format"])
    script["artifact_sha256"] = file_digest(plan["script"])
    expected = bind_requirements(production_requirements(profile, plan["format"], variant=script["production_variant"]), script)
    if requirements != expected:
        raise WorkflowError("music receipt requirements differ from the pinned profile and edit")
    prepared = validate_plan(plan, requirements, base=Path(receipt["manifest"]["path"]).parent, project=project, script=script)
    expected_inputs = [receipt["manifest"], file_record(Path(project) / "channels" / profile["id"] / "channel.json"), *prepared["inputs"]]
    if receipt["inputs"] != expected_inputs:
        raise WorkflowError("music receipt omitted a required exact input")
    work = Path(receipt["command"]["path"]).parent
    if document(receipt["command"]) != build_command(plan, prepared, requirements, work, Path(output)):
        raise WorkflowError("native music command omits or changes required composition effects")
    records = [receipt[key] for key in ("command", "technical_review", "fragment_contract", "fragment_index", "fragments")]
    if prepared["lyrics"] is not None:
        lyric = receipt.get("lyrics")
        if not isinstance(lyric, dict) or lyric.get("command") != lyric_command(plan, prepared, work, project):
            raise WorkflowError("vocal delivery needs the canonical one-word lyric execution")
        lyric_plan = document(lyric["plan"])
        checked(lyric["mask"])
        if document(lyric["cuts"]) != {"fps": 30, "cut_frames": prepared["cuts"]}:
            raise WorkflowError("music lyric contract changes the exact cut accents")
        validate_lyric_plan(lyric_plan, plan, prepared, project)
        records.extend([lyric["plan"], lyric["mask"], lyric["cuts"]])
    elif receipt.get("lyrics") is not None:
        raise WorkflowError("instrumental delivery must not add lyric captions")
    if document(receipt["fragment_contract"]) != fragment_contract(plan, prepared):
        raise WorkflowError("fragment contract differs from the original footage/music intervals")
    if document(receipt["fragment_index"]) != [{"file": str(output), "sha256": receipt["media"]["sha256"],
                                               "qa": receipt["technical_review"]["path"]}]:
        raise WorkflowError("fragment journal must identify this exact final export")
    fragments = helper(project, "automation/music_fragments.py", "ytv_music_fragments_check")
    if document(receipt["fragments"]) != fragments.collect(checked(receipt["fragment_index"])):
        raise WorkflowError("fragment journal is stale or identifies another export")
    for record in records:
        checked(record)
    return [*receipt["inputs"], *receipt["engine"], *records]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--work-dir", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    args = parser.parse_args()
    receipt = render(args.manifest, args.output, args.work_dir, json.loads(args.requirements.read_text()))
    print(json.dumps({"output": receipt["media"], "receipt": str(args.output.resolve()) + ".delivery.json",
                      "review_status": "UNVERIFIED"}))


if __name__ == "__main__":
    main()
