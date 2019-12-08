from gevent import monkey
monkey.patch_all()

from case.urllib3_noverify import run
