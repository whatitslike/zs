import time
import queue
import threading

import requests
from bs4 import BeautifulSoup


class Proxy:

    def __init__(self):
        self.__proxies = queue.Queue()
        self._proxy_repo = [
            'http://www.kuaidaili.com/free/inha/1/',
            'http://www.kuaidaili.com/free/inha/2/',
            'http://www.kuaidaili.com/free/inha/3/',
            'http://www.kuaidaili.com/free/inha/4/',
            'http://www.kuaidaili.com/free/inha/5/',
            'http://www.kuaidaili.com/free/inha/6/',
            'http://www.kuaidaili.com/free/inha/7/',
            'http://www.kuaidaili.com/free/inha/8/',
            'http://www.kuaidaili.com/free/inha/9/',
            'http://www.kuaidaili.com/free/inha/10/',
        ]

    def _parse_content(self, soup_obj):
        trs = soup_obj.find_all('tr')
        for tr in trs:
            ip = tr.find_all(attrs={'data-title': 'IP'})
            port = tr.find_all(attrs={'data-title': 'PORT'})
            if ip and port:
                url = 'http://%s:%s' % (ip[0].text, port[0].text)
                self.__proxies.put(url)
                print('added new proxy: %s' % url)

    def _retrieve_proxy(self):
        while True:
            for url in self._proxy_repo:
                try:
                    r = requests.get(url)
                    soup = BeautifulSoup(r.content)
                    self._parse_content(soup)
                except Exception as e:
                    print(e)

            time.sleep(10)

    def start(self):
        t = threading.Thread(target=self._retrieve_proxy)
        t.setDaemon(True)
        t.start()

    def get(self):
        return self.__proxies.get()


if __name__ == '__main__':
    p = Proxy()
    p.start()
