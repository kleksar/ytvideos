"""Synthetic export passports for settings and release-gate regression tests."""
from math import gcd

def passport(m, manifest, prepared, audio, output, encoder='libx264', video_bitrate='800k'):
    w,h=prepared['canvas'];g=gcd(w,h);copy=audio['codec_name']=='aac'
    target='STREAM_COPY' if copy else ('256k' if int(audio['channels'])>=2 else '192k')
    return {'status':'READY_TO_RENDER','edit':{'timeline_id':str(manifest)},
            'timeline':{'width':w,'height':h,'aspect_ratio':f'{w//g}:{h//g}','sample_aspect_ratio':'1:1',
                        'fps':'30/1','frame_count':prepared['frames'],'duration_seconds':prepared['frames']/30,
                        'output_color_space':'Rec.709 SDR'},
            'required_delivery':{'container':'MP4','video':{'codec_name':'h264','pix_fmt':'yuv420p',
                'scan':'progressive','cadence':'constant 30/1 fps','color_primaries':'bt709','color_transfer':'bt709',
                'color_space':'bt709','color_range':'tv'},
                'audio_contract':{'accepted_complete_mix':m.delivery.file_record(prepared['audio']),
                    'codec_name':'aac','profile':'LC','channels':int(audio['channels']),
                    'sample_rate':int(audio['sample_rate']),'target_bit_rate':target}},
            'encoding':{'requested_arguments':{'encoder':encoder,'video_bitrate':video_bitrate,
                        'audio_bitrate':target}},
            'preflight':{'output_path':str(output),'unresolved_required_fields':[]}}
