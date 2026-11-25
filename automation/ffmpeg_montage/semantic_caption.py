"""Fixed semantic colours with the explicitly supplied soft-word edit style.

Only used by an owner-selected local edit recipe; this is not a new default
for the illustrated or Resolve subtitle pipelines.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


class SemanticCaption:
    def __init__(self, card, phrase, palette, font_path, sample_rate, style):
        self.c = card
        self.id = card["id"]
        self.start = card["start_seconds"]
        self.end = card["end_seconds"]
        self.style = style
        self.palette = palette
        self.width, self.height = style["canvas"]
        self.rows, self.tokens = [], []
        words = phrase["resolved_words"] if phrase else None
        n = 0
        for row in card["rows"]:
            text = " ".join(t["text"] for t in row["tokens"])
            font = ImageFont.truetype(str(font_path), row["font_size"])
            width = font.getlength(text)
            if width > style["max_width"]:
                raise ValueError(f"{self.id}: caption exceeds explicit width")
            x = (self.width - width) / 2
            masks = []
            for stroke, alpha, offset in [(0, 255, (0, 0)), (1, 255, (0, 0)),
                                           (2, 165, (5, 7))]:
                im = Image.new("L", (self.width, self.height))
                ImageDraw.Draw(im).text((x + offset[0], row["baseline"] + offset[1]),
                                        text, font=font, anchor="ls", fill=180 if stroke == 2 else alpha,
                                        stroke_width=stroke, stroke_fill=alpha)
                masks.append(np.asarray(im))
            cur, tokens = 0, []
            for token in row["tokens"]:
                word = token["text"]
                lo = x + font.getlength(text[:cur])
                hi = x + font.getlength(text[:cur + len(word)])
                start = words[n]["start_sample"] / sample_rate if words else self.start + .1
                tk = {**token, "start": start, "lo": lo, "hi": hi}
                tokens.append(tk)
                self.tokens.append(tk)
                n += 1
                cur += len(word) + 1
            self.rows.append({"tokens": tokens, "masks": masks, "text": text,
                              "font_size": font.size, "width": width,
                              "baseline": row["baseline"]})
        self.full_at = max(t["start"] - style["reveal_lead"] + style["reveal_duration"]
                           for t in self.tokens)
        self.full_texture = None

    def texture(self, t):
        if t >= self.full_at and self.full_texture is not None:
            return self.full_texture
        shape = (self.height, self.width)
        fill, edge, shadow = [np.zeros(shape, np.uint8) for _ in range(3)]
        colours = {name: np.zeros(shape, np.uint8) for name in self.palette}
        for row in self.rows:
            for tk in row["tokens"]:
                amount = smooth((t - tk["start"] + self.style["reveal_lead"]) /
                                self.style["reveal_duration"])
                dy = round(self.style["reveal_rise"] * (1 - amount))
                lo = max(0, math.floor(tk["lo"]) - 7)
                hi = min(self.width, math.ceil(tk["hi"]) + 9)
                for dest, mask in zip((fill, edge, shadow), row["masks"]):
                    layer = np.zeros(shape, np.uint8)
                    layer[:, lo:hi] = (mask[:, lo:hi] * amount).astype(np.uint8)
                    if dy:
                        layer = np.roll(layer, dy, axis=0)
                        layer[:dy] = 0
                    np.maximum(dest, layer, out=dest)
                    if dest is fill:
                        np.maximum(colours[tk["colour"]], layer,
                                   out=colours[tk["colour"]])
        out = Image.new("RGBA", (self.width, self.height))
        for name, mask in colours.items():
            for radius, strength in self.style["glow"]:
                alpha = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(radius))
                alpha = alpha.point(lambda q: min(255, round(q * strength)))
                layer = Image.new("RGBA", out.size, (*self.palette[name], 0))
                layer.putalpha(alpha)
                out.alpha_composite(layer)
        rim = Image.fromarray(edge).filter(ImageFilter.MaxFilter(5))
        layer = Image.new("RGBA", out.size, (*self.style["outline_rgb"], 0))
        layer.putalpha(rim.point(lambda q: round(q * self.style["outline_alpha"])))
        out.alpha_composite(layer)
        for name, mask in colours.items():
            layer = Image.new("RGBA", out.size, (*self.palette[name], 0))
            layer.putalpha(Image.fromarray(mask))
            out.alpha_composite(layer)
        sh = Image.new("RGBA", out.size, (*self.style["shadow_rgb"], 0))
        sh.putalpha(Image.fromarray(shadow).filter(ImageFilter.GaussianBlur(2)))
        if t >= self.full_at:
            self.full_texture = out, sh
        return out, sh

    def image(self, t):
        block, shadow = self.texture(t)
        if self.c.get("outro"):
            out = Image.alpha_composite(shadow, block)
            alpha = smooth((t - self.start) / self.style["reveal_duration"])
        else:
            phase = t - self.start
            dx = self.style["float_x"] * math.sin(phase * 1.7)
            dy = self.style["float_y"] * math.sin(phase * 2.2)
            angle = self.style["float_degrees"] * math.sin(phase * 1.9)
            block = block.rotate(angle, Image.Resampling.BICUBIC)
            shadow = shadow.rotate(angle, Image.Resampling.BICUBIC)
            out = Image.new("RGBA", (self.width, self.height))
            out.alpha_composite(shadow, (round(dx + 2), round(dy + 3)))
            out.alpha_composite(block, (round(dx), round(dy)))
            alpha = min(1, max(0, (t - self.start) / self.style["fade_in"]),
                        max(0, (self.end - t) / self.style["fade_out"]))
        out.putalpha(out.getchannel("A").point(lambda q: round(q * alpha)))
        return out
