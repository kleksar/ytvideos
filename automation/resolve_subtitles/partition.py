"""Partition planned caption display into native shot sections without changing speech.

All intervals are absolute, half-open Resolve record frames. A word index is
the original planner index, not a shot-local index. None denotes neutral style.
This module never writes media, accesses Resolve or changes native timed SRT.
"""
from __future__ import annotations


def _name(value, field):
    if not isinstance(value, str) or not value or value != value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError(f"{field} must be an exact nonempty identifier")
    return value


def _span(record, label):
    if not isinstance(record, dict):
        raise ValueError(f"{label} must be an object")
    start, end = record.get("start_frame"), record.get("end_frame")
    if type(start) is not int or type(end) is not int or not 0 <= start < end:
        raise ValueError(f"{label} requires positive half-open absolute frame bounds")
    return start, end


def _text(value, label):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError(f"{label} requires nonempty single-line text")
    return value


def _shot_records(shots):
    if not isinstance(shots, list) or not shots:
        raise ValueError("explicit ordered shot spans are required")
    result, ids = [], set()
    cursor = None
    for shot in shots:
        start, end = _span(shot, "shot")
        identity = _name(shot.get("id"), "shot id")
        carrier = _name(shot.get("carrier_id"), "shot carrier_id")
        if identity in ids:
            raise ValueError("shot IDs must be unique")
        if cursor is not None and start != cursor:
            raise ValueError("shot spans have a gap, overlap or ambiguous order")
        ids.add(identity)
        cursor = end
        result.append(dict(id=identity, carrier_id=carrier, start_frame=start, end_frame=end, sections=[]))
    return result


def _cue_records(cues, first, last):
    if not isinstance(cues, list) or not cues:
        raise ValueError("planned speech cues are required")
    result, ids = [], set()
    previous_cue_end, previous_index = first, -1
    for cue in cues:
        start, end = _span(cue, "cue")
        identity = _name(cue.get("id"), "cue id")
        text = _text(cue.get("text"), "cue text")
        words = cue.get("words")
        if identity in ids or start < previous_cue_end or end > last:
            raise ValueError("cues overlap, are unordered, duplicate IDs, or fall outside shot coverage")
        if not isinstance(words, list) or not words:
            raise ValueError("planned cue is missing its word intervals")
        states, clean_words = [], []
        cursor = start
        for word in words:
            a, b = _span(word, "word")
            index = word.get("index")
            word_text = _text(word.get("text"), "word text")
            if type(index) is not int or index != previous_index + 1:
                raise ValueError("planned word indices are missing, repeated or unordered")
            if a < cursor or b > end:
                raise ValueError("word intervals overlap or fall outside their planned cue")
            if cursor < a:
                states.append(dict(start_frame=cursor, end_frame=a, word_index=None))
            states.append(dict(start_frame=a, end_frame=b, word_index=index))
            clean_words.append(dict(word))
            previous_index, cursor = index, b
        if " ".join(word["text"] for word in clean_words) != text:
            raise ValueError("planned cue text disagrees with its word indices")
        if any(key in cue for key in ("spoken_start_frame", "spoken_end_frame")) and (
            (cue.get("spoken_start_frame"), cue.get("spoken_end_frame"))
            != (clean_words[0]["start_frame"], cursor)
        ):
            raise ValueError("planned spoken bounds disagree with word intervals")
        if cursor < end:
            states.append(dict(start_frame=cursor, end_frame=end, word_index=None))
        result.append(dict(cue_id=identity, text=text, start_frame=start, end_frame=end,
                           words=clean_words, states=states))
        ids.add(identity)
        previous_cue_end = end
    return result


def _anchor_display(planned, shots, anchors):
    """Opt-in late cut starts; speech/CC data is never modified."""
    if not isinstance(anchors,list):
        raise ValueError('display_cut_anchors must be a list')
    by_cue={cue['cue_id']:i for i,cue in enumerate(planned)}
    by_shot={shot['id']:shot for shot in shots}
    seen=set();moves={}
    for anchor in anchors:
        if not isinstance(anchor,dict) or set(anchor)!={'cue_id','shot_id','start_frame'}:
            raise ValueError('cut anchor requires exact cue_id, shot_id and start_frame')
        cue_id,shot_id=anchor['cue_id'],anchor['shot_id'];frame=anchor['start_frame']
        if cue_id not in by_cue or shot_id not in by_shot or cue_id in seen:
            raise ValueError('Unknown or duplicate display cut anchor')
        if type(frame) is not int or frame!=by_shot[shot_id]['start_frame']:
            raise ValueError('Display anchor must equal the declared picture cut')
        cue=planned[by_cue[cue_id]];first=cue['words'][0]
        if not first['start_frame']<=frame<first['end_frame']:
            raise ValueError('Cut anchor must be during first spoken word; cannot hide it entirely or anticipate speech')
        moves[by_cue[cue_id]]=frame;seen.add(cue_id)
        by_shot[shot_id]['picture_cut_anchor']=True
    # Simultaneous edits use original boundaries, not iteration order.
    original=[(c['start_frame'],c['end_frame']) for c in planned]
    for i,frame in moves.items():
        planned[i]['start_frame']=frame
        if i and original[i-1][1]==original[i][0]:
            planned[i-1]['end_frame']=frame
    previous_end=shots[0]['start_frame']
    for cue in planned:
        a,b=cue['start_frame'],cue['end_frame']
        if not previous_end<=a<b:
            raise ValueError('Conflicting anchored display intervals')
        # Word starts/ends remain immutable; only visible intersections change.
        states=[];cursor=a
        for word in cue['words']:
            left,right=max(a,word['start_frame']),min(b,word['end_frame'])
            if left>=right:continue
            if cursor<left:states.append(dict(start_frame=cursor,end_frame=left,word_index=None))
            states.append(dict(start_frame=left,end_frame=right,word_index=word['index']));cursor=right
        if cursor<b:states.append(dict(start_frame=cursor,end_frame=b,word_index=None))
        cue['states']=states;previous_end=b


def partition_cues(cues, shots, display_cut_anchors=None):
    """Return shot records with clipped display sections and exact word states.

    Shot spans must be contiguous and cover every planned cue. Display gaps
    from the planner remain gaps. A cut during word speech preserves that
    highlight into the next shot; a cut during a hold preserves neutral text.
    """
    result = _shot_records(shots)
    planned = _cue_records(cues, result[0]["start_frame"], result[-1]["end_frame"])
    if display_cut_anchors is not None:
        _anchor_display(planned,result,display_cut_anchors)
    i = 0
    for shot in result:
        left, right = shot["start_frame"], shot["end_frame"]
        while i < len(planned) and planned[i]["end_frame"] <= left:
            i += 1
        j = i
        while j < len(planned) and planned[j]["start_frame"] < right:
            cue = planned[j]
            start, end = max(left, cue["start_frame"]), min(right, cue["end_frame"])
            states = [{**state, "start_frame": max(start, state["start_frame"]),
                       "end_frame": min(end, state["end_frame"])}
                      for state in cue["states"] if state["start_frame"] < end and start < state["end_frame"]]
            shot["sections"].append({**cue, "start_frame": start, "end_frame": end,
                                     "words": [dict(word) for word in cue["words"]], "states": states})
            j += 1
    return result
