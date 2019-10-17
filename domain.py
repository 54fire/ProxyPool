from config import MAX_SCORE
'''
定义代理IP的数据模型类型
'''


class Proxy(object):

    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_domain=None):
        # 代理IP的地址
        self.ip = ip
        # 代理ip的端口号
        self.port = port
        # 代理ip支持的协议类型：HTTP是0，HTTPS是1，HTTP和HTTPS都支持是2
        self.protocol = protocol
        # 代理ip的匿名程度，高匿为0，匿名为1，透明为2
        self.nick_type = nick_type
        # 代理ip的响应速度，单位s
        self.speed = speed
        # 代理ip的地区
        self.area = area
        # 代理ip的评分，用于衡量代理的可用性，默认值为MAX_SCORE=50
        self.score = score
        # 不可用域名列表
        self.disable_domain = disable_domain

    def __str__(self):
        # 返回一个字符串
        return str(self.__dict__)