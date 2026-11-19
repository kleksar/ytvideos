# Embedded dependencies are supplied by native.py and branded_native.py.
# ruff: noqa: F821
"""Sandboxed native Text+ phrase adapter, embedded after native.py/branded_native.py."""


def _phrase_equal(observed, expected):
    return (
        isinstance(observed, (int, float))
        and abs(observed - expected) < 1e-7
    )


def _phrase_inputs(tool, expected):
    for key, value in expected.items():
        actual = tool.GetInput(key, 0)
        ok = _phrase_equal(actual, value) if isinstance(value, (int, float)) else actual == value
        require(ok, 'Native title input does not match: ' + key)
        require(not getattr(tool, key).GetExpression(), 'Unexpected title expression: ' + key)


def _phrase_center(tool, center):
    actual = tool.GetInput('Center', 0)
    require(actual and all(_phrase_equal(actual[i + 1], x) for i, x in enumerate(center)),
            'Native title center differs')
    require(not tool.Center.GetExpression(), 'Unexpected title center expression')


def verify_phrase_graph(comp, row):
    style = row['style']
    panel_style = style['panel']
    word = named_tool(comp, 'Template', 'TextPlus')
    panel = named_tool(comp, 'Panel', 'Background')
    mask = named_tool(comp, 'Rectangle1', 'RectangleMask')
    merge = named_tool(comp, 'Merge1', 'Merge')
    out = named_tool(comp, 'MediaOut1', 'MediaOut')
    require(len(comp.GetToolList(False)) == 5, 'Unexpected tools in native phrase title')
    raster = dict(zip(('Width', 'Height'), style['raster']))
    _phrase_inputs(word, dict(raster, StyledText=row['text'], Font=style['font'],
                             Style=style['face'], Size=style['size'],
                             **dict(zip(('Red1', 'Green1', 'Blue1', 'Alpha1'), style['color']))))
    _phrase_center(word, style['center'])
    _phrase_inputs(panel, dict(raster, **dict(zip(
        ('TopLeftRed', 'TopLeftGreen', 'TopLeftBlue', 'TopLeftAlpha'), panel_style['color']))))
    _phrase_inputs(mask, dict(Width=panel_style['width'], Height=panel_style['height'],
                              CornerRadius=0, SoftEdge=0))
    _phrase_center(mask, panel_style['center'])
    require_connection(panel, 'EffectMask', 'Rectangle1', 'RectangleMask')
    require_connection(merge, 'Background', 'Panel', 'Background')
    require_connection(merge, 'Foreground', 'Template', 'TextPlus')
    require_connection(out, 'Input', 'Merge1', 'Merge')


def _phrase_verify_item(item, row):
    require(item.GetMediaPoolItem() is None and item.GetClipEnabled(),
            'Expected an enabled native title without media')
    require(item.GetStart() == row['start_frame'] and item.GetEnd() == row['end_frame'],
            'Native title placement differs')
    require(item.GetFusionCompCount() == 1, 'Native title must have exactly one composition')
    verify_phrase_graph(item.GetFusionCompByIndex(1), row)


def _phrase_mark(timeline, token, label):
    markers = timeline.GetMarkers() or {}
    for frame in range(timeline.GetEndFrame() - timeline.GetStartFrame()):
        if frame not in markers:
            require(timeline.AddMarker(frame, 'Blue', label, '', 1, token),
                    'Cannot record native phrase operation marker')
            return
    raise RuntimeError('No free frame for native phrase operation marker')


def _phrase_has(timeline, token):
    return bool(timeline.GetMarkerByCustomData(token))


def _phrase_readback(timeline, lane, layout, count):
    rows = sorted((timeline.GetItemListInTrack('video', lane) or []), key=lambda item: item.GetStart())
    require(len(rows) == count, 'Unexpected title count; inspect candidate, do not retry blindly')
    ids = []
    for item, row in zip(rows, layout):
        _phrase_verify_item(item, row)
        ids.append(item.GetUniqueId())
    require(all(ids) and len(set(ids)) == len(ids), 'Invalid native title identities')
    return ids


