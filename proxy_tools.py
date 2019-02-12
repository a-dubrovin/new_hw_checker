# -*- coding: utf-8 -*-
import requests
from lxml.html import fromstring


PROXY_LIST_URL = 'https://free-proxy-list.net/'


class RotateProxy:

    def __init__(self, proxy_list_url=PROXY_LIST_URL):
        self.url = proxy_list_url
        self.proxies = self.get_proxies()

    def get_proxies(self):
        response = requests.get(self.url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                # Grabbing IP and corresponding PORT
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return proxies

    def iget_proxy(self):
        for proxy in self.get_proxies():
            yield proxy
