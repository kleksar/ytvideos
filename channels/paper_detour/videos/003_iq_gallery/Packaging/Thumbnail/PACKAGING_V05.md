# IQ Gallery Shorts — selected cover and metadata v05

Status: local package prepared for review. The user selected the cover; the title and description are still candidates until the actual Studio card preview is checked. Nothing has been applied in Studio or uploaded.

## Project rules found

There is no single Paper Detour document that specifies an exact title/description/hashtag formula. The rules are split across these sources:

- `ytv-video-packaging` requires an honest title/thumbnail pair, the story topic in the title's first visible words, and a check of the actual Shorts card preview before final acceptance. It says not to invent a universal title-length limit.
- `youtube-upload` keeps hashtags in the description separate from the Studio Tags field, says not to infer audience or disclosure defaults, and requires verifying actual saved state when uploading.
- `ytv-youtube-release` routes Paper releases through the playlist registry and the upload skill; it does not authorize publication as part of preparing a package.
- `SHORTS_RELEASE_STRATEGY.md` governs Shorts archive/legacy_stories/release timing but does not prescribe title, description, or hashtag copy.
- The Paper Shorts example 004 uses a compact description and four relevant hashtags: `#Shorts`, topic tags, and `#PaperDetour`. The 001 upload copy also uses short descriptions and separate optional tags.
- `YOUTUBE_PLAYLISTS.md` says IQ Gallery may receive its own playlist only after at least two episodes are published. This one is not assigned a playlist.

The v04 draft used a generic three-hashtag recommendation and omitted the channel's `#Shorts` precedent in the separate Tags field. This v05 package corrects that and keeps the title unchanged.

## Proposed title and description

**Title (45 characters):** `13 Famous People and Their Reported IQ Scores`

The first words identify the subject; the title complements the cover question instead of repeating it. Keep it as a candidate until the YouTube channel card preview confirms that the subject remains clear when the title is truncated.

**Description (407 characters):**

```text
Explore published IQ estimates associated with 13 famous people, including John F. Kennedy, Richard Feynman, Garry Kasparov, Kanye West, RM, and Marilyn vos Savant.

These figures come from different sources and have not been verified through one standardized, comparable test. This is an entertainment-focused collection, not a scientifically established IQ ranking.

#Shorts #IQ #FamousPeople #PaperDetour
```

Four hashtags follow the existing Paper Shorts example. YouTube may display up to three from the description near the title; they are not Studio Tags.

## Separate Studio Tags

`Paper Detour, Shorts, IQ, famous people IQ, reported IQ scores, John F Kennedy, Garry Kasparov, Richard Feynman, Kanye West, Logan Paul, RM Kim Namjoon, Nolan Gould, Frank Lampard, Kate Beckinsale, Sharon Stone, Lee Byung-hun, Quentin Tarantino, Marilyn vos Savant`

## Other prepared fields

- Category: Entertainment (`category_id` 27)
- Video language: English (`en`)
- Audio language: English (`en`)
- Playlist: none for now; follow the two-published-episodes threshold in the playlist registry.
- Visibility when uploaded: Private pending final review.
- Pinned comment draft: “Which reported IQ estimate surprised you the most? Remember, these figures come from different sources and aren't directly comparable.” Not posted.
- Audience, paid-promotion, and altered/synthetic-content fields: not set in this local package. Confirm each from approved episode information and the actual Studio upload form; do not rely on defaults.
- Public description contains no internal source list or AI mention.

The cover and video use visibly stylized paper-diorama imagery. Current YouTube guidance says non-realistic AI content does not require altered/synthetic disclosure; reassess the final video at upload if any imagery becomes photorealistic.

## Selected cover

The exact PNG selected by the user is preserved at `Packaging/Thumbnail/Selected/v04/iq_gallery_short_thumbnail_v04_selected_source.png`. It is pixel-identical to the attached image and to the earlier ImageGen output recorded in the JSON. The large 2160×3840 JPEG is `Packaging/Thumbnail/Selected/v04/iq_gallery_short_thumbnail_v04_selected_2160x3840.jpg`; the phone preview and centered 2:3 crop are in `Packaging/Thumbnail/QA/v04/`.

At 360×640, the question is readable. The centered 2:3 proxy trims some top-row hair and lower portrait edges. The Studio card preview remains pending because the package has not been applied to an uploaded/private draft.

## Consultation and references

The title and metadata copy came from one request in the YT Видео ChatGPT project chat, where the visible mode was **Extra High**. The later channel-format correction was mechanical and follows the current Paper rules and accepted local metadata examples.

- Metadata JSON: `Packaging/Metadata/iq_gallery_shorts_packaging_v05.json`
- Prior draft, superseded: `Packaging/Thumbnail/PACKAGING_V04.md`
- Paper Shorts example: `channels/paper_detour/videos/004_last_video/Packaging/Metadata/004_en_last_video_v5_20261101_youtube.json`
- Upload-copy example: `channels/paper_detour/videos/001_radio_game/UPLOAD_READY.md`
- Shorts packaging rules: `ytv-video-packaging` and `youtube-upload`
- [YouTube title/description limits](https://support.google.com/youtube/answer/57404?hl=en-uk)
- [YouTube hashtag guidance](https://support.google.com/youtube/answer/6390658?hl=en)
- [YouTube guidance on video tags](https://support.google.com/youtube/answer/16559650?hl=en)
- [YouTube synthetic-content disclosure](https://support.google.com/youtube/answer/14328491?hl=en)

No title, description, tags, thumbnail, playlist, audience, disclosure, visibility, comment, or publication state was changed in YouTube Studio.
