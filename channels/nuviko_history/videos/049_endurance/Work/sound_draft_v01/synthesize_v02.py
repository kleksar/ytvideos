"""Endurance original synth sketch; machine-generated, requires listening/mix approval."""
import wave
from pathlib import Path
import numpy as np
SR=44100
DURATION=559.84
OUT=Path(__file__).with_name('music_draft_v02.wav')
# Time, relative bed intensity. Smooth transitions, including deliberate near-silence.
points=np.array([(0,.25),(20,.65),(80,.58),(100,.25),(106,.0),(111,.15),(145,.38),(158,.05),(165,.35),(200,.45),(245,.34),(254,.12),(265,.53),(310,.69),(337,.35),(345,.02),(354,.35),(390,.4),(423,.3),(432,.12),(443,.24),(455,.10),(470,.16),(489,0),(499,.35),(514,.47),(527,.50),(530,.18),(538,.22),(542,.16),(548,.24),(554,.1),(556,0),(559.84,0)])
# Separate slow overlapping note envelopes avoid clicks and fixed repetitive loops.
notes=[(110.0,164.81),(98.0,146.83),(110.0,164.81),(87.31,130.81),(110.0,164.81),(98.0,155.56),(110.0,164.81),(116.54,174.61),(110.0,164.81)]
with wave.open(str(OUT),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
 for n in range(0,int(DURATION*SR),SR*4):
  count=min(SR*4,int(DURATION*SR)-n); t=(np.arange(count,dtype=np.float64)+n)/SR
  level=np.interp(t,points[:,0],points[:,1]); signal=np.zeros(count,dtype=np.float64)
  for k in range(int(t[0]//30)-1,int(t[-1]//30)+1):
   if k<0: continue
   local=t-k*30; e=np.clip(local/7,0,1)*np.clip((38-local)/8,0,1); e=e*e*(3-2*e)
   f1,f2=notes[k%len(notes)]
   signal+=e*(.48*np.sin(2*np.pi*f1*t)+.25*np.sin(2*np.pi*f2*t)+.07*np.sin(2*np.pi*(f2*2)*t))
  # Very gentle pulse only during the open-ocean crossing; synthesis is not an environmental effect.
  active=np.clip((t-262)/9,0,1)*np.clip((329-t)/10,0,1)
  period=60/68*2; phase=np.mod(t-262,period); env=np.exp(-phase*3.2)*active
  signal+=.10*env*np.sin(2*np.pi*196*t)
  out=np.clip(signal*level*.030,-1,1)
  w.writeframes((out*32767).astype('<i2').tobytes())
print(OUT)
