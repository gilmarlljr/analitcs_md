import datetime
import logging
import os
import sys

from loguru import logger as log

from core.path import Path


def loguru_config():
    log_format = "<green>[{time:DD-MM-YYYY HH:mm:ss.SSS}] </green><blue>[{thread.name}]</blue> {name} <level>[{level}] {message}</level>"
    log.remove()
    log.add(sys.stdout,
            format=log_format)
    log_name = "{time:DD-MM-YYYY}.log"
    log.add(os.path.join(Path.logs_path, log_name), rotation="500 MB",
            format=log_format, retention="30 days", compression="zip")


def logging_config():
    import logging

    logger = logging.getLogger()
    # create formatter
    formatter = logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d] [%(threadName)s] %(name)s [%(levelname)s] %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S')
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    log_filename = 'libs-logs-' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

    file_handler = logging.FileHandler(filename=os.path.join(Path.lib_logs_path, log_filename))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger_peewee = logging.getLogger('peewee')
    logger_peewee = logging.getLogger('peewee')
    logger_peewee.addHandler(file_handler)
    logger_peewee.addHandler(stream_handler)



class LogConfig:
    def __init__(self):
        loguru_config()
        logging_config()


if __name__ == "__main__":
    log.debug("teste de log Debug");
    log.error("teste de log Error");
    log.success("teste de log Sucess");
    log.warning("teste de log Warning");
    log.critical("teste de log Critical");
