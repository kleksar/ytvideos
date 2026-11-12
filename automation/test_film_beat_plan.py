import unittest

import numpy as np

from film_beat_plan import make_plan
from music_beats import RATE


class BeatPlanTest(unittest.TestCase):
    def test_pulse_is_measured_and_offset_to_full_timeline(self):
        samples = np.random.default_rng(5).normal(0, 0.0001, 12 * RATE).astype('float32')
        for time in np.arange(.35, 11.8, 2 / 3):
            start = round(time * RATE)
            n = np.arange(500)
            samples[start:start + len(n)] += (np.sin(2 * np.pi * 80 * n / RATE) * np.exp(-n / 100)).astype('float32')
        result = make_plan(samples, 24, 3.5, 3.7, 2, 6)
        self.assertAlmostEqual(result['pulse']['bpm'], 90, delta=1)
        for row, expected in zip(result['selected_transitions'], np.arange(3.85, 15.3, 4 / 3)):
            self.assertAlmostEqual(row['time_seconds'], expected, delta=.045)
            self.assertLessEqual(abs(row['frame_seconds'] - row['time_seconds']), 1 / 48 + 1e-6)

    def test_silence_is_not_a_beat_map(self):
        with self.assertRaises(ValueError):
            make_plan(np.zeros(8 * RATE, dtype='float32'), 24, 0, 0, 1, 1)


if __name__ == '__main__':
    unittest.main()
