from core import constants, logger as log_config
from core.config.config_loader import ConfigLoader
from core.dependencies import DependenciesDownloader
from core.training_models.models_loader import ModelsLoader
from features.embedding.task.text_clean_task import TextCleanTask
from core.persistence.db.db_factory import DatabaseFactory
from core.persistence.db.transition_manager import TrasactionManager
from core.task_manager import TaskManager
from features.gather.connector import Connector
from features.gather.task.gather_task import GatherTask
from loguru import logger as log
__version__ = constants.app_version

if __name__ == '__main__':
    log.success("####\n")
    log.success("#### Iniciando o AMDisorder versao: {} \n", __version__)
    log.success("####")
    log_config
    DependenciesDownloader
    ModelsLoader.getInstance().load()
    db_factory = DatabaseFactory(__version__)
    db_factory.start_db()
    TrasactionManager(db_factory.database)
    config = ConfigLoader.get_config()
    reddit_config = config.reddit_config.get()
    con = Connector.reddit(reddit_config)
    gather_task = GatherTask(con)

    text_clean_task = TextCleanTask()
    TaskManager({gather_task, text_clean_task}).execute()
