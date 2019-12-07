#!/bin/bash
ENGINE="$1"
CONCURRENCY="$2"
NUM_TASKS="$3"

started=$(date +%s%N)
./runtest.py $ENGINE -c $CONCURRENCY -n $NUM_TASKS &
test_pid=$!
perf stat -p $test_pid -o var/runtest.perf &
perf_pid=$!
py-spy record --nonblocking -o var/runtest.svg -p $test_pid &
spy_pid=$!

wait $test_pid
ended=$(date +%s%N)
elapsed=$(python -c "print(round(($ended - $started)/1000000000, 3))")
echo "ELAPSED: $elapsed sec"
echo $elapsed > var/runtest.time
echo $elapsed > var/$ENGINE.time

kill -INT $perf_pid
cpu=$(cat var/runtest.perf  | grep "CPUs utilized" | sed 's/.* \([0-9.]\+\) *CPUs.*/\1/')
cpu_perc=$(python -c "print(round($cpu * 100, 1))")
echo "CPU: $cpu_perc"
echo $cpu_perc > var/runtest.cpu
echo $cpu_perc > var/$ENGINE.cpu

wait $spy_pid
cp var/runtest.svg var/$ENGINE.svg
