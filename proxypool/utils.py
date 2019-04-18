import requests
from fake_useragent import UserAgent, FakeUserAgentError
from proxypool.settings import HEADERS
from requests.exceptions import ConnectionError


def get_page(url):
    print("正在获取:%s" % url)
    try:
        res = requests.get(url=url, headers=HEADERS)
        if res.status_code == 200:
            return res.text
    except ConnectionError:
        print("爬取失败", url)
        return None
