import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import torch
from sam2.build_sam import build_sam2
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator
base=Path('/Users/diplomat/ytvideos')
imgpath=Path(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
img=np.asarray(Image.open(imgpath).convert('RGB'))
model=build_sam2('configs/sam2.1/sam2.1_hiera_t.yaml',str(base/'Shared/Image_Motion/Tools/sam2-local/models/sam2.1_hiera_tiny.pt'),device='mps',apply_postprocessing=False)
generator=SAM2AutomaticMaskGenerator(model,points_per_side=16,pred_iou_thresh=.86,stability_score_thresh=.90,crop_n_layers=0,min_mask_region_area=300)
with torch.inference_mode(): masks=generator.generate(img)
print('count',len(masks),'image',img.shape)
rank=sorted(enumerate(masks),key=lambda x:(-x[1]['area'],x[1]['bbox'][1]))
source=Image.fromarray(img); sheet=Image.new('RGB',(img.shape[1]*3,img.shape[0]*2),'white'); d=ImageDraw.Draw(sheet)
for j,(idx,m) in enumerate(rank[:6]):
 mask=m['segmentation']; panel=source.copy(); tint=Image.new('RGB',source.size,(40,210,220)); panel.paste(tint,(0,0),Image.fromarray(mask.astype('uint8')*110))
 draw=ImageDraw.Draw(panel); bx,by,bw,bh=map(int,m['bbox']); draw.rectangle([bx,by,bx+bw,by+bh],outline='red',width=3)
 panel.thumbnail((img.shape[1],img.shape[0])); ox=(j%3)*img.shape[1]; oy=(j//3)*img.shape[0]; sheet.paste(panel,(ox,oy)); d.text((ox+8,oy+8),f"#{idx} a={m['area']} bbox={m['bbox']} iou={m['predicted_iou']:.3f} stab={m['stability_score']:.3f}",fill='red')
sheet.save(out/'top_masks.jpg',quality=90)
Path(out/'report.txt').write_text('\n'.join(f"{idx} area={m['area']} bbox={m['bbox']} iou={m['predicted_iou']} stability={m['stability_score']}" for idx,m in rank[:50])+'\n')
