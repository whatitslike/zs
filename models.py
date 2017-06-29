import datetime
import threading

from elasticsearch import Elasticsearch

from utils import (
    do_request,
    answer_queue,
    question_queue,
    article_queue,
)


es = Elasticsearch()


class Base:

    _type = None
    _queue = None
    _threads_num = 3

    def __init__(self, json_obj):
        self._data = json_obj

    def save(self):
        if self._data['type'] != self._type:
            return

        if 'status' in self._data:
            del self._data['status']

        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        self._data.update({'_added_at': now_str})
        es.index(index='zhihu', doc_type=self._type, id=self._data['id'], body=self._data)

    @classmethod
    def _do_job(cls):
        while True:
            url = cls._queue.get()
            json_obj = do_request(url)
            obj = cls(json_obj)
            obj.save()

    @classmethod
    def start(cls):
        for i in range(cls._threads_num):
            t = threading.Thread(target=cls._do_job)
            t.setDaemon(True)
            t.start()


class Question(Base):

    _type = 'question'
    _queue = question_queue



class Answer(Base):

    _type = 'answer'
    _queue = answer_queue


class Article(Base):

    _type = 'article'
    _queue = article_queue
