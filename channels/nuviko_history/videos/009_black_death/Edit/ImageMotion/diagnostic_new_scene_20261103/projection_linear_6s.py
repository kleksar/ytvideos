import json, math, sys
import numpy as np
from depthflow.scene import DepthScene
from PIL import Image
job=json.load(open(sys.argv[1]))
class Parallax(DepthScene):
 def update(self):
  self.state.height=.2
  self.state.steady=0.0
  self.state.sticky=True
  self.state.zoom=1.05
  self.state.isometric=job['isometric']
  self.state.offset=(job['amplitude']*self.tau,0.0)
scene=Parallax(backend='headless')
scene.input(image=job['image'],depth=np.load(job['depth'],allow_pickle=False))
scene.main(output=job['output'],fps=30,time=6,width=1920,height=1080,quality=80,ssaa=1,turbo=False)
