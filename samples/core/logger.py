import datetime
import logging
import os

from core.path import Path


class Logger:
    def __init__(self):
        # create logger
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(logging.DEBUG)
        # create formatter
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

        # create console handler and set level to debug
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(self.formatter)

        # create file handler and set level to debug
        self.log_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

    # add ch to logger
    def setLogger(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.ch)
        fh = logging.FileHandler(filename=os.path.join(Path.logs_path, self.log_filename))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        return self

    def w(self, message):
        self.logger.warning(message)

    def i(self, message):
        self.logger.info(message)

    def d(self, message):
        self.logger.debug(message)

    def e(self, message):
        self.logger.error(message)

    def c(self, message):
        self.logger.critical(message)
