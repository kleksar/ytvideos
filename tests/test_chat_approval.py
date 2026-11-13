import unittest
from datetime import datetime, timezone
from uuid import uuid4

import test_workflow
from ytvideos.errors import Conflict, WorkflowError


class ChatApproval(unittest.TestCase):
    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.fixture.script_ready()
        self.service = self.fixture.service
        self.service.approvals.public_key = None

    def event(self):
        run = self.service.store.get(self.fixture.run_id)
        artifact = self.service.next(run['id'])['approval_requests'][0]['artifact']
        thread, message = str(uuid4()), str(uuid4())
        return {'event': {'event_id': f'chat:{thread}:{message}', 'actor': 'user', 'source': 'chat',
                          'run_id': run['id'], 'kind': 'script', 'artifact_id': artifact['id'],
                          'sha256': artifact['sha256'], 'created_at': datetime.now(timezone.utc).isoformat(),
                          'scope': 'produce_video', 'revision': run['revision']},
                'chat': {'thread_id': thread, 'message_id': message, 'text': 'Confirmed. Make the video.'}}

    def test_chat_opens_production_once_without_a_key(self):
        envelope = self.event()
        self.service.approve(envelope)
        self.service.approve(envelope)
        result = self.service.next(self.fixture.run_id)
        self.assertEqual({t['id'] for t in result['tasks']}, {'storyboard', 'audio', 'packaging'})
        events = [e for e in self.fixture.store.events(self.fixture.run_id) if e['kind'] == 'user.approved']
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['payload']['chat'], envelope['chat'])

    def test_changed_bytes_and_revision_are_rejected(self):
        envelope = self.event()
        envelope['event']['sha256'] = '0' * 64
        with self.assertRaises(Conflict):
            self.service.approve(envelope)
        envelope = self.event()
        self.service.revise(self.fixture.run_id, 'script', 'new version')
        self.fixture.complete('script', test_workflow.SCRIPT)
        with self.assertRaisesRegex(Conflict, 'revision'):
            self.service.approve(envelope)

    def test_missing_message_and_non_user_actor_are_rejected(self):
        for field in ('text', 'message_id', 'thread_id'):
            envelope = self.event()
            envelope['chat'].pop(field)
            with self.assertRaises(WorkflowError):
                self.service.approve(envelope)
        envelope = self.event()
        envelope['event']['actor'] = 'assistant'
        with self.assertRaises(WorkflowError):
            self.service.approve(envelope)

    def test_mp4_acceptance_does_not_authorize_publication(self):
        self.service.approve(self.event())
        run = self.service.store.get(self.fixture.run_id)
        run['tasks']['render']['status'] = 'complete'
        run['tasks']['render']['outputs'] = ['fixture-mp4']
        run['approvals']['mp4'] = {'artifact_id': 'fixture-mp4', 'revision': run['revision'], 'scope': 'accept_mp4'}
        with self.assertRaisesRegex(WorkflowError, 'explicit user release'):
            self.service._publication_guard(run, 'upload')
