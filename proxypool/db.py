import random
import re
from redis import StrictRedis
from proxypool.settings import *
from proxypool.error import ProxyPoolEmpty


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        :param host:redis地址
        :param port: redis端口
        :param password: redis密码
        """
        self.db = StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        if not re.match("\d+\.\d+\.\d+\.\d+\:\d+", proxy):
            print("代理:%s 格式不符合规范,丢弃!" % proxy)
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return random.choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise ProxyPoolEmpty

    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score >= MIN_SCORE:
            print("代理%s测试超时当前分数为%s,减1." % (proxy, score))
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print("代理%s当前分数为0,被删除。" % proxy)
            return self.db.zrem(REDIS_KEY, proxy)

    def exitst(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        print("代理%s可用,设置为%s" % (proxy, MAX_SCORE))
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        return self.db.zrevrange(REDIS_KEY, start, stop)


if __name__ == '__main__':
    proxy = "192.178.33.131:1000"
    redis = RedisClient()
    redis.max(proxy)
    redis.decrease(proxy)
    redis.decrease(proxy)

