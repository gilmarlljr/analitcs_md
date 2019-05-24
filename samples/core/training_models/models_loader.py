import os

from gensim.models import KeyedVectors
from loguru import logger as log

from core.path import Path


class ModelsLoader:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        if ModelsLoader.__instance is None:
            ModelsLoader()
        return ModelsLoader.__instance

    def __init__(self):
        self.word2Vec = None
        self.w2v_loaded = False
        if ModelsLoader.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ModelsLoader.__instance = self

    def load_w2v_models(self):
        log.debug("Loading Word2Vec model")
        if self.w2v_loaded:
            log.debug("Word2Vec model already loaded ")
            return
        if not os.path.exists(Path.w2v_model):
            log.debug("Loading: %s" % Path.google_w2v_model)
            self.word2Vec = KeyedVectors.load_word2vec_format(Path.google_w2v_model, limit=500000, binary=True)
            self.save_w2v()
        else:
            log.debug("Loading: %s" % Path.w2v_model)
            self.word2Vec = KeyedVectors.load_word2vec_format(Path.w2v_model, binary=True)
        log.debug("Word2Vec model loaded ")
        self.w2v_loaded = True

    def save_w2v(self):
        log.debug("Saving model: Word2Vec")
        self.word2Vec.save_word2vec_format(Path.w2v_model, binary=True)