def _phrase_subtitles(timeline, with_ids=False):
    return [[(item.GetUniqueId() if with_ids else None, item.GetStart(), item.GetEnd(), item.GetName())
             for item in (timeline.GetItemListInTrack('subtitle', i) or [])]
            for i in range(1, timeline.GetTrackCount('subtitle') + 1)]


def _phrase_shape(candidate, source_shapes, track_state, replaced, lane, finalized, subtitle_shape):
    video = content_signature(candidate, 'video')
    expected_video = [
        [] if finalized and i in replaced else rows
        for i, rows in enumerate(source_shapes['video'], 1)
    ]
    require(len(video) == lane and video[:-1] == expected_video,
            'Candidate picture layout changed')
    require(content_signature(candidate, 'audio') == source_shapes['audio'],
            'Candidate audio layout changed')
    require(_phrase_subtitles(candidate) == subtitle_shape,
            'Candidate subtitle cues changed')
    for kind in ('audio', 'video', 'subtitle'):
        for i, expected in track_state[kind].items():
            require(bool(candidate.GetIsTrackEnabled(kind, i)) ==
                    (expected and kind != 'subtitle' and not (kind == 'video' and i in replaced)),
                    'Candidate track enable state changed')


def _phrase_state(candidate, token, total):
    count = 0
    while count < total and _phrase_has(candidate, token + ':done:' + str(count)):
        require(_phrase_has(candidate, token + ':pending:' + str(count)),
                'Unrecognized title checkpoint')
        count += 1
    for i in range(count, total):
        require(not _phrase_has(candidate, token + ':pending:' + str(i)) and
                not _phrase_has(candidate, token + ':done:' + str(i)),
                'Uncertain title batch; inspect candidate, do not retry blindly')
    return count


def _phrase_timecode_frames(value, fps):
    parts = value.split(':')
    require(len(parts) == 4 and all(part.isascii() and part.isdigit() and len(part) == 2
                                   for part in parts), 'Expected non-drop HH:MM:SS:FF timecode')
    hours, minutes, seconds, frames = map(int, parts)
    require(hours < 24 and minutes < 60 and seconds < 60 and frames < fps,
            'Invalid native title staging timecode')
    return ((hours * 60 + minutes) * 60 + seconds) * fps + frames


def _phrase_staging_point(base, target, timecode):
    rate = str(base.GetSetting('timelineFrameRate')).removesuffix('.0')
    require(rate.isascii() and rate.isdigit() and int(rate) > 0,
            'Native title staging requires integer non-drop frame rate')
    fps = int(rate)
    start = _phrase_timecode_frames(base.GetStartTimecode(), fps)
    stage = _phrase_timecode_frames(timecode, fps)
    require(target['origin_frame'] + stage - start == target['end_frame'],
            'Native title staging point must be the exact source timeline end')


