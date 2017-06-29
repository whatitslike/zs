from .base import BaseSource


class Hot(BaseSource):

    def __init__(self):
        super(Hot, self).__init__()

        self._start_urls = [
            'https://api.zhihu.com/explore/modules/pages?page_token=page%3Ahot_content%3Aday&limit=20&offset=20',
            'https://api.zhihu.com/explore/modules/pages?excerpt_len=70&page_token=page%3Ahot_content%3Aweek',
            'https://api.zhihu.com/explore/modules/pages?excerpt_len=70&page_token=page%3Ahot_content%3Amonth',
        ]

    def _parse(self, json_objs):
        for obj in json_objs['data']:
            t = obj.get('target_type')

            if t == 'answer':
                url = obj['target']['url']
                self.produce_answer(url)

                url = obj['target']['question']['url']
                self.produce_question(url)

            elif t == 'article':
                url = obj['target']['url']
                self.produce_article(url)
