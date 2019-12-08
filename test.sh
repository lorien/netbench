#!/bin/bash
/usr/bin/time -v -o var/z -- echo "ok" &
echo "B"
wait $!
