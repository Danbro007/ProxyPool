# Redis数据配置#
REDIS_PORT = 6379
REDIS_HOST = "localhost"
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'
# 测试API#
TEST_API = 'http://www.baidu.com'
# 测试代理超时#
PROXY_TIMEOUT = 10
# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300
# 代理池阈值设置#
POOL_UPPER_THRESHOLD = 2000
# 请求头设置#
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
# 代理分数设置#
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
# 一次测试代理数量配置#
BATCH_TEST_SIZE = 40
# 是否开启代理测试器#
ENABLE_TESTER = True
# 是否开启代理获取器#
ENABLE_GETTER = True
#是否开启API#
ENABLE_API = True
# API接口#
API_HOST = '127.0.0.1'
API_PORT = 5433
