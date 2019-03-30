import os

from gensim.models import KeyedVectors

from core.path import Path

__name__ = "MODELS LOADER"

from loguru import logger as log


class ModelsLoader:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ModelsLoader.__instance == None:
            ModelsLoader()
        return ModelsLoader.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ModelsLoader.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ModelsLoader.__instance = self

    def load(self):
        log.debug("Carregando Modelos")
        log.debug("Iniciando o carregamento do modelo: googleWord2Vec")
        self.googleWord2Vec = KeyedVectors.load_word2vec_format(
            os.path.join(Path.bin, 'GoogleNews-vectors-negative300.bin'), binary=True)
        log.debug("Modelo carregado")
