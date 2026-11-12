# Endurance narration text identity reconciliation

The ElevenLabs request receipt records text SHA-256 `77674fd879312fc574139b0f4689d9cb015f200b248d36915d59eae39b1b41d3`. Reconstructing the 8,506 characters from the provider's `alignment.characters` produces exactly that hash. The retained `voice_en_text_v01.txt` contains the same 8,506 characters followed by a single LF newline, for 8,507 characters and SHA-256 `0c445b917804aee66bde9b4a89201858eabb244aeb018261f5ce15640eb6a8ca`. A character diff found only that final newline. The MP3 hash matches the provider receipt, `b972311d983172c43d6a48b568824c3ef94650b8e6bfe4868997da7258893ce3`.

This establishes that the retained text and the submitted character sequence differ only by a final newline. The provider alignment is not audible listening. Pronunciation, complete audible coverage and subtitle sync remain UNVERIFIED.
