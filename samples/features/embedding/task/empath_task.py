from empath import Empath
from loguru import logger as log
from peewee import JOIN

from core.persistence.models import Post, PostEmbendding
from core.task_manager import Task
from core.util import b64decode_and_decompress

__name__ = "EMPATH TASK"


class EmpathTask(Task):

    def __init__(self):
        super(EmpathTask, self).__init__()

    def execute(self):
        lexicon = Empath()
        posts = Post.select().join(PostEmbendding, JOIN.LEFT_OUTER, on=(PostEmbendding.post_id == Post.id)) \
            .where(
            (PostEmbendding.id.is_null() | PostEmbendding.empath == False) & PostEmbendding.content_cleaned == True)
        for post in posts.iterator():
            content = b64decode_and_decompress(post.content)
            log.debug("\n\n\n Teste: " + content)
        # print(lexicon.analyze(
        #     , normalize=True))

    def interval(self):
        return 60 * 5
