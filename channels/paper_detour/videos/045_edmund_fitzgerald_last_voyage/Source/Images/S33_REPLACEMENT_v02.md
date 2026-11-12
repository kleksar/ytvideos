# S33 replacement v02

- Purpose: correct the observed subtitle overlap in S33 while retaining the accepted story, object, style, and Coast Guard hypothesis status.
- Input/edit target: `Source/Images/paper_v01/S33.png` (same hatch, seam, and single blue-gray water trace).
- Selected result: `Source/Images/paper_v02/S33.png`
- SHA-256: `fe0e3d6405cbb499fabad97c5983e4eece422d6440ce30df28796377c07b4bb2`
- Actual file: opaque RGB PNG, 1672×941, 2,767,406 bytes. Requested target was 3840×2160; returned dimensions are recorded as 1672×941 and are not described as native 4K. Aspect ratio matches the accepted 16:9 source.
- Full-frame review: Paper/card fibers, layered edge thickness, continuous deck plane, contact shadows and lighting are visible. The hatch assembly and complete water trace sit above the subtitle band; no new object or mechanism is introduced. The visible seam and water remain an illustration of a hypothesis, not proof about a specific real hatch.
- Continuity: S32 still introduces the gradual-water hypothesis; S33 retains its proposed hatch-seam route; S34 still shows the ship sitting lower. Camera remains whole-image scale 1.04 with only the accepted horizontal center shift 0.51→0.49.
- Creation tool: built-in image_gen edit; source image was opened with `view_image` before editing.
- Exact selected prompt:

> Use the referenced image as the exact edit target and style reference. Edit only composition. Create a complete full-bleed 16:9 handmade paper/card diorama, maximum available image quality/detail, target 4K UHD 3840×2160. Keep the same single dark charcoal hatch cover, same diagonal angle and scale, same warm tan layered deck surface, same fibers/cut edges/physical thickness/contact shadows, same soft cool side light, and the same single blue-gray water trace. Raise/recompose the existing hatch assembly within the same continuous deck so the seam and the complete droplet/trickle appear together in the upper-middle, centered near (0.50, 0.33); keep all water above y=0.60. This provides generous clearance from the actual lower subtitle layer throughout the accepted whole-frame camera motion (scale 1.04, horizontal pan center 0.49–0.51). Continue the identical natural paper deck plane through the lower frame with subtle physical texture and shadows; do not place any hatch edge or water there and do not make an artificial blank text band. This remains only a conditional illustration of the Coast Guard hypothesis about a not-sufficiently-watertight hatch seam. No new objects, additional water sources, people, damage, machinery, lettering, logos, frame, bars, or story changes.

- Limitation: full-frame still checked; final caption composite and camera extrema still need recheck before MP4 render.
