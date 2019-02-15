import json
import logging

import os

from core.config import config
from core.logger import Logger


class ConfigLoader:
    log = Logger().setLogger("[CONFIG LOADER]")
    @staticmethod
    def load_config(path):
        ConfigLoader().log.i("Carregando configuracoes do JSON")
        with open(os.path.join(path, 'config.json')) as json_file:
            data = json.load(json_file)
            ConfigLoader.log.i("Salvando ou atualizando reddit_config")
            reddit_config = config.RedditConfig.insert(id="1",
                                                       client_id=data['reddit_config']['client_id'],
                                                       client_secret=data['reddit_config']['client_secret'],
                                                       password=data['reddit_config']['password'],
                                                       user_agent=data['reddit_config']['user_agent'],
                                                       username=data['reddit_config']['username']).on_conflict(
                'replace').execute()
            ConfigLoader.log.d("Salvando ou atualizando config")
        return config.Config.insert(reddit_config=reddit_config).on_conflict(
                'replace').execute()


if __name__ == '__main__':
    ConfigLoader.load_config("E:\\workspace\\analitcs_md\\samples\\gather")
