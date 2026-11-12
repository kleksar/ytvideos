import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('repository_check', Path(__file__).resolve().parents[1] / 'scripts/check_repository.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class RepositoryCheckTest(unittest.TestCase):
    def test_historical_agent_notes_are_not_inputs_but_current_channel_links_are_checked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for folder in ('.agent', '.agents/skills', 'docs', 'channels/example', '.codex/agents'):
                (root / folder).mkdir(parents=True, exist_ok=True)
            for name in ('AGENTS.md', 'README.md', 'COLLABORATION.md', '.agent/skill-catalog.md'):
                (root / name).write_text('# Entry\n')
            (root / '.agent/skill-catalog.json').write_text(json.dumps({'skills': []}))
            (root / '.agent/old-ledger.md').write_text('[historical](missing.md)\n')
            (root / 'channels/example/AGENTS.md').write_text('[current](missing.md)\n')
            errors, _, _ = checker.check(root)
            self.assertEqual(len(errors), 1)
            self.assertIn('channels/example/AGENTS.md', errors[0])


if __name__ == '__main__':
    unittest.main()
