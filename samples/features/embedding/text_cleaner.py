import re

from loguru import logger as log

from features.embedding.contractions import expandContractions


class TextCleaner:
    @log.catch
    def clean(self, sentence):
        new_sentence = sentence
        new_sentence = self.remove_url(new_sentence)
        new_sentence = self.remove_whitespaces(new_sentence)
        new_sentence = self.expand_contractions(new_sentence)
        return new_sentence

    @log.catch
    def remove_url(self, sentence):
        return re.sub(r"http\S+", "", sentence)

    @log.catch
    def expand_contractions(self, sentence):
        new_sentence = re.sub(r"[’`´]", "'", sentence)
        new_sentence = re.sub(r"[.!?]", ".", new_sentence)
        return expandContractions(new_sentence)

    @log.catch
    def remove_whitespaces(self, sentence):
        return ' '.join(sentence.split())
