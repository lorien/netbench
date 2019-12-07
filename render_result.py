#!/usr/bin/env python3
import shutil
import os
from jinja2 import Template

TPL_PAGE = '''
<body>
<div style="">
    {% for case in cases %}
    <a href="#case-{{ case.name }}">
        {{ case.name }}
        ({{ case.cpu }}%, {{ case.elapsed }})
    </a>
    {% if not loop.last %}
    &nbsp; | &nbsp;
    {% endif %}
    {% endfor %}
</div>
<div style="">
    {% for case in cases %}
        <a name="case-{{ case.name }}">
        <div>
            <h2>
                {{ case.name }}:
                &ndash;
                {{ case.cpu }}% CPU
                &ndash;
                {{ case.elapsed }} sec
            </h2>
            <img src="files/{{ case.name }}.svg">
        </div>
    {% endfor %}
</div>
</body>
'''

def main():
    result_dir = 'var/result'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.makedirs(result_dir)
    os.makedirs(result_dir + '/files')
    cases = []
    for name in ('socket', 'urllib', 'urllib3', 'ioweb'):
        with open('var/%s.cpu' % name) as inp:
            cpu = inp.read()
        with open('var/%s.time' % name) as inp:
            elapsed = inp.read()
        cases.append({
            'name': name,
            'cpu': cpu,
            'elapsed': elapsed,
        })
        shutil.copy(
            'var/%s.svg' % name,
            'var/result/files/%s.svg' % name
        )
    page = Template(TPL_PAGE).render(cases=cases)
    with open(result_dir + '/index.html', 'w') as out:
        out.write(page)


if __name__ == '__main__':
    main()
