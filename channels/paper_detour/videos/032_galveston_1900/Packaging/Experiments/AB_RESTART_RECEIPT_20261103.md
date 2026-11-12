# 032 Galveston — native A/B restart receipt

**Executed:** 2026-11-03 11:27 Europe/Belgrade (10:27 UTC)  
**Channel:** Paper Detour (`UCMVfdfaNxV3ZkI3_J3Eejzw`)  
**Video:** [Galveston: The City That Raised Its Ground](https://www.youtube.com/watch?v=lRkxm3mij5o), `lRkxm3mij5o`

## Before

- Fresh Studio page was explicitly switched to Paper Detour and the target video `lRkxm3mij5o`.
- The A/B dialog showed the setup form, with the current title and current thumbnail as option 1, and no active-test report. This established the canceled state before the new write.
- YouTube Data API status read immediately before the Studio operation confirmed this video belongs to the Paper Detour channel, is public, processed, and has no upload/processing failure.
- Description and visibility were not changed. The existing title and image were retained as baseline option 1.

## Saved test

- Test type: **title + thumbnail pair** (three concurrent variants).
- Option 1: **Galveston: The City That Raised Its Ground** — existing Studio thumbnail, “WHERE'S THE GROUND?”.
- Option 2: **How Galveston Lifted Buildings After the 1900 Hurricane** — `Thumbnails/AB_20261103/variant_b_church_lift.jpg`, “HOW DID IT RISE?”.
- Option 3: **Galveston Built a Seawall — Then Raised Its Streets** — `Thumbnails/AB_20261103/variant_c_raised_grade.jpg`, “THE GROUND ROSE”.
- Both alternate image files were uploaded through Studio's A/B dialog. The preview showed all three expected images and exact title pairings before saving.
- Studio confirmation: “Изменения сохранены.” After saving the video details, Studio showed “Тестирование…” on the video and in Analytics → Reach.
- The live Reach report visibly lists all three thumbnail/title pairs and “Осталось 13 дней 23 часа.” Watch-time-share entries are “–” for all three at read-back, meaning not yet available.
- Description stayed unchanged. Public visibility stayed unchanged. No winner was selected; no stop action was taken.

## Verification limits

- Studio is the native A/B write/read surface; the project API adapter records that the public YouTube Data API has no A/B management endpoint.
- No native experiment ID was exposed.
- The active Studio report confirmed the three uploaded images, their titles, the running status, and remaining time. Current per-variant performance is not yet available.
