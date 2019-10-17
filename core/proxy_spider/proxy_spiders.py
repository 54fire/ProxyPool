import requests

from core.proxy_spider.base_spider import BaseSpider


class XiciSpider(BaseSpider):
    urls = ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 4)]
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()'
    }
    def get_page_from_url(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        response = requests.get(url, headers=headers)
        return response.content

class Ip3366Spider(BaseSpider):
    urls = ['http://www.ip3366.net/free/?stype={}&page={}'.format(i, j) for i in range(1, 4, 2) for j in range(1, 8)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }

class KuaiSpider(BaseSpider):
    urls = ['http://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 4)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }

class ProxylistplusSpide(BaseSpider):
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1, 4)]
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[5]/text()'
    }
    def get_page_from_url(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)'}
        response = requests.get(url, headers=headers)
        return response.content

class Ip66Spider(BaseSpider):
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 4)]
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }

class Jisu(BaseSpider):
    urls = ['http://www.superfastip.com/welcome/freeip/{}'.format(i) for i in range(1, 4)]
    group_xpath = '/html/body/div[3]/div/div/div[2]/div/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }


if __name__ == '__main__':
    spider = Jisu()
    for proxy in spider.get_proxies():
        print(proxy)