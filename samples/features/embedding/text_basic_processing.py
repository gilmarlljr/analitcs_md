import pandas as pd
from loguru import logger as log
from nltk.corpus import stopwords
from textblob import TextBlob


class TextBasicProcessing:
    stop = stopwords.words('english')

    @log.catch
    def process(self, sentence):
        sentences = sentence.split(".")
        new_sentence = ""
        for each_sentence in sentences:
            each_sentence = self.to_lower(each_sentence)
            each_sentence = self.remove_punctuation(each_sentence)
            each_sentence = self.remove_stopwords(each_sentence)
            each_sentence = self.remove_frequent(each_sentence)
            each_sentence = self.remove_rare(each_sentence)
            each_sentence = self.spell_correct(each_sentence)
            new_sentence += " " + each_sentence
        print(str(TextBlob(sentence).sentiment))
        print(str(TextBlob(new_sentence).sentiment))
        return new_sentence

    @log.catch
    def to_lower(self, sentence):
        return " ".join(x.lower() for x in sentence.split())

    @log.catch
    def remove_punctuation(self, sentence):
        return sentence.replace('[^\w\s,]', '')

    @log.catch
    def remove_stopwords(self, sentence):
        return " ".join(x for x in sentence.split() if x not in TextBasicProcessing.stop)

    @log.catch
    def remove_frequent(self, sentence):
        freq = pd.Series(' '.join(sentence).split()).value_counts()[:10]
        freq = list(freq.index)
        return " ".join(x for x in sentence.split() if x not in freq)

    @log.catch
    def remove_rare(self, sentence):
        freq = pd.Series(' '.join(sentence).split()).value_counts()[-10:]
        freq = list(freq.index)
        return " ".join(x for x in sentence.split() if x not in freq)

    @log.catch
    def spell_correct(self, sentence):
        return str(TextBlob(sentence).correct())

    @log.catch
    def tokenization(self, sentence):
        return ' '.join(sentence.split())

    @log.catch
    def stemming(self, sentence):
        return ' '.join(sentence.split())

    @log.catch
    def lemmatization(self, sentence):
        return ' '.join(sentence.split())
