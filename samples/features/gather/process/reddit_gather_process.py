import threading

from loguru import logger as log
from peewee import DoesNotExist
from praw import Reddit

from core.persistence.db.transition_manager import TransactionManager
from core.persistence.models import Post
from core.util import compress_and_b64encode, md5_text




class RedditGatherProcess(threading.Thread):

    def __init__(self, connector: Reddit, url):
        super(RedditGatherProcess, self).__init__()
        self.name = self.name.replace("Thread", "RedditGather")
        self.connector = connector
        self.url = url

    def run(self):
        log.debug("iniciando processo de coleta da url:" + self.url)
        subreddit = self.connector.subreddit(self.url)
        new_subreddit = subreddit.new(limit=200)
        posts = []
        count = 0
        colected = 0
        for submission in new_subreddit:
            try:
                username = submission.author.name
            except Exception:
                username = '[deleted]'
            content = compress_and_b64encode(submission.selftext)

            post = {'title': submission.title,
                    'username': username,
                    'likes_score': submission.score,
                    'url': submission.shortlink,
                    'content': content,
                    'main_url': self.url,
                    'social_media': Post.SOCIAL_MEDIAS.REDDIT,
                    'md5': md5_text(
                        str(str(Post.SOCIAL_MEDIAS.REDDIT) + "|" + username + "|" + submission.title + "|" + self.url))
                    }
            try:
                Post.get(Post.md5 == post.get('md5'))
            except DoesNotExist:
                posts.append(post)
            count += 1
            if posts.__len__() == 10 or (count == 100 and posts.__len__() != 0):
                TransactionManager.trasaction(Post.insert_many(posts).on_conflict_ignore())
                colected += posts.__len__()
                posts = []
        log.success("Coleta da URL '" + self.url + "' coletado " + str(colected) + " posts.")

    def verify_md5(self, posts):
        verified_posts = []
        for post in posts:
            try:
                Post.get(Post.md5 == post.md5)
            except Exception:
                verified_posts.append(post)
        return verified_posts
