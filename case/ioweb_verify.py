from gevent import monkey
monkey.patch_all()
from ioweb import Crawler, Request

from util import DEFAULT_HEADERS


class TestCrawler(Crawler):
    def __init__(self, taskq, verify, *args, **kwargs):
        self.local_taskq = taskq
        self.local_verify = verify
        super(TestCrawler, self).__init__(*args, **kwargs)

    def task_generator(self):
        while True:
            try:
                url = self.local_taskq.pop()
            except IndexError:
                break
            else:
                yield Request(
                    name='page',
                    url=url,
                    headers=DEFAULT_HEADERS,
                    verify=self.local_verify,
                )

    def handler_page(self, req, res):
        print('%s => %d byts' % (
            res.status,
            len(res.data),
        ))


def run(taskq, ncur):
    bot = TestCrawler(taskq, True, network_threads=ncur)
    bot.run()
