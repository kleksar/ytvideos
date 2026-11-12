"""Complete the full-film visual revision, retaining the fixed narration and timing grid."""
import json
from pathlib import Path

E = Path(__file__).resolve().parents[2]
d = json.loads((E/'Storyboard/storyboard_v02_timing_conform_draft.json').read_text())
d.update(status='AUTHOR_ACCEPTED_PRODUCTION_STORYBOARD', authorization='User accepted revision brief; explicitly waived Extra High for 032; subsequently authorized complete production and Private YouTube review upload.', new_images_created='Three church sources made; three full-film replacements planned below.', unassigned_church_slots=0)
d['revision_logic'] = {
    'opening_payoff':'R001 establishes the elevated threshold and missing ground. R102 deliberately returns to the identical file during lived reconstruction. R125 returns to the same illustrative house after fill and permanent foundation; this is a visual motif, not an identified household biography.',
    'two_defenses':'R070 shows the seawall alone. R071–R072 keep land behind it low. Only R073–R074 reveal the second intervention. The 9/16/17-foot facts are spoken in separate contexts, never put on a common numerical axis.',
    'human_cost':'R089–R106 move between occupied houses, changing utilities, fill, boardwalks and household expense. No invented invoice, quotation, property owner identity or exact canal route.',
    'church':'CH01 authentic photograph on physical carrier; CH02 reconstruction whole; CH03 small tool; CH04 coordinated human stations; CH05 whole-building payoff.',
    'ending_time':'R116–R122 show later storms and limits of protection. R123–R127 are retrospective project/loss images under reflective narration; R128 returns to the modern coastline. No claim that all shots follow a continuous day.',
    'quiet_sections':'R048–R060 remain restrained and non-graphic. One sober minimum-death-toll cue; otherwise give loss and recovery images room.'}
new = {
 'R072':('Source/Images/revision_v02/R072_v01.png', 'One complete handmade card engineering maquette, same warm gray physical tabletop, blue layered sea on LEFT, a thick pale concrete seawall in center and three small cream timber houses on RIGHT. Oblique side view from landward side: the ground behind the seawall is visibly still low, a clear empty vertical difference to the wall crest. No raised earth yet, no flooding behind the wall, no figures, arrows, labels, numerals or second panel. This is an illustrative physical model, not a measured scale diagram. Keep wall top, complete sea edge and houses inside inner 80 percent; leave quiet upper area for accent. Reference scene_070_v01 establishes material and side orientation.', 'The wall does not remove the low land behind it.'),
 'R074':('Source/Images/revision_v02/R074_v01.png', 'One complete handmade paper/card physical engineering maquette in the SAME world as scene_070_v01: blue layered Gulf at LEFT, thick pale seawall in middle-left, three cream period houses on RIGHT. Change the land behind the wall: visible layered warm sand fill now forms a higher, gently sloping grade behind the seawall; the nearest house is safely supported on temporary timber cribbing above a small remaining unfilled pocket, showing that structures must be supported before fill reaches them. One continuous material model, not split-screen, no labels/arrows/numerical datum, no universal height claim. Protect wall, fill surface, supported house; quiet upper quarter for cue.', 'Only now reveal the second defense: change the ground while supporting buildings.'),
 'R125':('Source/Images/revision_v02/R125_v01.png', 'Return to the SAME illustrative cream clapboard porch house from scene_001_v01, with blue-gray shutters, central open dark doorway, pale turned porch posts and porch balustrade. Keep recognizably the same eye-level frontal geometry, but frame a little wider to preserve the roof/porch and ground margin. It is now after grade raising: warm compact sand and a rebuilt modest pedestrian path reach the house, permanent masonry foundation replaces exposed temporary cribbing, a short safe grounded step meets the porch. No elevated plank over a void; the open air beneath the entrance has become ground. A tiny exposed side strip shows layered sand beside the permanent foundation, not an underground transparent house. Clear morning Gulf light, honest modest completion, no utopian city. No people, text, labels or numbers. Upper center reserve only quiet wall/sky, do not obscure doorway.', 'Answer the opening threshold: the changed ground now meets the home.')}
