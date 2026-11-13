"""Trusted local Codex hook entry; no host trust or configuration mutation."""
from pathlib import Path

from ytvideos.session_guard import main

main(Path(__file__).resolve().parents[2])
