#!/bin/sh
# Regenerates the README's rendered figures from the tool itself. Run from the repo root.
#   docs/assets/idle.png, stressed.png   one frame each, readings pinned
#   docs/assets/health.gif               the scripted build (needs ffmpeg)
# The hero image (hero-ghostty.png) is a real screenshot and is not made here.
set -eu
cd "$(dirname "$0")/.."
./health --png docs/assets/idle.png --readings temp=38,load=0.1,mem=0.15,disk=0.3,hour=14
./health --png docs/assets/stressed.png --readings temp=73,load=4.7,mem=0.6,disk=0.8,hour=14
if command -v ffmpeg >/dev/null 2>&1; then
  tmp="$(mktemp -d)"
  ./health --demo "$tmp" --fps 8 --size 900x450
  ffmpeg -loglevel error -y -framerate 8 -i "$tmp/frame-%04d.png" \
    -vf "split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=none" \
    -loop 0 docs/assets/health.gif
  rm -rf "$tmp"
else
  echo "ffmpeg not found: health.gif left as is" >&2
fi
ls -la docs/assets
