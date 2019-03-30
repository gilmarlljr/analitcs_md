import os

import nltk

from core.path import Path


class DependenciesDownloader:
    nltk.data.path.append(os.path.join(Path.bin, 'ntlk_data'))
    nltk.download('stopwords', download_dir=os.path.join(Path.bin, 'ntlk_data'))
