"""Deterministic static Nuviko typography. No audio, motion or editor mutations.

Each role is a separate full-canvas RGBA layer. The editable source is style.json.
Original scene bytes are read-only; composites are visual proofs, not replacements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as PILLOW_VERSION

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def intersects(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


class Renderer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.w, self.h = cfg["canvas"]
        self.ss = cfg["supersample"]
        self.fonts = {k: ImageFont.truetype(v["path"], v["size"] * self.ss)
                      for k, v in cfg["fonts"].items()}
        self.palette = cfg["palette"]

    def blank(self):
        return Image.new("RGBA", (self.w * self.ss, self.h * self.ss), (0, 0, 0, 0))

    def width(self, text, role, tracking=0):
        font = self.fonts[role]
        # Sum individual advances when tracked, matching draw_text exactly.
        return ((sum(font.getlength(c) for c in text) / self.ss + tracking * (len(text)-1))
                if tracking else font.getlength(text) / self.ss)

    def text_height(self, lines, role):
        boxes = [self.fonts[role].getbbox(t) for t in lines]
        top = min(b[1] for b in boxes)
        bottom = max(b[3] for b in boxes)
        return (bottom - top) / self.ss, top / self.ss

    def box(self, layer, xy, fill):
        x0, y0, x1, y1 = xy
        ImageDraw.Draw(layer).rectangle(
            (round(x0*self.ss), round(y0*self.ss), round(x1*self.ss)-1, round(y1*self.ss)-1),
            fill=fill)

    def draw_text(self, layer, text, role, x, top, tracking=0, ink_top=None):
        font = self.fonts[role]
        draw = ImageDraw.Draw(layer)
        # Normalize the ink's left bearing and top, not the font's em box.
        b = font.getbbox(text)
        y = (top - (b[1]/self.ss if ink_top is None else ink_top))*self.ss
        pen = x*self.ss - b[0]
        if tracking:
            for c in text:
                draw.text((pen, y), c, font=font, fill=self.palette["ink"])
                pen += font.getlength(c) + tracking*self.ss
        else:
            draw.text((pen, y), text, font=font, fill=self.palette["ink"])

    def wrap(self, text, max_width):
        if not text.strip():
            raise ValueError("Empty subtitle")
        words = text.split()
        lines, current = [], ""
        for word in words:
            if self.width(word, "subtitle") > max_width:
                raise ValueError(f"Unbreakable word exceeds subtitle width: {word}")
            test = (current + " " + word).strip()
            if current and self.width(test, "subtitle") > max_width:
                lines.append(current)
                current = word
            else:
                current = test
        lines.append(current)
        if len(lines) > self.cfg["subtitle"]["max_lines"]:
            raise ValueError("Cue exceeds two-line sample envelope; split the actual timed cue")
        return lines

    def subtitle(self, scene):
        p = self.cfg["subtitle"]
        max_width = scene["subtitle_max_width"] - 2*p["pad_x"]
        lines = scene.get("subtitle_lines") or self.wrap(scene["subtitle"], max_width)
        assert " ".join(lines) == scene["subtitle"], "Manual wrapping changes the text"
        assert 0 < len(lines) <= p["max_lines"]
        assert all(self.width(line,"subtitle") <= max_width for line in lines), "Manual line overflows"
        line_h, top_bearing = self.text_height(lines, "subtitle")
        widths = [self.width(line, "subtitle") for line in lines]
        w = math.ceil(max(widths) + 2*p["pad_x"])
        h = math.ceil(line_h*len(lines) + p["line_gap"]*(len(lines)-1) + 2*p["pad_y"])
        x, y = round(scene["subtitle_center"]-w/2), p["bottom"]-h
        layer = self.blank()
        self.box(layer, [x,y,x+w,y+h], self.palette["paper"])
        for i, line in enumerate(lines):
            self.draw_text(layer, line, "subtitle", scene["subtitle_center"]-widths[i]/2,
                           y+p["pad_y"]+i*(line_h+p["line_gap"]), ink_top=top_bearing)
        return layer, {"text": scene["subtitle"], "lines": lines, "box": [x,y,x+w,y+h]}

    def location(self, scene):
        p = self.cfg["location"]
        x, y = scene["location_xy"]
        text = scene["location"]
        th, _ = self.text_height([text], "location")
        w = math.ceil(self.width(text, "location")+2*p["pad_x"]+p["edge"])
        h = math.ceil(th+2*p["pad_y"])
        layer = self.blank()
        self.box(layer, [x,y,x+w,y+h], self.palette["paper"])
        self.box(layer, [x,y,x+p["edge"],y+h], self.palette["ochre"])
        self.draw_text(layer, text, "location", x+p["edge"]+p["pad_x"],y+p["pad_y"])
        return layer, {"text": text, "box": [x,y,x+w,y+h]}

    def accent(self, scene):
        p = self.cfg["accent"]
        x, y = scene["accent_xy"]
        text = scene["accent"]
        th, _ = self.text_height([text], "accent")
        w = math.ceil(self.width(text, "accent",p["tracking"])+2*p["pad_x"])
        h = math.ceil(th+2*p["pad_y"]+2*p["rule_width"])
        layer = self.blank()
        if scene["accent_backing"]:
            self.box(layer, [x,y,x+w,y+h], self.palette["paper"])
        self.box(layer,[x,y,x+w,y+p["rule_width"]],self.palette["ink"])
        self.box(layer,[x,y+h-p["rule_width"],x+w,y+h],self.palette["ink"])
        self.draw_text(layer,text,"accent",x+p["pad_x"],y+p["rule_width"]+p["pad_y"],p["tracking"])
        return layer, {"text": text, "box": [x,y,x+w,y+h], "backing":scene["accent_backing"]}

    def run(self, scene, out, tag):
        source = (ROOT/scene["source"]).resolve()
        assert sha(source) == scene["source_sha256"], f"Source changed: {source}"
        original = Image.open(source).convert("RGBA")
        assert original.size == (self.w,self.h), "Canvas differs from actual source"
        composite = original.copy()
        records = {}
        previous = []
        for role in ("location","accent","subtitle"):
            layer, record = getattr(self,role)(scene)
            box = record["box"]
            m = self.cfg["safe_margin"]
            assert box[0]>=m and box[1]>=m and box[2]<=self.w-m and box[3]<=self.h-m, (tag,role,"safe margin",box)
            for roi in scene["protected"]:
                assert not intersects(box,roi["rect"]), (tag,role,"protected",roi["name"])
            assert all(not intersects(box,b) for b in previous), (tag,role,"layer collision")
            previous.append(box)
            layer = layer.resize((self.w,self.h),Image.Resampling.LANCZOS)
            assert layer.mode == "RGBA" and layer.getextrema()[3][0] == 0
            bbox = layer.getbbox()
            assert bbox and bbox[0]>=box[0]-3 and bbox[1]>=box[1]-3 and bbox[2]<=box[2]+3 and bbox[3]<=box[3]+3
            path = out/"layers"/f"{tag}_{role}.png"
            layer.save(path)
            composite = Image.alpha_composite(composite,layer)
            record.update({"path":str(path.relative_to(out)),"sha256":sha(path),"alpha_bbox":bbox})
            records[role]=record
        proof=out/"proofs"/f"{tag}.png"
        composite.convert("RGB").save(proof)
        phone_w = self.cfg["phone_width"]
        phone_h = round(self.h*phone_w/self.w)
        phone = composite.convert("RGB").resize((phone_w,phone_h),Image.Resampling.LANCZOS)
        phone_path = out/"phone"/f"{tag}_390.png"
        phone.save(phone_path)
        assert sha(source)==scene["source_sha256"], "Source modified"
        return {"id":tag,"source":scene["source"],"source_sha256":sha(source),"roles":records,
                "protected":scene["protected"],"proof":str(proof.relative_to(out)),"proof_sha256":sha(proof),
                "phone":str(phone_path.relative_to(out)),"phone_sha256":sha(phone_path),
                "checks":{"source_unchanged":True,"safe_margins":True,"protected_rois_clear":True,
                          "layers_do_not_overlap":True,"transparent_layers":True}},phone


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,default=ROOT/"rendered")
    args=ap.parse_args()
    cfg=json.loads((ROOT/"style.json").read_text())
    out=args.out.resolve()
    for folder in ("layers","proofs","phone"):
        (out/folder).mkdir(parents=True,exist_ok=True)
    renderer=Renderer(cfg)
    scenes=list(cfg["scenes"])
    probe=next(s.copy() for s in scenes if s["id"]==cfg["wrap_probe"]["scene"])
    probe["subtitle"]=cfg["wrap_probe"]["subtitle"]
    probe["subtitle_lines"]=cfg["wrap_probe"].get("subtitle_lines")
    cases=[(s,s["id"]) for s in scenes]+[(probe,"S01_wrap_probe")]
    records,phones=[],[]
    for scene,tag in cases:
        record,phone=renderer.run(scene,out,tag)
        records.append(record)
        phones.append((tag,phone))
    # 1:1 grid: each phone frame is exactly 390x219, with labels outside the frame.
    fw,fh=phones[0][1].size
    grid=Image.new("RGB",(fw*2+24, (fh+36)*2+24),"#24231F")
    draw=ImageDraw.Draw(grid)
    label_font=ImageFont.truetype(cfg["fonts"]["location"]["path"],20)
    for i,(tag,phone) in enumerate(phones):
        x,y=12+(i%2)*fw,12+(i//2)*(fh+36)
        draw.text((x+8,y+6),tag,font=label_font,fill="#F3E9D5")
        grid.paste(phone,(x,y+36))
    grid.save(out/"phone_comparison.png")
    fonts={k:{**v,"actual_name":renderer.fonts[k].getname(),"sha256":sha(v["path"])}
           for k,v in cfg["fonts"].items()}
    receipt={"version":cfg["version"],"canvas":cfg["canvas"],"phone_size":phones[0][1].size,
             "style_sha256":sha(ROOT/"style.json"),"renderer_sha256":sha(Path(__file__)),
             "python":platform.python_version(),"pillow":PILLOW_VERSION,"fonts":fonts,
             "assets":records,"status":"STATIC_PROOFS_GENERATED", "review_record":"../QA.json",
             "scope":"Static reproducible typography examples only; no timing, animation, audio, export, independent or historical QA."}
    (out/"manifest.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"output":str(out),"cases":len(records),"layers":len(records)*3,
                      "phone_size":phones[0][1].size,"checks":"passed"}))


if __name__=="__main__":
    main()
