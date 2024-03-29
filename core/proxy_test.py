from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import schedule
import time

from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validater import check_proxy
from config import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT, TEST_PROXIES_INTERVAL

'''
9. 实现代理池的检测模块
目的：检查代理IP的可用性，保证代理池中代理IP基本可用
思路
    1. 在proxy_test.py中，创建ProxyTester类
    2. 提供一个 run 方法，用于处理检测代理IP核心逻辑
        2.1 从数据库中获取所以代理IP
        2.2 遍历代理IP列表
        2.3 检测代理可用性
        2.4 如果代理不可用，让代理分数-1，如果代理分数等于0就从数据库中删除该代理IP
        2.5 如果代理可用，就恢复该代理的分数，更新到数据库中
'''

class ProxyTester(object):

    def __init__(self):
        self.mongo_pool = MongoPool()
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __check_callback(self, temp):
        self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    def run(self):
        # 提供一个 run 方法，用于处理检测代理IP核心逻辑
        # 2.1 从数据库中获取所以代理IP
        proxies = self.mongo_pool.find_all()
        # 2.2 遍历代理IP列表
        for proxy in proxies:
            # self.__check_one_proxy(proxy)
            # 把代理ip添加到队列中
            self.queue.put(proxy)
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)
        self.queue.join()

    def __check_one_proxy(self):
        ''' 检查一个代理IP的可用性 '''
        proxy = self.queue.get()
        # 2.3 检测代理可用性
        print(proxy)
        proxy = check_proxy(proxy)
        if proxy.speed == -1:
            proxy.score -= 1
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                # 否则更新该代理ip
                self.mongo_pool.update_one(proxy)
        else:
            # 2.5 如果代理可用，就恢复该代理的分数，更新到数据库中
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        self.queue.task_done()

    @classmethod
    def start(cls):
        # 4.2.1 创建本类对象
        proxy_tester = cls()
        proxy_tester.run()

        schedule.every(TEST_PROXIES_INTERVAL).hours.do(proxy_tester.run)
        while True:
            schedule.run_pending()
            time.sleep(1)



if __name__ == '__main__':
    # pt = ProxyTester()
    # pt.run()
    ProxyTester.start()


