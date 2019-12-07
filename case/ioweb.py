from gevent import monkey
monkey.patch_all()
from ioweb import Crawler, Request

from util import run_threads, DEFAULT_HEADERS


class TestCrawler(Crawler):
    def __init__(self, taskq, *args, **kwargs):
        self.test_taskq = taskq
        super(TestCrawler, self).__init__(*args, **kwargs)

    def task_generator(self):
        while True:
            try:
                url = self.test_taskq.pop()
            except IndexError:
                break
            else:
                yield Request(
                    name='page',
                    url=url,
                    headers=DEFAULT_HEADERS,
                )

    def handler_page(self, req, res):
        print('%s => %d byts' % (
            res.status,
            len(res.data),
        ))


def run(taskq, ncur):
    bot = TestCrawler(taskq, network_threads=ncur)
    bot.run()
