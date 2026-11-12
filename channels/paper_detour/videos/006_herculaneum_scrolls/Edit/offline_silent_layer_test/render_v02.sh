#!/bin/zsh
set -eu
base='/Users/diplomat/ytvideos/channels/paper_detour/videos/006_herculaneum_scrolls/Source/Images/layer_test_01'
out='/Users/diplomat/ytvideos/channels/paper_detour/videos/006_herculaneum_scrolls/Edit/offline_silent_layer_test'
grain='/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Source/Graphics/film_grain_8s_prores4444.mov'
ffmpeg -hide_banner -loglevel error -n -filter_complex_threads 2 \
 -loop 1 -framerate 30 -i "$base/background_clean_v02.png" \
 -loop 1 -framerate 30 -i "$base/cradle_rgba_v01.png" \
 -loop 1 -framerate 30 -i "$base/scroll_rgba_v02.png" \
 -loop 1 -framerate 30 -i "$base/accent_what_remains_rgba_v01.png" \
 -loop 1 -framerate 30 -i "$base/tray_rgba_v01.png" \
 -i "$grain" \
 -filter_complex_script "$out/filters_v02.txt" -map '[final]' -an -t 6 -r 30 \
 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -movflags +faststart "$out/silent_layer_test_v02.mp4"
