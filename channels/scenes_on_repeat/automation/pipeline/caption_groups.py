"""Validate reviewed one-line groups against the timed film dialogue."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MAX_CHARS = 16
ROOT = Path(__file__).resolve().parents[4]
SEGMENTER = ROOT / ".agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py"
spec = spec_from_file_location("ytv_semantic_grouping", SEGMENTER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load shared sentence boundary rules: {SEGMENTER}")
segmenter = module_from_spec(spec)
spec.loader.exec_module(segmenter)


def resolve_groups(words, phrases):
    """Map exact reviewed lines to words, rejecting splits across sentences."""
    sentence_ends = {end for _, end in segmenter.sentence_ranges(words)}
    groups = []
    start = 0
    for phrase in phrases:
        tokens = phrase.split()
        if not tokens or phrase != " ".join(tokens) or len(phrase) > MAX_CHARS:
            raise ValueError(f"Expected one caption line of 1–{MAX_CHARS} characters: {phrase!r}")
        end = start + len(tokens)
        group = words[start:end]
        if tokens != [word["text"] for word in group]:
            raise ValueError(f"Caption changes or skips timed words: {phrase!r}")
        if any(boundary in sentence_ends for boundary in range(start + 1, end)):
            raise ValueError(f"Caption crosses a sentence boundary: {phrase!r}")
        groups.append(group)
        start = end
    if start != len(words):
        raise ValueError("Caption groups omit timed words")
    return groups
