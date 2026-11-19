"""Offline tests for picture-cut alignment of display, not speech cues."""
from copy import deepcopy
from pathlib import Path
import tempfile
from unittest import TestCase
from unittest.mock import Mock, patch

from layout import native_layout
from partition import partition_cues
from test_branded_native import native, RECIPE
from test_layout import Font
from test_planning import fixture, planning


def shots(cuts):
    return [dict(id=f"shot-{n}", carrier_id=f"carrier-{n}", start_frame=a, end_frame=b)
            for n, (a, b) in enumerate(zip(cuts, cuts[1:]))]


def states(section):
    return [(x['start_frame'], x['end_frame'], x['word_index']) for x in section['states']]


class Georgia(Font):
    def getname(self):
        return ('Georgia', 'Bold')


class CutAnchorTests(TestCase):
    def setUp(self):
        self.request = fixture()
        self.plan = planning.plan_subtitles(self.request)
        self.cues = self.plan['cues']
        self.origin = self.plan['target']['origin_frame']
        self.shots = shots([self.origin, 86432, 86434, 86454, 86490])
        self.anchor = dict(cue_id='C0002', shot_id='shot-1', start_frame=86432)

    def test_default_and_explicit_empty_unchanged(self):
        baseline = partition_cues(self.cues, self.shots)
        self.assertEqual(baseline, partition_cues(self.cues, self.shots, []))
        self.assertEqual(baseline[0]['sections'][-1]['start_frame'], 86430)
        self.assertFalse(any(shot.get('picture_cut_anchor') for shot in baseline))

    def test_two_frame_delay_holds_previous_neutrally_and_carries_highlight_across_cut(self):
        # Extend the synthetic first word to cover a second picture cut.
        self.cues[1]['words'][0]['end_frame'] = 86436
        self.cues[1]['spoken_end_frame'] = 86436
        self.shots = shots([self.origin, 86432, 86433, 86454, 86490])
        result = partition_cues(self.cues, self.shots, [self.anchor])
        previous = result[0]['sections'][-1]
        self.assertEqual(previous['cue_id'], 'C0001')
        self.assertEqual(states(previous)[-1], (86421, 86432, None))
        first, next_shot = result[1]['sections'][0], result[2]['sections'][0]
        self.assertEqual(states(first), [(86432,86433,2)])
        self.assertEqual(states(next_shot), [(86433,86436,2), (86436,86454,None)])
        self.assertEqual(first['words'], self.cues[1]['words'])
        self.assertEqual(next_shot['words'], self.cues[1]['words'])
        self.assertTrue(result[1]['picture_cut_anchor'])
        self.assertNotIn('picture_cut_anchor', result[2])

    def test_existing_display_gap_is_not_filled(self):
        self.cues[0]['end_frame'] = 86427
        result = partition_cues(self.cues, self.shots, [self.anchor])
        self.assertEqual(result[0]['sections'][-1]['end_frame'], 86427)
        self.assertEqual(result[1]['sections'][0]['start_frame'], 86432)

    def test_invalid_anchor_shapes_and_boundaries_fail(self):
        for anchors, pattern in (
            ([dict(self.anchor,start_frame=86432.0)], 'picture cut'),
            ([dict(self.anchor,start_frame=86431)], 'picture cut'),
            ([dict(self.anchor,shot_id='missing')], 'Unknown'),
            ([dict(self.anchor,cue_id='missing')], 'Unknown'),
            ([self.anchor,self.anchor], 'duplicate'),
            ([dict(self.anchor,shot_id='shot-3',start_frame=86454)], 'first spoken word'),
            ([dict(self.anchor,shot_id='shot-0',start_frame=self.origin)], 'first spoken word'),
            ([dict(self.anchor,shot_id='shot-1',start_frame=86436)], 'first spoken word'),
        ):
            if anchors[0]['start_frame'] == 86436:
                shot_records = shots([self.origin, 86436, 86454, 86490])
            else:
                shot_records = self.shots
            with self.subTest(anchors=anchors), self.assertRaisesRegex(ValueError, pattern):
                partition_cues(self.cues, shot_records, anchors)

    def test_layout_uses_display_anchor_but_preserves_plan_and_exact_srt(self):
        with tempfile.TemporaryDirectory() as temp:
            font = Path(temp) / 'Georgia Bold.ttf'
            font.write_bytes(b'synthetic')
            self.plan['style']['style']['font'] = str(font)
            anchors = [self.anchor]
            before = deepcopy((self.plan,self.shots,anchors))
            result = native_layout(self.plan,self.shots,'nuviko-history-long-native-v1',
                                   font_loader=lambda *a, **k: Georgia(), display_cut_anchors=anchors)
            self.assertEqual((self.plan,self.shots,anchors),before)
            first = result['shots'][1]['nodes'][0]
            self.assertEqual((first['first'],first['active_first']),(0,0))
            self.assertIn('00:00:01,000 --> 00:00:01,100\nwaits.',self.plan['srt'])

    def test_native_exact_cut_guard_leaves_unanchored_inner_sections_allowed(self):
        carrier = Mock()
        carrier.GetStart.return_value = 100
        with self.assertRaisesRegex(RuntimeError, 'not an actual carrier picture cut'):
            native.require_picture_cut(carrier, {'start_frame':125, 'picture_cut_anchor':True})
        native.require_picture_cut(carrier, {'start_frame':125})
        carrier.GetStart.return_value = 125
        native.require_picture_cut(carrier, {'start_frame':125, 'picture_cut_anchor':True})

    def test_native_preflight_rejects_virtual_shot_boundary_before_checkpoint(self):
        resolve, manager, project, base, carrier = [Mock() for _ in range(5)]
        resolve.Fusion().FontManager.GetFontList.return_value = {'Georgia':{'Bold':'synthetic'}}
        carrier.GetUniqueId.return_value = 'carrier-1'
        carrier.GetStart.return_value = 86431
        carrier.GetEnd.return_value = 86440
        shot = {**self.shots[1], 'picture_cut_anchor': True}
        before={}
        with patch.multiple(native,create=True,
                            identity=Mock(return_value=(manager,project,base)),
                            snapshot=Mock(return_value=before),items=Mock(return_value=[carrier])):
            with self.assertRaisesRegex(RuntimeError,'not an actual carrier picture cut'):
                native.install_branded(resolve,{},before,{'recipe':RECIPE,'shots':[shot]},
                                       [],'owned.srt',['owned.comp'],'candidate','token',[])
        manager.SaveProject.assert_not_called()
        base.DuplicateTimeline.assert_not_called()
