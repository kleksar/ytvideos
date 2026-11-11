#!/usr/bin/env python3
"""Validate current entries; historical evidence is not workflow input."""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT, known_paths=()):
    errors = []
    known = set(known_paths)
    catalog = json.loads((root / ".agent/skill-catalog.json").read_text())
    actual = set((root / ".agents/skills").glob("*/SKILL.md"))
    listed = {root / entry["path"] for entry in catalog["skills"]}
    if actual != listed:
        errors.append("skill catalog differs from discoverable SKILL.md files")
    if len({entry["name"] for entry in catalog["skills"]}) != len(listed):
        errors.append("duplicate skill names")
    if len((root / "AGENTS.md").read_bytes()) > 8000:
        errors.append("AGENTS.md exceeds the 8 KB entry budget")
    for entry in catalog["skills"]:
        path = root / entry["path"]
        if not path.exists():
            errors.append(f"missing skill: {entry['path']}")
            continue
        content = path.read_text()
        if not content.startswith("---\n") or not re.search(r"^name:\s*" + re.escape(entry["name"]) + r"\s*$", content, re.M):
            errors.append(f"invalid skill frontmatter: {entry['path']}")
        if not re.search(r"^description:\s*\S", content, re.M):
            errors.append(f"missing trigger description: {entry['path']}")
        if len(content.encode()) > 12000:
            errors.append(f"skill exceeds 12 KB: {entry['path']}")
    if list((root / ".agents/skills").rglob("*.py")):
        errors.append("executable helpers belong in automation/helpers")
    docs = [root / name for name in ("AGENTS.md", "README.md", "COLLABORATION.md")]
    docs += list((root / "docs").rglob("*.md")) + list((root / ".agents/skills").rglob("*.md"))
    docs += list((root / ".agent").glob("*.md")) + list((root / "channels").glob("*/AGENTS.md"))
    docs += list((root / "channels").glob("*/profile.md")) + list((root / ".codex/agents").glob("*.md"))
    for path in docs:
        if not path.exists():
            errors.append(f"missing entry {path.relative_to(root)}")
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            for target in re.findall(r"\]\(([^)]+)\)", line):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                target = target.split("#", 1)[0]
                resolved = (path.parent / target).resolve()
                if not resolved.is_relative_to(root.resolve()):
                    errors.append(f"{path.relative_to(root)}:{number}: link leaves repository")
                elif not resolved.exists() and str(resolved.relative_to(root)) not in known:
                    errors.append(f"{path.relative_to(root)}:{number}: missing link {target}")
    return errors, len(docs), len(listed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--known-paths", type=Path, help="Verified remote paths for a source-only snapshot")
    args = parser.parse_args()
    known = json.loads(args.known_paths.read_text()) if args.known_paths else []
    errors, documents, skills = check(known_paths=known)
    print(json.dumps({"errors": errors, "documents_checked": documents, "skills": skills}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
