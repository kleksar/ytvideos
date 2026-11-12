from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np

ep=Path(sys.argv[1])
work=ep/'Work/sound_v04'
source=ep/'Work/sound_draft_v01'
prior_mix=source/'mix_draft_v02.wav'
prior_bed=source/'music_draft_v02.wav'
voice=ep/'Source/Voice/voice_en_v01/voice_en.mp3'
sr=44100

def decode(path):
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-f','f64le','-ac','1','-ar',str(sr),'-'])
    return np.frombuffer(pcm,dtype='<f8')

def write_pcm(samples,path):
    subprocess.run(['ffmpeg','-v','error','-n','-f','f64le','-ar',str(sr),'-ac','1','-i','-',
                    '-c:a','pcm_s24le',str(path)], input=samples.astype('<f8').tobytes(),check=True)

def db(x):
    return round(float(20*np.log10(max(x,1e-12))),3)

def rms(x):
    return float(np.sqrt(np.mean(x*x)))

mix=decode(prior_mix)
music=decode(prior_bed)
n=len(mix)
assert len(music)==n==24688944
speech=mix-music
original=decode(voice)
assert len(original)==n
delta=db(rms(speech-original))
assert delta<-90, delta
t=np.arange(n,dtype=np.float64)/sr
points=[
 (0,3.2),(20,4.2),(84,3.1),(100,3.2),(106,1),(112,3.2),(143,3.3),(158,2.0),
 (168,3.1),(233,3.4),(250,2.8),(255,4.2),(278,5.25),(310,6.35),(320,6.1),
 (337,3.45),(345,1.8),(354,3.2),(393,3.8),(423,3.3),(446,4.0),(461,3.0),(482,3.8),
 (496.0,3.5),(501.3,3.0),(503.25,.04),(510.5,.04),(511.7,3.3),(515.2,5.0),
 (522.0,5.25),(527.0,4.8),(530.7,2.1),(537.0,1.6),(542.8,2.4),(551.0,3.3),(556.0,0),(559.84,0)]
a=np.asarray(points)
bed=music*np.interp(t,a[:,0],a[:,1])
# Soft upper partials add movement on small speakers. The return after the ship
# reveal uses sustained open intervals rather than a second narration-like line.
add=np.zeros(n)
for start,stop,freqs,level,attack,release in [
 (258,280,(293.66,440.0),.012,4,4),
 (278,302,(261.63,392.0),.015,5,5),
 (300,322,(293.66,440.0),.022,5,4),
 (320,339,(261.63,392.0),.010,3,6),
 (510.67,521,(293.66,440.0,587.33),.023,2.1,3.5),
 (518,531,(329.63,440.0,659.25),.023,4.0,2.5),
 (544,559.84,(293.66,440.0),.010,4.0,5.0)]:
 i,j=round(sr*start),min(n,round(sr*stop)); u=t[i:j]-start
 e=np.sin(np.pi/2*np.clip(u/attack,0,1))**2*np.sin(np.pi/2*np.clip((stop-start-u)/release,0,1))**2
 partial=np.zeros(len(u))
 for k,f in enumerate(freqs):
  partial+=(.76**k)*(np.sin(2*np.pi*f*u+.12*np.sin(2*np.pi*.24*u))+.08*np.sin(4*np.pi*f*u))
 add[i:j]+=level*e*partial/len(freqs)
bed+=add
# Leave headroom for the narration at the loudest crossing beats.
bed*=np.interp(t,[0,278,299,320,338,559.84],[1,1,.76,.76,1,1])

final=speech+bed
assert np.max(np.abs(final))<.985
target=work/'mix_en_v04.wav'
stem=work/'music_en_v04.wav'
write_pcm(bed,stem)
write_pcm(final,target)
regions={'intro':(7,30),'crossing_start':(257,279),'crossing_high':(301,319),
         'ship_o':(503.25,510.5),'ship_reveal':(513,525),'memorial':(538,543)}
stats={}
for name,(start,end) in regions.items():
 sl=slice(round(start*sr),round(end*sr)); s,b=map(lambda x: db(rms(x[sl])),(speech,bed))
 stats[name]={'seconds':[start,end],'voice_rms_dbfs':s,'music_rms_dbfs':b,
              'voice_minus_music_rms_db':round(s-b,3),'music_change_db':round(b-db(rms(music[sl])),3)}
assert stats['ship_reveal']['music_rms_dbfs']-stats['ship_o']['music_rms_dbfs']>25
assert stats['crossing_high']['music_change_db']>12
assert db(rms((decode(target)-decode(stem))-speech))<-120
def ref(path):
 h=hashlib.sha256()
 with path.open('rb') as file:
  for chunk in iter(lambda:file.read(1024*1024),b''): h.update(chunk)
 return {'path':str(path),'sha256':h.hexdigest()}
report={'final_mix':ref(target),'music':ref(stem),'previous_mix':ref(prior_mix),'previous_music':ref(prior_bed),
        'voice':ref(voice),'samples':n,'sample_rate':sr,'voice_delta_from_original_rms_dbfs':delta,
        'sample_peak_dbfs':db(np.max(np.abs(final))),'regions':stats,'music_automation':points,
        'source_rights':'Original episode synthesized score and locally synthesized added partials. No third-party recordings or samples.',
        'subjective_audio_listening':'UNVERIFIED'}
(work/'AUDIO_HANDOFF_v04.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(stats,indent=2))
