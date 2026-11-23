"""Pure native API operations, also embedded verbatim in official MCP run_script.

No imports, filesystem, app launch, export, playback or publication in this module.
"""

def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def items(timeline, kind):
    return [item for track in range(1, timeline.GetTrackCount(kind)+1)
            for item in (timeline.GetItemListInTrack(kind, track) or [])]


def signature(timeline, kind):
    return [[[item.GetUniqueId(), item.GetStart(), item.GetEnd(), item.GetLeftOffset(),
              item.GetRightOffset(), item.GetClipEnabled(), item.GetProperty(),
              item.GetMediaPoolItem().GetUniqueId() if item.GetMediaPoolItem() else None]
             for item in (timeline.GetItemListInTrack(kind, track) or [])]
            for track in range(1, timeline.GetTrackCount(kind)+1)]


def identity(resolve, target):
    manager = resolve.GetProjectManager()
    project = manager.GetCurrentProject()
    require(project and project.GetUniqueId() == target['project_id'], 'Wrong active project; do not switch automatically')
    timeline = project.GetCurrentTimeline()
    require(timeline and timeline.GetUniqueId() == target['timeline_id'], 'Wrong active timeline')
    require(not project.IsRenderingInProgress(), 'Resolve is rendering')
    require(timeline.GetStartFrame() == target['origin_frame'] and timeline.GetEndFrame() == target['end_frame'], 'Timeline range changed')
    require(str(timeline.GetSetting('timelineFrameRate')) in target['native_fps_values'], 'Timeline frame rate mismatch')
    width, height = (timeline.GetSetting(key) for key in ('timelineResolutionWidth','timelineResolutionHeight'))
    if width and height and str(width) != '0' and str(height) != '0':
        require([int(width), int(height)] == target['raster'], 'Timeline raster mismatch')
    else:
        require(target.get('explicit_missing_raster') is True, 'Timeline raster unavailable; explicit dimensions required')
    return manager, project, timeline


def snapshot(resolve, target):
    manager, project, timeline = identity(resolve, target)
    voice = []
    track_state = {str(i):bool(timeline.GetIsTrackEnabled('audio', i)) for i in range(1,timeline.GetTrackCount('audio')+1)}
    tracks = {item.GetUniqueId():i for i in range(1,timeline.GetTrackCount('audio')+1) for item in (timeline.GetItemListInTrack('audio',i) or [])}
    for item in items(timeline, 'audio'):
        media = item.GetMediaPoolItem()
        voice.append(dict(id=item.GetUniqueId(), start=item.GetStart(), end=item.GetEnd(),
                          left=item.GetLeftOffset(), right=item.GetRightOffset(),
                          enabled=item.GetClipEnabled(), properties=item.GetProperty(),
                          track_enabled=track_state[str(tracks[item.GetUniqueId()])], speed=item.GetSpeed(),
                          path=media.GetClipProperty('File Path') if media else None))
    return dict(target=target, voice=voice, audio_track_state=track_state, video_track_state={str(i):bool(timeline.GetIsTrackEnabled('video',i)) for i in range(1,timeline.GetTrackCount('video')+1)}, audio=signature(timeline, 'audio'),
                picture=signature(timeline, 'video'), timecode=timeline.GetCurrentTimecode(),
                page=resolve.GetCurrentPage())


def cue_readback(timeline):
    result = []
    for item in (timeline.GetItemListInTrack('subtitle', 1) or []):
        start, end = item.GetStart(), item.GetEnd()
        require(start == int(start) and end == int(end), 'Subframe subtitle bounds unsupported')
        result.append((int(start), int(end), item.GetName()))
    return result


def comparison_properties(properties):
    # Resolve 21.2 DuplicateTimeline omits these entirely unused AI defaults
    # on an audio item. Do not erase enabled effects or configured latent values.
    result = dict(properties)
    for prefix in ('AudioVoiceIsolation', 'AudioDialogueLeveler'):
        keys = [key for key in result if key.startswith(prefix)]
        if not result.get(prefix+'Enabled') and all(result[key] in (False, 0) for key in keys):
            for key in keys:
                del result[key]
    return result


