"""Conform single-utterance PCM16 mono voice clips offline, without editing the originals."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import sys
import wave
from array import array
from fractions import Fraction
from pathlib import Path


def _pcm(path):
    data = Path(path).read_bytes()
    with wave.open(io.BytesIO(data)) as stream:
        if (stream.getsampwidth(), stream.getnchannels(), stream.getcomptype()) != (2, 1, "NONE"):
            raise ValueError(f"{path}: expected uncompressed mono PCM16 WAV")
        hz, n = stream.getframerate(), stream.getnframes()
        if not 8_000 <= hz <= 192_000 or not 0 < n <= hz * 60:
            raise ValueError(f"{path}: unsupported sample rate or utterance length")
        raw = stream.readframes(n)
    if len(raw) != 2 * n:
        raise ValueError(f"{path}: truncated WAV")
    return data, raw, hz, n


def _round(value):
    return math.floor(value + Fraction(1, 2))


def _tight_edges(rms, peak, stable, low_fixed):
    """Link softer windows to speech; conservatively retain ambiguous detached events."""
    threshold = max(10.0, max(rms) * .004)
    peak_threshold = max(48.0, threshold * 3)
    soft = [i for i, (r, p) in enumerate(zip(rms, peak)) if r >= threshold or p >= peak_threshold]
    first, last = stable[0], stable[-1]
    for i in reversed(soft):
        if i >= first:
            continue
        if first - i > 3:
            break
        first = i
    for i in soft:
        if i <= last:
            continue
        if i - last > 3:
            break
        last = i

    # A brief weak event separated by at least 80ms of near-zero PCM is a review
    # candidate, not permission to remove it. Preserve detached activity that clears the
    # soft threshold: it can be a breath or final consonant despite a convincing gap.
    clusters = []
    for index in low_fixed:
        if not clusters or index - clusters[-1][-1] > 1:
            clusters.append([])
        clusters[-1].append(index)
    protected = [first, last]
    fixed_set = set(low_fixed)
    soft_set = set(soft)
    review = []
    for group in clusters:
        if group[-1] >= first and group[0] <= last:
            # Only actually strong/soft-connected samples set the envelope; low-level
            # samples adjoining it stay protected by the explicit sample guard.
            continue
        if not any(i in soft_set for i in group):
            continue
        start, stop = (group[-1] + 1, first) if group[-1] < first else (last + 1, group[0])
        quiet = any(all(j not in fixed_set for j in range(i, i + 8))
                    for i in range(start, stop - 7))
        is_detached_tiny = (
            quiet and len(group) <= 2 and max(peak[i] for i in group) <= 700
            and max(rms[i] for i in group) <= 200
        )
        if is_detached_tiny:
            review.append({"window_start": group[0], "window_end": group[-1] + 1,
                           "peak": max(peak[i] for i in group), "action": "retained_for_review"})
        protected.extend((group[0], group[-1]))
    # A relative gate can be too tall on a loud take. Never let the tighter
    # mode discard a peak above the absolute -44.3 dBFS PCM16 safety ceiling.
    hard_peak = 199
    protected.extend(i for i, p in enumerate(peak) if p > hard_peak)
    return first, last, min(protected), max(protected), {
        "soft_rms_threshold": threshold, "soft_peak_threshold": peak_threshold,
        "discard_peak_ceiling_pcm16": hard_peak,
        "detached_candidates": review,
    }


def analyze_wav(path, *, guard_ms=40, edge_mode="conservative"):
    """Return half-open source edges in samples; protect quiet transients beyond speech."""
    if edge_mode not in {"conservative", "tight"}:
        raise ValueError("unknown edge_mode")
    guard = Fraction(str(guard_ms))
    if not 0 <= guard <= 1000:
        raise ValueError("guard_ms must be in [0, 1000]")
    data, raw, hz, n = _pcm(path)
    pcm = array("h", raw)
    if sys.byteorder != "little":
        pcm.byteswap()
    block = max(1, hz // 100)
    rms = []
    peak = []
    for i in range(0, n, block):
        chunk = pcm[i:i + block]
        rms.append(math.sqrt(sum(v * v for v in chunk) / len(chunk)))
        peak.append(max(map(abs, chunk)))
    threshold = max(32, max(rms) * .018)
    loud = {i for i, value in enumerate(rms) if value >= threshold}
    stable = sorted(i for i in loud if any(i + delta in loud for delta in (-2, -1, 1, 2)))
    if len(stable) < 2:
        raise ValueError(f"{path}: no reliable speech span")
    # Retain low-level onsets and tails in the audio even if they are below the timing threshold.
    # Quiet/transient edge samples may be phonemes, breaths, clicks or other sound; do not gate them.
    protected = [i for i, (r, p) in enumerate(zip(rms, peak)) if r > 4 or p > 12]
    if not protected:
        raise ValueError(f"{path}: no protected waveform")
    margin = math.ceil(hz * guard / 1000)
    first, last, edge_in, edge_out, details = stable[0], stable[-1], protected[0], protected[-1], {}
    if edge_mode == "tight":
        first, last, edge_in, edge_out, details = _tight_edges(rms, peak, stable, protected)
    return {
        "sample_rate": hz, "samples": n, "speech_start": first * block,
        "speech_end": min(n, (last + 1) * block),
        "trim_start": max(0, edge_in * block - margin),
        "trim_end": min(n, (edge_out + 1) * block + margin),
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "measurement": {"window_samples": block, "timing_rms_threshold": threshold,
                        "protection_rms_threshold": 4, "protection_peak_threshold": 12,
                        "guard_samples": margin, **details},
    }


def plan_spacing(rows, *, fps=30, gap_ms=700, guard_ms=40, edge_mode="conservative"):
    """Produce frame placements for edited, ordered clips; leave internal silence intact."""
    fps, gap = Fraction(str(fps)), Fraction(str(gap_ms))
    if not 1 <= fps <= 240 or not 0 <= gap <= 10_000:
        raise ValueError("unsupported fps or gap_ms")
    if not isinstance(rows, list) or not rows:
        raise ValueError("expected a nonempty ordered clip list")
    result = []
    last_speech_end = None
    last_audio_end = Fraction(0)
    seen = set()
    target = gap * fps / 1000
    for src in rows:
        if not isinstance(src, dict):
            raise ValueError("each clip must be an object")
        cue = src.get("cue")
        if not isinstance(cue, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", cue) or cue in seen:
            raise ValueError(f"invalid or duplicate cue: {cue!r}")
        seen.add(cue)
        path = Path(src["wav"]).resolve()
        speed = Fraction(str(src["speed"]))
        if not 25 <= speed <= 400:
            raise ValueError(f"{cue}: unsupported constant speed percentage")
        found = analyze_wav(path, guard_ms=guard_ms, edge_mode=edge_mode)
        if src.get("wav_sha") is not None and found["source_sha256"] != src["wav_sha"]:
            raise ValueError(f"{cue}: stale source hash")
        frame = fps * 100 / (found["sample_rate"] * speed)
        lead = (found["speech_start"] - found["trim_start"]) * frame
        duration = (found["trim_end"] - found["trim_start"]) * frame
        audio_start = 0 if last_speech_end is None else _round(last_speech_end + target - lead)
        if audio_start < last_audio_end:
            raise ValueError(f"{cue}: target gap would overlap a protected audio handle")
        speech_start = audio_start + lead
        speech_end = audio_start + (found["speech_end"] - found["trim_start"]) * frame
        last_audio_end = audio_start + duration
        result.append({
            "cue": cue, "wav": str(path), "speed": str(speed), **found,
            "audio_start_frame": audio_start, "audio_end_frame": str(last_audio_end),
            "speech_start_frame": str(speech_start), "speech_end_frame": str(speech_end),
            "gap_from_previous_frames": None if last_speech_end is None else str(speech_start - last_speech_end),
        })
        last_speech_end = speech_end
    return {"schema": 1, "fps": str(fps), "gap_ms": str(gap), "target_gap_frames": str(target),
            "guard_ms": str(Fraction(str(guard_ms))), "edge_mode": edge_mode,
            "duration_frames": math.ceil(last_audio_end), "rows": result}


def materialize(plan, output_dir):
    """Write exact raw PCM subsets into a new folder; verify source hashes at write time."""
    dest = Path(output_dir)
    payloads = []
    ids = set()
    for row in plan["rows"]:
        cue = row["cue"]
        if not isinstance(cue, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", cue) or cue in ids:
            raise ValueError(f"invalid or duplicate cue: {cue!r}")
        ids.add(cue)
        fresh = analyze_wav(row["wav"], guard_ms=plan["guard_ms"],
                            edge_mode=plan.get("edge_mode", "conservative"))
        if any(row.get(k) != v for k, v in fresh.items()):
            raise ValueError(f"{cue}: source or measured edges changed after planning")
        data, raw, hz, n = _pcm(row["wav"])
        if (hashlib.sha256(data).hexdigest(), hz, n) != (
                row["source_sha256"], row["sample_rate"], row["samples"]):
            raise ValueError(f"{row['cue']}: source changed after planning")
        start, end = row["trim_start"], row["trim_end"]
        if not 0 <= start <= row["speech_start"] < row["speech_end"] <= end <= n:
            raise ValueError(f"{row['cue']}: unsafe trim boundaries")
        trimmed = raw[start * 2:end * 2]
        temp = io.BytesIO()
        with wave.open(temp, "wb") as out:
            out.setparams((1, 2, hz, 0, "NONE", "not compressed"))
            out.writeframes(trimmed)
        payloads.append((row, temp.getvalue(), hashlib.sha256(trimmed).hexdigest()))
    dest.mkdir()  # An existing destination could contain unrelated media. Never overwrite.
    for row, data, pcm_sha in payloads:
        target = dest / f"{row['cue']}.wav"
        with target.open("xb") as out:
            out.write(data)
        row.update(derived_wav=str(target.resolve()), derived_sha256=hashlib.sha256(data).hexdigest(),
                   derived_pcm_sha256=pcm_sha)
    return plan


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON list or object with items of cue/wav/speed (percent)")
    parser.add_argument("--fps", default="30")
    parser.add_argument("--gap-ms", default="700")
    parser.add_argument("--guard-ms", default="40")
    parser.add_argument("--edge-mode", choices=("conservative", "tight"), default="conservative",
                        help="tight opts into a quieter connected envelope and flags isolated edge artifacts")
    parser.add_argument("--output", type=Path, help="write plan to a new JSON file instead of stdout")
    parser.add_argument("--materialize-dir", type=Path, help="explicitly opt in to creating trimmed PCM copies")
    args = parser.parse_args(argv)
    try:
        if args.output and args.output.exists():
            raise FileExistsError(f"output already exists: {args.output}")
        data = json.loads(args.input.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data["items"]
        if isinstance(data, list):
            data = [
                {**row, "wav": str(args.input.parent / row["wav"])}
                if isinstance(row, dict) and "wav" in row else row
                for row in data
            ]
        plan = plan_spacing(data, fps=args.fps, gap_ms=args.gap_ms, guard_ms=args.guard_ms,
                            edge_mode=args.edge_mode)
        if args.materialize_dir is not None:
            materialize(plan, args.materialize_dir)
        output = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as dest:
                dest.write(output)
        else:
            print(output, end="")
    except (ValueError, KeyError, TypeError, ZeroDivisionError, OSError, EOFError, wave.Error) as exc:
        parser.exit(2, f"voice_spacing: {exc}\n")


if __name__ == "__main__":
    main()
