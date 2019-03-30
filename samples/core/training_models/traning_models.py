import os

from pycontractions import Contractions

from core.path import Path


class ExpandContractions:
    cont = Contractions(os.path.join(Path.bin, 'GoogleNews-vectors-negative300.bin'))

