#!/bin/bash
CASES=""
NCUR=10
NTASK=100
echo $NCUR > var/config.ncur
echo $NTASK > var/config.ntask
while read case; do
    ./profile.sh $case $NCUR $NTASK
done <cases_list
./render_result.py
