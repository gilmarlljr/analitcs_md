import praw
from loguru import logger as log

from core.persistence.models import RedditPage
from core.task_manager import Task
from features.gather.process.reddit_gather_process import RedditGatherProcess

__name__ = "GATHER TASK"


class GatherTask(Task):

    def __init__(self, connector):
        super(GatherTask, self).__init__()
        self.connector = connector

    def execute(self):
        if isinstance(self.connector, praw.Reddit):
            self.reddit_process()
        return True

    def interval(self):
        return 60 * 5  # 5 min

    def reddit_process(self):
        log.debug("iniciando processo de coleta")
        # for pages in RedditPage.select().where(RedditPage.reddit_config_id == 1):
        #     RedditGatherProcess(self.connector, pages.url).start()
