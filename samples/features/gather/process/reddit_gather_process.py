import threading

from loguru import logger as log
from peewee import DoesNotExist
from praw import Reddit
from praw.models import Submission

from core.persistence.db.transition_manager import TransactionManager
from core.persistence.models import Post, User
from core.util import compress_and_b64encode, md5_text

post_limit = 200


class RedditGatherProcess(threading.Thread):

    def __init__(self, connector: Reddit, url):
        super(RedditGatherProcess, self).__init__()
        self.name = self.name.replace("Thread", "RedditGather")
        self.connector = connector
        self.url = url

    def run(self):

        log.debug("iniciando processo de coleta da url:" + self.url)
        subreddit = self.connector.subreddit(self.url)
        new_subreddit = subreddit.new(limit=post_limit)

        posts = []
        users = []
        count = 0
        collected = 0
        exist_count = 0
        for submission in new_subreddit:
            user = self.__create_user(submission)
            post = None
            if user is not None:
                users.append(user.to_dict())
                post = self.__create_post(user, submission)
            if post is not None:
                posts.append(post.to_dict())
                count += 1
            else:
                exist_count += 1
            if posts.__len__() == 10 or exist_count == 5 or count == post_limit:
                if posts.__len__() != 0:
                    log.debug("inserindo " + str(count))
                    TransactionManager.trasaction(User.insert_many(users).on_conflict_ignore())
                    TransactionManager.trasaction(Post.insert_many(posts).on_conflict_ignore())
                    collected += posts.__len__()
                    posts = []
                    users = []
                if exist_count == 5:
                    break
        log.success("Coleta da URL '" + self.url + "' coletado " + str(collected) + " posts.")

    def __create_user(self, submission: Submission):
        user = User()
        user_subreddit = None
        try:
            user.username = submission.author.name
            user_subreddit = submission.author.subreddit
        except Exception:
            user.username = '[unknown]'
        if user_subreddit is not None:
            user.display_name = user_subreddit['display_name']
            user.about = user_subreddit['description']
        else:
            user.display_name = user.username
            user.about = ''
        user.gender = User.GENDERS.NONE
        user.social_media = User.SOCIAL_MEDIAS.REDDIT
        return user

    def __create_post(self, user: User, submission: Submission):
        md5 = md5_text(
            str(str(User.SOCIAL_MEDIAS.REDDIT) + "|" + user.username + "|" + submission.title + "|" + self.url))
        try:
            Post.get(Post.md5 == md5)
            log.debug("existe " + md5)
            return None
        except DoesNotExist:
            post = Post()
            post.user = user
            post.title = submission.title
            post.content = compress_and_b64encode(submission.selftext)
            post.url = submission.shortlink
            post.likes_score = submission.score
            post.main_url = self.url
            post.md5 = md5
            return post

    def __verify_md5(self, posts):
        verified_posts = []
        for post in posts:
            try:
                Post.get(Post.md5 == post.md5)
            except Exception:
                verified_posts.append(post)
        return verified_posts
