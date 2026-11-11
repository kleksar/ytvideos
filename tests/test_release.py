from datetime import datetime, timedelta, timezone
import unittest

from ytvideos.release import (ReadbackReceipt, ReleaseError, ReleasePolicy, ReleaseSpec,
                             guard_write, prepare_release_plan, requirement_matrix, validate_receipts)


NOW = datetime(2030, 1, 1, tzinfo=timezone.utc)
CHANNEL = 'UC' + 'x' * 22
VIDEO = 'abc123_XY-z'
POLICY = ReleasePolicy(end_screen=True, ab_test=True, shorts_related=True)


def payload():
    return {
        'run_id': 'episode-1', 'revision': 1, 'channel_id': CHANNEL,
        'format': 'long', 'has_speech': True,
        'metadata': {
            'title': 'A complete story', 'description': 'A factual description.',
            'tags': ['history', 'a story'], 'category_id': '27', 'language': 'en', 'audio_language': 'en',
            'made_for_kids': False, 'contains_synthetic_media': True, 'license': 'youtube',
            'age_restricted': False, 'paid_promotion': False,
        },
        'media_sha256': 'a' * 64, 'duration_seconds': 90,
        'publish_at': (NOW + timedelta(days=1)).isoformat(),
        'thumbnail_sha256': 'b' * 64, 'caption': {'sha256': 'c' * 64, 'language': 'en'},
        'playlist_na_reason': 'No suitable playlist after checking the channel inventory.',
        'end_screen': {'start_seconds': 80, 'end_seconds': 90,
                       'elements': [{'type': 'subscribe', 'target_id': CHANNEL},
                                    {'type': 'video', 'target_id': 'xyz123_XY-z'}]},
    }


def receipt(spec, requirement, **overrides):
    value = {'key': requirement.key, 'channel_id': CHANNEL, 'video_id': VIDEO,
             'release_sha256': spec.sha256,
             'method': 'studio_readback' if requirement.provider == 'studio' else 'api_readback',
             'observation_id': 'readback-123', 'evidence_sha256': 'd' * 64,
             'observed_at': NOW.isoformat(), 'observed_value': requirement.expected}
    return ReadbackReceipt.from_dict({**value, **overrides})


def receipts(spec, phase='pre_schedule'):
    return tuple(receipt(spec, r) for r in requirement_matrix(spec, POLICY) if r.applicable and r.phase == phase)


def grant(spec):
    return {'run_id': spec.run_id, 'channel_id': spec.channel_id, 'media_sha256': 'a' * 64,
            'release_sha256': spec.sha256, 'approval_event_id': 'chat-message-100',
            'operation_id': 'op-100', 'action': 'schedule'}


