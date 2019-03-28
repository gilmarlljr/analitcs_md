from empath import Empath
from peewee import JOIN

from core.embedding.text_cleaner import TextCleaner
from core.logger import Logger
from core.persistence.db import TrasactionManager
from core.persistence.models import Post, PostEmbendding
from core.task_manager import Task
from core.util import b64decode_and_decompress


class EmpathTask(Task):
    log = Logger().setLogger("[Empath Task]")

    def __init__(self):
        super(EmpathTask, self).__init__()

    def execute(self):
        lexicon = Empath()
        posts = Post.select().join(PostEmbendding, JOIN.LEFT_OUTER, on=(PostEmbendding.post_id == Post.id)) \
            .where(
            (PostEmbendding.id.is_null() | PostEmbendding.empath == False) & PostEmbendding.content_cleaned == True)
        for post in posts.iterator():
            content = b64decode_and_decompress(post.content)
            EmpathTask.log.d("\n\n\n Teste: " + content)
        # print(lexicon.analyze(
        #     , normalize=True))

    def interval(self):
        return 60 * 5


class TextCleanTask(Task):
    log = Logger().setLogger("[Text Clean Task]")

    def __init__(self):
        super(TextCleanTask, self).__init__()

    def execute(self):
        posts = Post.select().join(PostEmbendding, JOIN.LEFT_OUTER, on=(PostEmbendding.post_id == Post.id)).where(
            PostEmbendding.id.is_null() or PostEmbendding.content_cleaned == False)
        embenddings = []
        count = 0
        cleaned = 0
        for post in posts.iterator():
            content = b64decode_and_decompress(post.content)
            content = TextCleaner.remove_url(content)
            embendding = {'post_id': post.id,
                          'characters_count': TextCleaner.characters_count(content),
                          'words_count': TextCleaner.words_count(content),
                          'stopwords_count': TextCleaner.stopwords_count(content),
                          'numerics_count': TextCleaner.numerics_count(content),
                          'uppercase_count': TextCleaner.uppercase_count(content),
                          'average_word_length': TextCleaner.average_word_length(content),
                          'content_cleaned': True
                          }
            embenddings.append(embendding)
            count += 1
            if embenddings.__len__() == 10 or (count == 100 and embenddings.__len__() != 0):
                TrasactionManager.trasaction(PostEmbendding.insert_many(embenddings).on_conflict_ignore())
                cleaned += embenddings.__len__()
                embenddings = []

        TextCleanTask.log.d("[SUCESS] Foi realizada a limpeza de " + str(cleaned) + " posts.")
        # print(lexicon.analyze(
        #     , normalize=True))

    def interval(self):
        return 60 * 5
