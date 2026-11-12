#!/usr/bin/env python3
"""Read-only guard for one exact Palmier project and timeline ID.

Palmier 0.12+ edits projects and timelines concurrently. This guard no longer
requires the target project or timeline to be visible; it validates the project
path, project ID, and timeline ID together and never changes the active tab.
"""
import argparse
import json
import os
import sys
import urllib.error

from inspect_connection import PalmierConnection


def same_project(path, requested):
    """Compare existing absolute filesystem objects, following compatibility links."""
    if not all(isinstance(p, str) and p and os.path.isabs(p) for p in (path, requested)):
        return False
    try:
        return os.path.samefile(path, requested)
    except OSError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-path", required=True)
    parser.add_argument("--timeline-id", required=True)
    args = parser.parse_args()
    try:
        connection = PalmierConnection()
        connection.connect()
        projects = connection.read_tool("manage_project", {"action": "list"})
        matches = [x for x in projects.get("projects", [])
                   if same_project(x.get("path"), args.project_path)]
        if len(matches) != 1 or not matches[0].get("isAccessible"):
            raise ValueError("Project path does not resolve to one accessible Palmier project")
        project = matches[0]
        if not project.get("isOpen"):
            raise ValueError("Project is not loaded; open it in the background, then rerun this guard")
        inventory = connection.read_tool("get_media", {"projectId": project["id"]})
        timeline_matches = [t for t in inventory.get("timelines", [])
                            if t.get("timelineId") == args.timeline_id]
        if len(timeline_matches) != 1:
            raise ValueError("Timeline ID is missing from this project's inventory")
        timeline = connection.read_tool("get_timeline", {
            "projectId": project["id"], "timelineId": args.timeline_id})
        if timeline.get("timelineId") != args.timeline_id:
            raise ValueError("Timeline snapshot does not match the requested timeline ID")
        print(json.dumps({
            "project_id": project["id"],
            "project_path": project.get("path"),
            "project_is_visible": project.get("isVisible"),
            "timeline_id": timeline["timelineId"],
            "name": timeline.get("name"),
            "fps": timeline.get("fps"),
            "width": timeline.get("width"),
            "height": timeline.get("height"),
            "total_frames": timeline.get("totalFrames"),
            "tracks": timeline.get("tracks", []),
            "note": "ID-scoped snapshot only: visibility does not select the target; recheck before editing. Track data does not verify playback or captions.",
        }, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, urllib.error.URLError) as exc:
        print(f"Palmier guard stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
