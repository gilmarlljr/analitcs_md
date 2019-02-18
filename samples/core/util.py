import base64
import gzip
import hashlib
from enum import Enum


def compress_and_b64encode(s: str):
    return str(base64.b64encode(gzip.compress(bytes(s, encoding='utf-8'))), 'utf-8')


def b64decode_and_decompress(s: str):
    return str(gzip.decompress(base64.b64decode(bytes(s, encoding='utf-8'))), 'utf-8')


def md5_file(file_name):
    hash_md5 = hashlib.md5()
    chunk_size = 1024
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_text(s: str):
    hash_md5 = hashlib.md5()
    chunk_size = 1024
    lines = [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]
    for line in lines:
        hash_md5.update(bytes(line, encoding='utf-8'))
    return hash_md5.hexdigest()


class CustomEnum(Enum):
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, description: str = None):
        self._description_ = description

    def __str__(self):
        return self.value

    # this makes sure that the description is read-only
    @property
    def description(self):
        return self._description_
