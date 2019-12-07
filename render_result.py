#!/usr/bin/env python3
import shutil
import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

def main():
    result_dir = 'var/result'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.makedirs(result_dir)
    os.makedirs(result_dir + '/files')
    cases = []
    for name in (
            'socket', 'urllib',
            'urllib3_nocertifi', 'urllib3_certifi',
            'ioweb_noverify', 'ioweb_verify',
        ):
        with open('var/%s.cpu' % name) as inp:
            cpu = inp.read().strip()
        with open('var/%s.time' % name) as inp:
            elapsed = inp.read().strip()
        cases.append({
            'name': name,
            'cpu': cpu,
            'elapsed': elapsed,
        })
        shutil.copy(
            'var/%s.svg' % name,
            'var/result/files/%s.svg' % name
        )
    page = env.get_template('result.html').render(cases=cases)
    with open(result_dir + '/index.html', 'w') as out:
        out.write(page)


if __name__ == '__main__':
    main()
