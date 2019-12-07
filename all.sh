#!/bin/bash
CASES="socket urllib urllib3_nocertifi urllib3_certifi ioweb_noverify ioweb_verify"
for case in $CASES; do
    ./profile.sh $case 10 100
done
./render_result.py