class ReleaseTests(unittest.TestCase):
    def test_preparation_does_not_require_approval_and_does_not_claim_publication(self):
        data = payload()
        del data['media_sha256']
        del data['publish_at']
        result = prepare_release_plan(ReleaseSpec.from_dict(data), POLICY, now=NOW)
        self.assertIn('Missing media_sha256', result['blockers'])
        self.assertIn('Missing publish_at', result['blockers'])
        self.assertEqual(result['status'], 'prepared_not_published')
        self.assertNotIn('approved', result)

    def test_snapshot_cannot_be_changed_by_caller(self):
        data = payload()
        spec = ReleaseSpec.from_dict(data)
        digest = spec.sha256
        data['metadata']['title'] = 'Changed'
        restored = spec.to_dict()
        restored['metadata']['title'] = 'Changed again'
        self.assertEqual(spec.sha256, digest)
        self.assertEqual(spec.to_dict()['metadata']['title'], 'A complete story')

    def test_strict_booleans_and_revisions(self):
        for key in ('made_for_kids', 'contains_synthetic_media', 'age_restricted', 'paid_promotion'):
            for invalid in ('false', 0, None):
                with self.subTest(key=key, invalid=invalid):
                    data = payload()
                    data['metadata'][key] = invalid
                    with self.assertRaises(ReleaseError):
                        ReleaseSpec.from_dict(data)
        for invalid in (True, 1.0, '1', 0):
            data = payload()
            data['revision'] = invalid
            with self.assertRaises(ReleaseError):
                ReleaseSpec.from_dict(data)

    def test_missing_or_unknown_metadata_fields_rejected(self):
        for patch in ({'privacy': 'public'}, {'tags': []}, {'license': True}, {'language': ''}, {'title': '<bad>'}):
            data = payload()
            data['metadata'].update(patch)
            with self.assertRaises(ReleaseError):
                ReleaseSpec.from_dict(data)
        data = payload()
        del data['metadata']['made_for_kids']
        with self.assertRaises(ReleaseError):
            ReleaseSpec.from_dict(data)

    def test_tags_use_quoted_multiterm_length(self):
        data = payload()
        data['metadata']['tags'] = ['a ' * 249 + 'b']  # 499 chars + quoted overhead.
        with self.assertRaises(ReleaseError):
            ReleaseSpec.from_dict(data)

    def test_schedule_is_aware_normalized_and_future(self):
        data = payload()
        data['publish_at'] = '2030-01-02T02:00:00+02:00'
        spec = ReleaseSpec.from_dict(data)
        self.assertEqual(spec.to_dict()['publish_at'], '2030-01-02T00:00:00Z')
        self.assertFalse(prepare_release_plan(spec, POLICY, now=NOW)['blockers'])
        data['publish_at'] = '2030-01-02T00:00:00'
        with self.assertRaises(ReleaseError):
            ReleaseSpec.from_dict(data)
        data['publish_at'] = (NOW + timedelta(minutes=5)).isoformat()
        self.assertIn('Schedule is not safely in the future',
                      prepare_release_plan(ReleaseSpec.from_dict(data), POLICY, now=NOW)['blockers'])

    def test_na_reason_required_and_unavailable_capability_is_not_na(self):
        data = payload()
        del data['playlist_na_reason']
        result = prepare_release_plan(ReleaseSpec.from_dict(data), POLICY, now=NOW,
                                      capabilities={'api': True, 'studio': False})
        self.assertIn('Missing N/A reason for playlist', result['blockers'])
        self.assertTrue(any('studio for end_screen' in x for x in result['blockers']))
        end = next(x for x in result['requirements'] if x['key'] == 'end_screen')
        self.assertTrue(end['applicable'])

    def test_ab_is_after_publish_and_does_not_block_scheduling(self):
        spec = ReleaseSpec.from_dict(payload())
        result = prepare_release_plan(spec, POLICY, now=NOW)
        self.assertFalse(result['blockers'])
        ab = next(x for x in result['requirements'] if x['key'] == 'ab_test')
        self.assertEqual(ab['phase'], 'after_publish')
        self.assertTrue(ab['applicable'])
        self.assertIn('Unverified saved value: ab_test', validate_receipts(spec, POLICY, (), video_id=VIDEO, phase='after_publish'))

    def test_shorts_have_thumbnail_and_related_but_no_ab_or_end_screen(self):
        data = payload()
        data['format'] = 'short'
        del data['end_screen']
        data['related_video_id'] = 'xyz123_XY-z'
        spec = ReleaseSpec.from_dict(data)
        matrix = {x.key: x for x in requirement_matrix(spec, POLICY)}
        self.assertTrue(matrix['thumbnail'].applicable)
        self.assertTrue(matrix['related_video'].applicable)
        self.assertFalse(matrix['ab_test'].applicable)
        self.assertFalse(matrix['end_screen'].applicable)
        self.assertFalse(prepare_release_plan(spec, POLICY, now=NOW)['blockers'])

    def test_kids_and_short_duration_ineligible_without_changing_audience(self):
        data = payload()
        del data['end_screen']
        data['metadata']['made_for_kids'] = True
        matrix = {x.key: x for x in requirement_matrix(ReleaseSpec.from_dict(data), POLICY)}
        self.assertFalse(matrix['ab_test'].applicable)
        self.assertFalse(matrix['end_screen'].applicable)
        self.assertTrue(matrix['made_for_kids'].expected)
        data['metadata']['made_for_kids'] = False
        data['duration_seconds'] = 24
        matrix = {x.key: x for x in requirement_matrix(ReleaseSpec.from_dict(data), POLICY)}
        self.assertFalse(matrix['end_screen'].applicable)

    def test_end_screen_is_native_configuration_not_only_outro(self):
        for start, stop in ((60, 70), (89, 90), (70, 91)):
            data = payload()
            data['end_screen'].update(start_seconds=start, end_seconds=stop)
            with self.assertRaises(ReleaseError):
                ReleaseSpec.from_dict(data)
        spec = ReleaseSpec.from_dict(payload())
        values = list(receipts(spec))
        i = next(i for i, x in enumerate(values) if x.key == 'end_screen')
        requirement = next(x for x in requirement_matrix(spec, POLICY) if x.key == 'end_screen')
        values[i] = receipt(spec, requirement, method='api_readback')
        self.assertIn('Unverified saved value: end_screen', validate_receipts(spec, POLICY, tuple(values), video_id=VIDEO))

    def test_all_applicable_receipts_bind_saved_values(self):
        spec = ReleaseSpec.from_dict(payload())
        self.assertEqual(validate_receipts(spec, POLICY, receipts(spec), video_id=VIDEO), ())
        self.assertIn('Unverified saved value: publish_at', validate_receipts(spec, POLICY, receipts(spec), video_id=VIDEO, phase='scheduled'))
        all_receipts = receipts(spec) + receipts(spec, 'scheduled')
        self.assertEqual(validate_receipts(spec, POLICY, all_receipts, video_id=VIDEO, phase='scheduled'), ())

    def test_changed_title_wrong_channel_and_wrong_revision_invalidate_receipts(self):
        spec = ReleaseSpec.from_dict(payload())
        title = next(x for x in requirement_matrix(spec, POLICY) if x.key == 'title')
        for patch in ({'channel_id': 'UC' + 'y' * 22}, {'release_sha256': 'f' * 64},
                      {'observed_value': 'Different title'}, {'video_id': 'xyz123_XY-z'}):
            values = tuple(x for x in receipts(spec) if x.key != 'title') + (receipt(spec, title, **patch),)
            self.assertIn('Unverified saved value: title', validate_receipts(spec, POLICY, values, video_id=VIDEO))

    def test_boolean_coercion_cannot_pass_observed_values(self):
        spec = ReleaseSpec.from_dict(payload())
        item = next(x for x in requirement_matrix(spec, POLICY) if x.key == 'made_for_kids')
        values = tuple(x for x in receipts(spec) if x.key != item.key) + (receipt(spec, item, observed_value=0),)
        self.assertIn('Unverified saved value: made_for_kids', validate_receipts(spec, POLICY, values, video_id=VIDEO))

    def test_generic_receipt_assertion_is_not_evidence(self):
        spec = ReleaseSpec.from_dict(payload())
        item = requirement_matrix(spec, POLICY)[0]
        for value in ('PASS', 'true', True):
            with self.assertRaises(ReleaseError):
                receipt(spec, item, observation_id=value)
        with self.assertRaises(ReleaseError):
            validate_receipts(spec, POLICY, ({'accepted': True},), video_id=VIDEO)

    def test_captions_must_be_manual_serving_and_not_draft(self):
        spec = ReleaseSpec.from_dict(payload())
        cap = next(x for x in requirement_matrix(spec, POLICY) if x.key == 'captions')
        for patch in ({'status': 'syncing'}, {'isDraft': True}, {'trackKind': 'ASR'}):
            changed = {**cap.expected, **patch}
            values = tuple(x for x in receipts(spec) if x.key != 'captions') + (receipt(spec, cap, observed_value=changed),)
            self.assertIn('Unverified saved value: captions', validate_receipts(spec, POLICY, values, video_id=VIDEO))

    def test_guard_requires_reserved_operation_and_exact_verified_binding(self):
        spec = ReleaseSpec.from_dict(payload())
        guard_write(spec, grant(spec), action='schedule', operation_state='reserved', policy=POLICY, now=NOW)
        for state in ('unknown', 'pending', 'confirmed', 'new'):
            with self.assertRaises(ReleaseError):
                guard_write(spec, grant(spec), action='schedule', operation_state=state, policy=POLICY, now=NOW)
        for patch in ({'media_sha256': 'f' * 64}, {'channel_id': 'UC' + 'y' * 22},
                      {'action': 'upload'}, {'approval_event_id': ''}):
            with self.assertRaises(ReleaseError):
                guard_write(spec, {**grant(spec), **patch}, action='schedule', operation_state='reserved', policy=POLICY, now=NOW)
        with self.assertRaises(ReleaseError):
            guard_write(spec, {**grant(spec), 'action': 'publish_public'}, action='publish_public',
                        operation_state='reserved', policy=POLICY, now=NOW)


if __name__ == '__main__':
    unittest.main()
