"""Offline Resolve-shaped fakes; no connection to the live app."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("resolve_subtitles_native_test", Path(__file__).with_name("native.py"))
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


class Media:
    def __init__(self, path):
        self.path = path

    def GetUniqueId(self): return "media-id:" + self.path
    def GetClipProperty(self, key): return self.path if key == "File Path" else None


class Item:
    def __init__(self, name, start, end, uid=None):
        self.name = name
        self.start = start
        self.end = end
        self.uid = uid or name
        self.moves = []
        self.media = Media(name)
        self.enabled = True
        self.properties = {"ZoomX": 1.0, "ZoomY": 1.0}

    def GetName(self): return self.name
    def GetUniqueId(self): return self.uid
    def GetStart(self): return self.start
    def GetEnd(self): return self.end
    def GetLeftOffset(self): return 0
    def GetRightOffset(self): return 0
    def GetClipEnabled(self): return self.enabled
    def GetProperty(self): return dict(self.properties)
    def GetSpeed(self): return {'Percentage':100}
    def GetMediaPoolItem(self): return self.media

    def SetPosition(self, settings, ripple):
        self.moves.append((dict(settings), ripple))
        self.end += settings["startFrame"] - self.start
        self.start = settings["startFrame"]
        return True


class Timeline:
    def __init__(self, app, name="SOURCE", uid="timeline-exact"):
        self.app = app
        self.name = name
        self.uid = uid
        self.cursor = "01:00:04:02"
        self.marker = {}
        self.tracks = {"audio": [[Item("audio.wav", 100, 190)]],
                       "video": [[Item("picture.mov", 100, 190)]],
                       "subtitle": [[Item("prior caption", 103, 109)]]}
        self.track_name = {"subtitle": {1: "Prior CC"}}
        self.track_enable = {"subtitle": {1: True}}

    def GetName(self): return self.name
    def GetUniqueId(self): return self.uid
    def GetStartFrame(self): return 100
    def GetEndFrame(self): return 190
    def GetStartTimecode(self): return "00:00:03:10"
    def GetCurrentTimecode(self): return self.cursor
    def GetTrackCount(self, kind): return len(self.tracks[kind])
    def GetItemListInTrack(self, kind, index):
        return self.tracks[kind][index - 1] if index <= len(self.tracks[kind]) else []

    def GetSetting(self, setting):
        return {"timelineFrameRate": "30", "timelineResolutionWidth": "1920",
                "timelineResolutionHeight": "1080"}.get(setting)

    def SetCurrentTimecode(self, timecode):
        self.cursor = timecode
        return True

    def DuplicateTimeline(self, name):
        self.app.duplicate_count += 1
        duplicate = Timeline(self.app, name, f"candidate-{self.app.duplicate_count}")
        duplicate.tracks = copy.deepcopy(self.tracks)
        for track in duplicate.tracks.values():
            for clips in track:
                for clip in clips:
                    clip.uid += "-copy"
        duplicate.track_name = copy.deepcopy(self.track_name)
        duplicate.track_enable = copy.deepcopy(self.track_enable)
        self.app.timelines.append(duplicate)
        return duplicate

    def DeleteTrack(self, kind, index):
        self.tracks[kind].pop(index - 1)
        self.track_name.get(kind, {}).pop(index, None)
        self.track_enable.get(kind, {}).pop(index, None)
        return True

    def AddTrack(self, kind):
        self.tracks[kind].append([])
        self.track_enable.setdefault(kind, {})[len(self.tracks[kind])] = True
        return True

    def SetTrackName(self, kind, index, name):
        self.track_name.setdefault(kind, {})[index] = name
        return True

    def GetTrackName(self, kind, index): return self.track_name.get(kind, {}).get(index)

    def SetTrackEnable(self, kind, index, state):
        self.track_enable.setdefault(kind, {})[index] = state
        return True

    def GetIsTrackEnabled(self, kind, index): return self.track_enable.get(kind, {}).get(index, True)

    def AddMarker(self, frame, color, name, note, duration, custom_data):
        self.marker[custom_data] = {"name": name, "frame": frame}
        return True

    def GetMarkerByCustomData(self, token): return self.marker.get(token, {})


class App:
    def __init__(self, expected):
        self.base = Timeline(self)
        self.current = self.base
        self.timelines = [self.base]
        self.page = "edit"
        self.expected = expected
        self.import_offsets = [4] * len(expected)
        self.saves = 0
        self.duplicate_count = 0
        self.import_calls = 0
        self.append_calls = 0

    def GetProjectManager(self): return self
    def GetCurrentProject(self): return self
    def GetUniqueId(self): return "project-exact"
    def GetCurrentTimeline(self): return self.current
    def IsRenderingInProgress(self): return False
    def GetCurrentPage(self): return self.page
    def OpenPage(self, page):
        self.page = page
        return True

    def SetCurrentTimeline(self, timeline):
        self.current = timeline
        return True

    def SaveProject(self):
        self.saves += 1
        return True

    def GetTimelineCount(self): return len(self.timelines)
    def GetTimelineByIndex(self, index): return self.timelines[index - 1]
    def GetMediaPool(self): return self

    def ImportMedia(self, paths):
        self.import_calls += 1
        self.page = "media"
        return paths

    def AppendToTimeline(self, placements):
        self.append_calls += 1
        assert placements[0]["trackIndex"] == 1
        self.current.tracks["subtitle"][0] = [Item(text, start+shift, end+shift)
                                              for (start,end,text),shift in zip(self.expected,self.import_offsets)]
        return self.current.tracks["subtitle"][0]


class NativeTests(unittest.TestCase):
    def setUp(self):
        self.expected = [(109, 119, "New York"), (123, 130, "Second cue")]
        self.app = App(self.expected)
        self.target = dict(project_id="project-exact", timeline_id="timeline-exact", origin_frame=100,
                           end_frame=190, native_fps_values=["30"], raster=[1920, 1080])
        self.before = native.snapshot(self.app, self.target)
        self.name = "OWNED native subtitles"
        self.token = "specific-operation-token"

    def install(self):
        return native.install(self.app, self.target, self.before, self.expected,
                              "synthetic.srt", self.name, self.token)

    def install_track(self, rows):
        self.app.base.tracks["subtitle"][0] = [Item(text, start, end) for start,end,text in rows]

    def test_normalize_only_uniform_offsets(self):
        for offset in (-5, 0, 7):
            with self.subTest(offset=offset):
                self.install_track([(a+offset,b+offset,t) for a,b,t in self.expected])
                self.assertEqual(native.normalize_import(self.app.base,self.expected),offset)
                self.assertEqual(native.cue_readback(self.app.base), self.expected)
                moves = [clip.moves for clip in self.app.base.tracks["subtitle"][0]]
                self.assertEqual(moves, [[({"startFrame": a}, False)] if offset else []
                                         for a,_,_ in self.expected])

    def test_bad_count_text_duration_or_nonuniform_are_not_shifted(self):
        for rows, failure in (
            ([(115, 125, "New York")], "count"),
            ([(115, 125, "Different"), (129, 136, "Second cue")], "text or duration"),
            ([(115, 124, "New York"), (129, 136, "Second cue")], "text or duration"),
            ([(115, 125, "New York"), (130, 137, "Second cue")], "Nonuniform"),
        ):
            with self.subTest(failure=failure):
                self.install_track(rows)
                with self.assertRaisesRegex(RuntimeError, failure):
                    native.normalize_import(self.app.base,self.expected)
                self.assertEqual(native.cue_readback(self.app.base), rows)
                self.assertTrue(all(not clip.moves for clip in self.app.base.tracks["subtitle"][0]))

    def test_duplicate_isolated_track_and_idempotent_reuse(self):
        source_subtitle = native.cue_readback(self.app.base)
        result = self.install()
        self.assertEqual(result["status"], "CREATED")
        self.assertEqual(result["native_cues"], 2)
        self.assertEqual(result["branded_style"], "NOT_APPLIED")
        self.assertEqual(result["playback"], "UNVERIFIED")
        self.assertEqual(result["import_offset_corrected"], 4)
        self.assertIs(self.app.current, self.app.base)
        self.assertEqual(native.snapshot(self.app,self.target), self.before)
        self.assertEqual(native.cue_readback(self.app.base), source_subtitle)
        self.assertTrue(self.app.base.GetIsTrackEnabled("subtitle",1))
        candidate = self.app.timelines[1]
        self.assertFalse(candidate.GetIsTrackEnabled("subtitle",1))
        self.assertEqual(native.cue_readback(candidate), self.expected)
        self.assertEqual(self.install()["status"], "UNCHANGED")
        self.assertEqual((self.app.duplicate_count,self.app.import_calls,self.app.append_calls), (1,1,1))

    def test_reject_modified_owned_candidate_and_unowned_name_collision(self):
        self.app.timelines.append(Timeline(self.app,self.name,"someone-else"))
        with self.assertRaisesRegex(RuntimeError,"unowned"):
            self.install()
        self.assertEqual(self.app.duplicate_count,0)
        self.assertIs(self.app.current,self.app.base)
        self.app.timelines.pop()
        self.install()
        candidate = self.app.timelines[1]
        candidate.tracks["subtitle"][0][1].name = "User changed the subtitle"
        with self.assertRaisesRegex(RuntimeError,"modified"):
            self.install()
        self.assertEqual((self.app.duplicate_count,self.app.import_calls), (1,1))
        self.assertIs(self.app.current,self.app.base)
        self.assertEqual(candidate.tracks["subtitle"][0][1].name, "User changed the subtitle")

    def test_fractional_bound_is_not_rounded_into_proven_uniform_offset(self):
        self.install_track([(109.5, 119.5, "New York"), self.expected[1]])
        with self.assertRaisesRegex(RuntimeError, "Subframe"):
            native.normalize_import(self.app.base, self.expected)
        self.assertFalse(self.app.base.tracks["subtitle"][0][0].moves)

    def test_owned_candidate_rechecks_picture_identity_and_lane_state(self):
        self.install()
        candidate = self.app.timelines[1]
        candidate.tracks["video"][0][0].media = Media("new-same-duration.mov")
        with self.assertRaisesRegex(RuntimeError, "Candidate video changed"):
            self.install()
        candidate.tracks["video"][0][0].media = Media("picture.mov")
        candidate.SetTrackEnable("subtitle", 1, True)
        with self.assertRaisesRegex(RuntimeError, "subtitle lane changed"):
            self.install()
        candidate.SetTrackEnable("subtitle", 1, False)
        candidate.AddTrack("subtitle")
        with self.assertRaisesRegex(RuntimeError, "subtitle lane changed"):
            self.install()
        self.assertEqual((self.app.duplicate_count, self.app.import_calls), (1, 1))
        self.assertIs(self.app.current, self.app.base)

    def test_stale_source_stops_before_save_or_import(self):
        self.app.base.tracks["audio"][0][0].properties["Volume"] = -7
        with self.assertRaisesRegex(RuntimeError, "Timeline changed"):
            self.install()
        self.assertEqual((self.app.saves, self.app.import_calls, self.app.duplicate_count), (0, 0, 0))

    def test_view_restoration_attempts_page_and_playhead_after_timeline_failure(self):
        original_set = self.app.SetCurrentTimeline
        restored = []

        def set_timeline(timeline):
            if timeline is self.app.base:
                raise RuntimeError("synthetic timeline restore error")
            return original_set(timeline)

        def playhead(timecode):
            restored.append(("playhead", timecode))
            return True

        def page(page_name):
            restored.append(("page", page_name))
            return True

        self.app.SetCurrentTimeline = set_timeline
        self.app.base.SetCurrentTimecode = playhead
        self.app.OpenPage = page
        with self.assertRaisesRegex(RuntimeError, "Could not restore source view: timeline"):
            self.install()
        self.assertEqual(restored, [("playhead", self.before["timecode"]), ("page", self.before["page"])])

    def test_failed_candidate_kept_disabled_without_touching_source(self):
        source_subtitle = native.cue_readback(self.app.base)
        self.app.import_offsets = [4,8]
        with self.assertRaisesRegex(RuntimeError,"Nonuniform"):
            self.install()
        self.assertIs(self.app.current,self.app.base)
        self.assertEqual(native.snapshot(self.app,self.target),self.before)
        self.assertEqual(native.cue_readback(self.app.base),source_subtitle)
        self.assertEqual(len(self.app.timelines),2)
        self.assertFalse(self.app.timelines[1].GetIsTrackEnabled("subtitle",1))
        self.assertFalse(self.app.timelines[1].GetMarkerByCustomData(self.token))


if __name__ == "__main__":
    unittest.main()
