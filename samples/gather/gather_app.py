import praw

from core.logger import Logger
from core.persistence.models import RedditPage
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
        for pages in RedditPage.select().where(RedditPage.reddit_config_id == 1):
            RedditGather(self.connector, pages.url).start()


