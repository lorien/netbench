#!/bin/bash
CASES=""
NCUR=50
NTASK=500
echo $NCUR > var/config.ncur
echo $NTASK > var/config.ntask
while read case; do
    ./profile.sh $case $NCUR $NTASK
done <config
./render_result.py
