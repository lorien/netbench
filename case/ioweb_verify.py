from gevent import monkey
monkey.patch_all()

from .ioweb_threaded_verify import TestCrawler


def run(taskq, ncur):
    bot = TestCrawler(taskq, True, network_threads=ncur)
    bot.run()
