from loguru import logger as log

__name__ = "TRANSITION MANAGER"


class TrasactionManager:
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
                log.e("Erro ao processar a transação: " + str(e))
                transaction.rollback()
                return TrasactionManager.FAILURE
        return TrasactionManager.SUCESS
