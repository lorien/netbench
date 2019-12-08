from util import run_threads
from .urllib3_certifi import make_request
import urllib3

urllib3.disable_warnings()


def worker(taskq):
    while True:
        try:
            url = taskq.pop()
        except IndexError:
            break
        else:
            make_request(
                url, use_certify=False, cert_reqs='CERT_NONE'
            )


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
