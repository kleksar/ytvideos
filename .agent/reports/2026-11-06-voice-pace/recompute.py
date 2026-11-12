"""Read-only verification of the six retained calibration samples."""
import hashlib
import json
import pathlib
import re

folder = pathlib.Path(__file__).resolve().parent
root = folder.parents[2]
data = json.loads((folder / "measurements.json").read_text())
for sample in data["samples"]:
    for kind, evidence in sample["files"].items():
        path = root / evidence["path"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != evidence["sha256"]:
            raise ValueError(f"Evidence changed: {path} ({kind})")
    words = json.loads((root / sample["files"]["word_map"]["path"]).read_text())["words"]
    count = sum(bool(re.search(r"\w", token))
                for token in " ".join(w["text"] for w in words).split())
    span = max(w["end"] for w in words) - min(w["start"] for w in words)
    rate = 60 * count / span
    assert count == sample["counted_words"]
    assert abs(span - sample["speech_span_seconds"]) < 1e-6
    assert abs(rate - sample["effective_words_per_minute"]) < 1e-6
    print(f"{sample['episode']}: {count} / {span:.6f}s = {rate:.3f} words/min")
print("PASS: evidence hashes and all six calculations match; no listening QA claimed.")
