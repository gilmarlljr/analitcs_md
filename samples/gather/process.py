import threading
import time
from random import randint

from core.logger import Logger


class RedditGather(threading.Thread):
    log = Logger().setLogger("[Reddit Gather Process]")

    def __init__(self, connector, url_page):
        threading.Thread.__init__(self)
        self.connector = connector
        self.url_page = url_page

    def run(self):
        RedditGather.log.d("iniciando processo de coleta da url:" + self.url_page)
        time.sleep(randint(1, 5))
        RedditGather.log.d("done processo de coleta da url:" + self.url_page)
