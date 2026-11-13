"""Small shared checks for documents used as current production instructions.

Evidence and historical sources remain valid data. This guard prevents explicitly
historical material from becoming a new run's rule packet; it is not a semantic
detector for every stale sentence and never rewrites an existing pinned packet.
"""

from pathlib import PurePosixPath
import re


HISTORICAL_DIRECTORIES = {
    "archive", "archives", "legacy", "consultations", "reports", "proposals",
    "receipts", "logs", "evals",
}
HISTORICAL_FILES = {"history.md", "changelog.md", "change_log.md", "migration-ledger.md"}
# These retained inventories and episode decisions are data, not instructions for
# a new run. Do not infer this from dates: dated, accepted brand references remain
# valid inputs.
DATA_ONLY_PATHS = {
    ".agent/episode-registry.md",
    ".agent/asset_cleanup_20261102.md",
    ".agent/stories_storage_review_2026-11-02.md",
    ".agent/youtube_studio_setup_20261105.md",
    ".agent/validation-report-20261101.md",
    "channels/paper_detour/rarovista_timeline_coordination.md",
    "channels/paper_detour/rarovista_visual_direction_draft.md",
}
HISTORY_HEADING = re.compile(
    r"^(?:история\s+изменений|журнал\s+изменений|changelog|change\s+history|"
    r"revision\s+history|version\s+history)(?:\b|$)", re.I
)


def prose_lines(text):
    """Retain line numbers while excluding fenced Markdown examples."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, rest = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not rest.strip():
                fence = None
            yield number, ""
        else:
            yield number, line if fence is None else ""


def current_reference_error(path, text=None):
    """Return an actionable error for an explicitly historical rule source."""
    parts = tuple(part.casefold() for part in PurePosixPath(path).parts)
    historical = (any(part in HISTORICAL_DIRECTORIES for part in parts[:-1])
                  or (parts and parts[-1] in HISTORICAL_FILES)
                  or "/".join(parts) in DATA_ONLY_PATHS
                  or parts[:2] in {(".agent", "research"), (".agents", "research")}
                  or (parts and parts[0] in {"output", "work"})
                  or (len(parts) > 3 and parts[0] == "channels"
                      and parts[2] in {"videos", "episodes"}))
    if historical:
        return f"historical evidence cannot be a current task requirement: {path}"
    if text is None:
        return None
    frontmatter = re.match(r"\A\ufeff?---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if frontmatter and re.search(
        r"^(?:status|document_role|role):\s*['\"]?(?:history|historical|archive|archived|"
        r"superseded|obsolete|legacy)['\"]?\s*(?:#.*)?$", frontmatter.group(1), re.M | re.I
    ):
        return f"historical document metadata cannot supply current task requirements: {path}"
    previous = ""
    for number, line in prose_lines(text):
        heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        title = heading.group(1) if heading else previous if re.fullmatch(r"\s{0,3}(?:=+|-+)\s*", line) else ""
        title = re.sub(r"[*_`]", "", title).strip()
        if HISTORY_HEADING.match(title):
            return (f"{path}:{number}: change history is not a current task requirement; "
                    "keep the current rule here and its history in Git")
        previous = line.strip()
    return None
