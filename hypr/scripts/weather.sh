#!/bin/bash
CITY="Barranquilla"
WEATHER=$(curl -s "wttr.in/${CITY}?format=%C+%t&lang=es" 2>/dev/null)
echo "󰅟 $WEATHER"