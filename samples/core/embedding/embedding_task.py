from empath import Empath

from core.logger import Logger
from core.persistence.models import Post
from core.task_manager import Task
from core.util import b64decode_and_decompress


class EmpathTask(Task):
    log = Logger().setLogger("[Empath Task]")

    def __init__(self):
        super(EmpathTask, self).__init__()

    def execute(self):
        lexicon = Empath()
        posts = Post.select(Post)
        for post in posts:
            content = b64decode_and_decompress(post.content)
            EmpathTask.log.d("\n\n\n Teste: "+content)
        # print(lexicon.analyze(
        #     , normalize=True))

    def interval(self):
        return 60*5
