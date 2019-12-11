from empath import Empath
from loguru import logger as log
from peewee import JOIN

# from core.persistence.models import Post, PostEmbendding
from core.task_manager import Task
from core.util import b64decode_and_decompress
from features.embedding.text_basic_processing import TextBasicProcessing


class EmpathTask(Task):

    def __init__(self):
        super(EmpathTask, self).__init__()

    def execute(self):

        content = TextBasicProcessing().process("I used to be this way too. I hated mushrooms. I still hate mushrooms that are just sautéed in a pan. I’ve found that cutting them into slices, covering them in olive oil and salt, and putting them in the oven at 425 for like half an hour makes them amazing. They get like a tough, crispy exterior and the interior isn’t weird anymore. It also gets a nice nutty flavor. It’s one of my favorite foods now.")
        # lexicon = Empath()
        # posts = Post.select().join(PostEmbendding, JOIN.LEFT_OUTER, on=(PostEmbendding.post_id == Post.id)) \
        #     .where(
        #     (PostEmbendding.id.is_null() | PostEmbendding.empath == False) & PostEmbendding.content_cleaned == True)
        # for post in posts.iterator():
            content = b64decode_and_decompress(content)
            log.debug("\n\n\n Teste: " + content)
        # print(lexicon.analyze(
        #     , normalize=True))

    def interval(self):
        return 60 * 5