def content_signature(timeline, kind):
    result = [[list(row[1:]) for row in track] for track in signature(timeline, kind)]
    for track in result:
        for row in track:
            row[5] = comparison_properties(row[5])
    return result


def verify_candidate(candidate, base, expected, token, before):
    require(candidate.GetMarkerByCustomData(token), 'Candidate name belongs to unowned work')
    require(candidate.GetTrackCount('subtitle') == 1 and not candidate.GetIsTrackEnabled('subtitle', 1), 'Owned candidate subtitle lane changed')
    require(cue_readback(candidate) == expected, 'Owned candidate modified; refusing overwrite')
    require(candidate.GetStartFrame() == base.GetStartFrame() and candidate.GetEndFrame() == base.GetEndFrame(), 'Candidate duration changed')
    for key in ('timelineFrameRate', 'timelineResolutionWidth', 'timelineResolutionHeight'):
        require(candidate.GetSetting(key) == base.GetSetting(key), 'Candidate settings changed')
    for kind in ('audio', 'video'):
        require(content_signature(base, kind) == content_signature(candidate, kind), 'Candidate '+kind+' changed')
        require([before[kind+'_track_state'][str(i)] for i in range(1,base.GetTrackCount(kind)+1)] ==
                [bool(candidate.GetIsTrackEnabled(kind,i)) for i in range(1,candidate.GetTrackCount(kind)+1)], 'Candidate track enable changed')


def normalize_import(timeline, expected):
    """Correct only proven uniform import placement, NEVER speech alignment."""
    actual = cue_readback(timeline)
    require(len(actual) == len(expected), 'Native subtitle count mismatch')
    require(all(b-a == y-x and text == other for (a,b,text),(x,y,other) in zip(expected,actual)),
            'Native import text or duration differs; cannot normalize')
    offsets = {x-a for (a,b,text),(x,y,other) in zip(expected,actual)}
    require(len(offsets) == 1, 'Nonuniform native import offset; abort without shifting speech')
    shift = offsets.pop()
    if shift:
        for item in timeline.GetItemListInTrack('subtitle', 1):
            require(item.SetPosition({'startFrame':item.GetStart()-shift}, False), 'Native SetPosition failed')
    require(cue_readback(timeline) == expected, 'Exact native cue readback failed')
    return shift


