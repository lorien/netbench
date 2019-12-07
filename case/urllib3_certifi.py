import logging

from urllib3 import PoolManager, __version__
import certifi

from util import run_threads, DEFAULT_HEADERS


def make_request(url, use_certify):
    mgr = PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=(
            certifi.where() if use_certify else None
        ),
    )
    res = mgr.request('GET', url, headers=DEFAULT_HEADERS)
    print('%s => %d bytes' % (
        res.status,
        len(res.data),
    ))


def worker(taskq):
    while True:
        try:
            url = taskq.pop()
        except IndexError:
            break
        else:
            make_request(url, use_certify=True)


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
