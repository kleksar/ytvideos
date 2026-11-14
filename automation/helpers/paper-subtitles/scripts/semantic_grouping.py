#!/usr/bin/env python3
"""Shared sentence-first, syntax-aware grouping for one-line long subtitles.

This is a deterministic first pass, not a language parser. It keeps exact word
tokens/timings, joins two complete sentences when enabled and they fit, protects common
syntactic bonds, then selects the fewest readable lines within the measured
font width. The returned map remains subject to editorial review.
"""
from __future__ import annotations

import math
import re
from typing import Iterable, Sequence


VERSION = "sentence-syntax-width-v7"
INFINITY = float("inf")

ARTICLES_DETERMINERS = set("a an the this that these those some any each every either neither no another all both such".split())
POSSESSIVES = set("my your his her its our their whose".split())
PREPOSITIONS = set("about above across after against along among around as at before behind below beneath beside between beyond but by despite down during except for from in inside into like near of off on onto out outside over past per round since than through throughout till to toward under underneath until up upon via with within without".split())
ADJUNCT_PREPOSITIONS = set("during before after since until throughout across around near outside inside over under beneath below above along".split())
AUXILIARIES = set("am is are was were be been being do does did have has had can could may might must shall should will would".split())
RELATIVES = set("who whom whose which that where when why".split())
COORDINATORS = set("and but or nor yet so".split())
SUBORDINATORS = set("because although though while whereas if unless once whenever wherever until since".split())
NEGATIONS = set("not never".split())
ATTACHED_MODIFIERS = set("often always usually sometimes frequently rarely seldom still already just also even only ever again".split())
SUBJECT_PRONOUNS = set("i you he she it we they".split())
PARTICLE_PREPS = set("in out up off on away back down over through for".split())
STRANDED_PREP_VERBS = set("fight fought look looked pay paid stand stood call called ask asked care cared search searched wait waited work worked live lived deal dealt speak spoke talk talked think thought listen listened rely relied depend depended prepare prepared come came go went sit sat run ran carry carried bring brought take took turn turned give gave put placed".split())
ATTRIBUTIVE_ADJECTIVES = set("medieval ancient modern early late western eastern northern southern roman greek british french english black great old new first second last".split())
VERB_COMPLEMENT_PREPS = {"live": {"on"}, "lived": {"on"}, "rely": {"on"}, "relied": {"on"}, "depend": {"on"}, "depended": {"on"}, "insist": {"on"}, "based": {"on"}, "focus": {"on"}, "focused": {"on"}, "care": {"for", "about"}, "cared": {"for", "about"}, "search": {"for"}, "searched": {"for"}, "wait": {"for"}, "waited": {"for"}, "look": {"for", "at"}, "looked": {"for", "at"}, "listen": {"to"}, "listened": {"to"}, "belong": {"to"}, "belonged": {"to"}, "consist": {"of"}, "consisted": {"of"}, "suffer": {"from"}, "suffered": {"from"}, "result": {"in"}, "resulted": {"in"}, "live": {"through"}, "lived": {"through"}}
WEAK_END = (ARTICLES_DETERMINERS | POSSESSIVES | PREPOSITIONS | AUXILIARIES |
            RELATIVES | COORDINATORS | SUBORDINATORS | NEGATIONS | SUBJECT_PRONOUNS |
            ATTACHED_MODIFIERS | set("to".split()))
ABBREVIATIONS = {
    "mr.", "mrs.", "ms.", "dr.", "prof.", "sr.", "jr.", "st.",
    "vs.", "etc.", "e.g.", "i.e.", "u.s.", "u.k.",
}
TERMINAL_RE = re.compile(r"[.!?…]+[\"'’”)}\]]*$")
CLAUSE_PUNCT_RE = re.compile(r"[,;:—–][\"'’”)}\]]*$")
WORD_EDGE_RE = re.compile(r"^[^\w]+|[^\w'’\-]+$", re.UNICODE)


def bare(token: str) -> str:
    """Return a lowercase lexical form while retaining internal apostrophes."""
    return WORD_EDGE_RE.sub("", str(token)).replace("’", "'").lower()


def is_sentence_end(token: str) -> bool:
    raw = str(token).strip()
    lexical = bare(raw)
    if raw.lower() in ABBREVIATIONS or re.fullmatch(r"(?:[a-z]\.){2,}", raw.lower()):
        return False
    return bool(TERMINAL_RE.search(raw))


