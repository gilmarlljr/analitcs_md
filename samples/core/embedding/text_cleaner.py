import re


class TextCleaner:
    remove_url = lambda x: re.sub(r"http\S+", "", x)
    words_count = lambda x: len(str(x.replace('[^\w\s]', '')).split(" "))
    characters_count = lambda x: 1
    stopwords_count = lambda x: 1
    numerics_count = lambda x: 1
    uppercase_count = lambda x: 1
    average_word_length = lambda x: 1
