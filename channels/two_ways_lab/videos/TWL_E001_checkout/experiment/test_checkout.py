import json
import unittest

from checkout import HERE, simulate


class CheckoutTest(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((HERE / "input.json").read_text())
        self.results = simulate(self.config)

    def test_rounds_and_service_order(self):
        self.assertEqual(self.results["item_totals"], {"A": 25, "B": 14})
        first, second = self.results["rounds"]
        self.assertEqual([list(lane.values()) for lane in first["completion_seconds"].values()],
                         [[32, 58], [8, 18, 30, 38, 48]])
        self.assertEqual([list(lane.values()) for lane in second["completion_seconds"].values()],
                         [[40, 74], [16, 34, 54, 70, 88]])
        self.assertEqual([(r["clear_seconds"], r["winner"], r["margin_seconds"]) for r in (first, second)],
                         [({"A": 58, "B": 48}, "B", 10), ({"A": 74, "B": 88}, "A", 14)])

    def test_keyframes_exclude_customers_who_complete_at_that_instant(self):
        self.assertEqual({k: v["remaining"] for k, v in self.results["states"].items()}, {
            "K03": {"A": ["A1", "A2"], "B": ["B3", "B4", "B5"]},
            "K04": {"A": ["A2"], "B": []},
            "K05": {"A": ["A2"], "B": ["B3", "B4", "B5"]},
            "K06": {"A": [], "B": ["B5"]},
        })

    def test_saved_events_match_current_input(self):
        self.assertEqual(self.results, json.loads((HERE / "events.json").read_text()))


if __name__ == "__main__":
    unittest.main()
