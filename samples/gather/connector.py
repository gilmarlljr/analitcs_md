import praw
import logging

from praw.exceptions import ClientException

from core.logger import Logger


class Connector:
    log = Logger().setLogger("[CONNECTOR]")

    @staticmethod
    def reddit(reddit_config):
        try:
            Connector.log.d("Criando conexão com o Reddit")
            return praw.Reddit(client_id=reddit_config.client_id,
                               client_secret=reddit_config.client_secret,
                               password=reddit_config.password,
                               user_agent=reddit_config.user_agent,
                               username=reddit_config.username)
        except ClientException:
            Connector.log.e("Erro ao conectar com o reddit")
