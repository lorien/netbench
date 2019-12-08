from urllib.request import Request, urlopen
import gzip

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
            if res.info().get('content-encoding') == 'gzip':
                data = gzip.decompress(res.read())
            else:
                data = res.read()
            print('%s => %d bytes' % (
                res.getcode(),
                len(data),
            ))


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
