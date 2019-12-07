from grab.spider import Spider, Task

from util import DEFAULT_HEADERS


class TestSpider(Spider):
    def __init__(self, taskq, *args, **kwargs):
        self.local_taskq = taskq
        super(TestSpider, self).__init__(*args, **kwargs)

    def task_generator(self):
        while True:
            try:
                url = self.local_taskq.pop()
            except IndexError:
                break
            else:
                yield Task(
                    name='page',
                    url=url,
                    headers=DEFAULT_HEADERS,
                    connection_reuse=False,
                )

    def task_page(self, grab, task):
        print('%s => %d byts' % (
            grab.doc.code,
            len(grab.doc.body),
        ))


def run(taskq, ncur):
    bot = TestSpider(
        taskq,
        thread_number=ncur,
        network_service='threaded',
        grab_transport='pycurl',
    )
    bot.run()
