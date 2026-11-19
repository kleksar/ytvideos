"""Offline phrase checkpoint and exact readback checks."""
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).parent
native = {}
for name in ('native.py', 'branded_native.py', 'phrase_native.py'):
    exec(compile((SCRIPTS / name).read_text(), name, 'exec'), native)


class Markers:
    def __init__(self, *tokens):
        self.tokens = set(tokens)

    def GetMarkerByCustomData(self, token):
        return {'customData': token} if token in self.tokens else {}


class PhraseTests(unittest.TestCase):
    def test_progress_accepts_complete_prefix(self):
        self.assertEqual(native['_phrase_state'](Markers('t:pending:0', 't:done:0'), 't', 2), 1)

    def test_uncertain_app_state_refuses_resume(self):
        for markers in (
            Markers('t:pending:0'),
            Markers('t:pending:0', 't:done:0', 't:pending:1'),
            Markers('t:done:0'),
            Markers('t:done:1'),
        ):
            with self.subTest(tokens=markers.tokens), self.assertRaises(RuntimeError):
                native['_phrase_state'](markers, 't', 2)

    def test_graph_value_and_expression_are_both_exact(self):
        class Tool:
            expression = None
            value = 0.8

            def GetInput(self, key, frame):
                return self.value

            def GetExpression(self):
                return self.expression

        tool = Tool()
        tool.TopLeftAlpha = tool
        native['_phrase_inputs'](tool, {'TopLeftAlpha': 0.8})
        tool.expression = 'time > 0'
        with self.assertRaisesRegex(RuntimeError, 'expression'):
            native['_phrase_inputs'](tool, {'TopLeftAlpha': 0.8})
        tool.expression = None
        tool.value = 0.7
        with self.assertRaisesRegex(RuntimeError, 'does not match'):
            native['_phrase_inputs'](tool, {'TopLeftAlpha': 0.8})

    def test_visibility_and_full_span_required_for_readback(self):
        from unittest.mock import patch
        class Tool:
            def __init__(self, **inputs):
                self.inputs = inputs
                self.expressions = {}
            def GetInput(self, key, frame):
                return self.inputs.get(key)
            def __getattr__(self, key):
                class Input:
                    def GetExpression(_self):
                        return self.expressions.get(key)
                return Input()
        class Comp:
            attrs = dict(COMPN_GlobalStart=0, COMPN_GlobalEnd=37,
                         COMPN_RenderStart=0, COMPN_RenderEnd=37)
            def GetAttrs(self):
                return self.attrs
        row = dict(start_frame=924, end_frame=962)
        comp = Comp()
        word, panel = Tool(GlobalIn=0, GlobalOut=37), Tool(GlobalIn=0, GlobalOut=37)
        merge = Tool(Blend=1)
        guard = native['_phrase_visibility_span']
        guard(comp, word, panel, merge, row)
        # The same guard is run on every item readback before UNCHANGED is returned.
        for tool, key, bad in ((merge, 'Blend', 0), (word, 'GlobalOut', 20),
                               (panel, 'GlobalOut', 20), (word, 'GlobalIn', 1)):
            old = tool.inputs[key]
            tool.inputs[key] = bad
            with self.subTest(key=key), self.assertRaises(RuntimeError):
                guard(comp, word, panel, merge, row)
            tool.inputs[key] = old
        merge.expressions['Blend'] = 'time < 20'
        with self.assertRaisesRegex(RuntimeError, 'expression'):
            guard(comp, word, panel, merge, row)
        merge.expressions.clear()
        for key in comp.attrs:
            with patch.dict(comp.attrs, {key: None}), self.assertRaisesRegex(RuntimeError, 'span'):
                guard(comp, word, panel, merge, row)

    def test_native_media_reference_rejected_before_graph_read(self):
        class Item:
            def GetMediaPoolItem(self):
                return object()

        with self.assertRaisesRegex(RuntimeError, 'without media'):
            native['_phrase_verify_item'](Item(), {})

    def test_exact_nonzero_origin_staging_point(self):
        class Timeline:
            def GetStartTimecode(self):
                return '01:00:00:00'

            def GetSetting(self, name):
                return '30.0'

        target = {'origin_frame': 108000, 'end_frame': 108993}
        native['_phrase_staging_point'](Timeline(), target, '01:00:33:03')
        for tc in ('01:00:33:02', '01:00:33:04', '01:00:33;03', '00:00:33:03'):
            with self.subTest(timecode=tc), self.assertRaises(RuntimeError):
                native['_phrase_staging_point'](Timeline(), target, tc)

    def test_restore_and_checkpoint_prevent_duplicate_after_failed_insert(self):
        from unittest.mock import patch

        class Timeline(Markers):
            def __init__(self, name):
                super().__init__()
                self.name = name

            def GetName(self):
                return self.name

            def GetUniqueId(self):
                return self.name

            def GetSetting(self, _key):
                return '30'

            def GetStartTimecode(self):
                return '00:00:00:00'

            def SetCurrentTimecode(self, _tc):
                return True

            def GetStartFrame(self):
                return 0

            def GetEndFrame(self):
                return 60

            def GetTrackName(self, _kind, _lane):
                return 'Native phrase titles token'

            def GetIsTrackEnabled(self, _kind, _lane):
                return True

            def GetTrackCount(self, _kind):
                return 0

            def GetMarkers(self):
                return {i: {} for i, _token in enumerate(self.tokens)}

            def AddMarker(self, _frame, _color, _label, _notes, _duration, token):
                self.tokens.add(token)
                return True

            def InsertFusionTitleIntoTimeline(self, _title):
                self.insertions += 1
                return None

        class Project:
            def __init__(self):
                self.timeline = base

            def GetTimelineCount(self):
                return 1

            def GetTimelineByIndex(self, _index):
                return candidate

            def SetCurrentTimeline(self, timeline):
                self.timeline = timeline
                return True

            def SaveProject(self):
                return True

            def OpenPage(self, _page):
                return True

        base, candidate = Timeline('source'), Timeline('owned')
        candidate.tokens.add('token')
        candidate.insertions = 0
        project = Project()
        target = dict(origin_frame=0, end_frame=60, raster=[608, 1080])
        before = dict(timecode='00:00:00:00', page='edit', picture=[[]])
        layout = [dict(start_frame=0, end_frame=60, text='Phrase', style={'raster': [608, 1080]})]
        overrides = dict(identity=lambda *_: (project, project, base),
                         snapshot=lambda *_: before, content_signature=lambda *_: [[]],
                         _phrase_shape=lambda *_: None, _phrase_readback=lambda *_: [])
        with patch.dict(native, overrides):
            install = native['install_phrase_batch']
            args = (project, target, before, layout, ['example.comp'], 'owned', 'token', {},
                    '00:00:02:00', 0, 1)
            with self.assertRaisesRegex(RuntimeError, 'staging failed'):
                install(*args)
            self.assertIs(project.timeline, base)
            with self.assertRaisesRegex(RuntimeError, 'Uncertain title batch'):
                install(*args)
            self.assertIs(project.timeline, base)
            self.assertEqual(candidate.insertions, 1)

    def test_resize_staged_title_before_moving_to_crowded_lane(self):
        class Title:
            def __init__(self, start):
                self.start = start
                self.neighbor_duration = 40
                self.calls = []

            def GetMediaPoolItem(self):
                return None

            def GetStart(self):
                return self.start

            def GetDuration(self):
                return 150

            def GetRightOffset(self):
                return 0

            def SetRightOffset(self, offset, ripple, preserve):
                self.calls.append(('resize', offset, ripple, preserve))
                if self.start < 100:
                    self.neighbor_duration = 20
                return True

            def SetPosition(self, position, ripple):
                self.calls.append(('move', position, ripple))
                self.start = position['startFrame']
                return True

        row = {'start_frame': 20, 'end_frame': 60}
        staged = Title(100)
        native['_phrase_place'](staged, row, 3, 100)
        self.assertEqual(staged.calls, [
            ('resize', 110, False, False),
            ('move', {'trackIndex': 3, 'startFrame': 20}, False),
        ])
        self.assertEqual(staged.neighbor_duration, 40)

        active = Title(20)
        with self.assertRaisesRegex(RuntimeError, 'inside populated timeline'):
            native['_phrase_place'](active, row, 3, 100)
        self.assertEqual(active.calls, [])
        self.assertEqual(active.neighbor_duration, 40)
