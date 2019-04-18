import random
import time
import requests
from pyquery import PyQuery as pq
from proxypool.settings import HEADERS
import re
from proxypool.utils import get_page


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs["__CrawlFunc__"] = []
        for k, v in attrs.items():
            if "crawl_" in k:
                attrs["__CrawlFunc__"].append(k)
                count += 1
        attrs["__CrawlFuncCount__"] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("获取到代理：%s" % proxy)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self):
        start_url = "https://www.kuaidaili.com/free/inha/{page}/"
        for i in range(1, 5):
            res = get_page(start_url.format(page=i))
            if res:
                doc = pq(res)
                trs = doc("tbody tr").items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ":".join([ip, port])
                time.sleep(random.randint(1, 4))

    def crawl_xicidaili(self):
        start_url = "https://www.xicidaili.com/wt/{}"
        for i in range(1, 5):
            res = requests.get(start_url.format(i), headers=HEADERS)
            if res:
                doc = pq(res.text)
                trs = doc("#ip_list tr:gt(0)").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(2)").text()
                    port = tr.find("td:nth-child(3)").text()
                    yield ":".join([ip, port])
                time.sleep(random.randint(1, 4))

    def crawl_66ip(self):
        start_url = "http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=2&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip"
        res = get_page(start_url)
        if res:
            proxies = re.findall("(\d+.*?)<br />", res)
            for proxy in proxies:
                yield proxy
            time.sleep(random.randint(1, 4))

    def crawl_89ip(self):
        start_url = "http://www.89ip.cn/index_{}.html"
        for i in range(1, 7):
            res = get_page(start_url.format(i))
            if res:
                doc = pq(res)
                trs = doc("tbody tr").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text()
                    port = tr.find("td:nth-child(2)").text()
                    yield ":".join([ip, port])
                time.sleep(random.randint(1, 4))

    def crawl_superfast(self):
        start_url = "http://www.superfastip.com/welcome/freeip/{}"
        for i in range(1, 11):
            res = get_page(start_url.format(i))
            if res:
                doc = pq(res)
                trs = doc("tbody tr:gt(2)").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text()
                    type = tr.find("td:nth-child(4)").text()
                    port = tr.find("td:nth-child(2)").text()
                    if "HTTPS" not in type:
                        yield ":".join([ip, port])
                time.sleep(random.randint(1, 4))

    def crawl_ip3366(self):
        start_url = "http://www.ip3366.net/?stype=1&page={}"
        for i in range(1, 11):
            res = get_page(start_url.format(i))
            if res:
                doc = pq(res)
                trs = doc("tbody tr").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text()
                    port = tr.find("td:nth-child(2)").text()
                    yield ":".join([ip, port])
                time.sleep(random.randint(1, 4))

    def crawl_xiladaili(self):
        start_url = "http://www.xiladaili.com/gaoni/{}/"
        for i in range(1, 11):
            res = get_page(start_url.format(i))
            if res:
                doc = pq(res)
                trs = doc("tbody tr").items()
                for tr in trs:
                    proxy = tr.find("td:nth-child(1)").text()
                    type = tr.find("td:nth-child(2)").text()
                    if re.match("\w+,", type):
                        yield proxy
                time.sleep(random.randint(1, 4))

    def crawl_gaonidaili_free(self):
        start_url = "http://www.xiladaili.com/api/?uuid=ee4bcc3648ad4df4973ea79146d30278&num=100&place=%E4%B8%AD%E5%9B%BD&category=1&protocol=1&sortby=0&repeat=1&format=3&position=1"
        res = get_page(start_url)
        if res:
            proxies = re.findall("\d+\.\d+\.\d+\.\d+\:\d+", res)
            for proxy in proxies:
                yield proxy


if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl_xicidaili()
    # proxies = freeproxy.get_proxyies("crawl_xicidaili")
