import os


class Path:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    logs_path = os.path.abspath(os.path.join(base_path, 'logs'))
    lib_logs_path = os.path.abspath(os.path.join(logs_path, 'libs'))
    db = os.path.abspath(os.path.join(base_path, '.db'))
    bin = os.path.abspath(os.path.join(base_path, 'bin'))

