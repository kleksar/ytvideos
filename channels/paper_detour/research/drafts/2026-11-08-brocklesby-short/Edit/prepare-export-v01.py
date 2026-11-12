from pathlib import Path
import datetime,hashlib,json,subprocess
ep=Path(__file__).resolve().parents[1]
root=next(p for p in ep.parents if (p/'automation/ffmpeg_montage').is_dir())
def sha(p):
 return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ref(p):
 return dict(path=str(p),sha256=sha(p))
def dump(p,o): p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
manifest=ep/'Edit/montage-v01.json'
p=json.loads(manifest.read_text())
plan=ep/'Work/plan-v01/plan.json'
prep=ep/'Work/sub-prep-v02'
version=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0]
out=ep/'Deliverables/Brocklesby-Paper-Detour-en-v01.mp4'
audio=Path(p['audio'])
deps=list(map(Path,[p['audio'],*(s['image'] for s in p['scenes']),*(x['path'] for x in p['overlays']),p['subtitles']['words'],p['subtitles']['transcript'],p['subtitles']['review'],p['audio_contract']['speed_evidence']]))+[prep/'subtitle_contract.json',ep/'Work/shot-map-v01.json']
passport=dict(schema_version=1,status='READY_TO_RENDER',episode='brocklesby-short',language='en',format='short',purpose='Internal review candidate',
 settings_profile=ref(root/'.agents/skills/ytv-video-export/references/delivery.md'),
 edit=dict(project_id='Brocklesby Paper Detour',timeline_id=str(manifest),saved_revision_evidence='edit-v01; exact versioned montage and plan',timeline_read_path=str(plan),timeline_read_sha256=sha(plan),dependencies=[ref(x) for x in deps]),
 timeline=dict(width=1440,height=2560,aspect_ratio='9:16',sample_aspect_ratio='1:1',fps='30/1',frame_count=1080,duration_seconds=36.0,output_color_space='Rec.709 SDR'),
 required_delivery=dict(container='MP4',video=dict(codec_name='h264',pix_fmt='yuv420p',scan='progressive',cadence='constant 30/1 fps',color_primaries='bt709',color_transfer='bt709',color_space='bt709',color_range='tv'),
  audio_contract=dict(owner_handoff=str(ep/'Assets/Audio/HANDOFF.md')+'; review candidate; subjective listening UNVERIFIED',accepted_complete_mix=ref(audio),source_rate_channels=dict(sample_rate_hz=48000,channels=2,codec='pcm_s24le'),codec_name='aac',profile='LC',sample_rate=48000,channels=2,target_bit_rate='256k')),
 encoding=dict(engine='FFmpeg montage.py',version_evidence=version,requested_arguments=dict(encoder='libx264',video_bitrate='20M',output_pix_fmt='yuv420p',fps='30/1',audio_codec='aac',audio_profile='aac_low',audio_bitrate='256k',audio_sample_rate=48000,audio_channels=2),quality_preferences=['Source resolution measured in scene manifest. Generated native portraits require enlargement; phone visual checks precede encode.'],capability_evidence='ffmpeg -encoders and --check-settings',engine_managed_fields=['CRF not exposed by renderer; actual VBR, H.264 profile/level and GOP']),
 preflight=dict(author='Codex',time=datetime.datetime.now(datetime.timezone.utc).isoformat(),authorization_references=['User accepted story and requested Short production','User explicitly authorized ElevenLabs and configured Keychain for narration'],fresh_settings_evidence=str(manifest),writer_and_export_state='New exclusive review output; no prior MP4',output_path=str(out),overwrite=False,media_lifecycle_receipt=str(ep/'Edit/pre-render-media-v01.md'),unresolved_required_fields=[]),render_receipt=None,qa_receipt=None,settings_check_receipt=None,render_provenance=None)
dump(ep/'Edit/export-contract-v02.json',passport)
