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

    config = {}
    with open('var/config.ncur') as inp:
        config['ncur'] = int(inp.read())
    with open('var/config.ntask') as inp:
        config['ntask'] = int(inp.read())
    cases = []
    with open('cases_list') as inp:
        names = inp.read().splitlines()
    for name in names:
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
    page = env.get_template('result.html').render(
        config=config,
        cases=cases,
    )
    with open(result_dir + '/index.html', 'w') as out:
        out.write(page)


if __name__ == '__main__':
    main()
