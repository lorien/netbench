from urllib3.contrib.pyopenssl import extract_from_urllib3

from case.urllib3_certifi import run as run_origin

def run(*args):
    extract_from_urllib3()
    run_origin(*args)
