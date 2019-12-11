import os
from loguru import logger as log

class Path:
    """dir"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    logs_dir = os.path.abspath(os.path.join(base_dir, 'logs'))
    lib_logs_dir = os.path.abspath(os.path.join(logs_dir, 'libs'))
    bin_dir = os.path.abspath(os.path.join(base_dir, 'bin'))
    stanford_models_dir = os.path.abspath(os.path.join(bin_dir, 'stanford_models'))

    """files"""
    db = os.path.abspath(os.path.join(base_dir, '.db'))
    w2v_model = os.path.abspath(os.path.join(bin_dir, 'w2v_model.bin'))
    google_w2v_model = os.path.abspath(os.path.join(bin_dir, 'GoogleNews-vectors-negative300.bin'))

    @staticmethod
    def create_dirs():
        Path.create_bin()
        Path.create_log()
        Path.create_lib_logs()

    @staticmethod
    def create_bin():
        Path.create_dir(Path.bin_dir)

    @staticmethod
    def create_log():
        Path.create_dir(Path.logs_dir)

    @staticmethod
    def create_lib_logs():
        Path.create_dir(Path.lib_logs_dir)

    @staticmethod
    def create_dir(path):
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                log.debug("Creation of the directory %s failed" % path)
