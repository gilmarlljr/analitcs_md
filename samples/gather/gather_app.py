from threading import Event

import praw

from core.logger import Logger
from core.persistence.models import RedditPage
from core.task_manager import Task
from gather.process import RedditGather


class GatherTask(Task):
    log = Logger().setLogger("[Gather APP]")

    def __init__(self, connector):
        super(GatherTask, self).__init__()
        self.connector = connector

    def execute(self):
        if isinstance(self.connector, praw.Reddit):
            self.reddit_process()
        return True

    def interval(self):
        return 60*10

    def reddit_process(self):
        GatherTask.log.d("iniciando processo de coleta")
        for pages in RedditPage.select().where(RedditPage.reddit_config_id == 1):
            RedditGather(self.connector, pages.url).start()



