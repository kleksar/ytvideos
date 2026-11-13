#!/usr/bin/env python3
"""Check current documentation and skill routing offline, without rewriting evidence."""
import argparse
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
# This offline gate runs before dependency installation. The shared documentation
# checks and stage routing use only the standard library.
sys.path.insert(0, str(ROOT / "src"))
from ytvideos.context import STAGE_REFERENCES  # noqa: E402
from ytvideos.documentation import current_reference_error, prose_lines  # noqa: E402

CATALOG = Path(".agent/skill-catalog.json")
CATALOG_VIEW = Path(".agent/skill-catalog.md")
ENTRIES = ("AGENTS.md", "README.md", "COLLABORATION.md", "ONBOARDING.md",
           ".agent/README.md", ".agent/documentation-index.md")
LINK = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?:<([^<>\n]*)>|((?:\\.|[^\\()\s]|\([^()\n]*\))*))"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"
)
DEFINITION = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))")
REFERENCE = re.compile(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]")


def markdown_links(text):
    lines = [(number, re.sub(r"(`+).*?\1", "", line)) for number, line in prose_lines(text)]
    definitions = {}
    for _, line in lines:
        match = DEFINITION.match(line)
        if match:
            label, angle, plain = match.groups()
            definitions[" ".join(label.casefold().split())] = angle or plain
    for number, line in lines:
        if DEFINITION.match(line):
            continue
        for match in LINK.finditer(line):
            yield number, match.group(1) if match.group(1) is not None else match.group(2)
        remainder = LINK.sub("", line)
        for label, reference in REFERENCE.findall(remainder):
            key = " ".join((reference or label).casefold().split())
            if key in definitions:
                yield number, definitions[key]
        remainder = REFERENCE.sub("", remainder)
        for label in re.findall(r"!?\[([^\]\n]+)\]", remainder):
            key = " ".join(label.casefold().split())
            if key in definitions:
                yield number, definitions[key]


def markdown_anchors(text):
    anchors = set()
    previous = ""
    for _, line in prose_lines(text):
        anchors.update(re.findall(r"<(?:a|span)\b[^>]*\b(?:id|name)=[\"']([^\"']+)[\"']", line))
        heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        title = heading.group(1) if heading else previous if re.fullmatch(r"\s{0,3}(?:=+|-+)\s*", line) else ""
        if title:
            title = LINK.sub(lambda match: re.match(r"!?\[([^\]]*)", match.group()).group(1), title)
            title = html.unescape(re.sub(r"<[^>]*>", "", title))
            slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
            candidate, suffix = slug, 0
            while candidate in anchors:
                suffix += 1
                candidate = f"{slug}-{suffix}"
            anchors.add(candidate)
        previous = line.strip()
    return anchors


def current_documents(root, errors=None, *, runtime_documents=None):
    errors = [] if errors is None else errors
    runtime_documents = set() if runtime_documents is None else runtime_documents
    docs = {root / name for name in ENTRIES} | {root / CATALOG_VIEW}
    runtime_documents.update(root / name for name in ENTRIES)
    runtime_documents.update(root / name for names in STAGE_REFERENCES.values() for name in names)
    runtime_documents.update((root / ".agents/skills").glob("*/SKILL.md"))
    for folder in ("docs", ".agents/skills"):
        docs.update((root / folder).rglob("*.md"))
    for name in ("AGENTS.md", "PROFILE.md", "profile.md", "README.md"):
        docs.update((root / "channels").glob(f"*/{name}"))
        runtime_documents.update((root / "channels").glob(f"*/{name}"))
    if (root / "channels/README.md").exists():
        docs.add(root / "channels/README.md")
    docs.update((root / ".codex/agents").glob("*.md"))
    for profile in (root / "channels").glob("*/channel.json"):
        try:
            if not profile.resolve().is_relative_to(root):
                raise ValueError("profile leaves repository")
            references = json.loads(profile.read_text(encoding="utf-8")).get("context_references", [])
            for reference in references:
                name = reference["path"]
                if not isinstance(name, str) or Path(name).suffix.lower() != ".md":
                    raise ValueError("context reference must name a Markdown document")
                path = root / name
                if not path.resolve().is_relative_to(root):
                    raise ValueError("context reference leaves repository")
                docs.add(path)
                runtime_documents.add(path)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            errors.append(f"{profile.relative_to(root)}: cannot check context references: {exc}")
    # Episode ledgers, archived references and untracked .agent notes are not rules.
    return sorted(docs)


def render_catalog(catalog):
    lines = [
        "# Каталог навыков", "",
        "Источник: [skill-catalog.json](skill-catalog.json). Загружать skill текущего task из `context`; "
        "весь каталог не является обязательным контекстом.", "",
        "<!-- Generated by scripts/check_repository.py --render-catalog; do not edit. -->", "",
        "| Навык | Применение |", "|---|---|",
    ]
    for entry in catalog["skills"]:
        description = " ".join(entry["description"].split()).replace("|", "\\|")
        lines.append(f"| [{entry['name']}](../{entry['path']}) | {description} |")
    return "\n".join(lines) + "\n"


