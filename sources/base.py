import time
import random
import threading
import traceback

from utils import (
    do_request,
    get_logger,
    answer_queue,
    question_queue,
    article_queue,
)


class BaseSource:

    def __init__(self):
        self._logger = get_logger()
        self.answer_queue = answer_queue
        self.question_queue = question_queue
        self.article_queue = article_queue
        self.directions = ['previous', 'next']
        self._start_urls = []

    def _parse_answer_url(self, q_url):
        schema = 'https://api.zhihu.com/questions/%s/answers'
        qid = q_url.split('/')[-1]
        return schema % qid

    @property
    def _start_url(self):
        return random.choice(self._start_urls)

    def produce_question(self, url):
        self.question_queue.put(url)

        answers_url = self._parse_answer_url(url)
        answer_json_objs = do_request(answers_url)
        count = 100
        while not answer_json_objs['paging']['is_end'] and count < 50:
            for obj in answer_json_objs['data']:
                self.answer_queue.put(obj['url'])
                count -= 1

            url = answer_json_objs['paging']['next']
            answer_json_objs = do_request(url)

    def produce_answer(self, url):
        self.answer_queue.put(url)

    def produce_article(self, url):
        self.article_queue.put(url)

    def _parse(self, json_objs):
        raise NotImplementedError

    def _start(self, url, direction):
        while True:
            try:
                json_objs = do_request(url)
                if json_objs['paging']['is_end']:
                    self._logger.info('end reached, sleep for 10 mins!')
                    time.sleep(600)

                    url = self._start_url
                    json_objs = do_request(url)
                    continue

                self._parse(json_objs)

                url = json_objs['paging'][direction]

            except:
                exstr = traceback.format_exc()
                self._logger.error(exstr)
                continue

            finally:
                time.sleep(10)

    def start(self):
        for start_url in self._start_urls:
            for direction in self.directions:
                t = threading.Thread(target=self._start, args=(start_url, direction))
                t.setDaemon(True)
                t.start()
