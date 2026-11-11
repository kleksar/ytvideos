"""Static routing and example arithmetic; these are not audience/semantic evals."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / 'evals/shorts_editorial'
SKILLS = ('ytv-write-script', 'ytv-produce-video', 'ytv-review-video')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


class EditorialRoutingTests(unittest.TestCase):
    def test_shorts_loop_is_mandatory_in_canonical_owner(self):
        text = read('docs/standards/editorial.md')
        self.assertIn('Для каждого Short обязательна естественная смысловая петля.', text)
        self.assertNotIn('Для каждого Short рассмотреть петлю', text)
        self.assertNotIn('решение «законченная версия без петли»', text)

    def test_script_procedure_has_named_steps_and_no_optional_loop_route(self):
        text = read('docs/standards/editorial.md')
        for step in ('Обещанная отдача', 'Один главный вопрос', 'Начало и конец вместе',
                     'Причинная середина', 'Устная редактура', 'Первый слушатель'):
            with self.subTest(step=step):
                self.assertIn(step, text)
        self.assertNotIn('Для Short рассмотреть петлю', read('.agents/skills/ytv-write-script/SKILL.md'))

    def test_all_affected_stages_link_to_editorial_owner(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                text = read(f'.agents/skills/{skill}/SKILL.md')
                self.assertIn('](../../../docs/standards/editorial.md)', text)
                self.assertLess(len(text.encode('utf-8')), 12000)

    def test_catalog_descriptions_match_skill_frontmatter(self):
        catalog = json.loads(read('.agent/skill-catalog.json'))
        expected_stages = {
            'ytv-write-script': ['research', 'script'],
            'ytv-produce-video': ['storyboard', 'scene_image', 'audio', 'subtitles', 'render'],
            'ytv-review-video': ['review'],
        }
        for name in SKILLS:
            with self.subTest(skill=name):
                entry = next(row for row in catalog['skills'] if row['name'] == name)
                text = read(entry['path'])
                match = re.search(r'^description: "(.*)"$', text, re.M)
                self.assertIsNotNone(match)
                self.assertEqual(entry['description'], match.group(1))
                self.assertEqual(entry['stages'], expected_stages[name])

    def test_review_requires_exact_mp4_seam_evidence(self):
        text = read('docs/standards/delivery.md')
        self.assertIn('## Петля Shorts: проверка точного MP4', text)
        for term in ('mp4_hash', 'timecodes', 'UNVERIFIED', 'первого просмотра', 'последних'):
            self.assertIn(term, text)

    def test_migration_and_evidence_are_not_approval_or_new_api(self):
        text = read('docs/standards/editorial.md')
        self.assertIn('Уже утверждённые тексты и MP4 автоматически не переписывать.', text)
        self.assertIn('не новые поля CLI/API', text)
        self.assertIn('Не обещать 120–150%', text)


class EditorialExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((EVAL / 'e001_model.json').read_text(encoding='utf-8'))

    def test_latest_complete_draft_is_immutable_reference_not_approval(self):
        narration = (EVAL / 'e001_reference_en.txt').read_bytes()
        self.assertEqual(hashlib.sha256(narration).hexdigest(), self.fixture['reference_sha256'])
        self.assertEqual(self.fixture['status'], 'EDITORIAL_REFERENCE_NOT_PRODUCTION_APPROVAL')
        self.assertTrue(narration.decode().startswith('Two full shopping carts.'))
        self.assertTrue(narration.decode().rstrip().endswith("Now imagine you're back at the checkout..."))
        self.assertEqual(self.fixture['live_review'], 'UNVERIFIED')

    def test_queue_completion_times(self):
        model = self.fixture['model']
        for lane in ('A', 'B'):
            time = 0
            events = []
            for items in model['items'][lane]:
                time += items * model['scan_seconds'] + model['payment_seconds']
                events.append(time)
            self.assertEqual(events, model['completion_seconds'][lane])
        self.assertEqual(model['completion_seconds']['B'][-1] - model['completion_seconds']['A'][-1], 14)

    def test_story_snapshots_match_completed_customers(self):
        model = self.fixture['model']
        for snapshot in self.fixture['snapshots']:
            for lane in ('A', 'B'):
                with self.subTest(time=snapshot['t'], lane=lane):
                    events = model['completion_seconds'][lane]
                    remaining = sum(t > snapshot['t'] for t in events)
                    self.assertEqual(remaining, snapshot['remaining'][lane])

    def test_last_basket_is_scanning_not_paying_at_74_seconds(self):
        model = self.fixture['model']
        start = model['completion_seconds']['B'][-2]
        scan_end = start + model['items']['B'][-1] * model['scan_seconds']
        self.assertLessEqual(start, 74)
        self.assertLess(74, scan_end)

    def test_explanation_matches_scan_saving_and_payment_penalty(self):
        model = self.fixture['model']
        scan_saving = (sum(model['items']['A']) - sum(model['items']['B'])) * model['scan_seconds']
        payment_penalty = (len(model['items']['B']) - len(model['items']['A'])) * model['payment_seconds']
        self.assertEqual(scan_saving, 22)
        self.assertEqual(payment_penalty, 36)
        self.assertEqual(payment_penalty - scan_saving, 14)

    def test_eval_cases_cover_failure_modes_without_fabricated_results(self):
        data = json.loads((EVAL / 'cases.json').read_text(encoding='utf-8'))
        self.assertEqual(data['execution_status'], 'NOT_RUN')
        cases = data['cases']
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        required = {'cold_open', 'causality', 'number_overload', 'missing_payoff',
                    'forced_loop', 'standalone_opening', 'invented_event',
                    'unsupported_guarantee', 'long_scope', 'valid_loop'}
        self.assertTrue(required.issubset({case['focus'] for case in cases}))
        for case in cases:
            self.assertTrue(case['input'])
            self.assertTrue(case['expected_observations'])
            self.assertNotIn('actual_result', case)


if __name__ == '__main__':
    unittest.main()
