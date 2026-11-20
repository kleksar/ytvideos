"""Verify the exact six-photo, five-person A/B and Grandma-contiguous models.

This is a fictional count of crossings, not observed shooting time.
Run: python model_check.py
"""
from itertools import permutations

GROUPS = {
    "parents": frozenset("MD"),
    "grandma_kids": frozenset("GSB"),
    "whole": frozenset("MDGSB"),
    "grandma": frozenset("G"),
    "kids": frozenset("SB"),
    "grandma_parents": frozenset("GMD"),
}
A = ("parents", "grandma_kids", "whole", "grandma", "kids", "grandma_parents")
B = ("grandma", "grandma_parents", "parents", "whole", "grandma_kids", "kids")
C = ("parents", "grandma_parents", "whole", "grandma_kids", "grandma", "kids")


def movements(order):
    before = frozenset()
    per_person = {person: 0 for person in "MDGSB"}
    for group in (*order, None):
        after = GROUPS[group] if group is not None else frozenset()
        for person in before ^ after:
            per_person[person] += 1
        before = after
    return sum(per_person.values()), per_person


def test_all():
    scores = [movements(order) for order in permutations(GROUPS)]
    assert len(scores) == 720
    assert movements(A) == (24, {"M": 6, "D": 6, "G": 4, "S": 4, "B": 4})
    assert movements(B) == (12, {"M": 2, "D": 2, "G": 4, "S": 2, "B": 2})
    assert movements(C) == (14, {"M": 2, "D": 2, "G": 2, "S": 4, "B": 4})
    assert min(total for total, _ in scores) == 12
    assert sum(total == 12 for total, _ in scores) == 8
    assert min(total for total, per in scores if per["G"] == 2) == 14
    return "PASS: 720 orders; A24 B12 C14; min=12 with 8 ties; Grandma-two-crossings minimum=14"


if __name__ == "__main__":
    print(test_all())
