"""Deterministic wait until the next customer can start at either checkout."""

import json
from itertools import accumulate
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEYFRAMES = {"K03": (1, 18), "K04": (1, 48), "K05": (2, 40), "K06": (2, 74)}


def simulate(config):
    scan = config["scan_seconds_per_item"]
    lanes = config["items_per_customer"]
    payments = config["payment_seconds_per_customer"]
    if set(lanes) != {"A", "B"} or not all(lanes.values()) or len(payments) != 2:
        raise ValueError("expected two populated lanes and two payment scenarios")
    if any(type(x) is not int or x <= 0 for x in (scan, *payments, *lanes["A"], *lanes["B"])):
        raise ValueError("this model requires positive integer item counts and times")
    rounds = []
    for payment in payments:
        completed = {
            lane: dict(zip(
                (f"{lane}{i}" for i in range(1, len(items) + 1)),
                accumulate(count * scan + payment for count in items),
            ))
            for lane, items in lanes.items()
        }
        elapsed = {lane: max(events.values()) for lane, events in completed.items()}
        margin = abs(elapsed["A"] - elapsed["B"])
        rounds.append({
            "payment_seconds": payment, "completion_seconds": completed, "clear_seconds": elapsed,
            "winner": min(elapsed, key=elapsed.get) if margin else None, "margin_seconds": margin,
        })
    return {
        "episode_id": config["episode_id"], "time_unit": config["time_unit"],
        "item_totals": {lane: sum(items) for lane, items in lanes.items()},
        "scan_seconds_per_item": scan, "rounds": rounds,
        "states": {
            key: {
                "round": number, "model_seconds": time,
                "remaining": {lane: [shopper for shopper, end in events.items() if end > time]
                              for lane, events in rounds[number - 1]["completion_seconds"].items()},
            }
            for key, (number, time) in KEYFRAMES.items()
        },
    }


if __name__ == "__main__":
    print(json.dumps(simulate(json.loads((HERE / "input.json").read_text())), indent=2))
