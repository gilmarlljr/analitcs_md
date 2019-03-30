import json
import os

from loguru import logger as log
from peewee import DoesNotExist

from core.path import Path
from core.persistence.db.transition_manager import TrasactionManager
from core.persistence.models import Config, RedditConfig, RedditPage
from core.util import md5_file

__name__ = "CONFIG LOADER"


class ConfigLoader:

    @staticmethod
    def get_config():
        json_file_path = os.path.join(Path.base_path, 'config.json')
        try:
            log.info("Carregando configuracoes do Banco")
            config = Config.get(Config.id == '1').get()
            log.info("verificando se ha alteracoes na configuracao")
            if config.md5 == md5_file(json_file_path):
                log.info("nao ha ateracoes")
                return config
            else:
                TrasactionManager.trasaction(Config.delete(), RedditConfig.delete(), RedditPage.delete())
        except DoesNotExist:
            pass
        return ConfigLoader.load_config(json_file_path)

    @staticmethod
    def load_config(json_file_path):
        log.info("Carregando configuracoes do JSON")
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            reddit_config = RedditConfig.insert(client_id=data['reddit_config']['client_id'],
                                                client_secret=data['reddit_config']['client_secret'],
                                                password=data['reddit_config']['password'],
                                                user_agent=data['reddit_config']['user_agent'],
                                                username=data['reddit_config']['username'],
                                                id=1).on_conflict(
                'replace')
            reddit_pages = []
            for page in data['reddit_config']['pages']:
                reddit_page = {'url': page['url'], 'reddit_config_id': 1}
                reddit_pages.append(reddit_page)
            pages = RedditPage.insert_many(reddit_pages).on_conflict('replace')
            config = Config.insert(id='1', reddit_config_id=1,
                                   md5=md5_file(json_file_path)).on_conflict('replace')
            log.info("Autalizando configuracoes no banco ")
            if TrasactionManager.trasaction(reddit_config, pages, config) is TrasactionManager.SUCESS:
                return Config.get(Config.id == '1').get()
            return None
