# Activate custom virtualenv
activate_this = '.env-urllib3-1-24/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})
import urllib3
assert urllib3.__version__ == '1.24.3'

from case.urllib3_certifi import run
