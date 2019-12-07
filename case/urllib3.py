from urllib3 import PoolManager

from util import run_threads, DEFAULT_HEADERS


def worker(taskq):
    while True:
        try:
            url = taskq.pop()
        except IndexError:
            break
        else:
            mgr = PoolManager()
            res = mgr.request('GET', url, headers=DEFAULT_HEADERS)
            print('%s => %d bytes' % (
                res.status,
                len(res.data),
            ))


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)