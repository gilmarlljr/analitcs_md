from pycontractions import Contractions

from core.training_models.models_loader import ModelsLoader
from loguru import logger as log

if __name__ == '__main__':
    sentences = [['first', 'sentence'], ['second', 'sentence']]
    text = ["and my cats keep gettinvg on my bed right as I´m about to sleep".replace("’","'"),
            "I`d like to know how I’d done that!"
            ]
    ModelsLoader.getInstance().load_w2v_models()
    cont = Contractions(kv_model=ModelsLoader.getInstance().word2Vec)
    cont.load_models()
    print(list(cont.expand_texts(text, precise=True)))
