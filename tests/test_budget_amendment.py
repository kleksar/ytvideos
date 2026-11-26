"""Budget amendments are owner-audited, atomic and do not dispatch media."""
from concurrent.futures import ThreadPoolExecutor
import contextlib
import io
import json
import os
import unittest
from unittest.mock import patch

import test_workflow
from ytvideos.cli import main
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.service import Production
from ytvideos.store import Store


class BudgetAmendmentTests(unittest.TestCase):
    postgres = False

    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.postgres = self.postgres
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.run_id = self.fixture.run_id
        self.service = self.new_service()

    def new_service(self):
        return Production(Store(self.fixture.db), self.fixture.directory / 'workspace', self.fixture.service.project,
                          clock=lambda: self.fixture.clock)

    def decision(self, **changes):
        return {'max_units': 6000, 'expected_version': self.fixture.store.get(self.run_id)['version'],
                'source': 'fixture://owner/budget-turn', 'message': 'Fixture owner permits a budget of 6000 units.',
                **changes}

    def test_amend_is_audited_without_changing_tasks_or_spending(self):
        before = self.fixture.store.get(self.run_id)
        result = self.service.amend_budget(self.run_id, **self.decision())
        after = self.fixture.store.get(self.run_id)
        self.assertEqual(result['previous_max_units'], 10)
        self.assertEqual(after['version'], before['version'] + 1)
        self.assertEqual(after['budget'], {**before['budget'], 'max_paid_units': 6000})
        for field in ('tasks', 'artifacts', 'approvals', 'pins', 'revision'):
            self.assertEqual(after[field], before[field])
        events = [e for e in self.fixture.store.events(self.run_id) if e['kind'] == 'budget.amended']
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['payload'], result)
        with self.fixture.store.transaction() as tx:
            self.assertEqual(tx.execute('SELECT COUNT(*) FROM operations').fetchone()[0], 0)

    def test_replay_same_decision_concurrently_is_idempotent(self):
        decision = self.decision()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.new_service().amend_budget(self.run_id, **decision), range(2)))
        self.assertEqual(results[0], results[1])
        self.assertEqual(self.fixture.store.get(self.run_id)['version'], decision['expected_version'] + 1)
        self.assertEqual(len([e for e in self.fixture.store.events(self.run_id) if e['kind'] == 'budget.amended']), 1)
        with self.assertRaisesRegex(Conflict, 'source'):
            self.service.amend_budget(self.run_id, **{**decision, 'max_units': 7000})

    def test_stale_decision_invalid_inputs_and_reservation_floor_are_atomic(self):
        def account(tx, run):
            run['budget'].update(spent=3, reserved=4, unknown_reserved=2)
        self.fixture.store.mutate(self.run_id, account)
        before = self.fixture.store.get(self.run_id)
        for change in ({'expected_version': before['version'] - 1}, {'max_units': 8}, {'max_units': -1},
                       {'max_units': True}, {'expected_version': True}, {'source': ''}, {'message': ' '}):
            with self.subTest(change=change), self.assertRaises(WorkflowError):
                self.service.amend_budget(self.run_id, **self.decision(**change))
            self.assertEqual(self.fixture.store.get(self.run_id), before)
        self.service.amend_budget(self.run_id, **self.decision(max_units=9))
        after = self.fixture.store.get(self.run_id)
        self.assertEqual((after['budget']['spent'], after['budget']['reserved'],
                          after['budget']['unknown_reserved']), (3, 4, 2))

    def test_wrong_pin_cancelled_and_signed_only_host_are_rejected(self):
        decision = self.decision()
        with patch('ytvideos.service.code_identity', return_value='wrong'), self.assertRaises(Conflict):
            self.service.amend_budget(self.run_id, **decision)
        with self.assertRaisesRegex(WorkflowError, 'signed-only'):
            self.fixture.service.amend_budget(self.run_id, **decision)
        self.service.cancel(self.run_id, 'fixture cancellation')
        with self.assertRaisesRegex(Conflict, 'cancelled'):
            self.service.amend_budget(self.run_id, **decision)

    def test_same_source_cannot_be_reused_for_another_run(self):
        decision = self.decision()
        self.service.amend_budget(self.run_id, **decision)
        other = self.service.create('paper_detour', 'other fixture')
        with self.assertRaisesRegex(Conflict, 'source'):
            self.service.amend_budget(other['id'], **decision)
        self.assertEqual(self.fixture.store.get(other['id'])['budget']['max_paid_units'], 0)

    def test_amendment_changes_claim_ceiling_but_reservation_still_applies(self):
        self.fixture.production_ready()
        with self.assertRaisesRegex(WorkflowError, 'paid budget exhausted'):
            self.service.claim(self.run_id, 'audio', 'fixture-worker', estimated_units=11)
        self.service.amend_budget(self.run_id, **self.decision(max_units=11))
        claim = self.service.claim(self.run_id, 'audio', 'fixture-worker', estimated_units=11)
        self.assertEqual(claim['estimated_units'], 11)
        self.assertEqual(self.fixture.store.get(self.run_id)['budget']['reserved'], 11)
        with self.assertRaisesRegex(Conflict, 'spent and reserved'):
            self.service.amend_budget(self.run_id, **self.decision(max_units=10, source='fixture://owner/lower'))

    def test_cli_and_budget_guard(self):
        run = self.fixture.store.get(self.run_id)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = main(['--db', self.fixture.db, '--workspace', str(self.fixture.directory / 'workspace'),
                           '--project-root', str(self.fixture.service.project), 'amend-budget', '--run', self.run_id,
                           '--max-units', '11', '--expected-version', str(run['version']),
                           '--source', 'fixture://cli', '--message', 'Fixture approval'])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(out.getvalue())['request']['max_units'], 11)
        self.assertEqual(self.fixture.store.get(self.run_id)['budget']['max_paid_units'], 11)


@unittest.skipUnless(os.environ.get('YTV_TEST_POSTGRES_URL'), 'isolated PostgreSQL not configured')
class PostgreSQLBudgetAmendmentTests(BudgetAmendmentTests):
    postgres = True


if __name__ == '__main__':
    unittest.main()
