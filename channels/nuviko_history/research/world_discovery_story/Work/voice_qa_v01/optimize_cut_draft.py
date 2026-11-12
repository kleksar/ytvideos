import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
p=Path(__file__).parent
source=json.loads((p/'scene_boundaries_joint_DRAFT.json').read_text())
b=source['blocks']; n=len(b)
orig=np.array([b[0]['cut_in']]+[x['cut_out'] for x in b])
# Boundary movement variables and absolute-value costs. Cut locations remain tentative.
c=np.r_[np.zeros(n+1),np.ones(n-1)]
A=[]; B=[]
for i in range(n):
 row=np.zeros(2*n); row[i+1]=1; row[i]=-1; A.append(row); B.append(6)
 A.append(-row); B.append(-4)
for i in range(1,n):
 row=np.zeros(2*n); row[i]=1; row[n+i]=-1; A.append(row); B.append(orig[i])
 row=np.zeros(2*n); row[i]=-1; row[n+i]=-1; A.append(row); B.append(-orig[i])
bounds=[(0,0)]+[(None,None)]*(n-1)+[(float(orig[-1]),float(orig[-1]))]+[(0,None)]*(n-1)
r=linprog(c,A_ub=np.array(A),b_ub=np.array(B),bounds=bounds,method='highs')
if not r.success: raise RuntimeError(r.message)
cuts=r.x[:n+1]; result=[]
for i,x in enumerate(b):
 y=dict(x); y['cut_in']=round(float(cuts[i]),3); y['cut_out']=round(float(cuts[i+1]),3); y['duration']=round(float(cuts[i+1]-cuts[i]),3)
 y['in_shift']=round(float(cuts[i]-orig[i]),3); y['out_shift']=round(float(cuts[i+1]-orig[i+1]),3)
 y['speech_before_cut']=round(max(0.,float(cuts[i])-x['speech_start']),3)
 y['speech_after_cut']=round(max(0.,x['speech_end']-float(cuts[i+1])),3)
 y['status']='DRAFT: inspect speech/image synchronization'; result.append(y)
out={'status':'EXPERIMENT ONLY: cut constraints do not establish semantic synchronization or audio quality; not accepted for edit','audio_sha256':source['audio_sha256'],'text_sha256':source['text_sha256'],'method':'linear programming minimizes total absolute shift from initial cuts, constraining shot duration 4–6 s; speech and end screen not verified','blocks':result,'additional_end_screen_seconds':10,'end_screen_note':'Proposed additional end screen after narration; imagery, sound and total timeline require decision.'}
(p/'scene_cuts_optimized_EXPERIMENT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('shots',n,'outside 4–6',sum(not 3.999<=z['duration']<=6.001 for z in result),'speech overlap flags',sum(z['speech_before_cut']>0.05 or z['speech_after_cut']>0.05 for z in result),'max boundary shift',round(max(abs(cuts-orig)),3))
for z in result:
 if z['speech_before_cut']>0.05 or z['speech_after_cut']>0.05: print(z['id'],z['duration'],'in',z['speech_before_cut'],'out',z['speech_after_cut'])
