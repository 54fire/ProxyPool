import requests
from lxml import etree

from utils.http import get_request_headers
from domain import Proxy

'''
1. 在base_spider.py文件中，
'''

class BaseSpider(object):
    urls = []
    group_xpath = ''
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):

        if urls:
            self.urls = urls

        if group_xpath:
            self.group_xpath = group_xpath

        if detail_xpath:
            self.detail_xpath = detail_xpath


    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_request_headers())
        return response.content

    def get_first_from_list(self, lis):
        return lis[0] if len(lis) !=0 else ''

    def get_proxies_from_page(self, page):
        element = etree.HTML(page)
        trs = element.xpath(self.group_xpath)
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            yield proxy

    def get_proxies(self):
        for url in self.urls:
            page = self.get_page_from_url(url)
            proxies = self.get_proxies_from_page(page)
            yield from proxies




if __name__ == '__main__':
    config = {
        'urls': ['http://www.ip3366.net/free/?stype=1&page={}'.format(i) for i in range(1,4)],
        'group_xpath': '//*[@id="list"]/table/tbody/tr',
        'detail_xpath': {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'}}
    '''
    config = {
        'urls': ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1,5)],
        'group_xpath': '//*[@id="ip_list"]/tr[position()>1]',
        'detail_xpath': {
            'ip': './td[2]/text()',
            'port': './td[3]/text()',
            'area': './td[4]/a/text()'}}
    '''

    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)