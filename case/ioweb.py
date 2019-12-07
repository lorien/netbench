from ioweb import request

from util import run_threads, DEFAULT_HEADERS


def worker(taskq):
    while True:
        try:
            url = taskq.pop()
        except IndexError:
            break
        else:
            res = request(url, headers=DEFAULT_HEADERS)
            print(res.status)


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
