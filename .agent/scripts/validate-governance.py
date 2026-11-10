#!/usr/bin/env python3
"""Compatibility entry point for the current repository contract check."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parents[2] / "scripts/check_repository.py"), run_name="__main__")
