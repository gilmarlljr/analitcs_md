import json
import logging

import os

from peewee import DoesNotExist

from core.config.config import *
from core.logger import Logger
from core.crypt import md5
from core.path import Path


class ConfigLoader:
    log = Logger().setLogger("[CONFIG LOADER]")

    @staticmethod
    def get_config():
        json_file_path = os.path.join(Path.base_path, 'config.json')
        try:
            ConfigLoader.log.i("Carregando configuracoes do Banco")
            config = Config.get(Config.id == '1').get()
            ConfigLoader.log.i("verificando se ha alteracoes na configuracao")
            if config.md5 == md5(json_file_path):
                ConfigLoader.log.i("nao ha ateracoes")
                return config
        except DoesNotExist:
            pass
        return ConfigLoader.load_config(json_file_path)

    @staticmethod
    def load_config(json_file_path):
        ConfigLoader.log.i("Carregando configuracoes do JSON")
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            ConfigLoader.log.i("Atualziando reddit_config")
            reddit_config = RedditConfig.insert(client_id=data['reddit_config']['client_id'],
                                                client_secret=data['reddit_config']['client_secret'],
                                                password=data['reddit_config']['password'],
                                                user_agent=data['reddit_config']['user_agent'],
                                                username=data['reddit_config']['username'],
                                                id=1).on_conflict(
                'replace').execute()
            reddit_pages = []
            for page in data['reddit_config']['pages']:
                reddit_page = {'url': page['url'], 'reddit_config': reddit_config}
                reddit_pages.append(reddit_page)
            ConfigLoader.log.d("Atualziando paginas")
            RedditPages.insert_many(reddit_pages).on_conflict('replace').execute()
            ConfigLoader.log.d("Atualziando config")
        return Config.insert(id='1', reddit_config=reddit_config,
                             md5=md5(json_file_path)).on_conflict(
            'replace').execute()

