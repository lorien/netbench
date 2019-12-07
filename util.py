from threading import Thread

DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "",#gzip, deflate",
    "Accept-Language": "en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Connection": "close"
}


def run_threads(taskq, ncur, worker):
    pool = []
    for _ in range(ncur):
        th = Thread(target=worker, args=[taskq])
        th.start()
        pool.append(th)
    [x.join() for x in pool]
