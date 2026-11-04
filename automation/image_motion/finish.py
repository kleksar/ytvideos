"""Deterministic screen-space G08 after the authored affine camera. No audio."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter


def camera_at(keys, frame):
    values = {}
    for name in ("position", "scale"):
        a, b = keys[name]
        t = min(1.0, max(0.0, (frame-a[0])/(b[0]-a[0])))
        values[name] = [a[k] + t*(b[k]-a[k]) for k in (1, 2)]
    return (*values["position"], *values["scale"])


def warp(plane, camera):
    x, y, sx, sy = camera
    h, w = plane.shape
    return np.asarray(Image.fromarray(plane).transform(
        (w, h), Image.Transform.AFFINE,
        (1/sx, 0, -x*w/sx, 0, 1/sy, -y*h/sy),
        resample=Image.Resampling.BICUBIC))


class Grain:
    def __init__(self, preset, width, height, seed):
        self.preset = preset
        self.shape = (height, width)
        self.sigma = preset["sigma_reference_px"] * min(width, height) / preset["reference_short_side"]
        self.rng = np.random.default_rng(seed)
        self.state = None
        a, b, c, d = preset["mask_y"]
        self.mask = np.interp(np.arange(256), [0, a, b, c, d, 255],
                              [0, 0, 1, 1, 0, 0]).astype(np.float32)

    def apply(self, clean):
        innovation = self.rng.standard_normal(self.shape, dtype=np.float32)
        gaussian_filter(innovation, self.sigma, output=innovation, mode="reflect")
        innovation -= innovation.mean()
        innovation /= innovation.std()
        if self.state is None:
            self.state = innovation
        else:
            rho = self.preset["rho"]
            self.state *= rho
            self.state += math.sqrt(1-rho*rho)*innovation
        low, high = self.preset["range_y"]
        return np.clip(np.rint(clean.astype(np.float32) + self.state *
                              self.preset["rms_y_codes"] * self.mask[clean]), low, high).astype(np.uint8)


def read_exact(stream, count):
    parts = bytearray()
    while len(parts) < count:
        block = stream.read(count-len(parts))
        if not block:
            raise RuntimeError(f"Short decoded frame: {len(parts)}/{count}")
        parts.extend(block)
    return parts


def render(job):
    w, h, n, fps = (job[k] for k in ("width", "height", "frames", "fps"))
    p = job["grain"]
    if w % 2 or h % 2 or min(w, h) < 16 or n < 2 or fps != p["update_hz"]:
        raise ValueError("G08 requires even dimensions, at least two frames and 30fps")
    input_color = job.get("input_color", "legacy-depthflow-bt601-srgb")
    if input_color == "legacy-depthflow-bt601-srgb":
        # Pinned DepthFlow 1.0.1 cache: RGB/sRGB encoded with default BT.601 matrix.
        colour = ("colorspace=iall=bt601-6-625:iprimaries=bt709:itrc=srgb:irange=tv:"
                  "all=bt709:range=tv:format=yuv420p,setsar=1")
    elif input_color == "bt709-limited":
        # layered_render.py tags its output as BT.709 limited YUV420p.
        colour = ("colorspace=iall=bt709:iprimaries=bt709:itrc=bt709:irange=tv:"
                  "all=bt709:range=tv:format=yuv420p,setsar=1")
    else:
        raise ValueError(f"Unsupported input_color: {input_color}")
    decode = ["ffmpeg", "-v", "error", "-i", job["input"], "-an", "-vf", colour,
              "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "yuv420p", "pipe:1"]
    encode = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "yuv420p",
              "-video_size", f"{w}x{h}", "-framerate", str(fps), "-i", "pipe:0", "-an",
              "-vf", "setsar=1,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709",
              "-c:v", "libx264", "-crf", "16", "-preset", "fast",
              "-tune", "grain", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
              "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
              "-movflags", "+faststart+negative_cts_offsets", "-use_editlist", "0", job["output"]]
    grain = Grain(p, w, h, job["seed"])
    count = w*h
    metrics = []
    with Path(job["log"]).open("a") as log:
        dec = subprocess.Popen(decode, stdout=subprocess.PIPE, stderr=log)
        enc = subprocess.Popen(encode, stdin=subprocess.PIPE, stderr=log)
        try:
            for i in range(n):
                data = np.frombuffer(read_exact(dec.stdout, count*3//2), np.uint8)
                camera = camera_at(job["camera"], i)
                clean = warp(data[:count].reshape(h, w), camera)
                uv = data[count:].reshape(2, h//2, w//2)
                y = grain.apply(clean)
                payload = y.tobytes() + b"".join(warp(plane, camera).tobytes() for plane in uv)
                enc.stdin.write(payload)
                if i in {0, n//2, n-1}:
                    delta = y.astype(np.float32)-clean
                    metrics.append({"frame": i, "camera": camera,
                                    "applied_rms": float(np.sqrt(np.mean(delta*delta))),
                                    "noise_hash": hashlib.sha256(grain.state.tobytes()).hexdigest()})
            # Extra frames are final-frame copies, never counted as visible movement.
            enc.stdin.write(payload)
            enc.stdin.write(payload)
            dec.stdout.close()
            enc.stdin.close()
            if dec.wait() or enc.wait():
                raise RuntimeError("Camera/grain pipeline failed; inspect finish log")
        except BaseException:
            for process in (dec, enc):
                if process.poll() is None:
                    process.kill()
                process.wait()
            raise
    receipt = {"input": job["input"], "output": job["output"], "frames": n+2,
               "visible_frames": n, "input_color": input_color,
               "grain": p, "sigma_output_px": grain.sigma,
               "seed": job["seed"], "camera": job["camera"], "metrics": metrics,
               "decode": decode, "encode": encode, "order": ["parallax", "camera", "grain"],
               "colour": "BT709 limited YUV420p; chroma has no added noise"}
    Path(job["receipt"]).write_text(json.dumps(receipt, indent=2)+"\n")


if __name__ == "__main__":
    render(json.loads(Path(sys.argv[1]).read_text()))
