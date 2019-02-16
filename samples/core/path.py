import os


class Path:
    base_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..'))
    logs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'logs'))




if __name__ == '__main__':
    Path.base_path
    Path.logs_path
