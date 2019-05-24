from loguru import logger as log
from peewee import JOIN

from features.embedding.text_cleaner import TextCleaner
from core.persistence.db.transition_manager import TransactionManager
from core.persistence.models import Post, PostEmbendding
from core.task_manager import Task
from core.util import b64decode_and_decompress




class TextCleanTask(Task):

    def __init__(self):
        super(TextCleanTask, self).__init__()

    def execute(self):
        posts = Post.select().join(PostEmbendding, JOIN.LEFT_OUTER, on=(PostEmbendding.post_id == Post.id)).where(
            PostEmbendding.id.is_null() or PostEmbendding.content_cleaned == False)
        embenddings = []
        count = 0
        cleaned = 0
        for post in posts.iterator():
            title = TextCleaner.remove_url(post.title)
            content = b64decode_and_decompress(post.content)
            content = TextCleaner.remove_url(content)
            text = TextCleaner.expand_contractions(title + " " + content)

            embendding = {'post_id': post.id,
                          'characters_count': TextCleaner.characters_count(text),
                          'words_count': TextCleaner.words_count(text),
                          'stopwords_count': TextCleaner.stopwords_count(text),
                          'numerics_count': TextCleaner.numerics_count(text),
                          'uppercase_count': TextCleaner.uppercase_count(text),
                          'average_word_length': TextCleaner.average_word_length(text),
                          'content_cleaned': True
                          }
            embenddings.append(embendding)
            count += 1
            if embenddings.__len__() == 10 or (count == 100 and embenddings.__len__() != 0):
                TransactionManager.trasaction(PostEmbendding.insert_many(embenddings).on_conflict_ignore())
                cleaned += embenddings.__len__()
                embenddings = []

        log.debug("[SUCESS] Foi realizada a limpeza de " + str(cleaned) + " posts.")
        # print(lexicon.analyze(
        #     , normalize=True))

    def interval(self):
        return 60 * 5
