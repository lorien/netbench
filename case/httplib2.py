import httplib2

from util import run_threads, DEFAULT_HEADERS


def worker(taskq):
    while True:
        try:
            url = taskq.pop()
        except IndexError:
            break
        else:
            http = httplib2.Http()
            res, data = http.request(
                url, 'GET', headers=DEFAULT_HEADERS
            )
            print('%s => %d bytes' % (
                res['status'],
                len(data),
            ))


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
