"""Replace the five v08 title cards and copy the accepted AAC mix."""
import json
import math
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from PIL import Image, ImageChops, ImageDraw

from render_ranked_v06 import CREAM, EDIT, EPISODE, FPS, HEIGHT, SHADOW, WIDTH, digest, font

BASE = EPISODE / "Deliverables" / "meme-time-machine-01_draft-v08.mp4"
OUTPUT = EPISODE / "Deliverables" / "meme-time-machine-01_draft-v09.mp4"
CENTER = (WIDTH // 2, HEIGHT // 2)
TITLE_TOP = 565
TITLE_BOTTOM = 1345
TITLE_HEIGHT = TITLE_BOTTOM - TITLE_TOP
START_SCALE = 2.75
LANDING_FRAME = 12
OVERSAMPLE = 3
FFMPEG = ["ffmpeg", "-nostdin", "-hide_banner", "-v", "error", "-n"]


def write_json(path, value):
    with path.open("x") as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")


def title_layer(text):
    scale = OVERSAMPLE
    layer = Image.new("RGBA", (WIDTH * scale, 230 * scale))
    anchor = (layer.width // 2, layer.height // 2)
    draw = ImageDraw.Draw(layer)
    point_size = 100
    face = font(point_size * scale)
    while draw.textlength(text, font=face) > 940 * scale:
        point_size -= 2
        face = font(point_size * scale)
    draw.text(anchor, text, font=face, anchor="mm", fill=CREAM,
              stroke_width=2 * scale, stroke_fill=SHADOW)
    return layer, anchor


def placement(frame):
    progress = min(frame / LANDING_FRAME, 1)
    remaining = 1 - progress
    # Positive screen-space angles turn clockwise. Approach zero upright.
    angle = -360 * remaining ** 1.65
    scale = 1 + (START_SCALE - 1) * remaining ** 2.8
    return angle, scale


def title_frames(card, slate_path, sequence_dir):
    slate = Image.open(slate_path).convert("RGBA")
    layer, (source_x, source_y) = title_layer(card["text"])
    center_x, center_y = CENTER[0], CENTER[1] - TITLE_TOP

    # Feather the edges of the title zone to keep the rank list clear.
    mask = Image.new("L", (1, TITLE_HEIGHT))
    mask.putdata([round(255 * min(y / 40, (TITLE_HEIGHT - 1 - y) / 40, 1))
                  for y in range(TITLE_HEIGHT)])
    mask = mask.resize((WIDTH, TITLE_HEIGHT))

    for frame in range(card["frame_out_exclusive"] - card["frame_in"]):
        angle, scale = placement(frame)
        radians = math.radians(angle)
        cosine = math.cos(radians) * OVERSAMPLE / scale
        sine = math.sin(radians) * OVERSAMPLE / scale
        inverse = (
            cosine, sine, source_x - cosine * center_x - sine * center_y,
            -sine, cosine, source_y + sine * center_x - cosine * center_y,
        )
        lettering = layer.transform((WIDTH, TITLE_HEIGHT), Image.Transform.AFFINE, inverse,
                                    resample=Image.Resampling.BICUBIC)
        lettering.putalpha(ImageChops.multiply(lettering.getchannel("A"), mask))
        composed = slate.copy()
        composed.alpha_composite(lettering, (0, TITLE_TOP))
        composed.convert("RGB").save(sequence_dir / f"{frame:02}.png", compress_level=1)


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
            f"setpts=PTS-STARTPTS[meme{i}]",
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
        "angle_ease_out_power": 1.65,
        "scale_ease_out_power": 2.8,
        "pivot": list(CENTER),
        "title_zone": [TITLE_TOP, TITLE_BOTTOM],
    }
    write_json(EDIT / "export-contract-v09.json", {
        **prior, "revision": "v09", "output": str(OUTPUT),
        "video": {**prior["video"], "operation": "replace title cards and encode", "crf": 17,
                  "source": str(BASE.relative_to(EPISODE)), "source_sha256": base_qa["sha256"]},
        "audio": {**prior["audio"], "mode": "copy accepted v08 AAC stream",
                  "copy_source": str(BASE.relative_to(EPISODE)), "copy_source_sha256": base_qa["sha256"]},
        "transitions": [{key: value for key, value in card.items() if key != "fade_in_frames"}
                        | {"motion": motion} for card in cards],
    })
    write_json(EDIT / "render-command-v09.json", {"extract_base_frames": extract, "render": args})
    subprocess.run(extract, check=True)
    for i, card in enumerate(cards):
        title_frames(card, scratch / f"slate-{i}.png", scratch / f"card-{i}")
    subprocess.run(args, check=True)


if __name__ == "__main__":
    with TemporaryDirectory(prefix="scenes-meme-v09-") as temp:
        render(Path(temp))
