import json
from pathlib import Path
methods={'first':[[('A',1),('B',1)],[('A',2),('B',2)],[('C',1)],[('C',2)]],'second':[[('A',1),('B',1)],[('A',2),('C',1)],[('B',2),('C',2)]]}
for steps in methods.values():
 assert all(len(x)<=2 for x in steps)
 assert sorted(y for x in steps for y in x)==sorted([(a,b) for a in 'ABC' for b in (1,2)])
 assert all(next(i for i,x in enumerate(steps) if (a,1) in x)<next(i for i,x in enumerate(steps) if (a,2) in x) for a in 'ABC')
assert len(methods['first'])==4 and len(methods['second'])==3
Path(__file__).with_name('events.json').write_text(json.dumps({'capacity':2,'minutes_per_side':1,'switch_time':0,'methods':methods},indent=2)+'\n')
