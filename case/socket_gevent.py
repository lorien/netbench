from gevent import monkey
monkey.patch_all()
from util import run_threads
from .socket import worker

def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
