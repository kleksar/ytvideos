import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from test_phrase_plan import fixture
import titles_command


class TitlesCommandTests(unittest.TestCase):
    def request(self):
        data = fixture()
        data['native_snapshot'] = {'picture': [], 'voice': []}
        data['native_titles']['replace_tracks'] = []
        return data

    def test_offline_default_creates_phrase_plan_without_connection(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(titles_command, 'ResolveMCP') as app:
            path = Path(tmp)/'request.json'
            path.write_text(json.dumps(self.request()))
            self.assertEqual(titles_command.main([str(path), '--output', tmp]), 0)
            app.assert_not_called()
            plan = json.loads((Path(tmp)/'phrase-plan.json').read_text())
            self.assertEqual(len(plan['layout']), 1)
            self.assertEqual(plan['inspector'], 'UNVERIFIED')

    def test_native_without_exclusive_fails_before_input_or_app(self):
        with patch.object(titles_command, 'ResolveMCP') as app, self.assertRaises(SystemExit):
            titles_command.main(['missing.json', '--output', '/unused', '--batch-start', '0'])
        app.assert_not_called()

    def test_finalize_without_candidate_bound_review_does_not_connect(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(titles_command, 'ResolveMCP') as app:
            data = self.request()
            data['target']['fps'] = '30'
            path = Path(tmp)/'request.json'
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'native review'):
                titles_command.main([str(path), '--output', tmp, '--finalize', '--exclusive-session'])
            app.assert_not_called()


if __name__ == '__main__':
    unittest.main()
