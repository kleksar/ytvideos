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
D = ("parents", "grandma", "grandma_parents", "whole", "grandma_kids", "kids")


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
    best = [per for total, per in scores if total == 12]
    assert all(per == {"M": 2, "D": 2, "G": 4, "S": 2, "B": 2} for per in best)
    assert movements(D) == (14, {"M": 4, "D": 4, "G": 2, "S": 2, "B": 2})
    constrained_best = [per for total, per in scores if total == 14 and per["G"] == 2]
    assert len(constrained_best) == 16
    assert constrained_best.count(movements(C)[1]) == 8
    assert constrained_best.count(movements(D)[1]) == 8
    return "PASS: 720 orders; A24 B12 C14 D14; 8 global optima all G4; 16 G2 optima split 8/8"


if __name__ == "__main__":
    print(test_all())
