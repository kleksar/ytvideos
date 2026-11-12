# Audio continuity v07 → v08

Decoded audio to PCM s16le with `ffmpeg -map 0:a:0 -c:a pcm_s16le -f hash -hash sha256 -` independently for v07 and v08; both produce `28e0a73ca76e95d4c7975924bbe607af321220a308f13d04712797fad210b35d`. Both versions use identical narration timing, subtitle inputs and scene frame boundaries; only the S24 image path changed in the scene list. The user listened to and approved sync in v07; this does not claim assistant listening.
