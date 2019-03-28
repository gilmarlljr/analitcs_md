import asyncio

from core import constants
from core.config.config_loader import ConfigLoader
from core.embedding.embedding_task import EmpathTask, TextCleanTask
from core.persistence.db import TrasactionManager, DatabaseFactory
from core.task_manager import TaskManager
from gather.connector import Connector
from gather.gather_task import GatherTask

__version__ = constants.app_version

if __name__ == '__main__':
    db_factory = DatabaseFactory(__version__)
    db_factory.start_db()
    TrasactionManager(db_factory.database)
    config = ConfigLoader.get_config()
    reddit_config = config.reddit_config.get()
    con = Connector.reddit(reddit_config)
    gather_task = GatherTask(con)

    text_clean_task = TextCleanTask()
    TaskManager({gather_task,text_clean_task}).execute()
