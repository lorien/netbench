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
    with open('config') as inp:
        names = inp.read().splitlines()
    for name in names:
        with open('var/%s.stat' % name) as inp:
            stat = dict(
                x.split('=') for x in
                inp.read().strip().split(',')
            )
            stat['cpu'] = stat['cpu'].rstrip('%')
            stat['rss'] = int(round(int(stat['rss']) / 1024))
        cases.append({
            'name': name,
            'stat': stat,
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
