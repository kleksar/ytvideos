import os
import re
import shutil
import tempfile
from pathlib import Path

from .errors import WorkflowError
from .util import file_digest


class ArtifactStore:
    """Immutable content addresses. Store this root on shared durable storage for multi-host work."""

    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, source, kind):
        if not isinstance(kind, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", kind):
            raise WorkflowError("artifact kind must be a stable lowercase identifier")
        source = Path(source).resolve()
        if not source.is_file() or source.stat().st_size == 0:
            raise WorkflowError(f"artifact must be an existing nonempty file: {source}")
        sha = file_digest(source)
        destination = self.root / "sha256" / sha[:2] / sha
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if file_digest(destination) != sha:
                raise WorkflowError("content-addressed artifact was corrupted")
        else:
            fd, temporary = tempfile.mkstemp(dir=destination.parent)
            try:
                with os.fdopen(fd, "wb") as out, source.open("rb") as incoming:
                    shutil.copyfileobj(incoming, out)
                    out.flush()
                    os.fsync(out.fileno())
                if file_digest(temporary) != sha:
                    raise WorkflowError("artifact changed while it was being imported")
                os.replace(temporary, destination)
            finally:
                Path(temporary).unlink(missing_ok=True)
        return {"id": f"{kind}:sha256:{sha}", "sha256": sha, "uri": f"sha256/{sha[:2]}/{sha}",
                "kind": kind, "size": destination.stat().st_size, "filename": source.name}

    def resolve(self, artifact):
        path = (self.root / artifact["uri"]).resolve()
        if not path.is_relative_to(self.root) or not path.is_file() or file_digest(path) != artifact["sha256"]:
            raise WorkflowError("artifact is missing, corrupt, or outside the configured artifact root")
        return path
