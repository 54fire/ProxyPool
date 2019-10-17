
MAX_SCORE = 50


# MongoDB数据库的URL
MONGO_URL = 'mongodb://127.0.0.1:27017'

PROXIES_SPIDERS = [
    # 爬虫的全类名，路径：模块.类名
    'core.proxy_spider.proxy_spiders.Ip3366Spider',
    'core.proxy_spider.proxy_spiders.XiciSpider',
    'core.proxy_spider.proxy_spiders.KuaiSpider',
    'core.proxy_spider.proxy_spiders.ProxylistplusSpide',
    'core.proxy_spider.proxy_spiders.Ip66Spider'
]

# 4.3.1 配置文件，增加爬虫运行时间间隔的配置，单位为小时
RUN_SPIDERS_INTERVAL = 2
# 配置检测代理ip的异步数量
TEST_PROXIES_ASYNC_COUNT = 10
# 配置检测代理IP的时间间隔, 单位为小时
TEST_PROXIES_INTERVAL = 2

# 获取代理IP最大数量
PROXIES_MAX_COUNT = 50