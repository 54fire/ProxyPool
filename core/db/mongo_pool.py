from pymongo import MongoClient
import pymongo
import random

from config import MONGO_URL
from domain import Proxy

class MongoPool(object):

    def __init__(self):
        # 建立数据库连接
        self.client = MongoClient(MONGO_URL)
        self.proxies = self.client['building_pool']['proxi']

    def __del__(self):
        # 关闭数据库连接
        self.client.close()

    def insert_one(self, proxy):
        """2.1 实现插入功能"""

        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            # 使用proxy.ip作为MongoDB中数据的主键：_id
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
        else:
            pass

    def update_one(self, proxy):
        """2.2 实现修改的功能"""
        self.proxies.update_one({'_id': proxy.ip}, {'$set':proxy.__dict__})

    def delete_one(self, proxy):
        """2.3 删除代理IP"""
        self.proxies.delete_one({'_id': proxy.ip})

    def find_all(self):
        """2.4 查询所有代理IP的功能"""
        cursor = self.proxies.find()
        for item in cursor:
            # 删除_id这个key
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        """
        3.1 实现查询功能：根据条件进行查询
        :param conditions:
        :param count:
        :return:
        """
        cursor = self.proxies.find(conditions, limit=count).sort([
            ('score', pymongo.DESCENDING),('speed', pymongo.ASCENDING)
        ])
        proxy_list = []
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=2):
        """
        3.2 实现根据协议类型 和 要访问网站的域名，获取代理IP列表
        :param protocol: 支持的协议http，https
        :param domain: 域名：jd.com
        :param count: 用于限制获取代理ip数量
        :param nick_type: 匿名类型，默认，获取高匿代理IP
        :return: 满足要求的代理IP
        """
        conditions = {'nick_type': nick_type}
        if protocol is None:
            # 如果没有传入协议类型，返回支持http和https的代理IP
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {"$in":[0,2]}
        else:
            conditions['protocol'] = {"$in":[1,2]}

        if domain:
            conditions['disable_domains'] = {'$nin': [domain]}

        return self.find(conditions, count=count)

    def random_proxy(self, protocol=None, domain=None, nick_type=2, count=0):
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, nick_type=nick_type, count=count)
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        if self.proxies.count_documents({'_id':ip, 'disable_domain':domain}) == 0:
            self.proxies.update_one({'_id':ip}, {'$push': {'disable_domain': domain}})
            return True
        return False



if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy('183.63.101.62','55555')
    # proxy = Proxy('184.63.101.62','55555')
    # proxy = Proxy('183.63.101.62','8888')
    # mongo.update_one(proxy)
    # proxy = Proxy('183.63.101.62','8888')
    # mongo.delete_one(proxy)
    for proxy in mongo.find_all():
        print(proxy)
    # dic4 = {'ip': '184.63.101.65', 'port': '55555', 'protocol': 0, 'nick_type': -1, 'speed': 1.8, 'area': None, 'score': 50, 'disable_domain': None}
    # proxy1 = Proxy(**dic1)
    # mongo.insert_one(proxy1)
    # proxy = mongo.get_proxies()
    # print(proxy)
