import sys,json,pathlib,hashlib,importlib.util,importlib.abc,importlib.machinery
root=pathlib.Path('/Users/diplomat/ytvideos');episode=root/'new_channel/videos/037_cost_of_living';video=episode/'Deliverables/037_EN_review_20261104.mp4'; receipt=pathlib.Path(str(video)+'.delivery.json');decision=episode/'Packaging/Metadata/USER_ACCEPTS_VISUAL_OVERLAP_20261104.md'; channel='UCMVfdfaNxV3ZkI3_J3Eejzw';expected='08148e7ed48c7928cf5a913919a8f7dfa51e5972c0aa83dedfc5ade2cf301bc4';required=['Subtitle placement overlaps story tokens in scenes S16 and S66; awaiting explicit user decision.']
d=json.loads(receipt.read_text()); assert d['media']['sha256']==expected and hashlib.sha256(video.read_bytes()).hexdigest()==expected;assert d['open_requirements']==required and d['review']['checks']['visual_placement']['status']=='FAIL';assert '«Да, загружай как есть»' in decision.read_text() and expected in decision.read_text()
path=root/'automation/ffmpeg_montage/delivery.py';source=path.read_text();old="if receipt.get('open_requirements') != []:";new="if receipt.get('open_requirements') != [] and receipt.get('open_requirements') != "+repr(required)+":"; assert source.count(old)==1;source=source.replace(old,new)
old="if check.get('status') != 'PASS' or not all(isinstance(check.get(field), str) and check[field].strip() for field in ('reviewer', 'method', 'coverage')):";new="if (check.get('status') != 'PASS' and not (key == 'visual_placement' and check.get('status') == 'FAIL')) or not all(isinstance(check.get(field), str) and check[field].strip() for field in ('reviewer', 'method', 'coverage')):";assert source.count(old)==1;source=source.replace(old,new)
namespace={'__file__':str(path),'__name__':'episode_exception_delivery'};exec(compile(source,str(path),'exec'),namespace);validate=namespace['validate_release'];validate(video,channel,receipt);print('PREFLIGHT_OK: user-accepted visual FAIL preserved, all other receipt checks passed',flush=True)
if '--preflight-only' in sys.argv:sys.exit(0)
sys.path.insert(0,str(root/'stories/automation/youtube'));import upload
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
original=importlib.util.spec_from_file_location
class Loader(importlib.abc.Loader):
 def create_module(self,spec):return None
 def exec_module(self,module):module.validate_release=validate
def select_spec(name,location,*args,**kwargs):
 if name=='ytv_delivery':return importlib.machinery.ModuleSpec(name,Loader())
 return original(name,location,*args,**kwargs)
importlib.util.spec_from_file_location=select_spec
meta=json.loads((episode/'Packaging/Metadata/UPLOAD_METADATA_20261104.json').read_text());token='/Users/diplomat/.local/share/story-youtube/paper-detour/token.json';state='/Users/diplomat/.local/share/story-youtube/paper-detour/037-cost-of-living-20261104.json'
try:
 with AuthorizedSession(Credentials.from_authorized_user_file(token,upload.SCOPES)) as session:result=upload.upload(session,video,meta,channel,state,delivery_receipt=str(receipt))
 print(json.dumps(upload.upload_result(result),ensure_ascii=False),flush=True)
except Exception as e:
 print('UPLOAD_ERROR',type(e).__name__,str(e) if isinstance(e,upload.UploadError) else '',file=sys.stderr);sys.exit(1)
