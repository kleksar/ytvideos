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

    def test_final_audio_hash_snapshot_and_unsupported_trim(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'voice.wav'; path.write_bytes(b'exact final source')
            snap={'voice':[dict(id='v1',enabled=True,left=0,start=10,end=40,path=str(path))]}
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

    def test_no_rounded_fractional_native_fps_alias(self):
        self.assertEqual(command.target_native({'fps':'30000/1001'})['native_fps_values'], ['30000/1001'])
        self.assertEqual(command.target_native({'fps':'30'})['native_fps_values'], ['30','30.0'])

if __name__=='__main__': unittest.main()