def is_sentence_end_at(words: Sequence[dict], index: int) -> bool:
    """Keep the numbered abbreviation ``No. 1`` within its sentence."""
    raw = str(words[index]["text"]).strip()
    if (raw == "No." and index + 1 < len(words)
            and re.match(r"^\d", str(words[index + 1]["text"]).strip())):
        return False
    return is_sentence_end(raw)


def sentence_ranges(words: Sequence[dict]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start = 0
    for i, word in enumerate(words):
        if is_sentence_end_at(words, i):
            ranges.append((start, i + 1))
            start = i + 1
    if start < len(words):
        ranges.append((start, len(words)))
    return ranges


def _crosses_keep_together(words: Sequence[dict], cut: int, pairs: set[tuple[str, str]]) -> bool:
    if cut <= 0 or cut >= len(words):
        return False
    # A no-space transcript join is one typographic unit even though each
    # spoken word has an independent highlight event. Splitting it would add
    # a cue boundary/space and change the exact caption text.
    if words[cut].get("join_previous", False):
        return True
    left, right = bare(words[cut - 1]["text"]), bare(words[cut]["text"])
    return (left, right) in pairs


def _require_keep_together(words: Sequence[dict], cut: int,
                           pairs: set[tuple[str, str]]) -> None:
    if _crosses_keep_together(words, cut, pairs):
        protected = _phrase(words[cut - 1:cut + 1])
        raise ValueError("group plan splits keep_together words: " + protected)


def _complete_lexical_do(group: Sequence[dict]) -> bool:
    """Recognize fronted-question complements such as `what could you do`.

    Here `do` is the main verb, not a stranded auxiliary, so a boundary after
    it can be syntactically complete when width forces the following clause
    onto another line.
    """
    if not group or bare(group[-1]["text"]) != "do":
        return False
    preceding = [bare(word["text"]) for word in group[:-1]]
    return "what" in preceding and "you" in preceding


def _complete_adverbial_inside(group: Sequence[dict]) -> bool:
    """Recognize locative adverb `inside` after a stay/remain verb."""
    if len(group) < 2 or bare(group[-1]["text"]) != "inside":
        return False
    return bare(group[-2]["text"]) in {
        "stay", "stays", "stayed", "staying", "remain", "remains",
        "remained", "remaining", "stand", "stands", "stood", "standing",
    }


def _forced_demonstrative_relative_split(words: Sequence[dict], cut: int,
                                         group: Sequence[dict], font,
                                         max_text_width: float,
                                         max_words: int | None = None) -> bool:
    """Allow `those / who...` only when its complete relative clause cannot fit."""
    if (not group or bare(group[-1]["text"]) != "those" or cut >= len(words)
            or bare(words[cut]["text"]) not in RELATIVES):
        return False
    end = cut
    while end < len(words):
        end += 1
        if is_sentence_end(words[end - 1]["text"]):
            break
    continuation = list(group) + list(words[cut:end])
    return not _fits(continuation, font, max_text_width, max_words)


def _forced_relative_marker_split(words: Sequence[dict], cut: int,
                                  previous: Sequence[dict], group: Sequence[dict],
                                  font, max_text_width: float,
                                  max_words: int | None = None) -> bool:
    """Allow a lone relative `that` only when the complete clause cannot fit.

    This narrowly supports reviewed Short cue plans such as
    `beneath a roof / that / might collapse?`: it keeps the modal and main
    verb together when the full relative clause exceeds the safe width.
    """
    if (len(group) != 1 or bare(group[0]["text"]) != "that" or not previous
            or cut >= len(words) or bare(words[cut]["text"]) not in AUXILIARIES):
        return False
    # Require a likely nominal antecedent at the end of the prior cue.
    antecedent = bare(previous[-1]["text"])
    if not antecedent or antecedent in WEAK_END or CLAUSE_PUNCT_RE.search(previous[-1]["text"]):
        return False
    end = cut
    while end < len(words):
        end += 1
        if is_sentence_end(words[end - 1]["text"]):
            break
    forced_clause = list(previous) + list(group) + list(words[cut:end])
    return not _fits(forced_clause, font, max_text_width, max_words)


def boundary_cost(words: Sequence[dict], cut: int, pairs: set[tuple[str, str]]) -> float:
    """Editorial cost of a boundary after words[:cut]; infinity means unsafe."""
    if cut <= 0 or cut >= len(words):
        return 0.0
    if _crosses_keep_together(words, cut, pairs):
        return INFINITY

    left_token = str(words[cut - 1]["text"])
    left, right = bare(left_token), bare(words[cut]["text"])
    # Punctuation closes a complete phrase/clause even when the final token
    # is a stranded phrasal-verb particle ("brought in,").
    if CLAUSE_PUNCT_RE.search(left_token):
        return 0.0
    if (left == "inside" and cut >= 2 and bare(words[cut - 2]["text"]) in {
            "stay", "stays", "stayed", "staying", "remain", "remains",
            "remained", "remaining", "stand", "stands", "stood", "standing",
    }):
        return 0.0
    # A predicate followed by correlative "not only" can introduce its
    # complement on the next line ("we learn not only / about ...").
    # Treating "only" as an unconditional hook can instead strand the
    # final noun of that complement on a line of its own.
    if left == "only" and cut >= 3 and bare(words[cut - 2]["text"]) == "not":
        return 4.0
    if (left in WEAK_END and not _complete_lexical_do(words[:cut])) or left.endswith("'s"):
        if left in PARTICLE_PREPS and cut >= 2 and bare(words[cut - 2]["text"]) in STRANDED_PREP_VERBS and right in SUBORDINATORS | COORDINATORS:
            return 1.0
        return INFINITY
    if left in ATTRIBUTIVE_ADJECTIVES and str(words[cut]["text"])[0:1].isupper():
        return INFINITY
    # Keep common multiword numeric values and units together.
    if left in {"hundred", "thousand", "million", "billion", "dozen"}:
        return INFINITY
    if left.isdigit() or left in {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"}:
        if right in {"hundred", "thousand", "million", "billion", "percent", "per", "cent", "years", "year", "days", "day", "hours", "hour", "miles", "mile", "coins", "coin", "people", "men", "women"}:
            return INFINITY

    # A line break before a relative pronoun strands it from its antecedent.
    # It is permitted only when width forces it; its predicate must then stay
    # with it (the previous-word rule prevents ending a line on "who").
    if right in RELATIVES:
        return 80.0
    if right in AUXILIARIES:
        return 45.0
    if right in ATTACHED_MODIFIERS or right.endswith("ly"):
        return 40.0
    if right in ARTICLES_DETERMINERS or right in POSSESSIVES:
        return 18.0
    if right == "to":
        # Infinitive and complement phrases are natural continuation starts
        # when their marker remains with what follows.
        return 2.0
    if right in VERB_COMPLEMENT_PREPS.get(left, set()):
        return 45.0
    if cut <= 2 and bare(words[0]["text"]) in COORDINATORS and right in PREPOSITIONS:
        return 45.0
    if right in PREPOSITIONS:
        # Genitive/complement prepositions bind tightly to the noun before
        # them. Temporal/spatial adjuncts are more natural line starts.
        if right in {"of", "for", "about", "with", "by", "as", "without", "around", "alongside"}:
            return 45.0
        return 2.0 if right in ADJUNCT_PREPOSITIONS else 18.0
    if right in COORDINATORS or right in SUBORDINATORS:
        return 32.0 if right in COORDINATORS else 4.0
    # Avoid breaking adjective + noun or a leading modifier from its head.
    if right and (left.endswith(("al", "ial", "ful", "less", "ous", "ive", "able", "ible", "ic", "ical", "ed", "ing"))):
        return 12.0
    return 8.0


def _pairs(values: Iterable[Sequence[str] | str]) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for value in values:
        parts = str(value).lower().split() if isinstance(value, str) else [str(x).lower() for x in value]
        if len(parts) != 2:
            raise ValueError("keep-together entries must contain exactly two words")
        out.add((bare(parts[0]), bare(parts[1])))
    return out


def _phrase(words: Sequence[dict]) -> str:
    return "".join(("" if i == 0 or w.get("join_previous", False) else " ")
                   + str(w["text"]) for i, w in enumerate(words))


def _validate_limits(max_text_width: float, max_words: int | None) -> None:
    if not math.isfinite(max_text_width) or max_text_width <= 0:
        raise ValueError("max_text_width must be finite and positive")
    if max_words is not None and (not isinstance(max_words, int) or isinstance(max_words, bool) or max_words < 1):
        raise ValueError("max_words must be a positive integer")


def _fits(words: Sequence[dict], font, max_text_width: float,
          max_words: int | None) -> bool:
    """Both routes measure the same font and enforce the same word limit."""
    return ((max_words is None or len(words) <= max_words)
            and float(font.getlength(_phrase(words))) <= max_text_width)


def boundary_warnings(groups: Sequence[Sequence[dict]]) -> list[dict]:
    """Expose forced/ambiguous breaks for full-sequence editorial review.

    Neither a heuristic warning nor its absence establishes semantic acceptance.
    In particular the max-word fallback must never silently become a PASS.
    """
    words = [word for group in groups for word in group]
    warnings = []
    cursor = 0
    for index, group in enumerate(groups[:-1]):
        cursor += len(group)
        if not is_sentence_end(group[-1]['text']):
            cost = boundary_cost(words, cursor, set())
            if not math.isfinite(cost) or cost >= 45:
                warnings.append({'after_group': index, 'left': _phrase(group),
                                 'right': _phrase(groups[index + 1]),
                                 'reason': 'forced_or_ambiguous_syntax_boundary'})
    return warnings


def _partition_sentence(words: Sequence[dict], font, max_text_width: float,
                        pairs: set[tuple[str, str]], max_words: int | None = None,
                        allow_weak_boundary: bool = False) -> list[list[dict]]:
    n = len(words)
    # Dynamic programming minimizes line count first. Within that, it favors
    # natural boundaries and avoids needlessly tiny neighboring lines.
    best: list[tuple[float, list[int]] | None] = [None] * (n + 1)
    best[n] = (0.0, [])
    for start in range(n - 1, -1, -1):
        for end in range(start + 1, n + 1):
            if max_words is not None and end - start > max_words:
                break
            group = words[start:end]
            width = float(font.getlength(_phrase(group)))
            if width > max_text_width:
                break
            if end < n:
                cut_cost = boundary_cost(words, end, pairs)
                if not math.isfinite(cut_cost):
                    left = bare(words[end - 1]['text'])
                    forced_possessive = (left.endswith("'s") and end < n
                        and float(font.getlength(_phrase(words[end - 1:end + 1]))) > max_text_width)
                    if allow_weak_boundary and not _crosses_keep_together(words, end, pairs) and (left in WEAK_END | {'hundred','thousand','million','billion','dozen'} or forced_possessive):
                        cut_cost = 2000.0 if forced_possessive or left not in WEAK_END else 1000.0
                    else:
                        continue
            else:
                cut_cost = 0.0
                # An unfinished sentence may not end on a syntactic hook.
                if bare(group[-1]["text"]) in WEAK_END and not is_sentence_end(group[-1]["text"]):
                    continue
            tail = best[end]
            if tail is None:
                continue
            utilization = width / max_text_width
            # Underfill is a light tie-breaker, never strong enough to add a
            # whole extra line or override a syntactic bond.
            underfill = 6.0 * (1.0 - utilization) ** 2
            short_group = 0.0
            if n > 1 and len(group) == 1:
                short_group = 100.0
            elif n > 2 and len(group) == 2 and not CLAUSE_PUNCT_RE.search(str(group[-1]["text"])):
                short_group = 25.0
            total = 10000.0 + cut_cost + underfill + short_group + tail[0]
            candidate = (total, [end] + tail[1])
            if best[start] is None or candidate[0] < best[start][0]:
                best[start] = candidate
    if best[0] is None:
        raise ValueError(
            f"sentence has no valid one-line partition with max_text_width={max_text_width:g}px, "
            f"max_words={max_words}: {_phrase(words)}; preserve exact words, font and keep_together "
            "and review the conflicting constraints before rendering"
        )
    result: list[list[dict]] = []
    start = 0
    for end in best[0][1]:
        result.append(list(words[start:end]))
        start = end
    return result


def group_words(words: Sequence[dict], font, max_text_width: float,
                keep_together: Iterable[Sequence[str] | str] = (), max_words: int | None = None,
                combine_sentences: bool = False) -> list[list[dict]]:
    """Group exact timed words sentence-first, protecting syntax and width."""
    _validate_limits(max_text_width, max_words)
    if not words:
        return []
    pairs = _pairs(keep_together)
    groups: list[list[dict]] = []
    ranges = sentence_ranges(words)
    index = 0
    while index < len(ranges):
        start, end = ranges[index]
        if combine_sentences and index + 1 < len(ranges):
            next_start, next_end = ranges[index + 1]
            combined = words[start:next_end]
            if (is_sentence_end(words[end - 1]["text"])
                    and is_sentence_end(words[next_end - 1]["text"])
                    and _fits(combined, font, max_text_width, max_words)):
                groups.append(list(combined))
                index += 2
                continue
        try:
            groups.extend(_partition_sentence(words[start:end], font, max_text_width, pairs, max_words))
        except ValueError:
            if max_words is None:
                raise
            groups.extend(_partition_sentence(words[start:end], font, max_text_width, pairs, max_words, allow_weak_boundary=True))
        index += 1
    cursor = 0
    for group in groups[:-1]:
        cursor += len(group)
        _require_keep_together(words, cursor, pairs)
    return groups


def plan_phrases(words: Sequence[dict], phrases: Sequence[str], font,
                 max_text_width: float, keep_together: Iterable[Sequence[str] | str] = (),
                 combine_sentences: bool = False,
                 boundary_exceptions: Sequence[dict] = (),
                 max_words: int | None = None) -> list[list[dict]]:
    """Resolve exact phrases using the automatic route's width/word constraints.

    Returning a plan is not semantic acceptance. Forced boundaries from the
    canonical automatic proposal remain visible through ``boundary_warnings``
    and require the same complete-sequence review as automatic grouping.
    """
    _validate_limits(max_text_width, max_words)
    if not phrases or not all(isinstance(x, str) and x.strip() for x in phrases):
        raise ValueError("group plan must be a non-empty list of phrases")
    pairs = _pairs(keep_together)
    automatic_boundaries: set[tuple[str, str]] = set()
    if max_words is not None:
        try:
            automatic = group_words(words, font, max_text_width, pairs, max_words,
                                    combine_sentences)
        except ValueError:
            # An explicit measured plan may resolve an automatic heuristic's
            # failure. It must still pass every hard constraint below.
            pass
        else:
            automatic_boundaries = {(_phrase(left), _phrase(right))
                                    for left, right in zip(automatic, automatic[1:])}
    exceptions: dict[tuple[str, str], str] = {}
    user_approved: set[tuple[str, str]] = set()
    for item in boundary_exceptions:
        if not isinstance(item, dict):
            raise ValueError("boundary exceptions must be objects with left, right, and reason")
        left, right, reason = (item.get(key) for key in ("left", "right", "reason"))
        if not all(isinstance(value, str) and value.strip() for value in (left, right, reason)):
            raise ValueError("boundary exceptions require exact left/right phrases and a reason")
        key = (left.strip(), right.strip())
        if key in exceptions:
            raise ValueError("duplicate subtitle boundary exception: " + left + " / " + right)
        exceptions[key] = reason.strip()
        if item.get("user_approved") is True:
            evidence = item.get("approval_evidence")
            evidence_sha256 = item.get("approval_sha256")
            if (not isinstance(evidence, str) or not evidence.strip()
                    or not isinstance(evidence_sha256, str)
                    or not re.fullmatch(r"[0-9a-f]{64}", evidence_sha256)):
                raise ValueError("user-approved boundary exceptions require approval evidence and its SHA-256")
            user_approved.add(key)
    groups: list[list[dict]] = []
    cursor = 0
    previous_exception = False
    for phrase_index, phrase in enumerate(phrases):
        group: list[dict] = []
        while cursor < len(words) and len(_phrase(group)) < len(phrase):
            group.append(words[cursor])
            cursor += 1
        if _phrase(group) != phrase:
            raise ValueError("group plan changes, skips, or reorders transcript words: " + phrase)
        if max_words is not None and len(group) > max_words:
            raise ValueError(f"group plan exceeds max_words={max_words}: {phrase}")
        if float(font.getlength(phrase)) > max_text_width:
            raise ValueError("group plan exceeds measured one-line width: " + phrase)
        group_start = cursor - len(group)
        _require_keep_together(words, group_start, pairs)
        internal_ends = sum(is_sentence_end_at(words, index) for index in range(group_start, cursor - 1))
        starts_sentence = group_start == 0 or is_sentence_end_at(words, group_start - 1)
        if internal_ends and not (combine_sentences and internal_ends == 1 and starts_sentence
                                  and is_sentence_end(group[-1]["text"])):
            raise ValueError("group plan crosses a spoken sentence boundary: " + phrase)
        correlative = (len(group) >= 3 and bare(group[-1]["text"]) == "only"
                       and bare(group[-2]["text"]) == "not")
        exception_key = (phrase, phrases[phrase_index + 1]) if phrase_index + 1 < len(phrases) else None
        exception = exceptions.pop(exception_key, None) if exception_key else None
        automatic_boundary = exception_key in automatic_boundaries
        left_words = [bare(word["text"]) for word in group]
        right_words = ([bare(word["text"]) for word in words[cursor:cursor + len(phrases[phrase_index + 1].split())]]
                       if phrase_index + 1 < len(phrases) else [])
        allowed_exception = bool(exception) and (
            (left_words[-1:] == ["even"] and right_words[:1] == ["in"])
            or (left_words[-1:] == ["it"] and right_words[:1] == ["because"]
                and left_words[:4] == ["he", "is", "doing", "it"])
            or (left_words[-1:] == ["it"] and right_words[:1] == ["with"]
                and "paid" in left_words and "for" in left_words[:-1])
            or (left_words[-1:] == ["has"] and right_words[:1] in (["another"], ["a"], ["the"])
                and len(left_words) >= 2)
            or (left_words[-2:] in (["handing", "over"], ["handed", "over"])
                and right_words[:1] in (["the"], ["his"], ["their"]))
            or (left_words[-2:] == ["from", "which"] and right_words[:1] == ["they"])
            or (left_words == ["by", "then", "voyager", "1", "was"]
                and right_words == ["about", "24", "billion", "kilometers"])
            or (left_words == ["with", "the", "program", "that"]
                and right_words == ["prepared", "information", "about"])
            or (left_words == ["prepared", "information", "about"]
                and right_words == ["the", "spacecraft's", "condition"])
            or (left_words[-1:] == ["around"]
                and right_words[:1] and right_words[0] in {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"}
                and any(x in {"hundred", "thousand", "million", "billion"} for x in right_words)
                and float(font.getlength(phrase + " " + phrases[phrase_index + 1])) > max_text_width
                and float(font.getlength(phrases[phrase_index + 1])) <= max_text_width)
            or (left_words[-1:] == ["been"] and "not" in left_words
                and len(right_words) >= 2 and right_words[0].endswith("ly")
                and float(font.getlength(phrase + " " + phrases[phrase_index + 1])) > max_text_width
                and float(font.getlength(phrases[phrase_index + 1])) <= max_text_width)
            or exception_key in user_approved
            or automatic_boundary
        )
        if exception and not allowed_exception:
            raise ValueError("subtitle boundary exception is not one of the supported forced splits: " + exception_key[0] + " / " + exception_key[1])
        cut = cursor - len(group)
        forced_relative = bool(groups) and _forced_relative_marker_split(
            words, cursor, groups[-1], group, font, max_text_width, max_words)
        if ((bare(group[-1]["text"]) in WEAK_END
             and not _complete_lexical_do(group)
             and not _complete_adverbial_inside(group)
             and not _forced_demonstrative_relative_split(words, cursor, group, font,
                                                         max_text_width, max_words))
                and not is_sentence_end(group[-1]["text"])
                and not CLAUSE_PUNCT_RE.search(group[-1]["text"])
                and not forced_relative
                and not correlative):
            if not allowed_exception and not automatic_boundary:
                raise ValueError("group plan leaves a syntactic hook at the line end: " + phrase)
        if groups:
            previous = groups[-1]
            if is_sentence_end(previous[-1]["text"]):
                pass
            else:
                cost = boundary_cost(words, cut, pairs)
                combined = _phrase(previous + group)
                if cost >= 80 and _fits(previous + group, font, max_text_width, max_words) and not previous_exception:
                    raise ValueError("group plan separates a relative clause that fits with its antecedent: " + combined)
        groups.append(group)
        previous_exception = allowed_exception
    if cursor != len(words):
        raise ValueError("group plan omits transcript words")
    if exceptions:
        left, right = next(iter(exceptions))
        raise ValueError("unused subtitle boundary exception: " + left + " / " + right)
    return groups
