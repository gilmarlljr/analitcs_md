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
    logger = logging.getLogger()
    # create formatter
    formatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] [%(threadName)s] [%(levelname)s] %(name)s: %(message)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    log_filename = 'libs-logs-' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'

    file_handler = logging.FileHandler(filename=os.path.join(Path.lib_logs_path, log_filename))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


logging_config()
loguru_config()

if __name__ == '__main__':
    @log.catch
    def my_function(x, y, z):
        # An error? It's caught anyway!
        return 1 / (x + y + z)


    my_function(0, 0, 0)

    log.debug("TESTE DE LOG")
    log.info("TESTE DE LOG")
    log.error("TESTE DE LOG")
    log.success("TESTE DE LOG")
    log.warning("TESTE DE LOG")
    log.critical("TESTE DE LOG")

    log.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")
