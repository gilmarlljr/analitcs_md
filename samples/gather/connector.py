import praw
from praw.exceptions import ClientException

from core.logger import Logger
from core.persistence.models import RedditConfig


class Connector:
    log = Logger().setLogger("[CONNECTOR]")

    @staticmethod
    def reddit(reddit_config: RedditConfig):
        try:
            Connector.log.d("Criando conexão com o Reddit")
            reddit = praw.Reddit(client_id=reddit_config.client_id,
                                 client_secret=reddit_config.client_secret,
                                 password=reddit_config.password,
                                 user_agent=reddit_config.user_agent,
                                 username=reddit_config.username)
            Connector.log.d("Conectado a API com o usuario: " + str(reddit.user.me()))
            return reddit
        except ClientException:
            Connector.log.e("Erro ao conectar com o reddit")
