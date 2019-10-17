# 打猴子补丁
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import importlib
import time
import schedule

from config import PROXIES_SPIDERS, RUN_SPIDERS_INTERVAL
from core.proxy_validate.httpbin_validater import check_proxy
from core.db.mongo_pool import MongoPool

'''
4. 使用`schedule`模块，实现每隔一定时间，执行一次爬取任务
    4.1 定义一个`start`的类方法
    4.2 创建当前类的对象，调用`run`方法
    4.3 使用`schedule`模块，每隔一定的时间，执行当前对象的`run`方法
'''
class RunSpider(object):

    def __init__(self):
        self.mongo_pool = MongoPool()
        # 协程池
        self.coroutine_pool = Pool()

    def get_spider_from_config(self):
        for full_class_name in PROXIES_SPIDERS:
            # 获取模块名和类名
            module_name, class_name = full_class_name.rsplit('.', maxsplit=1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            spider = cls()
            yield spider


    def run(self):
        spiders =self.get_spider_from_config()
        for spider in spiders:
            # self.__execute_one_spider_task(spider)
            self.coroutine_pool.apply_async(self.__execute_one_spider_task, args=(spider, ))
        self.coroutine_pool.join()

    def __execute_one_spider_task(self, spider):
        try:
            for proxy in spider.get_proxies():
                proxy = check_proxy(proxy)
                print(proxy)
                if proxy.speed != -1:
                    self.mongo_pool.insert_one(proxy)
        except Exception as ex:
            pass

    @classmethod
    def start(cls):
        rs = RunSpider()
        rs.run()
        # 4.3.1 配置文件，增加爬虫运行时间间隔的配置，单位为小时
        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(rs.run)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    # run = RunSpider()
    # run.run()
    RunSpider.start()
    ''' 测试 schedule
    def task():
        print('kk')

    schedule.every(2).seconds.do(task)
    while True:
        schedule.run_pending()
        time.sleep(1) '''