cue_specs = [
 ('P01','R006',['HOW DO YOU','SAVE A CITY?'],618,714,'question','The rebuilding question is the hook; deliberately give it visual weight rather than repeat every sentence.'),
 ('C03','R013',['less than nine feet'],1545,1620,'scale','Retain an intentional key quantity; natural ground estimate, not the seawall datum.'),
 ('C04','R021',['no weather satellites'],2525,2585,'information limit','Intentional key absence in 1900 forecasting, not an exhaustive list revealed early.'),
 ('C05','R035',['nearly sixteen feet'],4546,4606,'surge magnitude','Retain estimated surge wording in its own scene, separate from all other levels.'),
 ('C06','R055',['at least six thousand'],7083,7145,'minimum loss','Sober minimum, not exact total; crosses into R056 and must be checked on both images.'),
 ('C07','R068',['better chance next time'],8835,8889,'turning question','A deliberate forward-looking hinge after the immediate recovery.'),
 ('P02','R072',['A WALL',"ISN’T ENOUGH"],9258,9340,'contrast','Reveal the landward problem after the wall, without showing the next solution early.'),
 ('C09','R074',['raise the ground'],9497,9565,'second intervention','Intentional literal engineering turning point, after the wall has been explained.'),
 ('C10','R078',['seventeen feet'],10050,10113,'wall height','Height above mean low water, no comparison axis to natural ground or surge.'),
 ('C11','R083',['About two thousand buildings'],10702,10777,'distributed scale','Keep about and buildings; do not substitute count of all structures.'),
 ('P03','R090',['THE CITY','STILL LIVED'],11670,11750,'human continuity','Add the contrast of ordinary life persisting inside the construction site.'),
 ('C13','R096',['the new ground'],12667,12721,'physical payoff','Intentional label on the moment fill becomes the city’s supporting ground.'),
 ('P04','R104',['REBUILDING','HAD A PRICE'],13665,13745,'human burden','Connect public engineering to household expense; no invented sum or bill.'),
 ('T01','CH03',['700 JACKS','ONE CHURCH'],14498,14563,'many to one','The relation between small instruments and one immense building; one tool in image.'),
 ('T02','CH05',['MANY HANDS','ONE BUILDING'],14743,14833,'collective action','A complementary human-scale conclusion anchored to patient coordination, not literal highlighting of the final word lifts.'),
 ('P05','R120',['SAFER','NOT INVULNERABLE'],15990,16062,'limit','Frame the contrast between improved defense and continuing hurricane risk.'),
 ('P06','R125',['GROUND','UNDER THE DOOR'],16713,16798,'opening answer','Connect the completed foundation and filled ground back to the opening doorstep.')]
d['accent_plan'] = []
for cid,sid,lines,a,b,function,why in cue_specs:
    literal = ' '.join(lines) if cid.startswith('C') else {'P01':'how do you save a city','P02':'a problem behind it','P03':'a living city','P04':'property owners had to pay','P05':'did not make Galveston invulnerable','P06':'changed the ground','T01':'seven hundred jacks','T02':'many smaller lifts'}[cid]
    d['accent_plan'].append({'id':cid,'scene_id':sid,'lines':lines,'in_frame':a,'out_frame_exclusive':b,'function':function,'decision':{'literal_candidate':literal,'complementary_candidate':' / '.join(lines),'no_text_candidate':'Image and narration remain understandable; omit if both safe anchors are occupied.','selected':'literal key emphasis' if cid.startswith('C') else 'complementary framing','reason':why},'hold_frames':b-a-9,'timing_status':'ALIGNMENT_BASED_UNLISTENED','anchor':'alternate' if cid=='T02' else 'primary'})
