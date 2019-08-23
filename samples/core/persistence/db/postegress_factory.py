import inspect
import sys
import time

from loguru import logger as log
from peewee import ModelBase
from playhouse.migrate import PostgresqlMigrator

import core.persistence.models as models
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

        self.database = PostgresqlExtDatabase('amd_tcc', user='amd_tcc', password='123',
                                              host='localhost', port=5432, autocommit=True, autorollback=True)

        self.migrator = PostgresqlMigrator(self.database)
        self.app_version = version

    def connect(self):
        self.database.connect()

    def start_db(self):
        log.info("Iniciando migracao do banco")
        version = check_db_version()
        log.info("Versao do banco: " + str(version))
        self.connect()
        models_list = []
        for tuple in inspect.getmembers(sys.modules[models.__name__], inspect.isclass):
            if type(tuple[1]) is ModelBase and tuple[0] is not "BaseModel":
                models_list.append(tuple[1])
        if version == 0:
            log.info("Criando novo db")
            self.database.create_tables(models_list, safe=True)
            time.sleep(5)
            version = int(self.app_version.replace('.', ''))
            VersionControl.insert(id=1, app_version=version) \
                .on_conflict(conflict_target=VersionControl.id,
                             preserve=VersionControl.id,
                             update={VersionControl.app_version: version}).execute()
