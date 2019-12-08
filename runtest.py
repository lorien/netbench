#!/usr/bin/env python3
from argparse import ArgumentParser
from importlib import import_module
import os
import time


def main():
    parser = ArgumentParser()
    parser.add_argument('test_case')
    parser.add_argument('-c', '--concurrency', type=int, default=1)
    parser.add_argument('-n', '--num-tasks', type=int, default=1)
    parser.add_argument('--pid-file')
    opts = parser.parse_args()

    if opts.pid_file:
        with open(opts.pid_file, 'w') as out:
            out.write(str(os.getpid()))
    
    # Sleep a bit to give profilng tools a time
    # to start their work
    time.sleep(0.01)

    mod = import_module('case.%s' % opts.test_case)

    print('Loading tasks into queue')
    taskq = []
    for _ in range(opts.num_tasks):
        taskq.append('https://en.wikipedia.org/wiki/Python_(programming_language)')

    print('Starting test, c=%d, n=%d' % (opts.concurrency, opts.num_tasks))
    mod.run(taskq, opts.concurrency)
    print('Test finished')


if __name__ == '__main__':
    main()
