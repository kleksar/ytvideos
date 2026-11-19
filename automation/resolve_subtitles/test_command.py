import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))
import command

class CommandTests(unittest.TestCase):
    def test_result_envelope_strict(self):
        self.assertEqual(command.unpack({'content':[{'type':'text','text':'{"result":{"ok":true}}'}]}), {'ok':True})
        with self.assertRaises(RuntimeError):
            command.unpack({'content':[]})
        with self.assertRaises(RuntimeError):
            command.unpack({'structuredContent':[]})
        with self.assertRaisesRegex(RuntimeError,'Native script error'):
            command.unpack({'content':[{'type':'text','text':'{"error":"native failure"}'}]})

    def test_final_audio_hash_snapshot_and_unsupported_trim(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'voice.wav'; path.write_bytes(b'exact final source')
            snap={'voice':[dict(id='v1',enabled=True,track_enabled=True,speed={'Percentage':100},left=0,start=10,end=40,path=str(path))]}
            request={'native_snapshot':copy.deepcopy(snap),'placements':[dict(id='v1',speed=1,source_in=0,
                timeline_start=10,timeline_end=40,source_sha256=command.sha(path))]}
            self.assertEqual(command.validate_voice(request,snap),{str(path):command.sha(path)})
            request['placements'][0]['speed']=1.1
            with self.assertRaisesRegex(ValueError,'not supported'):
                command.validate_voice(request,snap)
            request['placements'][0]['speed']=1
            path.write_bytes(b'new audio')
            with self.assertRaisesRegex(ValueError,'hash differs'):
                command.validate_voice(request,snap)

    def test_view_is_not_candidate_identity(self):
        first={'timecode':'00:00:00:00','page':'edit','voice':[{'id':'one'}]}
        second=dict(first,timecode='00:00:01:00',page='fairlight')
        self.assertEqual(command.candidate_token({'cues':[]},first),command.candidate_token({'cues':[]},second))
        second['voice']=[{'id':'different'}]
        self.assertNotEqual(command.candidate_token({'cues':[]},first),command.candidate_token({'cues':[]},second))

    def test_native_rate_and_muted_track_rejected(self):
        for speed,enabled,error in ((200,True,'GetSpeed'),(100,False,'disabled')):
            snapshot={'voice':[dict(id='one',enabled=True,track_enabled=enabled,speed={'Percentage':speed})]}
            request={'native_snapshot':copy.deepcopy(snapshot),'placements':[dict(id='one')]}
            with self.subTest(speed=speed), self.assertRaisesRegex(ValueError,error):
                command.validate_voice(request,snapshot)

    def test_no_rounded_fractional_native_fps_alias(self):
        self.assertEqual(command.target_native({'fps':'30000/1001'})['native_fps_values'], ['30000/1001'])
        self.assertEqual(command.target_native({'fps':'30'})['native_fps_values'], ['30','30.0'])

if __name__=='__main__': unittest.main()