def frontmatter_value(content, field):
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
    values = re.findall(r"^" + field + r":\s*(.+)$", match.group(1), re.M) if match else []
    if len(values) != 1:
        return None
    value = values[0].strip()
    if value.startswith('"'):
        try:
            return json.loads(value)
        except ValueError:
            return None
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def check(root=ROOT, known_paths=()):
    root = Path(root).resolve()
    errors, known, anchors = [], set(known_paths), {}
    runtime_documents = set()
    docs = current_documents(root, errors, runtime_documents=runtime_documents)
    try:
        if not (root / CATALOG).resolve().is_relative_to(root):
            raise ValueError("catalog leaves repository")
        catalog = json.loads((root / CATALOG).read_text(encoding="utf-8"))
        skills = catalog["skills"]
        if not isinstance(skills, list) or any(
            not isinstance(entry, dict) or any(not isinstance(entry.get(key), str) or not entry[key]
                                              for key in ("name", "path", "description"))
            for entry in skills
        ):
            raise ValueError("skills must contain name, path and description strings")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [*errors, f"invalid skill catalog: {exc}"], len(docs), 0
    actual = set((root / ".agents/skills").glob("*/SKILL.md"))
    listed = {root / entry["path"] for entry in skills}
    if actual != listed:
        errors.append("skill catalog differs from discoverable SKILL.md files")
    if len({entry["name"] for entry in skills}) != len(skills) or len(listed) != len(skills):
        errors.append("duplicate skill names or paths")
    entrypoint = root / "AGENTS.md"
    if entrypoint.resolve().is_relative_to(root) and entrypoint.is_file() and len(entrypoint.read_bytes()) > 8000:
        errors.append("AGENTS.md exceeds the 8 KB entry budget")
    for entry in skills:
        path = root / entry["path"]
        if not path.resolve().is_relative_to(root) or not path.is_file():
            errors.append(f"missing or nonlocal skill: {entry['path']}")
            continue
        content = path.read_text(encoding="utf-8")
        if frontmatter_value(content, "name") != entry["name"]:
            errors.append(f"invalid skill frontmatter name: {entry['path']}")
        if frontmatter_value(content, "description") != entry["description"]:
            errors.append(f"skill description differs from catalog: {entry['path']}")
        if len(content.encode()) > 12000:
            errors.append(f"skill exceeds 12 KB: {entry['path']}")
    view = root / CATALOG_VIEW
    if view.resolve().is_relative_to(root) and view.is_file() and view.read_text(encoding="utf-8") != render_catalog(catalog):
        errors.append("skill catalog Markdown is stale; regenerate with --render-catalog")
    if list((root / ".agents/skills").rglob("*.py")):
        errors.append("executable helpers belong in automation/helpers")
    for path in docs:
        relative = path.relative_to(root)
        if not path.resolve().is_relative_to(root) or not path.is_file():
            errors.append(f"missing or nonlocal entry {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        if path in runtime_documents:
            error = (current_reference_error(relative.as_posix(), content)
                     or current_reference_error(path.resolve().relative_to(root).as_posix(), content))
            if error:
                errors.append(error)
        for number, target in markdown_links(content):
            try:
                parsed = urlsplit(html.unescape(target))
            except ValueError:
                errors.append(f"{relative}:{number}: invalid link {target}")
                continue
            if parsed.scheme or parsed.netloc:
                continue
            destination = unquote(parsed.path)
            resolved = (path.parent / destination).resolve() if destination else path.resolve()
            prefix = f"{relative}:{number}"
            if not resolved.is_relative_to(root):
                errors.append(f"{prefix}: link leaves repository: {target}")
            elif not resolved.exists():
                if resolved.relative_to(root).as_posix() not in known:
                    errors.append(f"{prefix}: missing link {target}")
                elif parsed.fragment:
                    errors.append(f"{prefix}: unverified anchor {target}; materialize the target document")
            elif parsed.fragment and resolved.suffix.lower() == ".md":
                if resolved not in anchors:
                    anchors[resolved] = markdown_anchors(resolved.read_text(encoding="utf-8"))
                if unquote(parsed.fragment) not in anchors[resolved]:
                    errors.append(f"{prefix}: missing heading anchor {target}")
    return errors, len(docs), len(listed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--known-paths", type=Path, help="Verified remote paths; absent anchor targets still need local content")
    parser.add_argument("--render-catalog", action="store_true", help="Print the Markdown projection; does not change files")
    args = parser.parse_args()
    if args.render_catalog:
        print(render_catalog(json.loads((ROOT / CATALOG).read_text(encoding="utf-8"))), end="")
        return 0
    known = json.loads(args.known_paths.read_text()) if args.known_paths else []
    errors, documents, skills = check(known_paths=known)
    print(json.dumps({"errors": errors, "documents_checked": documents, "skills": skills}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
