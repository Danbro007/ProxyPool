import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.settings import *
from proxypool.tester import Tester
from proxypool.getter import Getter


class Schduler:
    def tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            tester.run()
            print("测试器暂停")
            time.sleep(cycle)

    def getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            getter.run()
            print("获取器暂停")
            time.sleep(cycle)

    def api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if ENABLE_GETTER:
            getter_process = Process(target=self.getter)
            getter_process.start()
        if ENABLE_TESTER:
            tester_process = Process(target=self.tester)
            tester_process.start()
        if ENABLE_API:
            api_process = Process(target=self.api)
            api_process.start()


if __name__ == '__main__':
    tester = Tester()
    tester.run()
