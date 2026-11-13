"""Reject skipped concept work before accepting packaging or creating image tasks."""
import copy
import json
import os
import unittest

from test_release import payload
import test_workflow as workflow_fixture
from thumbnail_fixtures import plan_fixture
from ytvideos.errors import WorkflowError
from ytvideos.image_review import validate_plan
from ytvideos.release import ReleaseSpec


class ThumbnailPlanTests(unittest.TestCase):
    postgres = False

    def setUp(self):
        self.fixture = workflow_fixture.WorkflowContract()
        self.fixture.postgres = self.postgres
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service
        run = self.service.create('paper_detour', 'Synthetic long concept test', format='long',
                                  capabilities=self.fixture.run['capabilities'])
        self.fixture.run, self.fixture.run_id = run, run['id']
        self.run_id = run['id']
        self.fixture.production_ready()
        self.data = payload()
        self.data.update(run_id=self.run_id, channel_id=run['profile']['youtube_channel_id'])
        self.output = self.fixture.output(self.data)
        self.claim = self.service.claim(self.run_id, 'packaging', 'synthetic-package-worker')
        self.script = self.service._artifact(self.service.store.get(self.run_id), 'script')
        self.plan = plan_fixture(self.data, self.script['sha256'])

    def complete(self, plan):
        receipt = self.fixture.receipt('packaging', self.claim, self.output)
        data = json.loads(receipt.read_text())
        next(item for item in data['checks'] if item['name'] == 'thumbnail_plan')['observed'] = plan
        receipt.write_text(json.dumps(data))
        return self.service.complete(self.run_id, 'packaging', self.claim['token'], self.output, receipt, actual_units=0)

    def test_generic_pass_or_fewer_than_three_concepts_cannot_complete_long_packaging(self):
        for plan in ({'checked': True}, {**self.plan, 'concepts': self.plan['concepts'][:1]},
                     {**self.plan, 'concepts': self.plan['concepts'][:2]}):
            with self.subTest(plan=plan), self.assertRaises(WorkflowError):
                self.complete(plan)
        self.assertEqual(self.service.store.get(self.run_id)['tasks']['packaging']['outputs'], [])

    def test_incomplete_concepts_metadata_and_literal_duplicate_promises_are_rejected(self):
        for field in ('description', 'prompt', 'visual_intent', 'promise', 'first_confirmation',
                      'payoff', 'false_reading', 'overlay_text', 'intro_connection'):
            plan = copy.deepcopy(self.plan)
            plan['concepts'][1].pop(field)
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                self.complete(plan)
        for field, value in [('title', 'Not the selected title'), ('description', 'Not the description')]:
            plan = copy.deepcopy(self.plan)
            plan['concepts'][0][field] = value
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                self.complete(plan)
        plan = copy.deepcopy(self.plan)
        plan['concepts'][1]['promise'] = '  ' + plan['concepts'][0]['promise'].upper() + ' \n'
        with self.assertRaisesRegex(WorkflowError, 'repeat the same promise'):
            self.complete(plan)

    def test_stale_script_missing_selection_duplicate_ids_and_no_intro_are_rejected(self):
        variants = [{**self.plan, 'script_sha256': '0' * 64}, {**self.plan, 'selected_id': 'unknown'}]
        for mutate in ('id', 'intro_connection'):
            plan = copy.deepcopy(self.plan)
            if mutate == 'id':
                plan['concepts'][1]['id'] = plan['concepts'][0]['id']
            else:
                for concept in plan['concepts']:
                    concept['intro_connection'] = ''
            variants.append(plan)
        for plan in variants:
            with self.subTest(plan=plan), self.assertRaises(WorkflowError):
                self.complete(plan)

    def test_valid_plan_is_persisted_and_exact_concept_reaches_the_image_task(self):
        self.assertEqual(self.complete(self.plan)['status'], 'complete')
        concept = self.plan['concepts'][1]
        brief = {'id': concept['id'], 'title': concept['title'], 'prompt': concept['prompt'],
                 'visual_intent': concept['visual_intent'],
                 'reference_na_reason': 'Synthetic routing fixture has no artistic reference.'}
        task = self.service.add_thumbnail_task(self.run_id, brief)
        self.assertEqual(task['payload']['concept'], concept)
        context = self.service.context(self.run_id, task['id'])
        self.assertEqual(context['task']['payload']['concept'], concept)
        for patch in ({'id': 'invented'}, {'title': 'Another title'}, {'concept': {'id': 'invented'}}):
            with self.subTest(patch=patch), self.assertRaises(WorkflowError):
                self.service.add_thumbnail_task(self.run_id, {**brief, **patch})
        # A technical prompt correction keeps the same semantic concept; no new human gate.
        task = self.service.add_thumbnail_task(self.run_id, {**brief, 'prompt': 'Larger synthetic focal point'})
        self.assertEqual(task['payload']['concept'], concept)

    def test_short_needs_one_concept_not_an_invented_ab_experiment(self):
        data = {**self.data, 'format': 'short'}
        data.pop('end_screen')
        plan = plan_fixture(data, self.script['sha256'])
        self.assertEqual(len(validate_plan(plan, spec=ReleaseSpec.from_dict(data),
                                          script_sha256=self.script['sha256'])), 1)


@unittest.skipUnless(os.environ.get('YTV_TEST_POSTGRES_URL'), 'YTV_TEST_POSTGRES_URL is not configured')
class PostgreSQLThumbnailPlanTests(ThumbnailPlanTests):
    postgres = True
