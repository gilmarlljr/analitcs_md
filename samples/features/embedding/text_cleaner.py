import re

from loguru import logger as log

from core.training_models.traning_models import ExpandContractions


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
        new_sentence = ""
        for phrase in list(
                ExpandContractions().cont.expand_texts(re.compile("[.!?]").split(re.sub(r"[’`´]", "", sentence)),
                                                       precise=True)):
            new_sentence += phrase + "."
        return new_sentence

    @log.catch
    def remove_whitespaces(self, sentence):
        return ' '.join(sentence.split())
