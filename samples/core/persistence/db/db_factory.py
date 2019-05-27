from loguru import logger as log
from playhouse.migrate import SqliteMigrator
from playhouse.sqlite_ext import SqliteExtDatabase

from core.persistence.models import *


def check_db_version():
    try:
        log.info("Verificando versao do banco")
        version_control: VersionControl = VersionControl.get(VersionControl.id == '1').get()
        return version_control.app_version
    except Exception:
        pass
    return 0


class DatabaseFactory:

    def __init__(self, version: str):
        self.database = SqliteExtDatabase(Path.db,
                                          pragmas=(
                                              ('cache_size', -1024 * 64),  # 64MB page-cache.
                                              ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
                                              ('foreign_keys', 1),  # Enforce foreign-key constraints.
                                              ('threads ', 10),  # Max thread allowed.
                                              ('synchronous', 0)  # let OS handle fsync
                                          )
                                          )

        self.migrator = SqliteMigrator(self.database)
        self.app_version = version

    def connect(self):
        self.database.connect()

    def start_db(self):
        log.info("Iniciando migracao do banco")
        version = check_db_version()
        log.info("Versao do banco: " + str(version))
        self.connect()
        if version == 0:
            log.info("Criando novo db")
            self.database.create_tables([VersionControl, RedditConfig, Config, RedditPage, Post, Embendding],
                                        safe=True)
            version = int(self.app_version.replace('.', ''))
            VersionControl.insert(id=1, app_version=version).on_conflict('replace').execute()
