import os


class Path:
    base_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..'))
    logs_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..','logs'))



