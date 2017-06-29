import time


from sources import (
    explore_feeds,
    topstories,
)
from models import (
    Answer,
    Question,
    Article,
)


class Spider:

    def __init__(self):
        self.sources = [
            explore_feeds.ExploreFeeds(),
            topstories.TopStory(),
        ]
        self.consumers = [
            Answer,
            Question,
            Article,
        ]

    def do_crawl(self):
        for source in self.sources:
            source.start()

        for consumer in self.consumers:
            consumer.start()


if __name__ == '__main__':
    s = Spider()
    s.do_crawl()
    try:
        while True:
            time.sleep(2**10)  # actually sleep forever
    except KeyboardInterrupt:
        print('i am gone, Bye!')

