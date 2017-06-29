from elasticsearch import Elasticsearch


es = Elasticsearch()


class Question:

    def __init__(self, json_obj):
        self._data = json_obj

    def save(self):
        es.index(index='zhihu', doc_type='question', id=self._data['id'], body=self._data)


class Answer:

    def __init__(self, json_obj):
        self._data = json_obj

    def save(self):
        es.index(index='zhihu', doc_type='answer', id=self._data['id'], body=self._data)
