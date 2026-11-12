import json, sys, time
from math import cos, pi
from pathlib import Path
from depthflow.scene import DepthScene
ROOT=Path(__file__).resolve().parent
SHOTS=json.loads((ROOT.parent.parent/'Storyboard/SHOTLIST_v06.json').read_text())
n=int(sys.argv[1]); row=SHOTS[n-1]; frames=row['endFrame']-row['startFrame']; direction=1 if n%2 else -1
class GentleParallax(DepthScene):
    def update(self):
        self.state.height=.26
        self.state.steady=0.0
        self.state.sticky=True
        self.state.zoom=1.15 if n<=10 or n==18 else .90
        self.state.offset=(-direction*.165*cos(pi*self.tau),0.0)
start=time.monotonic(); scene=GentleParallax(backend='headless'); scene.input(image=row['framed_path']); scene.main(output=str(ROOT/f'raw_{n:02}.mp4'),fps=30,time=frames/30,width=1920,height=1080,quality=80,ssaa=1,turbo=False)
print(json.dumps({'scene':n,'frames':frames,'direction':direction,'time':round(time.monotonic()-start,1)}),flush=True)
