from loguru import logger as log


class TransactionManager:
    FAILURE = 'FAILURE'
    SUCESS = 'SUCESS'
    database = None

    def __init__(self, database):
        TransactionManager.database = database

    @staticmethod
    def trasaction(*args):
        for arg in args:
            try:
                arg.execute()
            except Exception as e:
                log.error("Erro ao processar a transação["+str(arg.model)+" | "+str(arg)+"]: " + str(e))
                return TransactionManager.FAILURE
        return TransactionManager.SUCESS