def install(resolve, target, before, expected, srt_path, candidate_name, token):
    manager, project, base = identity(resolve, target)
    require(snapshot(resolve, target) == before, 'Timeline changed since source verification')
    require(manager.SaveProject(), 'Could not checkpoint source project')
    pool = project.GetMediaPool()
    existing = [project.GetTimelineByIndex(i) for i in range(1, project.GetTimelineCount()+1)
                if project.GetTimelineByIndex(i).GetName() == candidate_name]
    require(len(existing) <= 1, 'Ambiguous candidate name')
    candidate = None
    created = False
    try:
        if existing:
            candidate = existing[0]
            require(candidate.GetMarkerByCustomData(token), 'Candidate name belongs to unowned work')
            require(project.SetCurrentTimeline(candidate), 'Cannot inspect owned candidate')
            verify_candidate(candidate, base, expected, token, before)
            return dict(status='UNCHANGED', candidate_id=candidate.GetUniqueId(), name=candidate_name,
                        native_cues=len(expected), branded_style='NOT_APPLIED', playback='UNVERIFIED')
        candidate = base.DuplicateTimeline(candidate_name)
        created = bool(candidate)
        require(candidate and project.SetCurrentTimeline(candidate), 'Cannot make isolated candidate')
        # In 21.2 GetIsTrackEnabled on an INACTIVE timeline returns false.
        # Capture source flags before switching, and inspect candidate only active.
        for kind in ('audio', 'video'):
            require(candidate.GetTrackCount(kind) == base.GetTrackCount(kind), 'Duplicate track count differs')
            for track in range(1, base.GetTrackCount(kind)+1):
                require(candidate.SetTrackEnable(kind, track, before[kind+'_track_state'][str(track)]), 'Cannot preserve track enable')
        # Existing subtitle tracks are untouched in the source, and removed only
        # from this new owned copy. Import has one unambiguous destination.
        for track in range(candidate.GetTrackCount('subtitle'), 0, -1):
            require(candidate.DeleteTrack('subtitle', track), 'Cannot prepare candidate subtitle track')
        require(candidate.AddTrack('subtitle'), 'Cannot create subtitle track')
        require(candidate.SetCurrentTimecode(candidate.GetStartTimecode()), 'Cannot position candidate for import')
        imported = pool.ImportMedia([srt_path])
        require(imported and len(imported) == 1, 'SRT Media Pool import failed')
        pool.AppendToTimeline([dict(mediaPoolItem=imported[0], recordFrame=target['origin_frame'], trackIndex=1)])
        shift = normalize_import(candidate, expected)
        require(candidate.SetTrackName('subtitle', 1, 'Native editable CC | '+token[:24]), 'Cannot name track')
        # Separate optional CC, not a replacement for profile-styled on-screen text.
        require(candidate.SetTrackEnable('subtitle', 1, False), 'Cannot suppress duplicate visible captions')
        require(candidate.GetStartFrame() == base.GetStartFrame() and candidate.GetEndFrame() == base.GetEndFrame(), 'Candidate duration changed')
        # Duplicated TimelineItem IDs may differ; compare content, not IDs.
        for kind in ('audio', 'video'):
            original = content_signature(base, kind)
            duplicate = content_signature(candidate, kind)
            require(original == duplicate, 'Candidate '+kind+' changed')
        require(candidate.AddMarker(0, 'Blue', 'Native subtitle recipe', '', 1, token), 'Cannot record ownership')
        verify_candidate(candidate, base, expected, token, before)
        require(manager.SaveProject(), 'Cannot save native candidate')
        return dict(status='CREATED', candidate_id=candidate.GetUniqueId(), name=candidate_name,
                    native_cues=len(expected), import_offset_corrected=shift,
                    branded_style='NOT_APPLIED', playback='UNVERIFIED')
    except Exception:
        if candidate and created:
            # No destructive cleanup: preserve uncertain app state for diagnosis.
            candidate.SetTrackEnable('subtitle', 1, False)
        raise
    finally:
        # No project switch or mouse takeover. A failed restoration is a failure.
        restored = []
        for action, label in ((lambda: project.SetCurrentTimeline(base), 'timeline'),
                              (lambda: base.SetCurrentTimecode(before['timecode']), 'playhead'),
                              (lambda: resolve.OpenPage(before['page']), 'page')):
            try:
                if not action():
                    restored.append(label)
            except Exception:
                restored.append(label)
        require(not restored, 'Could not restore source view: '+', '.join(restored))
        require(snapshot(resolve, target) == before, 'Source timeline changed during authoring; candidate is not accepted')


def discover_current(resolve):
    manager=resolve.GetProjectManager()
    project=manager.GetCurrentProject()
    require(project, 'No active project')
    timeline=project.GetCurrentTimeline()
    require(timeline, 'No active timeline')
    require(not project.IsRenderingInProgress(), 'Resolve is rendering')
    return dict(project_id=project.GetUniqueId(), timeline_id=timeline.GetUniqueId(),
                fps_observed=str(timeline.GetSetting('timelineFrameRate')),
                width_observed=str(timeline.GetSetting('timelineResolutionWidth')),
                height_observed=str(timeline.GetSetting('timelineResolutionHeight')),
                origin_frame=timeline.GetStartFrame(), end_frame=timeline.GetEndFrame())
