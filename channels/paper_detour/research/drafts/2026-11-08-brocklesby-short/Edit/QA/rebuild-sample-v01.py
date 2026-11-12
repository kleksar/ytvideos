import hashlib,json,subprocess,tempfile
from pathlib import Path
ep=Path(__file__).resolve().parents[2]
qa=ep/'Edit/QA'
run=qa/'brocklesby-en-v01'
p=json.loads((run/'report.json').read_text())
def sha(x): return hashlib.sha256(x.read_bytes()).hexdigest()
argv=p['frame_recipe']['argv'].copy()
assert argv[0]=='ffmpeg' and argv[-1].endswith('/scratch/qa/%06d.png') and str(ep/'Deliverables/Brocklesby-Paper-Detour-en-v01.mp4') in argv
with tempfile.TemporaryDirectory(prefix='brocklesby-qa-rebuild-') as tmp:
 dest=Path(tmp)
 argv[-1]=str(dest/'%06d.png')
 subprocess.run(argv,check=True)
 output=sorted(dest.glob('*.png'))
 assert len(output)==len(p['frame_map'])
 checked=[dict(frame=entry['index'],sha256=sha(file)) for entry,file in zip(p['frame_map'],output)]
 assert all(e['sha256']==sha(run/q['path']) for e,q in zip(checked,p['frame_map']))
data=dict(status='PASS',argv=argv,media_sha256=sha(ep/'Deliverables/Brocklesby-Paper-Detour-en-v01.mp4'),edit_revision='edit-v01',montage_sha256=sha(ep/'Edit/montage-v01.json'),export_contract_sha256=sha(ep/'Edit/export-contract-v02.json'),render_provenance_sha256=sha(ep/'Work/render-v02/render_provenance.json'),frames=checked)
(run/'edit-binding-and-rebuild-proof.json').write_text(json.dumps(data,indent=2)+'\n')
print('Reconstructed',len(checked),'frames with exact image hashes.')
