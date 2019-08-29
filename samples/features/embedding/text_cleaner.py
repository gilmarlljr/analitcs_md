import re

from loguru import logger as log
from nltk.corpus import stopwords

from core.training_models.traning_models import ExpandContractions


class TextCleaner:
    stop = stopwords.words('english')

    @staticmethod
    @log.catch
    def clean(sentence):
        new_sentence = sentence
        new_sentence = TextCleaner.remove_url(new_sentence)
        new_sentence = TextCleaner.remove_whitespaces(new_sentence)
        new_sentence = TextCleaner.expand_contractions(new_sentence)
        return new_sentence

    @staticmethod
    @log.catch
    def remove_url(sentence):
        return re.sub(r"http\S+", "", sentence)

    @staticmethod
    @log.catch
    def expand_contractions(sentence):
        new_sentence = ""
        for phrase in list(
                ExpandContractions().cont.expand_texts(re.compile("[.!?]").split(re.sub(r"[’`´]", "", sentence)),
                                                       precise=True)):
            new_sentence += phrase + "."
        return new_sentence

    @staticmethod
    @log.catch
    def remove_whitespaces(sentence):
        return ' '.join(sentence.split())
