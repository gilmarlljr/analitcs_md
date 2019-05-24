from loguru import logger as log


class TransactionManager:
    FAILURE = 'FAILURE'
    SUCESS = 'SUCESS'
    database = None

    def __init__(self, database):
        TransactionManager.database = database

    @staticmethod
    def trasaction(*args):
        with TransactionManager.database.atomic() as transaction:
            try:
                for arg in args:
                    arg.execute()
            except Exception as e:
                log.e("Erro ao processar a transação: " + str(e))
                transaction.rollback()
                return TransactionManager.FAILURE
        return TransactionManager.SUCESS
