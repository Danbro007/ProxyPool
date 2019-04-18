import asyncio
import aiohttp
import time
import sys

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.settings import *


class Tester:
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf-8")
                format_proxy = "http://" + proxy
                async with session.get(TEST_API, proxy=format_proxy, timeout=PROXY_TIMEOUT,
                                       allow_redirects=False) as response:
                    if response.status == 200:
                        self.redis.max(proxy)
                    else:
                        self.redis.decrease(proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError,
                    AttributeError):
                self.redis.decrease(proxy)

    def run(self):
        print("测试器开始运行")
        try:
            count = self.redis.count()
            print("当前剩余%s个代理" % count)
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print("正在测试第%s个--第%s个代理" % (start + 1, stop))
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print("代理测试器发生错误%s" % e.args)
