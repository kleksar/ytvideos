"""A deliberately small comparison model, not a stopwatch study."""
from collections import defaultdict
import json
from pathlib import Path
START=['blue','orange','green','purple','blue','orange','green','purple']
def direct(items):
    left=items.copy(); events=[]
    while left:
        seed=left.pop(0)
        for j,candidate in enumerate(left):
            events.append({'seed':seed,'candidate':candidate,'match':candidate==seed})
            if candidate==seed:
                left.pop(j);break
        else:raise ValueError('missing match')
    return events
def grouped(items):
    bins=defaultdict(list);events=[]
    for sock in items:
        bins[sock].append(sock); events.append({'sock':sock,'destination':sock})
    assert sorted(len(x) for x in bins.values())==[2]*4
    return events
if __name__=='__main__':
    d,g=direct(START),grouped(START)
    data={'start':START,'direct_comparisons':len(d),'sorting_placements':len(g),'direct_events':d,'sorting_events':g,'scope':'one point per comparison or per sock placed in colour pile; common pair removal omitted; no claim about elapsed time; placement includes identifying colour'}
    assert (len(d),len(g))==(10,8)
    Path(__file__).with_name('events.json').write_text(json.dumps(data,indent=2)+'\n'); print('direct comparisons:',len(d),'sorting placements:',len(g))
