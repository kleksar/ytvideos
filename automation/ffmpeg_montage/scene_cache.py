"""Bounded cache of rendered scene clips, with immutable keys and verified bytes.

Cache entries are expendable copies, never the only accepted source or final.
Each checkout materializes its own work copy before eviction can remove a key.
"""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import time


def sha256(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


@contextmanager
def lock(path):
    with path.open("a+b") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


class SceneCache:
    def __init__(self, root, *, max_bytes, engine_identity):
        if type(max_bytes) is not int or max_bytes < 1:
            raise ValueError("scene cache max_bytes must be positive")
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes
        self.engine = engine_identity

    def key(self, scene, canvas, encoder, bitrate):
        scene = dict(scene)
        image = scene.pop("image")
        frames = scene.pop("end_frame") - scene.pop("start_frame")
        contract = {"schema": 1, "image_sha256": sha256(image), "frames": frames, "scene": scene,
                    "canvas": canvas, "encoder": encoder, "bitrate": bitrate, "fps": 30, "engine": self.engine}
        return hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()

    def render(self, renderer, index, scene, work, canvas, encoder, bitrate):
        key = self.key(scene, canvas, encoder, bitrate)
        clip = self.root / f"{key}.mp4"
        metadata = self.root / f"{key}.json"
        destination = work / f"scene_{index:05d}.mp4"
        hit = False
        # One short-held global lock prevents eviction of an entry while it is
        # copied. Rendering itself never holds this lock, so unrelated scenes run.
        with lock(self.root / ".cache.lock"):
            if clip.is_file() and metadata.is_file():
                try:
                    saved = json.loads(metadata.read_text())
                except (ValueError, OSError):
                    saved = {}
                if saved.get("key") == key and sha256(clip) == saved.get("sha256"):
                    shutil.copy2(clip, destination)
                    os.utime(metadata, None)
                    hit = True
        if not hit:
            destination = renderer(index, scene, work, canvas, encoder, bitrate)
            if self.key(scene, canvas, encoder, bitrate) != key:
                raise ValueError("scene source changed during rendering; do not reuse this result")
            if destination.stat().st_size <= self.max_bytes:
                with lock(self.root / ".cache.lock"):
                    with tempfile.TemporaryDirectory(prefix="entry-", dir=self.root) as temporary:
                        temp = Path(temporary)
                        shutil.copy2(destination, temp / "clip.mp4")
                        (temp / "meta.json").write_text(json.dumps({"key": key, "sha256": sha256(destination),
                                                                 "size": destination.stat().st_size, "created_at": time.time()}))
                        os.replace(temp / "clip.mp4", clip)
                        os.replace(temp / "meta.json", metadata)
                    self._evict()
        (work / f"scene_{index:05d}.cache.json").write_text(json.dumps({"key": key, "hit": hit,
                                                                      "sha256": sha256(destination)}) + "\n")
        return destination

    def _evict(self):
        entries = [(path.with_suffix(".json"), path) for path in self.root.glob("[0-9a-f]" * 64 + ".mp4")]
        total = sum(clip.stat().st_size for _, clip in entries if clip.exists())
        for metadata, clip in sorted(entries, key=lambda item: (item[0] if item[0].exists() else item[1]).stat().st_mtime):
            if total <= self.max_bytes:
                break
            if clip.exists():
                total -= clip.stat().st_size
                clip.unlink()
            metadata.unlink(missing_ok=True)
