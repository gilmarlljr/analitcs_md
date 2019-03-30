import logging
import os

import gensim

from core.path import Path
from core.training_models.models_loader import ModelsLoader

if __name__ == '__main__':
    sentences = [['first', 'sentence'], ['second', 'sentence']]
    ModelsLoader.getInstance().load()
    model = ModelsLoader.getInstance().googleWord2Vec