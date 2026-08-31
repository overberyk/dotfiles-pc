#!/bin/bash
ART_URL=$(playerctl metadata mpris:artUrl 2>/dev/null)
DEST="/tmp/waybar-albumart.jpg"

if [[ "$ART_URL" == file://* ]]; then
    cp "${ART_URL#file://}" "$DEST" 2>/dev/null
elif [[ "$ART_URL" == http* ]]; then
    curl -s "$ART_URL" -o "$DEST" 2>/dev/null
fi