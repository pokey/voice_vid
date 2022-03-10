#!/usr/bin/env bash
# From https://stackoverflow.com/a/27573049
video="$1"
timestamp="$2"
output="$3"

ffmpeg -ss "$timestamp" -i "$video" -frames:v 1 -q:v 2 "$output"
