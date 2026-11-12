from pathlib import Path
import os
import cv2
import numpy as np
import torch
from PIL import Image
from simple_lama_inpainting import SimpleLama

root=Path(__file__).resolve().parent
image=Image.open('/Users/diplomat/ytvideos/channels/nuviko_history/videos/009_black_death/Assets/Generated/remake_v01/scene003_coin_mystery.png').convert('RGB')
raw=np.asarray(Image.open(root/'sam2/mask_FG.png').convert('L'))
mask=(raw>127).astype(np.uint8)*255
# Fill enclosed SAM holes and close only tiny gaps; keep open space between limbs.
def fill_holes(m):
    flood=m.copy()
    hh,ww=m.shape
    cv2.floodFill(flood,np.zeros((hh+2,ww+2),np.uint8),(0,0),255)
    return cv2.bitwise_or(m,cv2.bitwise_not(flood))
mask=fill_holes(mask)
mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
mask=fill_holes(mask)
alpha=cv2.GaussianBlur(mask,(0,0),0.55)
fg=np.dstack([np.asarray(image),alpha])
Image.fromarray(fg,'RGBA').save(root/'foreground.png')
# Restore only the subject plus a narrow contour band, preserving all other source pixels.
expanded=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(37,37)))
mask_img=Image.fromarray(expanded)
mask_img.save(root/'inpaint_mask_18px.png')
os.environ['LAMA_MODEL']='/Users/diplomat/ytvideos/Shared/Image_Motion/Tools/sam2-local/cache/torch/hub/checkpoints/big-lama.pt'
lama=SimpleLama(device=torch.device('mps'))
restored=lama(image,mask_img)
base=np.asarray(image).copy(); restored_arr=np.asarray(restored)[:image.height,:image.width]
base[expanded>0]=restored_arr[expanded>0]
Image.fromarray(base).save(root/'background.png')
overlay=np.asarray(image).copy(); tint=np.zeros_like(overlay); tint[:]=[50,200,220]
blended=cv2.addWeighted(overlay,.65,tint,.35,0)
preview=np.where((alpha>10)[:,:,None],blended,overlay)
Image.fromarray(preview).save(root/'mask_preview.png')
print({'size':image.size,'mask_area_pct':round(float((mask>0).mean()*100),3),'inpaint_area_pct':round(float((expanded>0).mean()*100),3),'foreground':str(root/'foreground.png'),'background':str(root/'background.png')})
