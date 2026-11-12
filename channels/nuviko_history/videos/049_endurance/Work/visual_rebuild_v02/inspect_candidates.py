"""Record local generation output and prepare contact sheets for human review."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from PIL import Image, ImageDraw


def file_record(path):
    with path.open("rb") as handle:
        digest = sha256(handle.read()).hexdigest()
    return {"path": str(path), "sha256": digest}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    run = args.run.resolve()
    requests = json.loads((run / "REQUESTS.json").read_text())
    previous = run / "GENERATION.json"
    prior = json.loads(previous.read_text()) if previous.exists() else []
    saved = {item["file"]["sha256"]: item for item in prior}
    records = []
    for request in requests:
        path = run / f"{request['id']}_{request['version']}.png"
        if not path.is_file():
            print(f"Missing {path.name}")
            continue
        record = file_record(path)
        if record["sha256"] in saved:
            records.append(saved[record["sha256"]])
            continue
        with Image.open(path) as image:
            dims = list(image.size)
        records.append({
            "id": request["id"],
            "version": request["version"],
            "file": record,
            "generation": "built-in ImageGen, new composition",
            "prompt": request["prompt"],
            "requested_dimensions": [2560, 1440],
            "native_dimensions": dims,
            "tool_controls": {"transparent_background": False},
            "reference_files": [file_record(Path(name)) for name in request["refs"]],
            "status": "REVIEW_REQUIRED",
        })
    previous.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")

    for offset in range(0, len(records), 9):
        sheet = Image.new("RGB", (1278, 774), "#101820")
        text = ImageDraw.Draw(sheet)
        for index, record in enumerate(records[offset:offset + 9]):
            path = Path(record["file"]["path"])
            with Image.open(path) as source:
                frame = source.convert("RGB")
            frame.thumbnail((426, 240))
            x, y = index % 3 * 426, index // 3 * 258
            text.text((x + 9, y + 2), path.name)
            sheet.paste(frame, (x, y + 18))
        sheet.save(run / f"CONTACT_{offset // 9 + 1:02d}.jpg", quality=90)
    print(f"{len(records)} records for {len(requests)} requests")


if __name__ == "__main__":
    main()
