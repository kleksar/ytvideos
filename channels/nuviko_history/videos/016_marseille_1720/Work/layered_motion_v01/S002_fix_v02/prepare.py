import os
from pathlib import Path
import cv2, numpy as np, torch
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from simple_lama_inpainting import SimpleLama
root=Path('/Users/diplomat/ytvideos'); d=Path(__file__).resolve().parent
im=Image.open(root/'stories/videos/016_marseille_1720/Source/Images/v01/S002.png').convert('RGB'); original=np.array(im); h,w=original.shape[:2]
os.environ['LAMA_MODEL']=str(root/'Shared/Image_Motion/Tools/sam2-local/cache/torch/hub/checkpoints/big-lama.pt')
model=build_sam2('configs/sam2.1/sam2.1_hiera_t.yaml',str(root/'Shared/Image_Motion/Tools/sam2-local/models/sam2.1_hiera_tiny.pt'),device='mps')
p=SAM2ImagePredictor(model); p.set_image(original)
pts=np.array([[480,410],[470,555],[620,401],[721,360]],np.float32)
masks,scores,_=p.predict(box=np.array([350,230,780,745],np.float32),point_coords=pts,point_labels=np.array([1,1,1,1]),multimask_output=True)
idx=max(range(len(masks)),key=lambda i:(sum(bool(masks[i][int(y),int(x)]) for x,y in pts),scores[i])); mask=masks[idx].astype(np.uint8)*255
mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
# Close internal pinholes while preserving external spaces between figures.
contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); mask=np.zeros_like(mask); cv2.drawContours(mask,contours,-1,255,cv2.FILLED)
solid=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
alpha=cv2.GaussianBlur(solid,(0,0),.55)
expanded=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(37,37)))
repaired=np.asarray(SimpleLama(device=torch.device('mps'))(im,Image.fromarray(expanded)))[:h,:w]; bg=original.copy(); bg[expanded>0]=repaired[expanded>0]
Image.fromarray(np.dstack([original,alpha]),'RGBA').save(d/'foreground.png'); Image.fromarray(bg,'RGB').save(d/'background.png'); Image.fromarray(alpha,'L').save(d/'mask.png')
print({'mask_percent':round(float((mask>0).mean()*100),2),'point_coverage':[bool(mask[int(y),int(x)]) for x,y in pts],'scores':scores.tolist()})
