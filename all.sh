#!/bin/bash
CASES=""
EXPLICIT_CASE="$1"
NCUR=50
NTASK=2000
echo $NCUR > var/config.ncur
echo $NTASK > var/config.ntask
echo $EXPLICIT_CASE
if [ -n "$EXPLICIT_CASE" ]; then
    ./profile.sh $EXPLICIT_CASE $NCUR $NTASK
else
    while read case; do
        ./profile.sh $case $NCUR $NTASK
    done <config
fi
./render_result.py
