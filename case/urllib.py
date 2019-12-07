from urllib.request import Request, urlopen

from util import run_threads, DEFAULT_HEADERS


def worker(taskq):
    while True:
        try:
            url = taskq.pop()
        except IndexError:
            break
        else:
            req = Request(url)
            for key, val in DEFAULT_HEADERS.items():
                req.add_header(key, val)
            res = urlopen(req)
            data = res.read()
            print('%s => %d bytes' % (
                res.getcode(),
                len(data),
            ))


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
