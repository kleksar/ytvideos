"""Offline Fusion-shaped fakes; no app, media, or real expression evaluation."""
import importlib.util
from pathlib import Path
import re
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location("branded_native_test", Path(__file__).with_name("branded_native.py"))
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


native.require = require


class Control:
    def __init__(self):
        self.expression = None

    def SetExpression(self, value):
        self.expression = value
        return None

    def GetExpression(self): return self.expression

    def sample(self, frame, default=None):
        if self.expression is None:
            return default
        parts = re.fullmatch(r"iif\(time >= (-?\d+) and time < (-?\d+), ([\d.]+), ([\d.]+)\)", self.expression)
        if not parts:
            raise AssertionError(f"Unexpected expression: {self.expression}")
        first, last, inside, outside = parts.groups()
        return float(inside if int(first) <= frame < int(last) else outside)


class Output:
    def __init__(self, tool):
        self.tool = tool

    def GetTool(self): return self.tool


class Inlet:
    def __init__(self, tool, name):
        self.tool, self.name = tool, name

    def GetConnectedOutput(self):
        tool = self.tool.connections.get(self.name)
        return Output(tool) if tool else None


class Tool:
    def __init__(self, kind, name=None):
        self.kind = kind
        self.name = name
        self.inputs = {}
        self.connections = {}
        for key in ("Input", "Foreground", "Background", "EffectMask"):
            setattr(self, key, Inlet(self, key))
        for key in ("Red1", "Green1", "Blue1", "Blend", "Alpha1"):
            setattr(self, key, Control())

    def SetAttrs(self, attrs):
        self.name = attrs["TOOLS_Name"]

    def GetAttrs(self): return {"TOOLS_Name": self.name, "TOOLS_RegID": self.kind}
    def SetInput(self, key, value, time=None): self.inputs[key] = value

    def GetInput(self, key, time=None):
        control = getattr(self, key, None)
        default = self.inputs.get(key)
        return control.sample(time, default) if time is not None and isinstance(control, Control) else default

    def ConnectInput(self, key, tool):
        self.connections[key] = tool
        return True


class Comp:
    def __init__(self, save):
        self.tools = [Tool("MediaOut", "MediaOut1")]
        self.locked = False
        self.save = save
        self.paths = []

    def Lock(self): self.locked = True
    def Unlock(self): self.locked = False

    def AddTool(self, kind, _x, _y):
        assert self.locked
        tool = Tool(kind)
        self.tools.append(tool)
        return tool

    def FindTool(self, name):
        return next((tool for tool in self.tools if tool.name == name), None)

    def GetToolList(self, *_):
        return dict(enumerate(self.tools))

    def Save(self, path):
        self.paths.append(path)
        return self.save


class Item:
    def __init__(self, *, save=True, import_ok=True, load_ok=True):
        self.graph = Comp(save)
        self.import_ok, self.load_ok = import_ok, load_ok
        self.operations = []
        self.names = []

    def AddFusionComp(self):
        self.operations.append("add")
        self.names.append("created")
        return self.graph

    def ImportFusionComp(self, path):
        self.operations.append(("import", path))
        if self.import_ok:
            self.names.append("imported")
            return self.graph

    def GetFusionCompNameList(self): return list(self.names)

    def LoadFusionCompByName(self, name):
        self.operations.append(("load", name))
        return self.graph if self.load_ok else None


RECIPE = {"raster": [1920,1080], "native_size": .048, "native_outline": .006,
          "font": {"family": "Georgia", "style": "Bold"},
          "neutral": "#F0ECDD", "active": "#F2C510", "outline": "#23123172"}


def shot(first, last, active):
    return {"nodes": [
        {"name": "word_000_New", "index": 0, "text": "New", "x": .44, "y": .14, "first": first, "last": last,
         "active_first": active[0], "active_last": active[1]},
        {"name": "word_001_York", "index": 1, "text": "York", "x": .56, "y": .14, "first": first, "last": last,
         "active_first": None, "active_last": None},
    ]}


