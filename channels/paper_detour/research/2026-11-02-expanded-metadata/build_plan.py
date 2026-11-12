from pathlib import Path
import json,re,hashlib,importlib.util,datetime
R=Path('/Users/diplomat/ytvideos');D=R/'new_channel/research/2026-11-02-expanded-metadata'
a=json.loads((D/'BEFORE.json').read_text());vid={x['id']:x for x in a['videos']}
paths={'0RaC4t7yn5o':'001_radio_game','85dwIXy_lZs':'001_radio_game/Shorts/01_radio_signal','7DygREwtxfY':'001_radio_game/Shorts/02_decoder','pdSgHe6ScTI':'002_margorie_mccall','xYS2XBeR_Jc':'003_iq_gallery','sA-PYrDl5H8':'008_boyfriend_brought_friend','r71aCn4p88A':'027_doomscrolling_short','-KW8jgSoEz0':'004_last_video','WQw7ny9svrk':'007_joshua_jessica','orQiLIvOL-8':'009_knorozov_asya','fvRm9Vxwagk':'028_taj_mahal','YRnIpr9P3iE':'033_time_stop'}
adds={'0RaC4t7yn5o':['#CassetteTape','#RadioUSP','#DataTransmission','#SoftwareHistory'],'85dwIXy_lZs':['#DataTransmission','#SoftwareDistribution'],'7DygREwtxfY':['#ClipInformatica','#RadioBroadcasting'],'fvRm9Vxwagk':['#Folklore','#IndianFolklore','#HistoricalLegends','#TajMahalLegend','#Architecture','#Storytelling','#PaperDetour'],'YRnIpr9P3iE':['#Shorts','#WhatIf','#ScienceFiction','#Superpowers','#LightAndSound','#Perception']}
reasons={'0RaC4t7yn5o':'Fill explicit storage medium, named station and program-transmission/history routes; preserve all technical caveats and chapters.','85dwIXy_lZs':'Add actual software distribution/data-transmission mechanism; keep recreation disclaimer and full-film link.','7DygREwtxfY':'Add exact show and broadcast route without suggesting verified game launch.','fvRm9Vxwagk':'Expand subject/genre/visual routes and identify the story as legend, not verified atrocity.','YRnIpr9P3iE':'Supply missing Shorts description tag and conditional what-if, superpower, light/sound and perception routes; no claim that time stopping is possible.'}
coverage={'pdSgHe6ScTI':'Name, Irish folklore, burial/robbers, legend genre and format covered; no claim of verified resurrection.','xYS2XBeR_Jc':'Reported IQ estimates, people and genre covered; no scientific ranking assertion.','sA-PYrDl5H8':'Dating conflict, friendship, boundaries, story genre and format covered; motive stays unknown.','r71aCn4p88A':'Hero, specific1888blizzard, geography, rescue/survival, women educators and format covered.','-KW8jgSoEz0':'Scrolling, time loss, social media, habits and digital wellbeing covered.','WQw7ny9svrk':'Griefbots, digital afterlife, technology and grief covered; no therapy/literal afterlife claims.','orQiLIvOL-8':'Knorozov/Asya, Maya writing, linguistics, monument and geography covered; chronology preserved.'}
newtitles={'fvRm9Vxwagk':vid['fvRm9Vxwagk']['snippet']['title']+' #TajMahal #Shorts','85dwIXy_lZs':vid['85dwIXy_lZs']['snippet']['title']+' #RetroComputing #Shorts'}
spec=importlib.util.spec_from_file_location('description_validator',R/'.agents/skills/ytv-youtube-descriptions/scripts/validate_description.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rows=[];preview=['# Paper Detour — expanded metadata rollout\n\n2026-11-02. User authorized upload031Private and updates to other editorial videos; later explicitly authorized coordinator to finish without Extra High after two empty responses. No publication/privacy changes for existing videos.\n']
for id,folder in paths.items():
 v=vid[id];s=v['snippet'];desc=s['description'];title=newtitles.get(id,s['title']);extra=adds.get(id,[])
 newdesc=desc
 if id=='fvRm9Vxwagk':newdesc=newdesc.replace('A dramatic paper-diorama retelling of Ahmad,','A dramatic paper-diorama retelling of the legend of Ahmad,',1)
 if extra:newdesc=newdesc.rstrip()+' '+' '.join(extra)
 tags=re.findall(r'#[A-Za-z0-9_]+',newdesc)
 assert len(tags)==len({x.lower() for x in tags}),id
 assert len(title)<=100 and len(newdesc.encode())<=5000 and '<' not in title+newdesc and '>' not in title+newdesc
 assert len(tags)+len(re.findall(r'#[A-Za-z0-9_]+',title))<=60
 original_tags=re.findall(r'#[A-Za-z0-9_]+',desc)
 assert all(tags.index(x)<len(original_tags) for x in original_tags)
 # Freeze all unchanged prose, links and chapters;028has an explicit authorized genre correction.
 body=desc[:desc.rfind('\n\n#')].strip() if '\n\n#' in desc else desc.strip()
 blocks=[{'label':'original_hashtags','text':' '.join(original_tags),'occurrences':1}]
 if id!='fvRm9Vxwagk':blocks.append({'label':'accepted_body_links_chapters','text':body,'occurrences':1})
 protected={'blocks':blocks}
 checked=mod.validate(newdesc,protected,desc);assert checked['valid'],checked
 out=R/'new_channel/videos'/folder/'Packaging/Metadata';out.mkdir(parents=True,exist_ok=True)
 (out/'DESCRIPTION_EN_EXPANDED_20261102.txt').write_text(newdesc)
 (out/'DESCRIPTION_EXPANDED_PROTECTED_20261102.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2)+'\n')
 (out/'TITLE_EN_EXPANDED_20261102.txt').write_text(title+'\n')
 row={'video_id':id,'episode_path':str(R/'new_channel/videos'/folder),'before_title':s['title'],'before_description':desc,'title':title,'description':newdesc,'description_hashtags':tags,'kept':original_tags,'added':extra,'removed':[],'reason':reasons.get(id,coverage.get(id)),'title_decision':'revise_hashtag_tail_only' if title!=s['title'] else 'keep','description_decision':'revise' if newdesc!=desc else 'keep','title_characters':len(title),'description_utf8_bytes':len(newdesc.encode()),'hashtag_count':len(tags),'coverage_status':'ready','exact_new_tag_usage':'unknown except existing own-catalog occurrences; search attempts and limits in RESEARCH.md','demand_trend':'unknown','validation':checked,'metadata_only':True,'privacy_before':v['status']['privacyStatus'],'status':'prepared' if newdesc!=desc or title!=s['title'] else 'no_change'}
 rows.append(row)
 preview+=['\n## '+id+' — '+row['status']+'\n\n'+title+'\n\n'+newdesc+'\n\nReason: '+row['reason']+'\n']
plan={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channel_id':a['channel']['id'],'scope':'12 existing current editorial videos;031separate upload','rows':rows,'excluded':[{'id':id,'reason':reason} for id,reason in {'OFqQ5PQwyMI':'Private grain preset test','NcJAyqebXC4':'Private grain test','4ZkHRuUEaYE':'Private grain test','8WNac9FGxKs':'Superseded private033comparison;currentversionYRnIpr9P3iE','QqMudxBNZgo':'Zero-duration technical livestream'}.items()],'protected':'Existing covers, category/languages/Tags,status/privacy/schedule, all playlist memberships/order,radio active title-thumbnail A/B variants; titles only2Shorts append exact tails.'}
(D/'PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');(D/'PREVIEW.md').write_text(''.join(preview))
print(json.dumps({'scope':len(rows),'changes':[{'id':x['video_id'],'title_characters':x['title_characters'],'hashtags':x['hashtag_count']} for x in rows if x['status']=='prepared'],'no_change':sum(x['status']=='no_change' for x in rows),'excluded':len(plan['excluded'])},indent=2))
