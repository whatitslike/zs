import time
import json
import queue
import threading
import traceback

import requests

import log
import proxy
from models import Question, Answer


class Spider:

    def __init__(self, proxies_queue):
        self._proxies = proxies_queue
        self._headers = {
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
        self._topstory_q = queue.Queue()
        self._question_q = queue.Queue()
        self._answer_q = queue.Queue()

    def _parse_topstory(self, objs):
        for obj in objs['data']:
            t = obj.get('type')
            if t != 'feed':
                continue

            t = obj.get('target')
            if not t:
                continue

            a = t.get('type')
            if a != 'answer':
                continue

            self._question_q.put(t['question']['url'])

    def _get_topstory(self):
        while True:
            url = self._topstory_q.get()
            log.logger.debug('get url %s' % url)
            try:
                json_obj = self._do_get(url)
                next_url = json_obj['paging']['previous']
                self._topstory_q.put(next_url)
                self._parse_topstory(json_obj)
            except:
                exstr = traceback.format_exc()
                log.logger.debug(exstr)
                continue
            finally:
                time.sleep(10)

    def _do_get(self, url):
        proxy = self._proxies.get()
        r = requests.get(url, headers=self._headers, proxies=[proxy, ])
        return json.loads(r.content)

    def _get_answer(self):
        while True:
            url = self._answer_q.get()
            log.logger.debug('get answer url: %s' % url)
            json_obj = self._do_get(url)
            for obj in json_obj['data']:
                s = Answer(obj)
                s.save()

    def _parse_answer_url(self, q_url):
        schema = 'https://api.zhihu.com/questions/%s/answers'
        qid = q_url.split('/')[-1]
        return schema % qid

    def _get_question(self):
        while True:
            url = self._question_q.get()
            log.logger.debug('get question url: %s' % url)
            json_obj = self._do_get(url)
            q = Question(json_obj)
            q.save()

            answer_url = self._parse_answer_url(url)
            self._answer_q.put(answer_url)

    def start(self):
        start_url = 'https://api.zhihu.com/topstory?action=pull&before_id=9&limit=10&action_feed=True&session_token=443067487ef8beca7e6eda932e25725d'
        self._topstory_q.put(start_url)
        tt = threading.Thread(target=self._get_topstory)
        tt.setDaemon(True)
        tt.start()

        ta = threading.Thread(target=self._get_answer)
        ta.setDaemon(True)
        ta.start()

        tq = threading.Thread(target=self._get_question)
        tq.setDaemon(True)
        tq.start()

        [t.join() for t in (tt, ta, tq)]
        log.logger.debug('exiting...')



if __name__ == '__main__':
    proxy = proxy.Proxy()
    proxy.start()

    s = Spider(proxy)
    s.start()
