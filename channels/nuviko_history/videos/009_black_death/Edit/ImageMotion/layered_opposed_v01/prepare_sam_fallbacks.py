import json
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

root=Path(__file__).resolve().parent
prompts=json.loads((root/'fallback_prompts.json').read_text())
out=root/'vision_masks'; out.mkdir(parents=True,exist_ok=True)
checkpoint='/Users/diplomat/ytvideos/Shared/Image_Motion/Tools/sam2-local/models/sam2.1_hiera_tiny.pt'
model=build_sam2('configs/sam2.1/sam2.1_hiera_t.yaml',checkpoint,device='mps',apply_postprocessing=False)
predictor=SAM2ImagePredictor(model)
receipt=[]
with torch.inference_mode():
 for spec in prompts:
  image=Image.open(spec['image']).convert('RGB')
  predictor.set_image(np.asarray(image).copy())
  pts=np.asarray([p[:2] for p in spec['points']],dtype=np.float32)
  labels=np.asarray([p[2] for p in spec['points']],dtype=np.int32)
  masks,scores,_=predictor.predict(point_coords=pts,point_labels=labels,
                                  box=np.asarray(spec['box'],dtype=np.float32),multimask_output=False)
  mask=np.asarray(masks[0],dtype=np.uint8)
  path=out/f"S{spec['scene']:03d}_sam2_v02.png"
  Image.fromarray(mask*255).save(path)
  entry={'scene':spec['scene'],'image':spec['image'],'mask':str(path),'score':float(scores[0]),
         'mask_area_percent':float(mask.mean()*100),'source_size':list(image.size),'method':'SAM2 box+points'}
  receipt.append(entry); print(json.dumps(entry))
(root/'sam_fallback_receipt_v02.json').write_text(json.dumps(receipt,indent=2)+'\n')
