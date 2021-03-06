import sys
import time


from sources import (
    explore_feeds,
    topstories,
    columns,
    hot,
    roundtables,
    topics,
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
            columns.Columns(),
            hot.Hot(),
            roundtables.RoundTables(),
            topics.Topics(),
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
    start = time.time()
    s = Spider()
    s.do_crawl()
    try:
        while True:
            if time.time() - start > 60 * 60:
                sys.exit()

            time.sleep(2**10)  # actually sleep forever
    except KeyboardInterrupt:
        print('i am gone, Bye!')

