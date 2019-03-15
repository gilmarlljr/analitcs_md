import threading
import uuid

from peewee import DoesNotExist
from praw import Reddit

from core.logger import Logger
from core.persistence.db import TrasactionManager
from core.persistence.models import Post
from core.util import compress_and_b64encode, md5_text


class RedditGather(threading.Thread):
    log = Logger().setLogger("[Reddit Gather Process]")

    def __init__(self, connector: Reddit, url):
        super(RedditGather, self).__init__()
        self.name = self.name.replace("Thread","RedditGather")
        self.connector = connector
        self.url = url

    def run(self):
        RedditGather.log.d("iniciando processo de coleta da url:" + self.url)
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
                TrasactionManager.trasaction(Post.insert_many(posts).on_conflict_ignore())
                colected += posts.__len__()
                posts = []
        RedditGather.log.d("[SUCESS] Coleta da URL '" + self.url + "' coletado " + str(colected) + " posts.")

    def verify_md5(self, posts):
        verified_posts = []
        for post in posts:
            try:
                Post.get(Post.md5 == post.md5)
            except Exception:
                verified_posts.append(post)
        return verified_posts
