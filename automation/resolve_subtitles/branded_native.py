"""Native Fusion graph authoring, embedded in official MCP run_script.

Caller supplies validated numeric layout, a new owned clip and an owned .comp path.
No filesystem access, external render, or font fallback here.
"""

def color_parts(value):
    value=value.lstrip('#')
    return [int(value[i:i+2],16)/255 for i in (0,2,4)]+[int(value[6:8],16)/255 if len(value)==8 else 1]


def phrase_expression(record):
    return f"iif(time >= {record['first']} and time < {record['last']}, 1, 0)"


def highlight_expression(record, active, neutral):
    if record['active_first'] is not None:
        return f"iif(time >= {record['active_first']} and time < {record['active_last']}, {active}, {neutral})"
    return None


def named_tool(comp, name, kind):
    tool=comp.FindTool(name)
    attrs=tool.GetAttrs() if tool else {}
    require(attrs.get('TOOLS_Name')==name and attrs.get('TOOLS_RegID')==kind,
            'Native caption topology tool differs: '+name)
    return tool


def require_connection(target, control, source_name, source_kind):
    inlet=getattr(target,control,None)
    output=inlet.GetConnectedOutput() if inlet else None
    source=output.GetTool() if output else None
    attrs=source.GetAttrs() if source else {}
    require(attrs.get('TOOLS_Name')==source_name and attrs.get('TOOLS_RegID')==source_kind,
            'Native caption topology connection differs: '+control)


def verify_caption_graph(comp, shot, recipe):
    neutral,active,outline=(color_parts(recipe[k]) for k in ('neutral','active','outline'))
    bg=named_tool(comp,'CaptionBackground','Background')
    for key,value in (('UseFrameFormatSettings',0),('Width',recipe['raster'][0]),
                      ('Height',recipe['raster'][1]),('TopLeftAlpha',0)):
        require(bg.GetInput(key,0)==value,'Native transparent background differs: '+key)
    previous_name,previous_kind='CaptionBackground','Background'
    for record in shot.get('panels',[]):
        name=record['name'];panel=named_tool(comp,name,'Background');mask=named_tool(comp,name+'Mask','RectangleMask')
        color=color_parts(recipe['panel']['color'])
        for key,value in dict(UseFrameFormatSettings=0,Width=recipe['raster'][0],Height=recipe['raster'][1],
                              TopLeftRed=color[0],TopLeftGreen=color[1],TopLeftBlue=color[2],TopLeftAlpha=color[3]).items():
            require(abs(panel.GetInput(key,0)-value)<1e-6,'Native panel color/raster changed')
        center=mask.GetInput('Center',0)
        require(abs(center[1]-record['x'])<1e-8 and abs(center[2]-record['y'])<1e-8,'Native panel position changed')
        for key,value in (('Width',record['width']),('Height',record['height']),('CornerRadius',0),('SoftEdge',0)):
            require(abs(mask.GetInput(key,0)-value)<1e-8,'Native panel geometry changed')
        require_connection(panel,'EffectMask',name+'Mask','RectangleMask')
        display=named_tool(comp,name+'Display','Merge')
        require(display.Blend.GetExpression()==phrase_expression(record),'Native panel timing changed')
        require_connection(display,'Foreground',name,'Background');require_connection(display,'Background',previous_name,previous_kind)
        previous_name,previous_kind=name+'Display','Merge'
    for record in shot['nodes']:
        word=named_tool(comp,record['name'],'TextPlus')
        require(word and word.GetInput('StyledText',0)==record['text'],'Native word text readback differs')
        require(word.GetInput('Font',0)==recipe['font']['family'] and word.GetInput('Style',0)==recipe['font']['style'],'Native font inputs differ')
        center=word.GetInput('Center',0)
        require(center and abs(center[1]-record['x'])<1e-8 and abs(center[2]-record['y'])<1e-8,'Native word geometry changed')
        numeric={'Size':recipe['native_size'],'UseFrameFormatSettings':0,'Width':recipe['raster'][0],
                 'Height':recipe['raster'][1],'Enabled2':1,'Thickness2':recipe['native_outline'],
                 'Red2':outline[0],'Green2':outline[1],'Blue2':outline[2],'Alpha2':outline[3],'Alpha1':neutral[3]}
        for key,expected in numeric.items():
            value=word.GetInput(key,0)
            require(isinstance(value,(int,float)) and abs(value-expected)<1e-6,'Native style/raster input differs: '+key)
        for n,key in enumerate(('Red1','Green1','Blue1')):
            expression=highlight_expression(record,active[n],neutral[n])
            observed=getattr(word,key).GetExpression()
            if expression is None:
                value=word.GetInput(key,0)
                require(not observed and isinstance(value,(int,float)) and abs(value-neutral[n])<1e-6,
                        'Native neutral color differs: '+key)
            else:
                require(observed==expression,'Native highlight expression differs: '+key)
        name='Display'+str(record['index'])
        display=named_tool(comp,name,'Merge')
        require(display.Blend.GetExpression()==phrase_expression(record),'Native phrase timing differs')
        require_connection(display,'Foreground',record['name'],'TextPlus')
        require_connection(display,'Background',previous_name,previous_kind)
        previous_name,previous_kind=name,'Merge'
    require_connection(named_tool(comp,'MediaOut1','MediaOut'),'Input',previous_name,previous_kind)