ch_files=['Source/Images/church_v02/CH01_actual_archive_v02.png','Source/Images/paper_v01/scene_107_v01.png','Source/Images/church_v02/CH03_v01.png','Source/Images/church_v02/CH04_v01.png','Source/Images/paper_v01/scene_110_v01.png']
ch_jobs=['Authentic 1907 archive integrated as unchanged photograph on a physical card carrier.','Whole reconstructed church, supported above ground.','Macro screw jack with load-contact, continuous beam and timber cribbing.','Three representative workers at three jack stations, medium side view.','Whole church returns after the tools and human coordination.']
for i,r in enumerate(d['scenes']):
    sid=r['scene_id'];r['timing_status']='PRODUCTION_GRID_CHARACTER_ALIGNMENT_DIVIDED_BY_1_05; no subjective listening'
    r['approved_revision_tasks']=[]
    if sid in new:
        path,prompt,purpose=new[sid];r.update(image_path=path,image_status='PLANNED',paper_composition_prompt_en=prompt,narrative_job=purpose,composition_status='NEW_COMPOSITION_FIXED_FOR_GENERATION')
    elif sid.startswith('CH'):
        j=int(sid[2:])-1;r.update(image_path=ch_files[j],image_status='AUTHOR_VISUALLY_REVIEWED',paper_composition_prompt_en=ch_jobs[j],narrative_job=ch_jobs[j],composition_status='CHURCH_BLOCK_V02');r['composition_record']='Storyboard/CHURCH_BLOCK_v02.md'
    elif sid=='R102':
        r.update(image_path='Source/Images/paper_v01/scene_001_v01.png',narrative_job='Deliberate return to the identical opening threshold; the voice now explains everyday access above the fill.',composition_status='REUSE_EXACT_OPENING_MOTIF')
    else:
        r['narrative_job']=r['source_nuviko_prompt_en'];r['composition_status']='RETAIN_ACCEPTED_COMPLETE_DI0RAMA_WITH_NEW_4_6_SECOND_INTERVAL'
    r['accent_cue_ids']=[c['id'] for c in d['accent_plan'] if c['scene_id']==sid or (sid=='R056' and c['id']=='C06')]
    r['caption_status']=' '.join(r['accent_cue_ids']) if r['accent_cue_ids'] else 'NO TEXT: allow the narrated action/state to carry this beat; avoid duplicating it.'
    oldmode=['pan-right','push-in','pan-left','pan-up','pull-out','pan-down'][i%6]
    r['motion']={'camera':oldmode,'preset':'gentle-aligned','depth_zoom':1,'protected':'Faces, hands, important building edges, supports and action object; inspect whole trajectory and final composite.','envelope':'gentle camera endpoint deviations; ordinary fill overscan 1.03–1.07; reduce individually if source edge margin is insufficient.'}
    if sid in ('R072','R074'):r['motion'].update(camera='pull-out',depth_zoom=.98,protected='Complete wall crest, model houses, material boundary and ground; no numerical common datum.')
    if sid in ('R001','R102','R125'):r['motion'].update(camera='push-in' if sid!='R102' else 'pull-out',protected='Door threshold, porch supports/permanent foundation, full safe walkway; upper lettering must leave the opening visible.')
    if sid.startswith('CH'):
        j=int(sid[2:])-1;r['motion'].update(camera=['push-in','pull-out','pan-right','pull-out','pan-right'][j],depth_zoom=[1,.95,1,1,.95][j],envelope='Explicit reviewed two-point path in editorial pilot; archive planar depth preserves source content; top anchoring on whole church shots.')
    r['factual_guardrail']=r.get('factual_guardrail','Historical reconstruction, not an exact event photograph; no invented quotes or personal identity.')
    r['cut']='direct';r['grain']='g08'
assert len(d['scenes'])==129
assert all(120<=r['out_frame_exclusive']-r['in_frame']<=180 for r in d['scenes'])
assert d['scenes'][0]['in_frame']==0 and d['scenes'][-1]['out_frame_exclusive']==17233
assert all(a['out_frame_exclusive']==b['in_frame'] for a,b in zip(d['scenes'],d['scenes'][1:]))
d['checks'].update(full_creative_coverage='129 explicit compositions and caption/no-caption choices',source_text_unchanged=True,source_voice_unchanged=True,independent_review='NOT_PERFORMED',full_film_edit='PENDING',new_sources='PLANNED files are not yet accepted PNGs')
(E/'Storyboard/storyboard_v02.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
out=['# Galveston 032 — production storyboard v02','', 'Author acceptance, 2026-11-02. Complete 129-shot production plan. Fixed English Odom narration, no new sound. 17233 frames / 30fps. Every shot 4–6 seconds. Timing derives from actual character alignment /1.05; subjective listening remains unverified. User waived Extra High for032 and authorized complete production plus Private YouTube review. New image files explicitly PLANNED until generated and inspected.','']
out += ['## Visual structure','']+[f'- **{k}**: {v}' for k,v in d['revision_logic'].items()]
out += ['', '## Shot-by-shot','']
for r in d['scenes']:
    out += [f"### {r['scene_id']} · {r['in_frame']}–{r['out_frame_exclusive']} · {(r['out_frame_exclusive']-r['in_frame'])/30:.3f}s",'',f"Voice: {r['current_spoken_words']}",'',f"Purpose/composition: {r['narrative_job']}",'',f"Source: `{r['image_path']}` — {r['image_status']}. {r['composition_type']}.",'',f"Accent: {r['caption_status']}",'',f"Motion: {r['motion']['camera']}; depth framing {r['motion']['depth_zoom']}; G08 after camera. Protected: {r['motion']['protected']}",'',f"Guardrail: {r['factual_guardrail']}",'']
out += ['## Accent decisions','']
for c in d['accent_plan']:
    z=c['decision'];out += [f"- **{c['id']}** {c['scene_id']} {c['in_frame']}–{c['out_frame_exclusive']}: {' / '.join(c['lines'])}. Literal: {z['literal_candidate']}. Complement: {z['complementary_candidate']}. No-text: {z['no_text_candidate']}. Choice: {z['selected']}; {z['reason']} Hold {c['hold_frames']} frames; entry/exit 4 frames each. Alignment based; listening unverified."]
out += ['', 'The complete JSON carries exact generation briefs, motion envelopes and all retained source provenance. Storyboard acceptance does not certify new PNGs, final framing, export, subtitles or YouTube state.']
(E/'Storyboard/storyboard_v02.md').write_text('\n'.join(out)+'\n')
print(json.dumps({'scenes':129,'new_full_film_images':list(new),'cues':len(d['accent_plan']),'coverage_frames':17233}))
