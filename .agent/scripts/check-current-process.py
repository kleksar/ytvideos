#!/usr/bin/env python3
"""Catch obsolete montage routes in active docs; does not audit archived evidence."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[2]
files=[ROOT/'AGENTS.md',ROOT/'channels/paper_detour/AGENTS.md',ROOT/'channels/nuviko_history/AGENTS.md',ROOT/'channels/nuviko_stories/AGENTS.md']
files += [ROOT/'.agent'/name for name in ('CHANNEL_BOOTSTRAP.md','documentation-index.md','skill-catalog.md')]
files += list((ROOT/'.agents/skills').rglob('*.md')) + list((ROOT/'.codex/agents').glob('*.toml')) + [ROOT/'.codex/agents/README.md',ROOT/'automation/ffmpeg_montage/README.md']
forbidden=[r'ytv-palmier-edit',r'references/palmier\.md',r'layered-motion\.md',r'motion-before-no-parallax',r'параллакс',r'\bparallax\b',r'зерн',r'\bgrain\b',r'\bg08\b']
errors=[]
for file in files:
 if not file.is_file():continue
 for number,line in enumerate(file.read_text().splitlines(),1):
  if any(re.search(pattern,line,re.I) for pattern in forbidden):errors.append(f'{file.relative_to(ROOT)}:{number}: obsolete montage route')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'Current-process route check: {len(files)} documents; no obsolete montage routes found.')
