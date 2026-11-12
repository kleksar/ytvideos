#!/bin/zsh
set -eu
p=${0:A:h:h}
slug=$1
v="$p/Deliverables/$slug/$slug.mp4"
w="$p/Work/$slug"
ffmpeg -v error -xerror -threads 2 -i "$v" -map 0:v:0 -map 0:a:0 -f null -
ffprobe -v error -show_streams -show_format -of json "$v" > "$w/probe.json"
shasum -a 256 "$v" "$p/Deliverables/$slug/$slug.en.srt" > "$w/export-sha256.txt"
ffmpeg -hide_banner -nostats -i "$v" -vn -af ebur128=peak=true -f null - 2> "$w/loudness.txt"
ffmpeg -v error -y -i "$v" -vn -ac 1 -ar 16000 "$w/final-audio.wav"
whisper "$w/final-audio.wav" --language en --model base.en --threads 4 --word_timestamps True --output_format json --output_dir "$w"
