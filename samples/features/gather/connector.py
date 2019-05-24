import praw
from loguru import logger as log
from praw.exceptions import ClientException

from core.persistence.models import RedditConfig




class Connector:

    @staticmethod
    def reddit(reddit_config: RedditConfig):
        try:
            log.debug("Criando conexão com o Reddit")
            reddit = praw.Reddit(client_id=reddit_config.client_id,
                                 client_secret=reddit_config.client_secret,
                                 password=reddit_config.password,
                                 user_agent=reddit_config.user_agent,
                                 username=reddit_config.username)
            log.debug("Conectado a API com o usuario: " + str(reddit.user.me()))
            return reddit
        except ClientException:
            log.e("Erro ao conectar com o reddit")
