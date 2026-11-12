from pathlib import Path
from datetime import datetime
import json,hashlib
root=Path(__file__).resolve().parents[2]; repo=Path('/Users/diplomat/ytvideos'); plan=root/'Work/preview_v01/edit_PREVIEW_v01.json'; output=root/'Edit/Previews/world_discovery_PREVIEW_v01.mp4'; mix=root/'Work/audio_trial_v01/mix_v03_EXPERIMENT_NOT_REVIEWED.wav'; profile=repo/'automation/ffmpeg_montage/profiles/long.json'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((repo/'.agents/skills/ytv-video-export/assets/export-contract.template.json').read_text())
p.update(status='READY_TO_RENDER',episode='world_discovery',language='en',format='long',purpose='PREVIEW ONLY for user viewing; content, mix, speech listening, sync and map visual review remain incomplete; not upload master')
p['settings_profile']={'path':str(profile),'sha256':h(profile)}
p['edit'].update(project_id='world_discovery_review_preview',timeline_id=str(plan),saved_revision_evidence='Preview manifest SHA-256; no project editor',timeline_read_path=str(plan),timeline_read_sha256=h(plan),dependencies=[])
p['timeline'].update(width=2560,height=1440,aspect_ratio='16:9',sample_aspect_ratio='1:1',fps='30/1',frame_count=14813,duration_seconds=14813/30,output_color_space='Rec.709 SDR')
p['required_delivery']['container']='MP4';p['required_delivery']['video']={'codec_name':'h264','pix_fmt':'yuv420p','scan':'progressive','cadence':'constant 30/1 fps','color_primaries':'bt709','color_transfer':'bt709','color_space':'bt709','color_range':'tv'}
p['required_delivery']['audio_contract']={'owner_handoff':str(root/'Work/audio_trial_v01/REVIEW.md'),'accepted_complete_mix':{'path':str(mix),'sha256':h(mix),'status':'candidate mix for preview only, not auditioned'},'source_rate_channels':'44100 Hz stereo','codec_name':'aac','profile':'LC','sample_rate':44100,'channels':2,'target_bit_rate':'256k'}
p['encoding'].update(engine='shared ffmpeg montage.py',version_evidence='render provenance snapshot',requested_arguments={'encoder':'libx264','video_bitrate':'20M','output_pix_fmt':'yuv420p','fps':'30/1','audio_codec':'aac','audio_profile':'aac_low','audio_bitrate':'256k','audio_sample_rate':44100,'audio_channels':2},quality_preferences={},capability_evidence='shared renderer settings check',engine_managed_fields=[])
p['preflight'].update(author='episode coordinator',time=datetime.now().astimezone().isoformat(),authorization_references=['User requested MP4 for review, no upload'],fresh_settings_evidence='shared renderer --check-settings',writer_and_export_state='new preview output',output_path=str(output),overwrite=False,media_lifecycle_receipt='Preview input inventory retained with episode; no other outputs changed',unresolved_required_fields=[])
contract=root/'Edit/Export/EXPORT_PREVIEW_v01.json';contract.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n');print(contract)
