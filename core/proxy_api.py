from flask import Flask
from flask import request
import json

from core.db.mongo_pool import MongoPool
from config import PROXIES_MAX_COUNT
'''
1. 在proxy_api.py中，创建ProxyApi类
2. 实现初始化方法
    2.1 初始一个Flask的Web服务
    2.2 实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
        可用通过 protocol 和 domain 参数对IP进行过滤
        protocol：当前请求的协议类型
        domain：当前请求域名
    2.3 实现根据协议类型和域名，提供获取多个高可用代理IP的服务
        可用通过 protocol 和 domain 参数对IP进行过滤
        实现给指定的IP上追加不可用域名的服务
    2.4 如果在获取IP的时候，有指定域名参数，将不再获取该IP，从而进一步提高代理IP的可用性
3. 实现run方法，用于启动Flask的Web服务
4. 实现start的类方法，用于通过类名，启动服务
'''

class ProxyApi(object):

    def __init__(self):
        # 2. 实现初始化方法
        # 2.1 初始一个Flask的Web服务
        self.app = Flask(__name__)
        self.mongo_pool = MongoPool()

        @self.app.route('/random')
        def random():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_proxy(protocol, domain, count=PROXIES_MAX_COUNT)
            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.ip, proxy.port)
            else:
                return '{}:{}'.format(proxy.ip, proxy.port)

        @self.app.route('/proxies')
        def proxies():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')

            proxies = self.mongo_pool.get_proxies(protocol, domain, count=PROXIES_MAX_COUNT)
            proxies = [proxy.__dict__ for proxy in proxies]
            return json.dumps(proxies)

    def run(self):
        self.app.run('0.0.0.0', port=9000)

if __name__ == '__main__':
    # proxy_api = ProxyApi()
    # proxy_api.run()
    pass
