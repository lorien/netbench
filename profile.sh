#!/bin/bash
ENGINE="$1"
CONCURRENCY="$2"
NUM_TASKS="$3"

./runtest.py $ENGINE -c $CONCURRENCY -n $NUM_TASKS &
test_pid=$!
perf stat -p $test_pid -o var/runtest.perf &
perf_pid=$!
py-spy record -o var/runtest.svg -p $test_pid &
spy_pid=$!

wait $test_pid
kill -INT $perf_pid

wait $spy_pid
cp var/runtest.svg var/$ENGINE.svg
