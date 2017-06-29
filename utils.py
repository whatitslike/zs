import json
import logging
import queue

import requests

import proxy


def get_logger():
    logger = logging.getLogger("zhihu-spider")
    formatter = logging.Formatter('%(name)-12s %(message)s')
    file_handler = logging.FileHandler("spider.log")
    file_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger


_headers = {
    'User-Agent': 'osee2unifiedRelease/3.53.0 (iPhone; iOS 10.3.2; Scale/2.00)',
    'x-app-za': 'OS=iOS&Release=10.3.2&Model=iPhone5,2&VersionName=3.53.0&VersionCode=634&Width=640&Height=1136',
    'X-UUID': 'ADDCp6n3-wtLBf1ji8mZKMzrJRMw29chulc=',
    'X-API-Version': '3.0.59',
    'X-APP-VERSION': '3.53.0',
    'Authorization': 'Bearer gt2.0AAAAAAVS-HUL-_epp8IwAAAAAAtNVQJgAgDrwCAkhbZVGCqAKUzf2ACgctdj1A==',
    'X-APP-Build': 'release',
    'X-Network-Type': 'Wifi',
    'Cookie': 'aliyungf_tc=AQAAAGg6XzlAOQQAorTAb5V5ghrEvuHc; z_c0=gt2.0AAAAAAVS-HUL-_epp8IwAAAAAAtNVQJgAgDrwCAkhbZVGCqAKUzf2ACgctdj1A==; d_c0=ADDCp6n3-wtLBf1ji8mZKMzrJRMw29chulc=|1498668306',
    'X-SUGER': 'SURGQT1BNjI5RTkwMi02RUFBLTQwODktOEQ2Ny02NTNGQTcwMTgxRjU=',
}

_proxy_queue = proxy.Proxy()
_proxy_queue.start()

_logger = get_logger()


def do_request(url):
    print('get url %s' % url)
    _logger.info(url)
    proxy = _proxy_queue.get()
    r = requests.get(url, headers=_headers, proxies=[proxy, ])
    jsobj = json.loads(r.content)
    return jsobj


answer_queue = queue.Queue()
question_queue = queue.Queue()
article_queue = queue.Queue()
