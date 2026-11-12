#!/usr/bin/env python3
"""Build a review-only Paper Detour 033 MP4 from accepted stills and one authorized TTS asset."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EPISODE = ROOT
CUES = json.loads((EPISODE / "Storyboard/ON_SCREEN_TEXT_CUES_v01.json").read_text())
PREFLIGHT = json.loads((EPISODE / "Source/Graphics/caption_preflight_v03/manifest.json").read_text())
SCENES = CUES["scenes"]
FPS = CUES["frame_rate"]
FRAME_COUNT = SCENES[-1]["end_frame"]
DURATION = FRAME_COUNT / FPS
VOICE = EPISODE / CUES["audio"]
GRAIN = EPISODE / "Edit/Automation/time_stop_visual_v01/film_grain_v01.mov"
OUT = EPISODE / "Edit/Previews/Paper_Detour_033_time_stop_EN_mix_preview_v03.mp4"

if OUT.exists():
    raise SystemExit(f"Refusing to overwrite {OUT}")
if len(SCENES) != 14 or len(CUES["cues"]) != 8:
    raise SystemExit("Expected 14 accepted stills and 8 accepted text cues")
if not VOICE.exists() or not GRAIN.exists():
    raise SystemExit("Required voice or grain asset is missing")

pair_map = {p["cue"]: p for p in PREFLIGHT["pairs"]}
cue_metrics = {c["id"]: c["metrics"] for c in PREFLIGHT["cues"]}
cmd = ["ffmpeg", "-hide_banner", "-y"]
# One static image input per direct-cut scene, decoded at the assigned frame count.
for s in SCENES:
    image = EPISODE / s["image"]
    frames = s["end_frame"] - s["start_frame"]
    cmd += ["-loop", "1", "-framerate", str(FPS), "-i", str(image)]
voice_idx = len(SCENES)
cmd += ["-i", str(VOICE)]
grain_idx = voice_idx + 1
cmd += ["-i", str(GRAIN)]
cue_input = {}
for cue in CUES["cues"]:
    cue_input[cue["id"]] = len(SCENES) + 2 + len(cue_input)
    cmd += ["-loop", "1", "-framerate", str(FPS), "-i", str(EPISODE / cue["asset"])]

filters = []
scene_labels = []
for i, s in enumerate(SCENES):
    frames = s["end_frame"] - s["start_frame"]
    label = f"scene{i}"
    filters.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps={FPS},trim=end_frame={frames},setpts=PTS-STARTPTS,format=rgba[{label}]")
    scene_labels.append(f"[{label}]")
filters.append("".join(scene_labels) + f"concat=n={len(scene_labels)}:v=1:a=0,tpad=stop_mode=clone:stop=1,format=rgba[base]")
filters.append(f"[{grain_idx}:v]trim=end_frame={FRAME_COUNT},setpts=PTS-STARTPTS,scale=1080:1920:flags=bicubic,format=rgba[grain]")
filters.append(f"[base][grain]overlay=shortest=1:format=auto[grained]")
current = "grained"
for n, cue in enumerate(CUES["cues"]):
    cue_id = cue["id"]
    idx = cue_input[cue_id]
    start = cue["start_frame"] / FPS
    end = cue["end_frame"] / FPS
    metrics = cue_metrics[cue_id]
    pair = pair_map[cue_id]
    comparison = next(x for x in pair["comparisons"] if x["anchor"] == pair["anchor"])
    x, y = comparison["layer_top_left_px"]
    alpha_in = 4 / FPS
    alpha_out = 5 / FPS
    final_cue = cue_id == "C14"
    fade_filters = f"fade=t=in:st={start:.6f}:d={alpha_in:.6f}:alpha=1"
    if not final_cue:
        fade_filters += f",fade=t=out:st={max(start,end-alpha_out):.6f}:d={alpha_out:.6f}:alpha=1"
    in_label = f"cue{n}"
    out_label = f"mix{n}"
    filters.append(f"[{idx}:v]trim=end_frame={FRAME_COUNT},setpts=PTS-STARTPTS,format=rgba,{fade_filters}[{in_label}]")
    filters.append(f"[{current}][{in_label}]overlay=x={x}:y={y}:eof_action=pass:shortest=0:enable='between(t,{start:.6f},{end:.6f})':format=auto[{out_label}]")
    current = out_label
# Voice source split at the accepted-answer boundary. Preserve the exact generated audio on both sides;
# insert only 2.16 seconds of timeline silence before S14 for the accepted post-answer beat.
pause = CUES["inserted_comedy_pause_s"]
filters += [
    f"[{voice_idx}:a]asplit=2[va][vb]",
    f"[va]atrim=start=0:end=46.000,asetpts=PTS-STARTPTS[va1]",
    f"[vb]atrim=start=46.000:end=48.000,asetpts=PTS-STARTPTS[vb1]",
    f"anullsrc=r=44100:cl=mono,atrim=duration={pause:.6f},asetpts=PTS-STARTPTS[silence]",
    "[va1][silence][vb1]concat=n=3:v=0:a=1,aresample=48000[aout]",
    f"[{current}]trim=end_frame={FRAME_COUNT},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[vout]",
]
cmd += ["-filter_complex", ";".join(filters), "-map", "[vout]", "-map", "[aout]",
        "-frames:v", str(FRAME_COUNT), "-r", str(FPS), "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(OUT)]
print("Frames:", FRAME_COUNT, "duration:", f"{DURATION:.6f}", "s; direct cuts:", len(SCENES), "cues:", len(CUES["cues"]))
print("Audio: accepted TTS split at 46.000 s with", f"{pause:.2f}", "s timeline silence; no other audio")
print("Output:", OUT)
subprocess.run(cmd, check=True)
