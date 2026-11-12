"""Animate the v08 title cards at 48 fps and copy the accepted AAC mix."""
import json
import math
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from PIL import Image, ImageChops, ImageFilter

from render_ranked_v06 import EDIT, EPISODE, FPS as SOURCE_FPS, WIDTH, digest
from render_ranked_v09 import (
    CENTER, FFMPEG, OVERSAMPLE, START_SCALE, TITLE_BOTTOM, TITLE_HEIGHT, TITLE_TOP,
    title_layer, write_json,
)

BASE = EPISODE / "Deliverables" / "meme-time-machine-01_draft-v08.mp4"
OUTPUT = EPISODE / "Deliverables" / "meme-time-machine-01_draft-v10.mp4"
FPS = SOURCE_FPS * 2
FRAME_RATIO = FPS // SOURCE_FPS
LANDING_FRAME = 28
START_BLUR = 19.0


def placement(frame):
    progress = min(frame / LANDING_FRAME, 1)
    eased = (1 - math.cos(math.pi * progress)) / 2
    remaining = 1 - eased
    # Positive screen-space angles turn clockwise.
    angle = -360 * remaining
    scale = 1 + (START_SCALE - 1) * remaining ** 2
    blur = START_BLUR * remaining ** 1.5
    return angle, scale, blur


def title_frames(card, slate_path, sequence_dir):
    slate = Image.open(slate_path).convert("RGBA")
    layer, (source_x, source_y) = title_layer(card["text"])
    center_x, center_y = CENTER[0], CENTER[1] - TITLE_TOP

    # Feather the edges of the title zone to keep the rank list clear.
    mask = Image.new("L", (1, TITLE_HEIGHT))
    mask.putdata([round(255 * min(y / 40, (TITLE_HEIGHT - 1 - y) / 40, 1))
                  for y in range(TITLE_HEIGHT)])
    mask = mask.resize((WIDTH, TITLE_HEIGHT))

    card_frames = (card["frame_out_exclusive"] - card["frame_in"]) * FRAME_RATIO
    for frame in range(card_frames):
        target = sequence_dir / f"{frame:02}.png"
        if frame > LANDING_FRAME:
            os.link(sequence_dir / f"{LANDING_FRAME:02}.png", target)
            continue
        angle, scale, blur = placement(frame)
        radians = math.radians(angle)
        cosine = math.cos(radians) * OVERSAMPLE / scale
        sine = math.sin(radians) * OVERSAMPLE / scale
        inverse = (
            cosine, sine, source_x - cosine * center_x - sine * center_y,
            -sine, cosine, source_y + sine * center_x - cosine * center_y,
        )
        lettering = layer.transform((WIDTH, TITLE_HEIGHT), Image.Transform.AFFINE, inverse,
                                    resample=Image.Resampling.BICUBIC)
        if blur > 0.05:
            lettering = lettering.convert("RGBa").filter(ImageFilter.GaussianBlur(blur)).convert("RGBA")
        lettering.putalpha(ImageChops.multiply(lettering.getchannel("A"), mask))
        composed = slate.copy()
        composed.alpha_composite(lettering, (0, TITLE_TOP))
        composed.convert("RGB").save(target, compress_level=1)


def render(scratch):
    prior = json.loads((EDIT / "export-contract-v08.json").read_text())
    base_qa = json.loads((EDIT / "qa-v08.json").read_text())
    assert digest(BASE) == base_qa["sha256"]
    assert not OUTPUT.exists()
    cards = prior["transitions"]
    reveals = prior["rank_reveals"]

    base_frame_select = "+".join(f"eq(n,{card['frame_in']})" for card in cards)
    extract = [*FFMPEG, "-i", str(BASE), "-vf", f"select='{base_frame_select}'",
               "-fps_mode", "passthrough", "-start_number", "0", str(scratch / "slate-%d.png")]
    args = [*FFMPEG, "-filter_complex_threads", "2", "-i", str(BASE)]
    graph = ["[0:v]split=" + str(len(cards)) + "".join(f"[base{i}]" for i in range(len(cards)))]
    parts = []
    for i, (card, meme) in enumerate(zip(cards, reveals)):
        sequence_dir = scratch / f"card-{i}"
        sequence_dir.mkdir()
        args += ["-framerate", str(FPS), "-start_number", "0", "-i", str(sequence_dir / "%02d.png")]
        graph += [
            f"[{i + 1}:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[title{i}]",
            f"[base{i}]trim=start_frame={meme['frame_in']}:end_frame={meme['frame_out_exclusive']},"
            f"setpts=PTS-STARTPTS,fps={FPS}[meme{i}]",
        ]
        parts.append(f"[title{i}][meme{i}]")
    graph.append(f'{"".join(parts)}concat=n={len(parts) * 2}:v=1:a=0,settb=1/{FPS},setpts=N[outv]')
    args += [
        "-filter_complex", ";".join(graph), "-map", "[outv]", "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-profile:v", "high",
        "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_trc", "bt709",
        "-color_primaries", "bt709", "-color_range", "tv", "-c:a", "copy",
        "-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
        "-movflags", "+faststart", str(OUTPUT),
    ]
    motion = {
        "direction": "clockwise",
        "start_degrees": -360,
        "end_degrees": 0,
        "start_scale": START_SCALE,
        "end_scale": 1,
        "landing_card_frame": LANDING_FRAME,
        "rotation_curve": "cosine ease in and out",
        "scale_curve": "square of the cosine remainder",
        "blur": {"type": "Gaussian", "target": "title layer", "start_radius_px": START_BLUR,
                 "end_radius_px": 0, "curve": "cosine remainder to the power of 1.5"},
        "pivot": list(CENTER),
        "title_zone": [TITLE_TOP, TITLE_BOTTOM],
    }
    def rescale_frames(record):
        return {**record, "frame_in": record["frame_in"] * FRAME_RATIO,
                "frame_out_exclusive": record["frame_out_exclusive"] * FRAME_RATIO}

    effect = prior["audio"]["title_effect"]
    write_json(EDIT / "export-contract-v10.json", {
        **prior, "revision": "v10", "output": str(OUTPUT),
        "fps": FPS, "frames": prior["frames"] * FRAME_RATIO,
        "segments": [rescale_frames(segment) for segment in prior["segments"]],
        "rank_reveals": [rescale_frames(reveal) for reveal in reveals],
        "video": {**prior["video"], "operation": "render titles at 48 fps, repeat each 24 fps meme frame twice and encode", "crf": 17,
                  "source": str(BASE.relative_to(EPISODE)), "source_sha256": base_qa["sha256"]},
        "audio": {**prior["audio"], "mode": "copy accepted v08 AAC stream",
                  "copy_source": str(BASE.relative_to(EPISODE)), "copy_source_sha256": base_qa["sha256"],
                  "title_effect": {**effect,
                                   "start_frames": [i * FRAME_RATIO for i in effect["start_frames"]],
                                   "end_frames_exclusive": [i * FRAME_RATIO for i in effect["end_frames_exclusive"]]}},
        "transitions": [{key: value for key, value in rescale_frames(card).items() if key != "fade_in_frames"}
                        | {"motion": motion} for card in cards],
    })
    write_json(EDIT / "render-command-v10.json", {"extract_base_frames": extract, "render": args})
    subprocess.run(extract, check=True)
    for i, card in enumerate(cards):
        title_frames(card, scratch / f"slate-{i}.png", scratch / f"card-{i}")
    subprocess.run(args, check=True)


if __name__ == "__main__":
    with TemporaryDirectory(prefix="scenes-meme-v10-") as temp:
        render(Path(temp))
