import os

from pycontractions import Contractions

from core.path import Path
from core.training_models.models_loader import ModelsLoader


class ExpandContractions:
    cont = Contractions(kv_model=ModelsLoader.getInstance().word2Vec)

