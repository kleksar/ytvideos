import datetime
import hashlib
import json
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path

episode = Path(__file__).resolve().parents[2]
records = Path(__file__).resolve().parent
previous = records / 'text-only-receipt-20261108.json'
journal = records / 'generator-originals-receipt-20261108.json'
generator = Path('/Users/diplomat/.codex/generated_images/01a1bb47-4a94-7973-a2a2-980075e7bc57')
title = 'His Engines Died. He Landed Two Planes. #AviationHistory #Shorts'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()

def verify(row):
    path = Path(row['path'])
    info = path.lstat()
    assert path.parent == generator and path.resolve() == path
    assert path.name.startswith('exec-') and path.suffix == '.png'
    assert stat.S_ISREG(info.st_mode) and info.st_nlink == row['nlink'] == 1
    assert (info.st_dev, info.st_ino, info.st_mtime_ns, info.st_size) == (
        row['device'], row['inode'], row['mtime_ns'], row['bytes'])
    assert digest(path) == row['sha256']
    return path

def save(data):
    temporary = journal.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(journal)

assert sys.argv[1:] == ['--execute']
assert not journal.exists()
history = json.loads(previous.read_text())
rows = history['external_holds']
assert history['remote_video_id'] == 'azhQEhV6ywg' and len(rows) == 11
assert len({row['path'] for row in rows}) == 11
requests = json.loads((episode / 'Source/Images/imagegen-requests.json').read_text())
assert {row['path'] for row in rows} == {row['path'] for row in requests}
paths = [verify(row) for row in rows]
public_url = 'https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DazhQEhV6ywg&format=json'
with urllib.request.urlopen(public_url, timeout=15) as response:
    public = json.load(response)
assert public['title'] == title and public['author_name'] == 'Paper Detour'
opened = subprocess.run(['/usr/sbin/lsof', '-Fn', '--', *map(str, paths)], capture_output=True, text=True)
assert opened.returncode == 1 and not opened.stdout and not opened.stderr
receipt = dict(started_at=now(), remote_video_id='azhQEhV6ywg',
               public_oembed='PASS', source_receipt_sha256=digest(previous),
               storage_state='PARTIAL_TEXT_ARCHIVE', results=[])
save(receipt)
for row in rows:
    path = verify(row)
    path.unlink()
    assert not path.exists() and not path.is_symlink()
    receipt['results'].append(dict(path=str(path), sha256=row['sha256'], bytes=row['bytes'], result='deleted'))
    save(receipt)
receipt.update(verified_at=now(), storage_state='TEXT_ONLY', deleted_files=len(rows),
               deleted_logical_bytes=sum(row['bytes'] for row in rows))
save(receipt)
print(f"Deleted {receipt['deleted_files']} verified generator originals, {receipt['deleted_logical_bytes']} logical bytes.")
