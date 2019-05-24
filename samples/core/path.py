import os


class Path:
    """dir"""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    logs_path = os.path.abspath(os.path.join(base_path, 'logs'))
    lib_logs_path = os.path.abspath(os.path.join(logs_path, 'libs'))
    bin = os.path.abspath(os.path.join(base_path, 'bin'))

<<<<<<< HEAD
    """files"""
    db = os.path.abspath(os.path.join(base_path, '.db'))
    w2v_model = os.path.abspath(os.path.join(bin, 'w2v_model.bin'))
    google_w2v_model = os.path.abspath(os.path.join(bin, 'GoogleNews-vectors-negative300.bin'))

    @staticmethod
    def create_dirs():
        Path.create_bin()
        Path.create_log()
        Path.create_lib_logs()

    @staticmethod
    def create_bin():
        Path.create_dir(Path.bin)

    @staticmethod
    def create_log():
        Path.create_dir(Path.logs_path)

    @staticmethod
    def create_lib_logs():
        Path.create_dir(Path.lib_logs_path)

    @staticmethod
    def create_dir(path):
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                log.debug("Creation of the directory %s failed" % path)
=======
>>>>>>> parent of e94d4b1... aaa
