# Palmier MCP — connection audit, 2026-11-03

The user requested MCP operation instead of manual Computer Use. This audit made read-only MCP calls; no timeline mutation, export, UI interaction, or account/configuration change was performed.

## Verified result

- Endpoint: `http://127.0.0.1:19789/mcp`, native Palmier Streamable HTTP MCP; negotiated protocol `2025-06-18`.
- Existing client: `stories/automation/palmier/inspect_connection.py`, `PalmierConnection`.
- Full paginated `tools/list`: 58 tools; [raw schemas](tools-list.json). Palmier tools were absent from the chat tool catalog, but the local server responded successfully. Their absence from the chat does not establish server unavailability.
- Read-only calls: `manage_project list`, `get_media`, `get_timeline` for both target timelines, `manage_snapshots list` for both.
- Project `FE6B0E4C`: `/Users/diplomat/ytvideos/new_channel/videos/038_47_ronin/Edit/Palmier/Paper Detour 038 47 Ronin Visual Assembly v01.palmier`.
- Timeline 1 `571C02AE`: empty, 0 frames; snapshot `20042C59` is actually named **Snapshot 1**. Earlier claimed rename to “Before v01 timeline build” did not persist.
- Timeline 2 `0488A0F6`: empty, 0 frames, no snapshots; 2560×1440, 30 fps, rec709. It remains available for future authorized assembly.
- [Project/media response](paper038-readback.json), [timeline/snapshot response](timeline-readback.json).

## Correction and working procedure

The previous conclusion “Palmier editing is blocked because MCP tools are not exposed in this runtime” was too broad. The local bridge was not tried then. It is available now, and the existing client supports direct MCP calls without opening windows or changing the frontmost project. Past availability cannot be reconstructed from this current probe.

The canonical edit skill now requires checking the local adapter when native chat tools are absent, reading actual live schemas, and using explicit project/timeline IDs. It routes transport details to the existing adapter. Computer Use is not an automatic editing fallback; the user's direct UI instruction is required for that path. Existing snapshot, ownership, exact readback and no-manual-.palmier rules remain in place.

Official reference: [Palmier Agent and MCP](https://www.palmier.io/docs/agent-and-mcp), read on 2026-11-03: local MCP server, Codex connection URL, background open/create, explicit project/timeline addressing, import, batch edits, snapshots and exports. Live schemas establish the installed server's exact arguments; public documentation alone does not.
