#!/bin/bash
ENGINE="$1"
CONCURRENCY="$2"
NUM_TASKS="$3"
PID_FILE="var/runtest.pid"

if [ -e $PID_FILE ]; then rm $PID_FILE; fi

# P      Percentage of the CPU that this job got.  This is just user + system times divided by the total running time.  It also prints a percentage sign.
# e      Elapsed real (wall clock) time used by the process, in seconds.
# M      Maximum resident set size of the process during its lifetime, in Kilobytes.
# c      Number of times the process was context-switched involuntarily (because the time slice expired).
# w      Number of times that the program was context-switched voluntarily, for instance while waiting for an I/O operation to complete.
# S      Total number of CPU-seconds used by the system on behalf of the process (in kernel mode), in seconds.
# U      Total number of CPU-seconds that the process used directly (in user mode), in seconds.

STAT_FORMAT="tsys=%S,tuser=%U,ttotal=%e,cpu=%P,rss=%M,swvol=%c,swinvol=%w"
/usr/bin/time -f $STAT_FORMAT -o var/runtest.stat -- ./runtest.py $ENGINE -c $CONCURRENCY -n $NUM_TASKS --pid-file $PID_FILE &
TIME_PID=$!

while [ ! -f $PID_FILE ]; do sleep 0.001; done
TEST_PID=$(cat $PID_FILE)

# redirect out/err py-spy output into file because overwise it deletes (!)
# output of other programs
py-spy record -r20 --nonblocking -o var/runtest.svg -p $TEST_PID > var/py_spy.log 2>&1 &
SPY_PID=$!

wait $TIME_PID
elapsed=$(cat var/runtest.stat | sed 's/.*ttotal=//' | cut -d, -f1)
cpu=$(cat var/runtest.stat | sed 's/.*cpu=//' | cut -d, -f1)
echo "ELAPSED: $elapsed sec"
echo "CPU: $cpu"
cp var/runtest.stat var/$ENGINE.stat

wait $SPY_PID
cp var/runtest.svg var/$ENGINE.svg
