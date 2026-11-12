import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import export_history_revised as module

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);root=Path(self.tmp.name)
        project=root/'film.palmier';project.mkdir();manifest=root/'manifest.json';manifest.write_text('{}');original=root/'old.json';original.write_text('{}');revision=root/'new.json';revision.write_text('{}')
        tracks=[{'index':0,'trackId':'t','clips':[{'id':'c','frames':[0,10],'mediaRef':'m'}]}]
        self.info={'root':root,'manifest':manifest,'original':original,'revision':revision,'revisionHash':module.sha(revision),'m':{'timeline':'film','frames':10},'r':{'project':str(project),'timelineId':'id'},'rev':{'manifestSha256':module.sha(manifest),'originalReceiptSha256':module.sha(original),'tracks':tracks},'out':root/'v2.mp4','journal':root/'export.json'}
        self.writes=[];self.active=False
        self.disk=patch.object(module.shutil,'disk_usage',return_value=type('Disk',(),{'free':20*1024**3})());self.disk.start();self.addCleanup(self.disk.stop)
    def call(self,name,args):
        if name=='manage_project':return {'active':{'path':self.info['r']['project']},'visible':{'path':self.info['r']['project']}}
        if name=='get_timeline':return {'id':'id','name':'film','fps':30,'width':1920,'height':1080,'totalFrames':10,'tracks':self.info['rev']['tracks']}
        if name=='manage_exports':return {'exports':[{'status':'rendering' if self.active else 'completed'}]}
        if name=='export_project':self.writes.append(args);return {'status':'queued','jobId':'job'}
        raise AssertionError(name)
    def test_queues_once_with_new_output_and_no_overwrite(self):
        result=module.execute(self.info,self.call)
        self.assertEqual(result['state'],'queued');self.assertEqual(len(self.writes),1)
        self.assertFalse(self.writes[0]['overwrite']);self.assertTrue(self.writes[0]['outputPath'].endswith('v2.mp4'))
    def test_active_export_prevents_queue(self):
        self.active=True
        with self.assertRaises(RuntimeError):module.execute(self.info,self.call)
        self.assertEqual(self.writes,[]);self.assertFalse(self.info['journal'].exists())
    def test_existing_journal_blocks_second_write(self):
        module.execute(self.info,self.call)
        with self.assertRaises(FileExistsError):module.execute(self.info,self.call)
        self.assertEqual(len(self.writes),1)

if __name__=='__main__':unittest.main()
