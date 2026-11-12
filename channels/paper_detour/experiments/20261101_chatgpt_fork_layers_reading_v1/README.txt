Paper Detour — ChatGPT fork layers test, 2026-11-01

MASTER + two UI forks; original BG, forks MG/FG. Visible mode Extra High.
Final experimental files: MASTER.png, BG.png, MG.png, FG.png, all 941x1672. MG/FG have true alpha.
COMPOSITE.png is local diagnostic alpha-over at zero offset and unit scale. It is not a production render.
Initial generation did not reliably preserve registration. ChatGPT supplied processed mask/image files afterward.
Self-review (not independent): trial works but carpet, chair/foot contour and contact shadows differ. Motion not checked.

BBox experiment requested by user: MG_generated_candidate.png -> MG_bbox_uniform_TEST.png, uniform scale and translation from bbox_transform.json. BBOX_TEST_comparison.jpg shows master, before, after, 50% overlay. General size/position improved; internal shape still differs. This test is not the final MG.png.

PROMPTS.txt contains original four generation prompts. Additional numbered prompts document narrow checks and corrections. Full details: experiment_log.json and metrics.json.
