import re
from loguru import logger as log
from nltk.corpus import stopwords

from core.training_models.traning_models import ExpandContractions


class TextDataExtractor:
    stop = stopwords.words('english')

    @staticmethod
    @log.catch
    def average_word_length(sentence):
        words = sentence.split()
        if len(words) is not 0:
            return (sum(len(word) for word in words) / len(words))

    @staticmethod
    @log.catch
    def words_count(sentence):
        return len(str(sentence.replace('[^\w\s]', '')).split(" "))

    @staticmethod
    @log.catch
    def characters_count(sentence):
        return str(sentence).__len__()

    @staticmethod
    @log.catch
    def stopwords_count(sentence):
        return len([sentence for sentence in sentence.split() if sentence in TextDataExtractor.stop])

    @staticmethod
    @log.catch
    def numerics_count(sentence):
        return len([sentence for sentence in sentence.split() if sentence.isdigit()])

    @staticmethod
    @log.catch
    def uppercase_count(sentence):
        return len([sentence for sentence in sentence.split() if sentence.isupper()])
