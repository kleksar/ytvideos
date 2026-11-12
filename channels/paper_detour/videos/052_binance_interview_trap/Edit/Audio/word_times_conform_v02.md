# Word alignment conform v02

- Source alignment: `word_times_en_v01.json`, provider map bound to `voice_en.mp3` SHA-256 `97df8dfb0f32e4b48e38ecf56fc831a48dadb399ed4db9471c23a9a0a19d1124`.
- Source recording: `voice_en.mp3`, 130.96 s, already generated at the accepted 1.10× speed.
- Accepted final mix: `accepted_mix_en_v01.m4a`, SHA-256 `5b8967058d01970deb170ce1a13ad2c1fd23b30b5e5ec26bea67b4eb0975d8fa`; speed evidence records that narration samples were retained unchanged and 10 seconds of digital silence appended, with the final AAC mix duration 140.96 s. The timeline adds 0.04 s to reach exactly 141 s. There is no narration cut, reordering, offset or additional retiming.
- Conform: copy the 337 provider word times from source time 0 at rate 1.0. Keep the exact transcript. The provider's final `consequences.` endpoint was 131.04 s, 0.08 s beyond the retained narration duration; only that final endpoint is set to the actual narration-stream end, 130.96 s. The audio file necessarily ends there, but its last-word boundary has not been confirmed by listening.
- Result map: `word_times_en_v02.json`, bound to the final mix SHA and trimmed UTF-8 transcript hash; total timeline is longer because the appended tail is silent.
- This is mechanical source-to-mix conformity, not audible synchronization verification. Compare first/middle/last phrase boundaries against playback before marking PASS.
