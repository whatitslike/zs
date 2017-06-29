from .base import BaseSource


class TopStory(BaseSource):

    def __init__(self):
        super(TopStory, self).__init__()

        self._start_urls = [
            'https://api.zhihu.com/topstory?action=pull&before_id=9&limit=10&action_feed=True&session_token=443067487ef8beca7e6eda932e25725d',
            'https://api.zhihu.com/topstory?action=pull&before_id=109&limit=10&action_feed=True&session_token=443067487ef8beca7e6eda932e25725d',
        ]

    def _parse(self, json_objs):
        for obj in json_objs['data']:
            t = obj.get('type')
            if t != 'feed':
                continue

            t = obj.get('target')
            if not t:
                continue

            a = t.get('type')
            if a != 'answer':
                continue

            self.produce_answer(t['url'])
            self.produce_question(t['question']['url'])
