from .base import BaseSource


class ExploreFeeds(BaseSource):

    def __init__(self):
        super(ExploreFeeds, self).__init__()

        self._start_url = 'https://api.zhihu.com/explore/feeds?limit=20&offset=20'

    def _parse(self, json_objs):
        for obj in json_objs['data']:
            t = obj.get('type')
            if t != 'explore_feed':
                continue

            t = obj.get('target', {}).get('type')
            if t == 'answer':
                url = obj['target']['url']
                self.produce_answer(url)

                url = obj['target']['question']['url']
                self.produce_question(url)

            elif t == 'article':
                url = obj['target']['url']
                self.produce_article(url)