def author_caption_comp(item, shot, recipe, export_path):
    fonts=resolve.Fusion().FontManager.GetFontList()
    require(isinstance(fonts,dict) and recipe['font']['style'] in fonts.get(recipe['font']['family'],{}), 'Required native font face unavailable; no fallback')
    c=item.AddFusionComp()
    require(c, 'Cannot create native caption comp')
    c.Lock()
    try:
        out=c.FindTool('MediaOut1')
        require(out,'Native MediaOut missing')
        bg=c.AddTool('Background',-4,0)
        require(bg,'Native transparent background missing')
        bg.SetAttrs({'TOOLB_NameSet':True,'TOOLS_Name':'CaptionBackground'})
        bg.SetInput('UseFrameFormatSettings',0)
        bg.SetInput('Width',recipe['raster'][0]);bg.SetInput('Height',recipe['raster'][1])
        bg.SetInput('TopLeftAlpha',0)
        chain=bg
        neutral,active,outline=(color_parts(recipe[k]) for k in ('neutral','active','outline'))
        for record in shot.get('panels',[]):
            name=record['name'];panel=c.AddTool('Background',-5,-2);mask=c.AddTool('RectangleMask',-6,-2)
            require(panel and mask,'Cannot create editable native panel')
            panel.SetAttrs({'TOOLS_Name':name});mask.SetAttrs({'TOOLS_Name':name+'Mask'})
            color=color_parts(recipe['panel']['color'])
            for key,value in dict(UseFrameFormatSettings=0,Width=recipe['raster'][0],Height=recipe['raster'][1],
                                  TopLeftRed=color[0],TopLeftGreen=color[1],TopLeftBlue=color[2],TopLeftAlpha=color[3]).items():panel.SetInput(key,value)
            mask.SetInput('Center',{1:record['x'],2:record['y']})
            for key,value in (('Width',record['width']),('Height',record['height']),('CornerRadius',0),('SoftEdge',0)):mask.SetInput(key,value)
            require(panel.ConnectInput('EffectMask',mask),'Cannot connect native panel mask')
            merge=c.AddTool('Merge',-3,-2);require(merge,'Cannot create native panel Merge')
            merge.SetAttrs({'TOOLS_Name':name+'Display'})
            require(merge.ConnectInput('Foreground',panel) and merge.ConnectInput('Background',chain),'Cannot compose panel')
            merge.Blend.SetExpression(phrase_expression(record));chain=merge
        for index,record in enumerate(shot['nodes']):
            word=c.AddTool('TextPlus',-3-index%4,-4-index//4)
            require(word,'Cannot add editable Text+')
            word.SetAttrs({'TOOLS_Name':record['name']})
            inputs={'StyledText':record['text'],'Font':recipe['font']['family'],
                    'Style':recipe['font']['style'],'Size':recipe['native_size'],
                    'UseFrameFormatSettings':0,'Width':recipe['raster'][0],'Height':recipe['raster'][1],
                    'Center':{1:record['x'],2:record['y']},'Enabled2':1,
                    'Thickness2':recipe['native_outline'],'Red2':outline[0],'Green2':outline[1],
                    'Blue2':outline[2],'Alpha2':outline[3],'Alpha1':neutral[3]}
            for key,value in inputs.items():word.SetInput(key,value)
            for n,key in enumerate(('Red1','Green1','Blue1')):
                word.SetInput(key,neutral[n])
                expression=highlight_expression(record,active[n],neutral[n])
                if expression is not None:
                    getattr(word,key).SetExpression(expression)
            merge=c.AddTool('Merge',index%12,index//12)
            require(merge,'Cannot add native word Merge')
            merge.SetAttrs({'TOOLS_Name':'Display'+str(record['index'])})
            require(merge.ConnectInput('Foreground',word) and merge.ConnectInput('Background',chain),'Cannot compose native word')
            merge.Blend.SetExpression(phrase_expression(record))
            require(merge.Blend.GetExpression()==phrase_expression(record),'Phrase expression readback differs')
            chain=merge
        require(out.ConnectInput('Input',chain),'Native MediaOut not connected')
        require(c.Save(export_path),'Cannot serialize native comp; do not import stale file')
    finally:
        c.Unlock()
    # Crucial proven Paper route: live-created graph/node values can look valid
    # while final composite is blank. Always reimport, activate, then sample later.
    before_names=item.GetFusionCompNameList() or []
    rebound=item.ImportFusionComp(export_path)
    require(rebound,'Cannot reimport serialized native comp')
    names=item.GetFusionCompNameList() or []
    new_names=[name for name in names if name not in before_names]
    # Resolve 21.2 can replace the sole newly-created composition in place.
    # Accept only that unambiguous single-comp case or one uniquely added name.
    if len(names)==1 and len(before_names)==1 and names==before_names:
        active_name=names[0]
    else:
        require(len(names)==len(before_names)+1 and len(new_names)==1 and names.count(new_names[0])==1,
                'Cannot identify imported native comp')
        active_name=new_names[0]
    active=item.LoadFusionCompByName(active_name)
    require(active,'Cannot activate imported native comp')
    verify_caption_graph(rebound,shot,recipe)
    verify_caption_graph(active,shot,recipe)
    return dict(words=len(shot['nodes']),serialized_comp=export_path,visual='UNVERIFIED')


def verify_branded(candidate, base, before, layout, token, expected_cc, replace_tracks):
    require(candidate.GetMarkerByCustomData(token),'Unowned branded candidate')
    require(candidate.GetStartFrame()==base.GetStartFrame() and candidate.GetEndFrame()==base.GetEndFrame(),'Branded duration changed')
    require(candidate.GetTrackCount('video')==base.GetTrackCount('video')+1,'Branded track count changed')
    require(content_signature(candidate,'video')[:-1]==content_signature(base,'video'),'Original picture clips changed')
    require(content_signature(candidate,'audio')==content_signature(base,'audio'),'Original audio changed')
    for kind in ('audio','video'):
        for track in range(1,base.GetTrackCount(kind)+1):
            desired=False if kind=='video' and track in replace_tracks else before[kind+'_track_state'][str(track)]
            require(bool(candidate.GetIsTrackEnabled(kind,track))==desired,'Original track state changed')
    require(candidate.GetTrackCount('subtitle')==1 and not candidate.GetIsTrackEnabled('subtitle',1),'Independent CC track changed')
    require(cue_readback(candidate)==expected_cc,'Independent CC timing changed')
    lane=candidate.GetTrackCount('video')
    require(candidate.GetIsTrackEnabled('video',lane),'Branded lane disabled')
    clips=candidate.GetItemListInTrack('video',lane) or []
    require(len(clips)==len(layout['shots']),'Branded clip count changed')
    for item,shot in zip(clips,layout['shots']):
        require((item.GetStart(),item.GetEnd())==(shot['start_frame'],shot['end_frame']),'Branded clip bounds changed')
        names=item.GetFusionCompNameList() or []
        require(names and len(set(names))==len(names),'Editable native comp missing or ambiguous')
        comp=item.LoadFusionCompByName(names[-1])
        require(comp,'Cannot activate owned native comp')
        verify_caption_graph(comp,shot,layout['recipe'])
    return len(clips)


def require_picture_cut(item, shot):
    if shot.get('picture_cut_anchor'):
        require(item.GetStart()==shot['start_frame'],
                'Declared display anchor is not an actual carrier picture cut')


def install_branded(resolve, target, before, layout, expected_cc, srt_path, comp_paths, candidate_name, token, replace_tracks):
    manager,project,base=identity(resolve,target)
    require(snapshot(resolve,target)==before,'Source changed since final-VO verification')
    require(len(comp_paths)==len(layout['shots']),'Missing owned comp paths')
    require(len(set(replace_tracks))==len(replace_tracks) and all(type(x) is int and 1<=x<=base.GetTrackCount('video') for x in replace_tracks),'Invalid replacement-track declaration')
    fonts=resolve.Fusion().FontManager.GetFontList()
    require(isinstance(fonts,dict) and layout['recipe']['font']['style'] in fonts.get(layout['recipe']['font']['family'],{}),'Native font face missing')
    original={item.GetUniqueId():item for item in items(base,'video')}
    carriers=[]
    for shot in layout['shots']:
        item=original.get(shot['carrier_id'])
        require(item and item.GetStart()<=shot['start_frame']<shot['end_frame']<=item.GetEnd(),'Carrier does not cover exact authored section')
        require_picture_cut(item,shot)
        require(item.GetSpeed().get('Percentage')==100,'Retimed carrier unsupported')
        require(item.GetMediaPoolItem(),'Carrier media unavailable')
        carriers.append(item)
    require(manager.SaveProject(),'Cannot checkpoint source')
    found=[project.GetTimelineByIndex(i) for i in range(1,project.GetTimelineCount()+1)
           if project.GetTimelineByIndex(i).GetName()==candidate_name]
    require(len(found)<=1,'Ambiguous branded candidate')
    candidate=None;created=False;lane=None
    try:
        if found:
            candidate=found[0]
            require(candidate.GetMarkerByCustomData(token),'Unowned branded candidate name')
            require(project.SetCurrentTimeline(candidate),'Cannot inspect branded candidate')
            verify_branded(candidate,base,before,layout,token,expected_cc,replace_tracks)
            return dict(status='UNCHANGED',candidate_id=candidate.GetUniqueId(),name=candidate_name,native_cues=len(expected_cc),branded_style='NATIVE_AUTHORED',visual='UNVERIFIED',playback='UNVERIFIED')
        candidate=base.DuplicateTimeline(candidate_name);created=bool(candidate)
        require(candidate and project.SetCurrentTimeline(candidate),'Cannot create branded candidate')
        for kind in ('audio','video'):
            for track in range(1,base.GetTrackCount(kind)+1):
                desired=False if kind=='video' and track in replace_tracks else before[kind+'_track_state'][str(track)]
                require(candidate.SetTrackEnable(kind,track,desired),'Cannot preserve source track state')
        require(candidate.AddTrack('video'),'Cannot create editable caption lane')
        lane=candidate.GetTrackCount('video')
        require(candidate.SetTrackName('video',lane,'Editable word highlights | '+token[-12:]),'Cannot name caption lane')
        require(candidate.SetTrackEnable('video',lane,True),'Cannot activate caption lane')
        pool=project.GetMediaPool()
        for item,shot,path in zip(carriers,layout['shots'],comp_paths):
            first=item.GetLeftOffset()+shot['start_frame']-item.GetStart()
            last=first+shot['end_frame']-shot['start_frame']
            added=pool.AppendToTimeline([dict(mediaPoolItem=item.GetMediaPoolItem(),startFrame=first,endFrame=last,mediaType=1,trackIndex=lane,recordFrame=shot['start_frame'])])
            require(added and len(added)==1,'Native caption carrier append failed')
            clip=added[0]
            require((clip.GetStart(),clip.GetEnd())==(shot['start_frame'],shot['end_frame']),'Native carrier timing differs; no guessed retime')
            clip.SetName(shot['id']+' | editable captions')
            author_caption_comp(clip,shot,layout['recipe'],path)
        # Same speech-only SRT contract as Phase 1, independent of display holds.
        for track in range(candidate.GetTrackCount('subtitle'),0,-1):
            require(candidate.DeleteTrack('subtitle',track),'Cannot prepare independent CC')
        require(candidate.AddTrack('subtitle'),'Cannot create independent CC')
        imported=pool.ImportMedia([srt_path]);require(imported and len(imported)==1,'Cannot import speech SRT')
        pool.AppendToTimeline([dict(mediaPoolItem=imported[0],recordFrame=target['origin_frame'],trackIndex=1)])
        shift=normalize_import(candidate,expected_cc)
        require(candidate.SetTrackEnable('subtitle',1,False),'Cannot prevent doubled captions')
        require(candidate.AddMarker(0,'Blue','Branded subtitle recipe','',1,token),'Cannot mark ownership')
        verify_branded(candidate,base,before,layout,token,expected_cc,replace_tracks)
        require(manager.SaveProject(),'Cannot save branded candidate')
        return dict(status='CREATED',candidate_id=candidate.GetUniqueId(),name=candidate_name,branded_style='NATIVE_AUTHORED',native_cues=len(expected_cc),import_offset_corrected=shift,visual='UNVERIFIED',playback='UNVERIFIED')
    except Exception:
        if created and candidate and lane is not None:
            candidate.SetTrackEnable('video',lane,False)
        raise
    finally:
        restored=[]
        for action,label in ((lambda: project.SetCurrentTimeline(base),'timeline'),
                             (lambda: base.SetCurrentTimecode(before['timecode']),'playhead'),
                             (lambda: resolve.OpenPage(before['page']),'page')):
            try:
                if not action():
                    restored.append(label)
            except Exception:
                restored.append(label)
        require(not restored,'Could not restore source view: '+', '.join(restored))
        require(snapshot(resolve,target)==before,'Source changed during native authoring')
