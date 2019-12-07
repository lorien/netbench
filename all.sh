#!/bin/bash
CASES="socket urllib urllib3 ioweb"
for case in $CASES; do
    ./profile.sh $case 10 20
done
