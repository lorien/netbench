#!/usr/bin/env python3
from argparse import ArgumentParser
from importlib import import_module


def main():
    parser = ArgumentParser()
    parser.add_argument('test_case')
    parser.add_argument('-c', '--concurrency', type=int, default=1)
    parser.add_argument('-n', '--num-tasks', type=int, default=1)
    opts = parser.parse_args()

    mod = import_module('case.%s' % opts.test_case)

    print('Loading tasks into queue')
    from queue import Queue, Empty
    taskq = []
    for _ in range(opts.num_tasks):
        taskq.append('https://en.wikipedia.org/wiki/Python_(programming_language)')

    print('Starting test, c=%d, n=%d' % (opts.concurrency, opts.num_tasks))
    mod.run(taskq, opts.concurrency)
    print('Test finished')


if __name__ == '__main__':
    main()