def install_phrase_batch(resolve, target, before, layout, comp_paths, candidate_name, token,
                         replace_tracks, insertion_timecode, batch_start, batch_size=5,
                         finalize=False):
    """Build or verify an isolated owned candidate; restore source view on every call.

    replace_tracks maps integer video track indices to the exact source item IDs
    on each declared old-caption-only lane. Caller binds inputs/comp hashes to token.
    Finalize is a separate call (batch_start == number of phrases).
    """
    manager, project, base = identity(resolve, target)
    require(snapshot(resolve, target) == before, 'Source changed since verification')
    require(type(batch_start) is int and type(batch_size) is int and 1 <= batch_size <= 5,
            'Native phrase batches must be bounded to 1–5 titles')
    require(layout and len(layout) == len(comp_paths) and 0 <= batch_start <= len(layout),
            'Invalid phrase batch layout or start')
    require(not finalize or batch_start == len(layout), 'Finalize is a separate post-build operation')
    require(all(type(i) is int and 1 < i <= len(before['picture']) and ids and
                ids == [item[0] for item in before['picture'][i - 1]]
                for i, ids in replace_tracks.items()), 'Old caption-only track IDs do not match source')
    for i, row in enumerate(layout):
        require(type(row['start_frame']) is int and type(row['end_frame']) is int and
                target['origin_frame'] <= row['start_frame'] < row['end_frame'] <= target['end_frame']
                and row['text'].strip() and row['style']['raster'] == target['raster'],
                'Invalid native phrase span, text or raster')
        require(i == 0 or layout[i - 1]['end_frame'] == row['start_frame'],
                'Phrase display spans must be contiguous')
    if not finalize:
        _phrase_staging_point(base, target, insertion_timecode)
    source_shapes = {kind: content_signature(base, kind) for kind in ('audio', 'video')}
    source_subtitles = _phrase_subtitles(base, True)
    subtitle_shape = _phrase_subtitles(base)
    track_state = {
        kind: {i: bool(base.GetIsTrackEnabled(kind, i)) for i in range(1, base.GetTrackCount(kind) + 1)}
        for kind in ('audio', 'video', 'subtitle')
    }
    lane = len(source_shapes['video']) + 1
    matches = [project.GetTimelineByIndex(i) for i in range(1, project.GetTimelineCount() + 1)
               if project.GetTimelineByIndex(i).GetName() == candidate_name]
    require(len(matches) <= 1, 'Ambiguous native title candidate name')
    try:
        if matches:
            candidate = matches[0]
            require(_phrase_has(candidate, token), 'Native title candidate is not owned')
            require(candidate.GetUniqueId() != base.GetUniqueId(), 'Candidate cannot be source')
            require(project.SetCurrentTimeline(candidate), 'Cannot activate native title candidate')
        else:
            require(batch_start == 0 and not finalize, 'Native title candidate is missing')
            require(manager.SaveProject(), 'Cannot checkpoint source project')
            candidate = base.DuplicateTimeline(candidate_name)
            require(candidate and candidate.GetUniqueId() != base.GetUniqueId()
                    and project.SetCurrentTimeline(candidate), 'Cannot create isolated native title candidate')
            require(candidate.AddTrack('video'), 'Cannot add dedicated native title track')
            require(candidate.SetTrackName('video', lane, 'Native phrase titles ' + token[-12:]),
                    'Cannot name native title track')
            for kind, tracks in track_state.items():
                for i, enabled in tracks.items():
                    require(candidate.SetTrackEnable(kind, i, enabled and kind != 'subtitle' and
                                                     not (kind == 'video' and i in replace_tracks)),
                            'Cannot set candidate track visibility')
            require(candidate.SetTrackEnable('video', lane, True), 'Cannot enable native title track')
            _phrase_mark(candidate, token, 'Native phrase candidate')
            require(manager.SaveProject(), 'Cannot checkpoint native title candidate')
        require(candidate.GetTrackName('video', lane) == 'Native phrase titles ' + token[-12:]
                and candidate.GetIsTrackEnabled('video', lane), 'Native title track identity changed')
        require(candidate.GetStartFrame() == target['origin_frame']
                and candidate.GetEndFrame() == target['end_frame'], 'Native title candidate range changed')
        for key in ('timelineFrameRate', 'timelineResolutionWidth', 'timelineResolutionHeight'):
            require(candidate.GetSetting(key) == base.GetSetting(key), 'Native title candidate settings changed')
        finalized = _phrase_has(candidate, token + ':finalized')
        require(finalized or not _phrase_has(candidate, token + ':finalizing'),
                'Uncertain cleanup state; inspect candidate, do not retry blindly')
        _phrase_shape(candidate, source_shapes, track_state, replace_tracks, lane, finalized, subtitle_shape)
        count = _phrase_state(candidate, token, len(layout))
        ids = _phrase_readback(candidate, lane, layout, count)
        status = 'UNCHANGED'
        if finalize and not finalized:
            require(count == len(layout), 'Cannot remove old caption clips before exact title readback')
            _phrase_mark(candidate, token + ':finalizing', 'Old caption removal pending')
            require(manager.SaveProject(), 'Cannot checkpoint old caption removal')
            old = [item for i in replace_tracks for item in
                   (candidate.GetItemListInTrack('video', i) or [])]
            require(not old or candidate.DeleteClips(old, False), 'Cannot remove old caption clips')
            _phrase_shape(candidate, source_shapes, track_state, replace_tracks, lane, True, subtitle_shape)
            _phrase_readback(candidate, lane, layout, count)
            _phrase_mark(candidate, token + ':finalized', 'Old caption removal verified')
            require(manager.SaveProject(), 'Cannot checkpoint finalized native title candidate')
            status, finalized = 'FINALIZED', True
        elif not finalize and not finalized and (count < min(batch_start + batch_size, len(layout))):
            require(count == batch_start, 'Batch start does not match saved progress')
            for index in range(count, min(count + batch_size, len(layout))):
                row = layout[index]
                _phrase_mark(candidate, token + ':pending:' + str(index), 'Native phrase pending')
                require(manager.SaveProject(), 'Cannot checkpoint pending native phrase')
                require(candidate.SetCurrentTimecode(insertion_timecode), 'Cannot seek native title staging point')
                item = candidate.InsertFusionTitleIntoTimeline('Text+')
                require(item and item.GetMediaPoolItem() is None and item.GetStart() >= target['end_frame'],
                        'Text+ staging failed or landed inside populated timeline; inspect candidate')
                duration = row['end_frame'] - row['start_frame']
                require(item.GetDuration() >= duration and item.SetRightOffset(
                    item.GetRightOffset() + item.GetDuration() - duration, False, False),
                    'Cannot set exact native title duration')
                require(item.SetPosition({'trackIndex': lane, 'startFrame': row['start_frame']}, False),
                        'Cannot move native title')
                names = item.GetFusionCompNameList() or []
                imported = item.ImportFusionComp(comp_paths[index])
                require(imported, 'Native phrase graph import failed')
                verify_phrase_graph(imported, row)
                after_names = item.GetFusionCompNameList() or []
                new_names = [name for name in after_names if name not in names]
                require(len(after_names) == 1 and (len(names) == 1 or len(new_names) == 1),
                        'Ambiguous native phrase graph import')
                activated = item.LoadFusionCompByName(after_names[0])
                require(activated, 'Cannot activate native phrase graph')
                verify_phrase_graph(activated, row)
                _phrase_shape(candidate, source_shapes, track_state, replace_tracks, lane, False, subtitle_shape)
                ids = _phrase_readback(candidate, lane, layout, index + 1)
                _phrase_mark(candidate, token + ':done:' + str(index), 'Native phrase verified')
                require(manager.SaveProject(), 'Cannot checkpoint verified native phrase')
            status = 'BATCH_VERIFIED'
        return dict(status=status, candidate_id=candidate.GetUniqueId(), native_titles=len(ids),
                    title_ids=ids, lane=lane, old_carriers_removed=finalized,
                    visual='UNVERIFIED', inspector_edit_move='UNVERIFIED', playback='UNVERIFIED')
    finally:
        failed = []
        for description, operation in (
            ('timeline', lambda: project.SetCurrentTimeline(base)),
            ('playhead', lambda: base.SetCurrentTimecode(before['timecode'])),
            ('page', lambda: resolve.OpenPage(before['page'])),
        ):
            try:
                if not operation():
                    failed.append(description)
            except Exception:
                failed.append(description)
        require(not failed, 'Cannot restore source view: ' + ', '.join(failed))
        require(snapshot(resolve, target) == before and _phrase_subtitles(base, True) == source_subtitles,
                'Source changed during phrase installation')



def finalize_phrase_candidate(resolve, target, before, layout, comp_paths, candidate_name, token,
                              replace_tracks):
    """Remove explicitly owned old captions after caller verifies live review proof."""
    return install_phrase_batch(resolve, target, before, layout, comp_paths, candidate_name,
                                token, replace_tracks, None, len(layout), finalize=True)
