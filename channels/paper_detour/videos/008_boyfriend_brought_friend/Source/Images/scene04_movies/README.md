# Scene 04 — movie date environment layers

**Status:** DRAFT assets for later compositing; not an approved or registered scene comp.

## Files

- `scene04_movies_background_v01.png` — 941×1672 RGB, opaque vertical background plate. Paper cinema room with blank screen, distant empty seating, aisle/floor. No people or film content.
- `scene04_cinema_seat_fg_v01.png` — 941×1672 RGBA, transparent canvas. Two close dark-blue empty seat backs/armrests intended as a near foreground occluder for the `MOVIES?` accent and lower seated bodies.
- `scene04_seated_trio_mg_v01.png` — 941×1672 RGBA transparent grouped character plane: the narrator in rust-orange, boyfriend in teal/blue, and Matt in coral, seated shoulder-to-shoulder and facing the screen. No chairs are baked into this plane; the foreground seat layer supplies the occlusion.
- `scene04_seated_trio_mg_3x4_sketch_not_for_use.png` — retained first iteration at 1087×1447, the wrong aspect ratio for this scene. Do not use in the edit; it was replaced by the correctly proportioned v01 above.

## Intended assembly

Scene 04 line: “Going to the movies? Matt came with us.”

Candidate order: BG cinema plate → grouped seated-trio MG → FG seat cutout → paper accent `MOVIES?` emerging from behind the foreground seat → continuous grain added last in the actual edit. The distant seating and screen are part of the BG. Keep the screen blank; this story does not identify a film. No signage, brands, posters, popcorn, other audience members, or dialogue are implied.

The trio is currently a pose/scale sketch until registered against the cinema BG and FG seat layer. Do not shift or crop the other assets merely to force a fit; revise the trio if the actual composite shows a mismatch.

All assets were generated with the built-in OpenAI imagegen tool. The approved Paper Detour paper-diorama image was used as a material reference; the user-selected Paper 004 scene 38.08 was used only as a depth/material reference, with its room, phone, person and props excluded. The transparent seat cutout used the generated cinema background as its lighting/perspective reference. The seated-trio layer uses `scene01_hook_master_v02.png` only for identity and clothes, plus the cinema background and seat cutout for scale/perspective. The correctly proportioned trio output is retained at `/Users/diplomat/.codex/generated_images/01a194c5-c133-7833-a824-cb6bf213332c/exec-d021a897-29b6-4074-a1bf-ae8fe3cd3cbc.png`; the earlier wide draft is retained as `exec-e92575a6-a680-43e5-a35e-abd3d603c27d.png`. The cinema BG and seat outputs are `exec-ea849c7b-a927-4fe8-a9a9-c104e5a4c8f9.png` and `exec-5abfeeb8-32b5-4ced-83f5-b51b689dd934.png`.

## Checks and limits

- Verified dimensions and formats: all three usable layers are 941×1672; background RGB/opaque; FG seat and trio RGBA/non-opaque. The earlier trio draft had the wrong 3:4 aspect and is explicitly excluded from use.
- Visually inspected each generated image. The BG has no characters, text or projected film; the FG has two paper seat backs with transparency above; the trio layer shows exactly the three intended characters with the specified clothing colors, facing the screen, without chairs or other story objects.
- Not checked: alpha fringe against the actual background, seat-to-trio registration, true chair contact, side-to-side movement, actual hiding/reveal of `MOVIES?`, or any movement in Palmier. The warm rim at hair/seat edges must be checked against the final composite; it may read as an outline if the cinema lighting does not support it.
- No character assets, audio, animation, Palmier changes or exports were made here.
