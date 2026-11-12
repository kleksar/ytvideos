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
masks,scores,_=p.predict(box=np.array([355,235,775,744],np.float32),point_coords=np.array([[480,410],[470,555]],np.float32),point_labels=np.array([1,1]),multimask_output=True)
mask=(masks[int(np.argmax(scores))].astype(np.uint8)*255)
# Keep the chosen connected figure; tiny gaps remain background rather than becoming inpainted islands.
count,labels,stats,_=cv2.connectedComponentsWithStats(mask,8); sizes=stats[1:,cv2.CC_STAT_AREA]; mask=np.uint8(labels==(1+int(np.argmax(sizes))))*255
alpha=cv2.GaussianBlur(mask,(0,0),0.55)
expanded=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(37,37)))
repaired=np.asarray(SimpleLama(device=torch.device('mps'))(im,Image.fromarray(expanded)))[:h,:w]
bg=original.copy(); opaque=alpha==255; bg[opaque]=repaired[opaque]
fg=np.dstack([original,alpha]); Image.fromarray(fg,'RGBA').save(d/'foreground.png'); Image.fromarray(bg,'RGB').save(d/'background.png'); Image.fromarray(alpha,'L').save(d/'mask.png')
# At time zero the original RGB is retained under all partially transparent pixels.
a=alpha.astype(np.float32)[:,:,None]/255; rebuilt=np.rint(original*a+bg*(1-a)).astype(np.uint8); print({'mask_percent':round(float((mask>0).mean()*100),2),'zero_shift_max_error':int(np.abs(rebuilt.astype(np.int16)-original.astype(np.int16)).max()),'zero_shift_changed_pixels':int(np.any(rebuilt!=original,axis=2).sum()),'scores':scores.tolist()})
