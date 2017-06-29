from utils import do_request
from .base import BaseSource


class RoundTables(BaseSource):

    def __init__(self):
        super(RoundTables, self).__init__()

        self._start_urls = [
            'https://api.zhihu.com/roundtables?excerpt_len=75'
        ]

    def _parse(self, json_objs):
        urls = []
        for obj in json_objs['data']:
            t = obj.get('type')
            if t != 'roundtable':
                continue

            urls.append(obj['url'])

        questions_url = [u + '/questions?excerpt_len=75' for u in urls]
        for url in questions_url:
            objs = do_request(url)
            while not objs['paging']['is_end']:
                for obj in objs['data']:
                    if obj['type'] != 'question':
                        continue

                    self.produce_question(obj['url'])

                next_url = objs['paging']['next']
                objs = do_request(next_url)
