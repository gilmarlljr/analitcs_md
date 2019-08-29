from pycontractions import Contractions

from core.training_models.models_loader import ModelsLoader


class ExpandContractions:
    def __init__(self):
        self.cont = Contractions(kv_model=ModelsLoader.getInstance().word2Vec)
        self.cont.load_models()
