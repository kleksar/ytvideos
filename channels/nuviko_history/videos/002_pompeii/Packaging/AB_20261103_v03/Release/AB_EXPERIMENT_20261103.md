# Pompeii Final Hours — native A/B/C experiment

{
  "channel_id": "UCbyLx6Rf3iWww4bPZJ2oo2A",
  "video_id": "3mhzbbbWA0g",
  "video_sha256": "5212f7f04dcb607a642dd24e9e3895290c05ab1a30fc6b702efd209bf9c672ff",
  "test_type": "native YouTube title and thumbnail experiment",
  "status": "active — Studio reports checking",
  "started_utc_approx": "2026-11-03T21:31:00Z",
  "primary_metric": "YouTube watch-time share",
  "description_fixed": {
    "file": "Descriptions/B_description_en.txt",
    "sha256": "51b2eacf17927bb59341aabc6ae5d58bddf46c6e779db49722c22eade6f4cd72"
  },
  "variants": [
    {
      "position": 1,
      "id": "B",
      "title": "Pompeii Wasn’t Buried by Lava. What Actually Destroyed It?",
      "thumbnail_file": "Thumbnails/B_thumbnail_v04.png",
      "thumbnail_sha256": "444c90fd29f99598e36173ed7112fb815af6dcaf9cf9ae8db3cf02865b11354a",
      "role": "current public/default package; first platform variant"
    },
    {
      "position": 2,
      "id": "A",
      "title": "Pompeii’s Choice: Flee the Falling Stones or Shelter?",
      "thumbnail_file": "Thumbnails/A_thumbnail_v03.png",
      "thumbnail_sha256": "fa53f96c7ceae92d2b86051266631e8c8e1fbce12a070c90fa89e408d0e32009"
    },
    {
      "position": 3,
      "id": "C",
      "title": "Pompeii’s Ordinary Lives, Preserved Under Ash",
      "thumbnail_file": "Thumbnails/C_thumbnail_v03.png",
      "thumbnail_sha256": "88098b1b327e8aaeb4f6b21db089e29874fa252b1c6dd939def4ab3470ba79a3"
    }
  ],
  "platform_behavior": "YouTube runs variants concurrently and selects by watch-time share. It may run up to two weeks. If there is no clear winner, the first submitted B variant remains the default. Do not change title/thumbnail while active; a change stops the test.",
  "artifacts_uploaded_to_studio": true,
  "local_assets_retirement": "authorized after remote readback; test variants remain stored in YouTube Studio"
}


## TEXT_ONLY update — 2026-11-03

Studio still displayed the test as checking when the channel video details page was inspected. All three variants were uploaded before local cleanup; their local thumbnail files were removed after preserving exact SHA-256 values above. Outcome remains pending. See `../../../../Edit/MediaLifecycle/TEXT_ONLY_REPORT_20261103.md`.
