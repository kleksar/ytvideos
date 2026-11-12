# Old render scratch cleanup

On 2026-11-05 17:12:38 +0100, scoped cleanup removed only `Work/production-20261105-v01/full_render_v01/picture.mp4` (device 16777233, inode 128230227, 1686346501 bytes) from the completed v01 render. It is the temporary concatenated picture before subtitles/audio; the completed review MP4, source images, mix, timeline, commands and provenance remain. No live process held the intermediate according to lsof. It can be regenerated from the saved plan and inputs; the historical render command records its former path. Deletion was authorized by the project standing instruction to clean completed owned temporary runs.

Removal confirmed: file no longer exists. APFS physical space reclaimed is not assumed.
