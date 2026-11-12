# Consultation: scene acceptance

Prompt: A storyboard specifies text inside generated images, but images without it reached the final edit. Recommend a minimal reliable handoff and acceptance control that detects missing assigned wording, preserves intentional text-free scenes, and avoids treating OCR or a checkbox as proof. Keep recommendations concise.

ChatGPT.com, Extra High; model label not independently confirmed; sent and empty composer verified; https://chatgpt.com/c/6aecdd38-6fbc-83eb-8a95-a62b5ad9caa1

Response (captured visible text):
Use a scene-level text contract plus visual acceptance gate. Do not impose a global rule that every image must contain text.

1. Storyboard handoff

Every scene must explicitly declare one of two states:

text_mode: exact — Image must contain specified wording
text_mode: none — Image is intentionally text-free

For exact, include exact wording, including capitalization and punctuation; scene ID and expected image filename; any placement or readability constraints. An unspecified text mode is an incomplete handoff, not permission to omit text.

2. Acceptance control

Before images enter the final edit: Generate a contact sheet using the actual final image assets. Display each image alongside its storyboard text requirement. Have a reviewer visually inspect every exact scene for presence of assigned wording, correct spelling and wording, readability at intended video resolution, no clipping or unwanted overlapping elements. For none scenes, confirm that no unintended text compromises the image.

3. Evidence, not checkbox compliance

Keep a lightweight acceptance record: Scene ID (storyboard reference), asset (exact filename and hash), expected text (exact wording or none), observed result (actual visible wording or absence), review (reviewer and decision). OCR can flag potential omissions or spelling differences, but cannot certify visual correctness. A checkbox records a decision; it does not establish that inspection happened.

4. Release gate

No unaccepted image may enter the final edit. If an image fails, regenerate or correct it, then inspect the replacement asset. A replacement invalidates the previous acceptance. This requires only a storyboard field, a contact sheet, and a human review step. It preserves intentional text-free scenes while making missing assigned wording detectable before rendering.

Capture is a faithful transcription with table and list formatting condensed; no claim of verbatim formatting. Decision: preserve free-form text and reconstruction modes, not just exact/none; record observed requirements and evidence per asset.
