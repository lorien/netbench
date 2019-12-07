from urllib3 import PoolManager

from util import run_threads, DEFAULT_HEADERS


def worker(taskq):
    mgr = PoolManager()
    while True:
        try:
            url = taskq.pop()
        except IndexError:
            break
        else:
            res = mgr.request('GET', url, headers=DEFAULT_HEADERS)
            print(res.status)


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