class BrandedNativeTests(unittest.TestCase):
    def setUp(self):
        from types import SimpleNamespace
        self.fonts = {"Georgia": {"Bold": "/synthetic/Georgia Bold.ttf"}}
        native.resolve = SimpleNamespace(Fusion=lambda: SimpleNamespace(
            FontManager=SimpleNamespace(GetFontList=lambda: self.fonts)))

    def test_missing_required_native_font_stops_before_comp_mutation(self):
        self.fonts["Georgia"] = {"Regular": "/synthetic/Georgia.ttf"}
        item = Item()
        with self.assertRaisesRegex(RuntimeError, "font face unavailable"):
            native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")
        self.assertEqual(item.operations, [])

    def test_exact_bounds_and_distinct_editable_words(self):
        item = Item()
        result = native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")
        self.assertEqual(item.operations, ["add", ("import","owned.comp"), ("load","imported")])
        self.assertFalse(item.graph.locked)
        self.assertEqual(item.graph.paths, ["owned.comp"])
        self.assertEqual(result["words"], 2)
        self.assertEqual(result["visual"], "UNVERIFIED")
        words = [tool for tool in item.graph.tools if tool.kind == "TextPlus"]
        self.assertEqual([tool.GetInput("StyledText",0) for tool in words], ["New","York"])
        self.assertIsNot(words[0], words[1])
        self.assertEqual([tool.GetInput("Font",0) for tool in words], ["Georgia","Georgia"])
        merges = [tool for tool in item.graph.tools if tool.kind == "Merge"]
        for i, merge in enumerate(merges):
            self.assertIs(merge.connections["Foreground"], words[i])
            self.assertEqual([merge.Blend.sample(t) for t in (3,4,9,10)], [0,1,1,0])
        self.assertIs(item.graph.FindTool("MediaOut1").connections["Input"], merges[-1])
        bg = next(tool for tool in item.graph.tools if tool.kind == "Background")
        self.assertEqual(bg.GetInput("TopLeftAlpha"), 0)
        for i, channel in enumerate(("Red1","Green1","Blue1")):
            neutral = native.color_parts(RECIPE["neutral"])[i]
            active = native.color_parts(RECIPE["active"])[i]
            self.assertEqual([words[0].GetInput(channel,t) for t in (4,5,7,8)], [neutral,active,active,neutral])
            self.assertIsNone(getattr(words[1],channel).GetExpression())
            self.assertEqual(words[1].GetInput(channel,6), neutral)

    def test_split_phrase_preserves_positions_and_neutral_hold(self):
        before, after = Item(), Item()
        native.author_caption_comp(before, shot(4,8,(5,8)), RECIPE, "first.comp")
        native.author_caption_comp(after, shot(0,6,(None,None)), RECIPE, "second.comp")
        for identity, x in (("word_000_New",.44), ("word_001_York",.56)):
            a, b = before.graph.FindTool(identity), after.graph.FindTool(identity)
            self.assertEqual(a.GetInput("Center",0), {1:x,2:.14})
            self.assertEqual(a.GetInput("Center",0), b.GetInput("Center",0))
            self.assertEqual(a.GetInput("StyledText",0), b.GetInput("StyledText",0))
            self.assertIsNone(b.Red1.GetExpression())

    def test_failed_import_or_activation_cannot_return_visual_status(self):
        for settings, pattern in (({"import_ok":False},"reimport"), ({"load_ok":False},"activate")):
            with self.subTest(settings=settings):
                item = Item(**settings)
                with self.assertRaisesRegex(RuntimeError, pattern):
                    native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")
                self.assertFalse(item.graph.locked)

    def test_reimport_checks_serialized_highlight_neutral_outline_raster_and_phrase(self):
        def change(comp, node, key, value):
            tool = comp.FindTool(node)
            control = getattr(tool, key, None)
            if isinstance(control, Control) and (value is None or isinstance(value, str)):
                control.SetExpression(value)
            else:
                tool.SetInput(key, value)

        failures = (
            ("word_000_New", "Red1", None, "highlight"),
            ("word_000_New", "Green1", "iif(time >= 7 and time < 8, 1, 0)", "highlight"),
            ("word_001_York", "Blue1", .02, "neutral"),
            ("word_001_York", "Blue1", "iif(time >= 7 and time < 8, 1, 0)", "neutral"),
            ("word_001_York", "Alpha2", .9, "Alpha2"),
            ("word_001_York", "Width", 1280, "Width"),
            ("Display0", "Blend", None, "phrase timing"),
        )
        for node, key, value, pattern in failures:
            with self.subTest(node=node, key=key, value=value):
                item = Item()
                perform_import = item.ImportFusionComp

                def corrupted_import(path):
                    comp = perform_import(path)
                    change(comp, node, key, value)
                    return comp

                item.ImportFusionComp = corrupted_import
                with self.assertRaisesRegex(RuntimeError, pattern):
                    native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")
                self.assertIn(("load","imported"), item.operations)
                self.assertFalse(item.graph.locked)

    def test_reimport_rejects_invisible_or_rewired_topology_and_background(self):
        failures = (
            (lambda c: c.FindTool("MediaOut1").connections.clear(), "connection differs: Input"),
            (lambda c: c.FindTool("Display0").ConnectInput("Foreground", c.FindTool("word_001_York")),
             "connection differs: Foreground"),
            (lambda c: c.FindTool("Display1").ConnectInput("Background", c.FindTool("CaptionBackground")),
             "connection differs: Background"),
            (lambda c: c.FindTool("CaptionBackground").SetInput("TopLeftAlpha", 1), "background differs: TopLeftAlpha"),
            (lambda c: c.FindTool("CaptionBackground").SetInput("Height", 720), "background differs: Height"),
        )
        for corrupt, pattern in failures:
            with self.subTest(pattern=pattern):
                item = Item()
                perform_import = item.ImportFusionComp

                def corrupted_import(path):
                    graph = perform_import(path)
                    corrupt(graph)
                    return graph

                item.ImportFusionComp = corrupted_import
                with self.assertRaisesRegex(RuntimeError, pattern):
                    native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")

    def test_loaded_comp_not_merely_imported_proxy_gets_verified(self):
        item = Item()
        item.LoadFusionCompByName = lambda name: Comp(save=True)
        with self.assertRaisesRegex(RuntimeError, "topology"):
            native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")

    def test_ambiguous_new_comp_names_refuse_activation(self):
        item = Item()
        original_import = item.ImportFusionComp

        def ambiguous_import(path):
            graph = original_import(path)
            item.names.append("second-result")
            return graph

        item.ImportFusionComp = ambiguous_import
        with self.assertRaisesRegex(RuntimeError, "identify"):
            native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")
        self.assertNotIn(("load","imported"), item.operations)

    def test_import_replacing_sole_comp_activates_and_verifies_that_name(self):
        item = Item()

        def replace(path):
            item.operations.append(("import", path))
            return item.graph

        item.ImportFusionComp = replace
        result = native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")
        self.assertEqual(item.operations, ["add", ("import","owned.comp"), ("load","created")])
        self.assertEqual(result["visual"], "UNVERIFIED")

    def test_editable_history_panel_and_corrupted_native_readback(self):
        recipe = dict(RECIPE, panel={"color":"#20252BCC"})
        section = shot(4,10,(5,8))
        section["panels"] = [dict(name="Panel0", x=.5, y=.14, width=.3, height=.1, first=4, last=10)]
        item = Item()
        result = native.author_caption_comp(item, section, recipe, "owned.comp")
        self.assertEqual(result["visual"], "UNVERIFIED")
        panel = item.graph.FindTool("Panel0")
        mask = item.graph.FindTool("Panel0Mask")
        display = item.graph.FindTool("Panel0Display")
        self.assertEqual(panel.GetInput("TopLeftAlpha"), 204/255)
        self.assertIs(panel.connections["EffectMask"], mask)
        self.assertEqual(mask.GetInput("Center"), {1:.5,2:.14})
        self.assertEqual([display.Blend.sample(frame) for frame in (3,4,9,10)], [0,1,1,0])
        self.assertIs(item.graph.FindTool("Display0").connections["Background"], display)
        for corrupt, pattern in (
            (lambda c: c.FindTool("Panel0").SetInput("TopLeftAlpha",1), "panel color/raster"),
            (lambda c: c.FindTool("Panel0Mask").SetInput("Width",.8), "panel geometry"),
            (lambda c: c.FindTool("Panel0").connections.pop("EffectMask"), "EffectMask"),
            (lambda c: c.FindTool("Panel0Display").connections.pop("Foreground"), "Foreground"),
        ):
            with self.subTest(pattern=pattern):
                item = Item()
                perform_import = item.ImportFusionComp

                def broken_import(path):
                    graph = perform_import(path)
                    corrupt(graph)
                    return graph

                item.ImportFusionComp = broken_import
                with self.assertRaisesRegex(RuntimeError, pattern):
                    native.author_caption_comp(item, section, recipe, "owned.comp")

    def test_existing_srt_candidate_is_read_back_without_new_duplicate_or_import(self):
        resolve, manager, project, base, candidate = [Mock() for _ in range(5)]
        before = {"timecode": "01:00:01:00", "page": "edit"}
        resolve.Fusion().FontManager.GetFontList.return_value = self.fonts
        base.GetTrackCount.return_value = 1
        project.GetTimelineCount.return_value = 1
        project.GetTimelineByIndex.return_value = candidate
        candidate.GetName.return_value = 'candidate'
        candidate.GetMarkerByCustomData.return_value = {"name":"owned"}
        candidate.GetUniqueId.return_value = 'candidate-id'
        verifier=Mock()
        with patch.multiple(native, create=True, identity=Mock(return_value=(manager,project,base)),
                            snapshot=Mock(return_value=before), items=Mock(return_value=[]),
                            verify_branded=verifier):
            result=native.install_branded(resolve,{},before,{"recipe":dict(RECIPE,panel=None),"shots":[]},
                                          None,None,[],"candidate","token",[],"technical.mp4")
        self.assertEqual(result['status'],'UNCHANGED')
        self.assertEqual(result['candidate_id'],'candidate-id')
        verifier.assert_called_once()
        self.assertIsNone(verifier.call_args.args[5])
        base.DuplicateTimeline.assert_not_called()
        project.GetMediaPool.assert_not_called()

    def test_failed_timeline_restore_still_restores_playhead_and_page(self):
        resolve, manager, project, base, candidate = [Mock() for _ in range(5)]
        before = {"timecode": "01:00:01:00", "page": "edit"}
        recipe = dict(RECIPE, panel=None)
        resolve.Fusion().FontManager.GetFontList.return_value = self.fonts
        base.GetTrackCount.return_value = 1
        base.DuplicateTimeline.return_value = candidate
        project.GetTimelineCount.return_value = 0
        project.SetCurrentTimeline.side_effect = [False, RuntimeError("synthetic restoration failure")]
        with patch.multiple(native, create=True,
                            identity=Mock(return_value=(manager,project,base)),
                            snapshot=Mock(return_value=before),
                            items=Mock(return_value=[])):
            with self.assertRaisesRegex(RuntimeError, "Could not restore source view: timeline"):
                native.install_branded(resolve,{},before,{"recipe":recipe,"shots":[]},
                                       [],"owned.srt",[],"candidate","token",[])
        base.SetCurrentTimecode.assert_called_once_with(before["timecode"])
        resolve.OpenPage.assert_called_once_with(before["page"])
        candidate.SetTrackEnable.assert_not_called()  # No new lane was added yet.

    def test_failed_save_does_not_reimport_possible_stale_bytes(self):
        item = Item(save=False)
        with self.assertRaisesRegex(RuntimeError, "(?i)sav|serializ"):
            native.author_caption_comp(item, shot(4,10,(5,8)), RECIPE, "owned.comp")
        self.assertEqual(item.operations, ["add"])
        self.assertFalse(item.graph.locked)


if __name__ == "__main__":
    unittest.main()
