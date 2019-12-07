from gevent import monkey
monkey.patch_all()

from .ioweb_verify import TestCrawler


def run(taskq, ncur):
    bot = TestCrawler(taskq, False, network_threads=ncur)
    bot.run()
