import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from collections import namedtuple
import revise_galveston_short04_photos as mod

class Tests(unittest.TestCase):
    def test_partial_mutation_is_durable_and_never_retried(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);project=root/'test.palmier';project.mkdir();manifest=root/'manifest';manifest.write_text('manifest');receipt=root/'receipt';receipt.write_text('receipt');photos=[]
            for i in range(2):
                path=root/f'photo{i}.jpg';path.write_text(str(i));photos.append({'path':str(path),'sha256':mod.sha(path),'frames':[851,917] if i==0 else [917,994]})
            tracks=[{'index':0,'trackId':'caption','type':'video','clips':[]}]
            r={'project':str(project),'timeline':'target','tracks':tracks}
            plan={'root':root,'manifest':manifest,'receipt':receipt,'journal':root/'revision','r':r,'photos':photos,'manifest_hash':mod.sha(manifest),'receipt_hash':mod.sha(receipt),'caption_track':'caption'}
            calls=[]
            def call(name,args):
                calls.append(name)
                if name=='manage_project':return {'active':{'path':str(project)},'visible':{'path':str(project)}}
                if name=='get_timeline':return {'id':mod.TIMELINE,'name':'target','fps':30,'width':1080,'height':1920,'totalFrames':1100,'tracks':tracks}
                if name=='manage_exports':return {'exports':[]}
                if name=='get_media':return {'assets':[]}
                if name=='import_media':raise TimeoutError('unknown outcome')
                raise AssertionError(name)
            usage=namedtuple('usage','total used free')(20*1024**3,1,19*1024**3)
            with patch.object(mod.shutil,'disk_usage',return_value=usage):
                with self.assertRaises(TimeoutError):mod.run(plan,call)
                journal=json.loads((root/'revision/01_import_media.json').read_text())
                self.assertEqual(journal['state'],'pending_outcome_unknown')
                with self.assertRaises(FileExistsError):mod.run(plan,call)
            self.assertEqual(calls.count('import_media'),1)
    def test_stable_track_checks_effects_and_content(self):
        a={'trackId':'one','index':0,'label':'V3','type':'video','clips':[{'id':'a','effects':[]}]}
        b={'trackId':'one','index':2,'label':'V1','type':'video','clips':[{'id':'a','effects':[]}]}
        self.assertEqual(mod.stable_track(a),mod.stable_track(b))
        b['clips'][0]['effects']=[{'type':'blur.gaussian'}]
        self.assertNotEqual(mod.stable_track(a),mod.stable_track(b))
if __name__=='__main__':unittest.main()
