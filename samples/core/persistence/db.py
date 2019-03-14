from playhouse.migrate import SqliteMigrator
from playhouse.sqlite_ext import SqliteExtDatabase

from core.logger import Logger
from core.persistence.models import *


class DatabaseFactory:
    log = Logger().setLogger("[DATABASE]")

    def __init__(self, version: str):
        self.database = SqliteExtDatabase(Path.db, pragmas=(
            ('cache_size', -1024 * 64),  # 64MB page-cache.
            ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
            ('foreign_keys', 1)))  # Enforce foreign-key constraints.
        self.migrator = SqliteMigrator(self.database)
        self.app_version = version

    def connect(self):
        self.database.connect()

    def check_db_version(self):
        try:
            DatabaseFactory.log.i("Verificando versao do banco")
            version_control: VersionControl = VersionControl.get(VersionControl.id == '1').get()
            return version_control.app_version
        except Exception:
            pass
        return 0

    def start_db(self):
        DatabaseFactory.log.i("Iniciando migracao do banco")
        version = self.check_db_version()
        DatabaseFactory.log.i("Versao do banco: " + str(version))
        self.connect()
        if version == 0:
            DatabaseFactory.log.i("Criando novo db")
            self.database.create_tables([VersionControl, RedditConfig, Config, RedditPage, Post], safe=True)
            version = int(self.app_version.replace('.', ''))
            VersionControl.insert(id=1, app_version=version).on_conflict('replace').execute()


class TrasactionManager:
    log = Logger().setLogger("[DATABASE - TRANSACTION]")
    FAILURE = 'FAILURE'
    SUCESS = 'SUCESS'
    database = None

    def __init__(self, database):
        TrasactionManager.database = database

    @staticmethod
    def trasaction(*args):
        with TrasactionManager.database.atomic() as transaction:
            try:
                for arg in args:
                    arg.execute()
            except Exception as e:
                TrasactionManager.log.e("Erro ao processar a transação: " + str(e))
                transaction.rollback()
                return TrasactionManager.FAILURE
        return TrasactionManager.SUCESS
