# Scene cache consultation

URL: https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aec772d-5ad4-83ed-b669-fbd0d00b398d
Model: GPT-6, Extra High. Sent exactly; posted message and empty composer confirmed, PENDING recorded then VERIFIED and lock released while answer generating.

## Prompt

Review a scene-level cache design for an existing FFmpeg montage: each still-image scene is independently encoded with motion, then clips are concat-copied and final captions, overlays and audio are composed and encoded. Recommend a conservative complete per-scene cache key, concurrency-safe publication and validation, handling hardware codec variation, provenance and interrupted or corrupt cache, and tests comparing cached and uncached final outputs. Do not use tools or modify files. Be concise.

## Answer

**Recommendation\:** Use a content-addressed, immutable per-scene cache with per-key `flock`, atomic publication, strict stream compatibility checks, and decoded-output regression tests. Keep captions, overlays, and audio outside the scene cache.

### 1\. Complete cache key

Compute `SHA256(canonical_json(spec))`, with sorted keys and explicit defaults.

The specification must include\:

- **Inputs\:** SHA-256 of the source image and every asset actually used by scene encoding.
- **Timeline\:** exact frame count, rational FPS, time base, scene duration and trim rules.
- **Motion\:** crop, zoom, pan, interpolation, easing, coordinate expressions, filter parameters and evaluation order.
- **Rendering\:** complete resolved filtergraph, scaling, aspect ratio, dimensions, pixel format, color space, transfer characteristics and range.
- **Encoding\:** codec, encoder implementation, profile, level, rate control, CRF/QP/bitrate, GOP, B-frames, presets, threading and all effective options.
- **Toolchain\:** FFmpeg version/build identity, relevant library versions, renderer implementation revision and dependency versions affecting output.
- **Hardware\:** encoder backend, device implementation, driver/runtime versions and relevant device capabilities.

Exclude captions, audio and overlays **only if they cannot affect scene-clip generation**\.

Maintain a separate assembly compatibility signature covering codec, dimensions, pixel format, time base, frame rate, codec extradata and relevant color metadata.

### 2\. Concurrency-safe publication

Use the following protocol\:

```text
compute cache key
    ↓
check complete manifest + validate cache entry
    ↓ miss
acquire flock(cache_key.lock)
    ↓
recheck cache
    ↓ miss
encode to unique temporary file on same filesystem
    ↓
validate + calculate SHA-256
    ↓
fsync video and manifest
    ↓
atomic rename video into final location
    ↓
atomic rename manifest LAST
    ↓
fsync directory
    ↓
release lock
```

Important constraints\:

- Readers consider an entry valid only when its manifest exists and verification passes.
- Keep lock files persistent; deleting them can introduce inode-based locking races.
- `flock` automatically releases after process termination, avoiding stale PID leases and PID reuse problems.
- Never overwrite valid immutable entries.
- Crashes leave only incomplete entries or orphaned temporary files, removable by garbage collection.
- Use a local filesystem with reliable advisory locks and atomic renames; network filesystems require separate validation of those guarantees.

### 3\. Cache validation and provenance

Store a manifest containing\:

```json
{
  "schema_version": 1,
  "key": "...",
  "source_sha256": "...",
  "render_spec_sha256": "...",
  "clip_sha256": "...",
  "ffmpeg_build": "...",
  "encoder_identity": "...",
  "pipeline_revision": "...",
  "stream_signature": "...",
  "frame_count": 150,
  "created_at": "..."
}
```

On cache hit\:

1. Verify schema, key, file size and clip SHA-256.
2. Use `ffprobe` to verify stream parameters, duration and frame count.
3. Verify stream compatibility with the other clips before concat-copy.
4. For newly published entries, require successful full decode, not just readable container metadata.

If validation fails, quarantine or discard the entry and regenerate under its per-key lock. Never silently reuse a partially written file.

Preserve the resolved FFmpeg command and input hashes in provenance so a rendered scene remains traceable to its exact inputs.

### 4\. Hardware encoder variation

**Do not treat hardware codecs as interchangeable.**

NVENC, VideoToolbox, VAAPI and software encoders can produce different bitstreams, frame characteristics or metadata with nominally identical settings.

Conservative policy\:

- Partition caches by encoder/backend and relevant driver/runtime identity.
- Require strict concat compatibility even when cache keys are valid.
- Prefer one consistent encoding backend for the entire montage.
- For reproducible regression tests, use a pinned software encoder.
- Do not require bitwise identical outputs across hardware environments.

If mixed cached clips cannot be safely concat-copied, regenerate incompatible clips using the selected common backend. Do not blindly copy them.

### 5\. Required tests

| Test | Expected result |
|--------|--------|
| Cold cache vs uncached | Equivalent decoded video and audio |
| Warm cache vs uncached | Same result, no scene re-encoding |
| Change one source image | Only dependent scene invalidated |
| Change motion parameters | Affected scene invalidated |
| Change captions/audio | Scene cache reused; final output updated |
| Two concurrent identical renders | One publisher; both receive valid clip |
| Kill encoder mid-write | No valid cache entry published |
| Truncated or modified clip | Cache rejected and regenerated |
| FFmpeg/encoder change | Relevant entries invalidated |
| Mixed backend clips | Compatibility verified or regeneration |
| Concatenation boundaries | No missing, duplicated or shifted frames |

Compare final outputs using\:

- **Video\:** decoded frame hashes for deterministic software encoding; otherwise PSNR/SSIM plus exact frame-count and timing checks.
- **Audio\:** decoded PCM comparison or a defined numerical tolerance.
- **Captions/overlays\:** frame-level checks at representative timestamps and segment boundaries.
- **Timeline\:** exact total frame count, timestamps and A/V synchronization.

Compressed MP4 SHA-256 equality is not an appropriate universal acceptance criterion.

### Acceptance criterion

The cache is production-ready when cold, warm, mixed-hit and uncached runs produce equivalent final decoded outputs; concurrent renders never publish incomplete clips; every change affecting scene pixels or encoding invalidates the correct entries; and corrupt or incompatible entries automatically fall back to regeneration.

**Scope recommendation\:** Introduce this beneath the existing scene renderer. Do not redesign the montage pipeline, add distributed locking, or cache the final composition until the per-scene implementation passes these tests.

