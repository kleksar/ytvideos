#!/usr/bin/env python3
"""Apply accepted screen-space G08 grain after a layered-motion camera render."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from finish import Grain, read_exact  # noqa: E402

PRESETS = json.loads((HERE / "grain_presets.json").read_text())["presets"]


def apply(input_path: Path, output_path: Path, image_sha256: str, frames: int,
          fps: int = 30, preset_name: str = "g08"):
    if preset_name not in PRESETS:
        raise ValueError(f"Unknown grain preset: {preset_name}")
    if output_path.exists():
        raise FileExistsError(f"Refusing to overwrite {output_path}")
    if fps != PRESETS[preset_name]["update_hz"]:
        raise ValueError("G08 currently requires 30fps")

    probe = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height,r_frame_rate,nb_frames,pix_fmt", "-of", "json", str(input_path)
    ], check=True, capture_output=True, text=True)
    stream = json.loads(probe.stdout)["streams"][0]
    width, height = int(stream["width"]), int(stream["height"])
    if int(stream.get("nb_frames", frames)) != frames or stream["r_frame_rate"] != "30/1":
        raise ValueError(f"Input timing mismatch: {stream}")
    if stream.get("pix_fmt") != "yuv420p" or width % 2 or height % 2:
        raise ValueError(f"Input must be even-dimension yuv420p: {stream}")

    preset = PRESETS[preset_name]
    seed_bytes = hashlib.sha256(bytes.fromhex(image_sha256) +
                                int(preset["seed"]).to_bytes(8, "big")).digest()[:8]
    seed = int.from_bytes(seed_bytes, "big")
    grain = Grain(preset, width, height, seed)
    frame_bytes = width * height * 3 // 2
    decode = ["ffmpeg", "-v", "error", "-i", str(input_path), "-an", "-frames:v", str(frames),
              "-f", "rawvideo", "-pix_fmt", "yuv420p", "pipe:1"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp = output_path.with_name(output_path.stem + ".partial" + output_path.suffix)
    encode = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "yuv420p",
              "-video_size", f"{width}x{height}", "-framerate", str(fps), "-i", "pipe:0",
              "-an", "-vf", "setsar=1,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709",
              "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-tune", "grain",
              "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
              "-colorspace", "bt709", "-color_range", "tv", "-movflags", "+faststart",
              str(temp)]
    dec = subprocess.Popen(decode, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    enc = subprocess.Popen(encode, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for _ in range(frames):
            data = np.frombuffer(read_exact(dec.stdout, frame_bytes), np.uint8)
            y = data[:width * height].reshape(height, width)
            y = grain.apply(y)
            enc.stdin.write(y.tobytes() + data[width * height:].tobytes())
        dec.stdout.close()
        enc.stdin.close()
        dec_err = dec.stderr.read().decode(errors="replace")
        enc_err = enc.stderr.read().decode(errors="replace")
        if dec.wait() or enc.wait():
            raise RuntimeError(f"G08 pipeline failed: decode={dec_err} encode={enc_err}")
        temp.replace(output_path)
    except BaseException:
        for process in (dec, enc):
            if process.poll() is None:
                process.kill()
            process.wait()
        temp.unlink(missing_ok=True)
        raise
    receipt = {
        "input": str(input_path.resolve()), "output": str(output_path.resolve()),
        "image_sha256": image_sha256, "frames": frames, "fps": fps,
        "width": width, "height": height, "preset": preset_name,
        "grain": preset, "seed": seed, "sigma_output_px": grain.sigma,
        "order": ["source still", "layered parallax", "opposed camera", "G08"]
    }
    receipt_path = output_path.with_suffix(output_path.suffix + ".g08.json")
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--image-sha256", required=True)
    parser.add_argument("--frames", required=True, type=int)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--preset", default="g08")
    args = parser.parse_args()
    apply(args.input, args.output, args.image_sha256, args.frames, args.fps, args.preset)


if __name__ == "__main__":
    main()
