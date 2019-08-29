from loguru import logger as log
from peewee import JOIN

from core.persistence.db.transition_manager import TransactionManager
from core.persistence.models import Post, Embendding
from core.task_manager import Task
from core.util import b64decode_and_decompress
from features.embedding.text_cleaner import TextCleaner
from features.embedding.text_data_extractor import TextDataExtractor


class TextCleanTask(Task):

    def __init__(self):
        super(TextCleanTask, self).__init__()

    def execute(self):
        posts = Post.select().join(Embendding, JOIN.LEFT_OUTER, on=(Embendding.post_id == Post.md5)).where(
            Embendding.id.is_null() or Embendding.content_cleaned.is_null())
        embenddings = []
        count = 0
        cleaned = 0
        for post in posts.iterator():
            title = TextCleaner.clean(post.title)
            content = b64decode_and_decompress(post.content)
            content = TextCleaner.clean(content)
            words_count = TextDataExtractor.words_count(content)
            characters_count = TextDataExtractor.characters_count(content)
            stopwords_count = TextDataExtractor.stopwords_count(content)
            average_word_length = TextDataExtractor.average_word_length(content)
            # text = TextCleaner.expand_contractions(title + " " + content)
            # embendding = {'post_id': post.md5,
            #               'characters_count': TextCleaner.characters_count(text),
            #               'words_count': TextCleaner.words_count(text),
            #               'stopwords_count': TextCleaner.stopwords_count(text),
            #               'numerics_count': TextCleaner.numerics_count(text),
            #               'uppercase_count': TextCleaner.uppercase_count(text),
            #               'average_word_length': TextCleaner.average_word_length(text),
            #               'content_cleaned': True
            #               }
            # embenddings.append(embendding)
            # count += 1
            # if embenddings.__len__() == 10 or (count == 100 and embenddings.__len__() != 0):
            #    # TransactionManager.trasaction(Embendding.insert_many(embenddings).on_conflict_ignore())
            #     cleaned += embenddings.__len__()
            #     embenddings = []

        log.debug("[SUCESS] Foi realizada a limpeza de " + str(cleaned) + " posts.")

    def interval(self):
        return 60 * 5
