from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.settings import *
import sys


class Getter:
    def __init__(self):
        self._conn = RedisClient()
        self._crawler = Crawler()

    def is_over_threshold(self):
        if self._conn.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("获取器开始运行")
        if not self.is_over_threshold():
            for callback_index in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_index]
                proxies = self._crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self._conn.add(proxy)
