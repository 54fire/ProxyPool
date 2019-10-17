import time
import requests
import json

from utils.http import get_request_headers
from domain import Proxy

'''
1. 检查代理IP速度和匿名程度：
    1. 代理IP速度，就是从发送请求到获取响应的时间间隔
    2. 匿名程度检查：
        1. 对 http://httpbin.org/get 或 https://httpbin.org/get 发送请求
        2. 如果响应的 orgin 中有','分割的两个IP就是透明代理IP
        3. 如果响应的headers 中包含 Proxy-Connection 说明是匿名代理IP
        4. 否则就是高匿代理IP
    3. 检查代理IP协议类型
        如果 http://httpbin.org/get 发送请求可以成功，说明支持http协议
        如果 https://httpbin.org/get 发送请求可以成功，说明支持https协议
'''


def check_proxy(proxy):
    '''
    用于检查指定代理IP的响应速度，匿名程度，支持协议类型
    :param proxy:
    :return:
    '''
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port)
    }
    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, False)
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy




def __check_http_proxies(proxies, is_http=True):
    # 匿名类型 高匿为2，匿名为1，透明为0
    nick_type = -1
    # 代理IP的响应速度
    speed = -1

    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'

    try:
        # 获取开始时间
        start = time.time()
        response = requests.get(test_url, headers=get_request_headers(), proxies=proxies, timeout=10)
        if response.ok:
            speed = round(time.time() - start, 2)

            dic = json.loads(response.text)
            origin = dic['origin']
            proxy_connection = dic['headers'].get('Proxy-Connection', None)
            if ',' in origin:
                nick_type = 2
            elif proxy_connection:
                nick_type = 1
            else:
                nick_type = 0

            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as e:
        return False, nick_type, speed

if __name__ == '__main__':
    proxy = Proxy('121.225.228.51','7798')
    print(check_proxy(proxy))
