# Gitignore inventory consultation

- Task: gitignore-inventory-20261106. Model: GPT-5.6 Sol; effort: Extra High.
- URL: https://chatgpt.com/c/6aeda8ac-dc90-83ed-b0e5-27293f3080a8
- Controlled lock acquired; prompt saved in companion file; exact visible message confirmed posted and composer empty; VERIFIED released. Answer completed and captured from visible accessibility text.

## Prompt

For a video production Git repository, what conservative, testable criteria distinguish generated image-sequence caches from source images, scene assets and metadata when adding path-specific gitignore rules? Give a short checklist; avoid assuming ignored files are disposable.

## Answer

Use path-specific `.gitignore` rules only when the directory’s role is proven by the production pipeline, not inferred from extensions or filenames.

- Provenance: generated cache files must be reproducibly created by a documented command/render step from tracked inputs. Record the producer and inputs.
- Rebuild test: move the candidate cache directory aside, run the relevant build/render, and verify equivalent files are regenerated without manual intervention.
- Consumer test: search code, manifests, scripts, configs, and CI for references. A path required as an input is not a cache merely because it contains PNG/JPEG files.
- Ownership boundary: prefer dedicated generated paths such as `build/...`, `cache/...`, `frames/.../generated/`. Do not ignore mixed directories containing source and generated assets.
- Sequence signature: generated sequences typically have deterministic numbered names, uniform dimensions/format, large contiguous ranges, and timestamps corresponding to one render. Treat these only as evidence, not proof.
- Source assets: keep manually created/downloaded reference images, approved scene artwork, masks/overlays, thumbnails, reusable backgrounds, or anything that cannot be deterministically reconstructed.
- Metadata: keep manifests, scene definitions, prompts, timing/cut data, hashes, IDs, provenance records, approvals, and configuration unless they are themselves demonstrably regenerated from tracked state.
- Round-trip verification: from a clean checkout plus documented external dependencies, confirm the ignored files can be recreated and the expected output still builds/tests correctly.
- Ignore narrowly: use rules such as `/projects/foo/render/frames/*.png`, not `*.png`, `frames/`, or broad recursive patterns unless every matching path has the same verified semantics.
- Deletion is separate: `.gitignore` only means “do not track by default.” Establish retention/deletion policy independently; ignored caches may still be expensive, required for debugging, or intentionally retained.
