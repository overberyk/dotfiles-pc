#!/bin/bash

if pgrep -f "kitty --class sysmonitor" >/dev/null; then
    hyprctl dispatch closewindow class:sysmonitor
else
    kitty --class sysmonitor -e btop &
    sleep 0.2
    hyprctl dispatch togglefloating class:sysmonitor
    hyprctl dispatch resizeactive exact 1200 700
    hyprctl dispatch centerwindow
fi