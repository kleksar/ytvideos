import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import revise_history_long as module

class Bridge:
    def __init__(self, project, tracks, active_export=False, fail_replace=False):
        self.project=project; self.tracks=copy.deepcopy(tracks); self.active_export=active_export
        self.fail_replace=fail_replace; self.writes=[]
    def call(self, name, args):
        if name=='manage_project': return {'active':{'path':self.project}, 'visible':{'path':self.project}}
        if name=='manage_exports': return {'exports':[{'status':'rendering' if self.active_export else 'completed'}]}
        if name=='get_timeline': return {'id':'timeline-id','name':'film','fps':30,'width':1920,'height':1080,'totalFrames':20,'tracks':copy.deepcopy(self.tracks)}
        if name=='get_media': return {'assets': ([{'id': args['ids'][0]}] if 'ids' in args else [])}
        self.writes.append(name)
        if name=='import_media': return {'mediaRef':'new'+str(sum(x=='import_media' for x in self.writes))}
        if name=='add_clips':
            if self.fail_replace: raise TimeoutError('unknown')
            entry=args['entries'][0]; clip={'id':entry['mediaRef']+'clip','mediaRef':entry['mediaRef'],'mediaType':'image','frames':[entry['startFrame'],entry['endFrame']]}
            track=self.tracks[0]; track['clips']=[x for x in track['clips'] if x['frames']!=clip['frames']]+[clip]
            return {'clips':[{'id':clip['id']}]}
        if name=='set_keyframes':
            clip=next(x for x in self.tracks[0]['clips'] if x['id']==args['clipId'])
            clip['keyframes']={'scale':args['keyframes']};return {}
        raise AssertionError(name)

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name); project=root/'editor.palmier';project.mkdir()
        manifest=root/'manifest.json';manifest.write_text('{"frames":20}')
        receipt=root/'original.json';receipt.write_text('{}')
        a=root/'030_corrected.png';a.write_bytes(b'a');b=root/'031_corrected.png';b.write_bytes(b'b')
        scale=[[0,1.0,1.0],[9,1.1,1.1]]
        clips=[{'id':f'old{i}','frames':[i*10,(i+1)*10],'mediaRef':f'media{i}','mediaType':'image','keyframes':{'scale':scale}} for i in range(2)]
        tracks=[{'index':0,'trackId':'track','type':'video','clips':clips}]
        self.plan={'root':root,'manifest':manifest,'manifestHash':module.sha(manifest),'original':receipt,'receiptHash':module.sha(receipt),
                   'journalDir':root/'journal','receipt':{'project':str(project),'timeline':'film','timelineId':'timeline-id','tracks':tracks},
                   'entries':[{'number':30+i,'path':str(p),'sha256':module.sha(p),'clipId':f'old{i}','trackId':'track','trackIndex':0,'frames':clips[i]['frames'],'keyframes':scale} for i,p in enumerate((a,b))]}
        self.bridge=Bridge(str(project),tracks)
        self.disk=patch.object(module.shutil,'disk_usage',return_value=type('Disk',(),{'free':20*1024**3})());self.disk.start();self.addCleanup(self.disk.stop)
    def test_replaces_only_expected_clips_and_preserves_motion(self):
        result=module.run(self.plan,self.bridge.call)
        self.assertEqual(result['status'],'revised')
        self.assertEqual(self.bridge.writes,['import_media','add_clips','set_keyframes']*2)
        self.assertEqual(len(list(self.plan['journalDir'].glob('*.json'))),7)
        self.assertEqual([c['frames'] for c in self.bridge.tracks[0]['clips']],[[0,10],[10,20]])
    def test_active_export_prevents_any_mutation(self):
        self.bridge.active_export=True
        with self.assertRaises(RuntimeError):module.run(self.plan,self.bridge.call)
        self.assertEqual(self.bridge.writes,[])
        self.assertFalse(self.plan['journalDir'].exists())
    def test_uncertain_replace_preserves_journal_and_stops(self):
        self.bridge.fail_replace=True
        with self.assertRaises(TimeoutError):module.run(self.plan,self.bridge.call)
        journal=self.plan['journalDir']/'030_replace.json'
        self.assertEqual(json.loads(journal.read_text())['state'],'outcome_unknown')
        self.assertEqual(self.bridge.writes,['import_media','add_clips'])
        self.assertFalse((self.plan['journalDir']/'031_import.json').exists())

if __name__=='__main__': unittest.main()
