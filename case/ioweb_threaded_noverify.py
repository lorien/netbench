from .ioweb_threaded_verify import TestCrawler


def run(taskq, ncur):
    bot = TestCrawler(taskq, False, network_threads=ncur)
    bot.run()
