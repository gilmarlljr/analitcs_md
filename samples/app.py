from core import constants
from core.config.config_loader import ConfigLoader
from core.persistence.db import TrasactionManager, DatabaseFactory
from gather.connector import Connector
from gather.gather_app import GatherAPP

__version__ = constants.app_version

if __name__ == '__main__':
    db_factory = DatabaseFactory(__version__)
    db_factory.start_db()
    TrasactionManager(db_factory.database)
    config = ConfigLoader.get_config()
    reddit_config = config.reddit_config.get()
    con = Connector.reddit(reddit_config)
    GatherAPP(con).process()
