import praw

from core.config.config import RedditPages
from core.config.config_loader import ConfigLoader
from core.logger import Logger
from gather.connector import Connector
from gather.process import RedditGather


class GatherAPP:
    log = Logger().setLogger("[Gather APP]")

    def __init__(self, connector):
        self.connector = connector

    def process(self):
        if isinstance(self.connector, praw.Reddit):
            self.reddit_process()

    def reddit_process(self):
        GatherAPP.log.d("iniciando gather APP")
        for pages in RedditPages.select().where(RedditPages.reddit_config_id == 1):
            RedditGather(con, pages.url).start()


if __name__ == '__main__':
    config = ConfigLoader.get_config()
    reddit_config = config.reddit_config.get()
    con = Connector.reddit(reddit_config)
    GatherAPP(con).process()
